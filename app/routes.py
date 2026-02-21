"""
API Routes for Invoice Generation
"""

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
    
    try:
        # Validate request data
        try:
            data = invoice_schema.load(request.json)
        except ValidationError as err:
            return jsonify({
                'error': 'Validation failed',
                'details': err.messages
            }), 400
        
        # Extract chat messages
        chat_messages = data['chats']
        
        # Parse chats using AI
        try:
            items = parse_chats(chat_messages)
        except Exception as e:
            return jsonify({
                'error': 'Failed to parse chat messages',
                'details': str(e)
            }), 500
        
        # Check if items were extracted
        if not items:
            return jsonify({
                'error': 'No items found in chat messages',
                'details': 'Please ensure your chat messages contain item names and prices'
            }), 400
        
        # Calculate totals
        totals = calculate_totals(items)
        
        # Generate invoice number
        invoice_number = get_next_invoice_number()
        
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
        
        # Generate UPI QR code
        payee_name = data.get('payee_name', Config.BUSINESS_NAME)
        qr_code_base64 = generate_upi_qr(
            upi_id=data['upi_id'],
            amount=totals['total'],
            payee_name=payee_name,
            invoice_number=invoice_number
        )
        
        # Generate PDF
        try:
            pdf_bytes = generate_pdf(
                invoice_data=invoice_data,
                items=items,
                totals=totals,
                qr_code_base64=qr_code_base64
            )
        except Exception as e:
            return jsonify({
                'error': 'Failed to generate PDF',
                'details': str(e)
            }), 500
        
        # Return PDF as downloadable file
        pdf_buffer = io.BytesIO(pdf_bytes)
        pdf_buffer.seek(0)
        
        return send_file(
            pdf_buffer,
            mimetype='application/pdf',
            as_attachment=True,
            download_name=f'invoice_{invoice_number}.pdf'
        )
        
    except Exception as e:
        return jsonify({
            'error': 'Internal server error',
            'details': str(e)
        }), 500


@api_bp.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'service': 'Invoice Generator API',
        'timestamp': datetime.now().isoformat()
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
