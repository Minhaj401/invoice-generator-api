"""
API Routes for Invoice Generation
"""

import logging
from flask import Blueprint, request, jsonify, send_file
from marshmallow import ValidationError
import io
from datetime import datetime

from app.schemas import InvoiceRequestSchema
from app.services.chat_parser import parse_chats, calculate_totals
from app.services.qr_generator import generate_upi_qr
from app.services.pdf_generator import generate_pdf
from app.utils.invoice_utils import get_next_invoice_number, format_date
from config import Config

logger = logging.getLogger(__name__)

# Create blueprint
api_bp = Blueprint('api', __name__, url_prefix='/api')

# Initialize schema
invoice_schema = InvoiceRequestSchema()


@api_bp.route('/generate-invoice', methods=['POST'])
def generate_invoice():
    """
    Generate PDF invoice from chat messages.
    
    Request JSON:
    {
        "chats": ["chat message 1", "chat message 2", ...],
        "upi_id": "merchant@paytm",
        "customer_name": "John Doe",
        "customer_phone": "+91-9876543210",  // optional
        "customer_email": "john@example.com",  // optional
        "payee_name": "Business Name"  // optional, defaults to config
    }
    
    Returns:
        PDF file as attachment
    """
    
    logger.info("Received invoice generation request")
    
    try:
        # Validate request data
        try:
            data = invoice_schema.load(request.json)
            logger.info(f"Request validated successfully. Chat messages count: {len(data['chats'])}")
        except ValidationError as err:
            logger.warning(f"Validation failed: {err.messages}")
            return jsonify({
                'error': 'Validation failed',
                'details': err.messages
            }), 400
        
        # Extract chat messages
        chat_messages = data['chats']
        logger.debug(f"Chat messages: {chat_messages}")
        
        # Parse chats using AI
        try:
            logger.info("Starting AI chat parsing with Gemini API...")
            items = parse_chats(chat_messages)
            logger.info(f"Successfully parsed {len(items)} items from chat")
        except Exception as e:
            logger.error(f"Failed to parse chat messages: {str(e)}", exc_info=True)
            return jsonify({
                'error': 'Failed to parse chat messages',
                'details': str(e)
            }), 500
        
        # Check if items were extracted
        if not items:
            logger.warning("No items found in chat messages")
            return jsonify({
                'error': 'No items found in chat messages',
                'details': 'Please ensure your chat messages contain item names and prices'
            }), 400
        
        # Calculate totals
        totals = calculate_totals(items)
        logger.info(f"Calculated totals - Subtotal: Rs.{totals['subtotal']}, Tax: Rs.{totals['tax']}, Total: Rs.{totals['total']}")
        
        # Generate invoice number
        invoice_number = get_next_invoice_number()
        logger.info(f"Generated invoice number: {invoice_number}")
        
        # Prepare invoice data
        invoice_data = {
            'invoice_number': invoice_number,
            'date': format_date(),
            'customer_name': data['customer_name'],
            'customer_phone': data.get('customer_phone', 'N/A'),
            'customer_email': data.get('customer_email', 'N/A'),
            'upi_id': data['upi_id'],
            # Use business details from request or fallback to config
            'business_name': data.get('business_name') or Config.BUSINESS_NAME,
            'business_address': data.get('business_address') or Config.BUSINESS_ADDRESS,
            'business_phone': data.get('business_phone') or Config.BUSINESS_PHONE,
            'business_email': data.get('business_email') or Config.BUSINESS_EMAIL,
            'business_gst': data.get('business_gst') or Config.BUSINESS_GST
        }
        logger.info(f"Invoice prepared for customer: {data['customer_name']}")
        
        # Generate UPI QR code
        payee_name = data.get('payee_name', Config.BUSINESS_NAME)
        logger.info(f"Generating UPI QR code for {payee_name}, amount: Rs.{totals['total']}")
        qr_code_base64 = generate_upi_qr(
            upi_id=data['upi_id'],
            amount=totals['total'],
            payee_name=payee_name,
            invoice_number=invoice_number
        )
        logger.info("UPI QR code generated successfully")
        
        # Generate PDF
        try:
            logger.info("Starting PDF generation...")
            pdf_bytes = generate_pdf(
                invoice_data=invoice_data,
                items=items,
                totals=totals,
                qr_code_base64=qr_code_base64
            )
            logger.info(f"PDF generated successfully, size: {len(pdf_bytes)} bytes")
        except Exception as e:
            logger.error(f"PDF generation failed: {str(e)}", exc_info=True)
            return jsonify({
                'error': 'Failed to generate PDF',
                'details': str(e)
            }), 500
        
        # Return PDF as downloadable file
        pdf_buffer = io.BytesIO(pdf_bytes)
        pdf_buffer.seek(0)
        
        logger.info(f"Successfully generated invoice {invoice_number}, sending PDF response")
        
        return send_file(
            pdf_buffer,
            mimetype='application/pdf',
            as_attachment=True,
            download_name=f'invoice_{invoice_number}.pdf'
        )
        
    except Exception as e:
        logger.error(f"Unexpected error in invoice generation: {str(e)}", exc_info=True)
        return jsonify({
            'error': 'Internal server error',
            'details': str(e)
        }), 500


@api_bp.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    logger.info("Health check requested")
    return jsonify({
        'status': 'healthy',
        'service': 'Invoice Generator API',
        'timestamp': datetime.now().isoformat()
    })


@api_bp.route('/status', methods=['GET'])
def status():
    """Status endpoint with environment information"""
    logger.info("Status check requested")
    
    import sys
    gemini_configured = bool(Config.GEMINI_API_KEY)
    
    return jsonify({
        'status': 'running',
        'service': 'Invoice Generator API',
        'timestamp': datetime.now().isoformat(),
        'python_version': sys.version,
        'environment': {
            'gemini_api_configured': gemini_configured,
            'business_name': Config.BUSINESS_NAME,
            'has_business_email': bool(Config.BUSINESS_EMAIL),
            'has_business_phone': bool(Config.BUSINESS_PHONE),
            'gst_rate': f"{Config.GST_RATE * 100}%"
        },
        'endpoints': {
            'generate_invoice': '/api/generate-invoice (POST)',
            'health': '/api/health (GET)',
            'status': '/api/status (GET)',
            'test_parse': '/api/test-parse (POST)'
        }
    })


@api_bp.route('/test-parse', methods=['POST'])
def test_parse():
    """
    Test endpoint to parse chats without generating PDF.
    Useful for debugging chat parsing.
    
    Request JSON:
    {
        "chats": ["chat message 1", "chat message 2", ...]
    }
    
    Returns:
        JSON with parsed items and totals
    """
    
    try:
        data = request.json
        
        if not data or 'chats' not in data:
            return jsonify({
                'error': 'Missing chats field'
            }), 400
        
        # Parse chats
        items = parse_chats(data['chats'])
        
        # Calculate totals
        totals = calculate_totals(items)
        
        return jsonify({
            'items': items,
            'totals': totals
        })
        
    except Exception as e:
        return jsonify({
            'error': str(e)
        }), 500
