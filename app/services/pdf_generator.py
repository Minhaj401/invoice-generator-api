"""
PDF Generator Service
Generates professional PDF invoices using ReportLab.
"""

from typing import Dict, List
from datetime import datetime, timedelta
from io import BytesIO
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image
from reportlab.lib.enums import TA_CENTER, TA_RIGHT, TA_LEFT, TA_JUSTIFY
from reportlab.pdfgen import canvas
from config import Config

# Professional Dark Blue Theme
COLOR_PRIMARY = colors.HexColor('#2C3E50')      # Dark Navy Blue (Main Theme)
COLOR_DARK_TEXT = colors.HexColor('#212529')    # Almost Black
COLOR_GRAY_TEXT = colors.HexColor('#6C757D')    # Medium Gray
COLOR_LIGHT_BG = colors.HexColor('#F8F9FA')     # Very Light Gray
COLOR_BORDER = colors.HexColor('#DEE2E6')       # Light Border Gray
COLOR_WHITE = colors.white                      # Pure White


def format_currency(amount):
    """Format currency amount with Rs. prefix"""
    return f"Rs. {amount:.2f}"


def generate_pdf(
    invoice_data: Dict,
    items: List[Dict],
    totals: Dict,
    qr_code_base64: str
) -> bytes:
    """
    Generate professional invoice matching industry standards.
    
    Args:
        invoice_data: Invoice metadata
        items: List of items
        totals: Calculated totals
        qr_code_base64: Base64 QR code
        
    Returns:
        PDF as bytes
    """
    
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4,
                           rightMargin=50, leftMargin=50,
                           topMargin=40, bottomMargin=50)
    
    elements = []
    styles = getSampleStyleSheet()
    
    # Calculate due date (7 days from invoice date)
    try:
        invoice_date = datetime.strptime(invoice_data['date'], '%Y-%m-%d')
        due_date = (invoice_date + timedelta(days=7)).strftime('%Y-%m-%d')
    except:
        due_date = invoice_data['date']
    
    # ===== TOP HEADER SECTION =====
    # Company Name and INVOICE title side by side
    header_data = [[
        Paragraph(
            f"<font size='20' color='#212529'><b>{invoice_data['business_name']}</b></font>",
            ParagraphStyle('CompanyName', parent=styles['Normal'], alignment=TA_LEFT, leading=24)
        ),
        Paragraph(
            f"<font size='28' color='#2C3E50'><b>INVOICE</b></font>",
            ParagraphStyle('InvoiceTitle', parent=styles['Normal'], alignment=TA_RIGHT, leading=32)
        )
    ]]
    
    header_table = Table(header_data, colWidths=[3.5*inch, 3.5*inch])
    header_table.setStyle(TableStyle([
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('LEFTPADDING', (0, 0), (-1, -1), 0),
        ('RIGHTPADDING', (0, 0), (-1, -1), 0),
        ('TOPPADDING', (0, 0), (-1, -1), 0),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 0),
    ]))
    elements.append(header_table)
    elements.append(Spacer(1, 15))
    
    # ===== COMPANY DETAILS AND INVOICE INFO SECTION =====
    # Left side: From (Company Details)
    from_section = Paragraph(
        f"<font size='9' color='#6C757D'><b>FROM:</b></font><br/>"
        f"<font size='10' color='#212529'><b>{invoice_data['business_name']}</b></font><br/>"
        f"<font size='9' color='#6C757D'>{invoice_data['business_address']}<br/>"
        f"Phone: {invoice_data['business_phone']}<br/>"
        f"Email: {invoice_data['business_email']}<br/>"
        f"GST No: {invoice_data['business_gst']}</font>",
        styles['Normal']
    )
    
    # Right side: Invoice Details Box
    invoice_info = [
        [
            Paragraph("<font size='9' color='#6C757D'><b>INVOICE NO:</b></font>", styles['Normal']),
            Paragraph(f"<font size='10' color='#212529'><b>{invoice_data['invoice_number']}</b></font>", 
                     ParagraphStyle('InfoValue', parent=styles['Normal'], alignment=TA_RIGHT))
        ],
        [
            Paragraph("<font size='9' color='#6C757D'><b>DATE:</b></font>", styles['Normal']),
            Paragraph(f"<font size='10' color='#212529'>{invoice_data['date']}</font>", 
                     ParagraphStyle('InfoValue', parent=styles['Normal'], alignment=TA_RIGHT))
        ],
        [
            Paragraph("<font size='9' color='#6C757D'><b>DUE DATE:</b></font>", styles['Normal']),
            Paragraph(f"<font size='10' color='#212529'>{due_date}</font>", 
                     ParagraphStyle('InfoValue', parent=styles['Normal'], alignment=TA_RIGHT))
        ],
        [
            Paragraph("<font size='9' color='#6C757D'><b>AMOUNT DUE:</b></font>", styles['Normal']),
            Paragraph(f"<font size='12' color='#2C3E50'><b>{format_currency(totals['total'])}</b></font>", 
                     ParagraphStyle('InfoValue', parent=styles['Normal'], alignment=TA_RIGHT))
        ]
    ]
    
    invoice_info_table = Table(invoice_info, colWidths=[1.5*inch, 1.5*inch])
    invoice_info_table.setStyle(TableStyle([
        ('ALIGN', (0, 0), (0, -1), 'LEFT'),
        ('ALIGN', (1, 0), (1, -1), 'RIGHT'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('BACKGROUND', (0, 0), (-1, -1), COLOR_LIGHT_BG),
        ('BOX', (0, 0), (-1, -1), 1, COLOR_BORDER),
        ('LINEBELOW', (0, 0), (-1, 2), 0.5, COLOR_BORDER),
    ]))
    
    # Combine FROM and Invoice Info
    top_info_row = Table([[from_section, invoice_info_table]], 
                         colWidths=[3.8*inch, 3.2*inch])
    top_info_row.setStyle(TableStyle([
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('LEFTPADDING', (0, 0), (-1, -1), 0),
        ('RIGHTPADDING', (0, 0), (-1, -1), 0),
    ]))
    elements.append(top_info_row)
    elements.append(Spacer(1, 20))
    
    # ===== BILL TO SECTION =====
    bill_to = Paragraph(
        f"<font size='10' color='#6C757D'><b>BILL TO:</b></font><br/>"
        f"<font size='12' color='#212529'><b>{invoice_data['customer_name']}</b></font><br/>"
        f"<font size='9' color='#6C757D'>"
        f"Phone: {invoice_data.get('customer_phone', 'N/A')}<br/>"
        f"Email: {invoice_data.get('customer_email', 'N/A')}</font>",
        styles['Normal']
    )
    
    bill_to_table = Table([[bill_to]], colWidths=[7*inch])
    bill_to_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.white),
        ('PADDING', (0, 0), (-1, -1), 12),
        ('BOX', (0, 0), (-1, -1), 1, COLOR_BORDER),
        ('LINEABOVE', (0, 0), (-1, 0), 3, COLOR_PRIMARY),
    ]))
    elements.append(bill_to_table)
    elements.append(Spacer(1, 20))
    
    # ===== ITEMS TABLE =====
    table_data = [
        [
            Paragraph("<font size='9' color='white'><b>ITEM</b></font>", styles['Normal']),
            Paragraph("<font size='9' color='white'><b>QTY</b></font>", styles['Normal']),
            Paragraph("<font size='9' color='white'><b>RATE</b></font>", styles['Normal']),
            Paragraph("<font size='9' color='white'><b>AMOUNT</b></font>", styles['Normal'])
        ]
    ]
    
    for idx, item in enumerate(items, 1):
        amount = item['quantity'] * item['price']
        table_data.append([
            Paragraph(f"<font size='10' color='#212529'>{item['item']}</font>", styles['Normal']),
            Paragraph(f"<font size='9' color='#212529'>{item['quantity']}</font>", 
                     ParagraphStyle('Center', parent=styles['Normal'], alignment=TA_CENTER)),
            Paragraph(f"<font size='9' color='#212529'>{format_currency(item['price'])}</font>", 
                     ParagraphStyle('Right', parent=styles['Normal'], alignment=TA_RIGHT)),
            Paragraph(f"<font size='10' color='#212529'><b>{format_currency(amount)}</b></font>", 
                     ParagraphStyle('Right', parent=styles['Normal'], alignment=TA_RIGHT))
        ])
    
    items_table = Table(table_data, colWidths=[3.5*inch, 0.8*inch, 1.3*inch, 1.4*inch])
    
    # Build table style
    table_style_commands = [
        # Header row
        ('BACKGROUND', (0, 0), (-1, 0), COLOR_PRIMARY),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('ALIGN', (0, 0), (0, 0), 'LEFT'),
        ('ALIGN', (1, 0), (1, 0), 'CENTER'),
        ('ALIGN', (2, 0), (-1, 0), 'RIGHT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 9),
        ('TOPPADDING', (0, 0), (-1, 0), 10),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 10),
        
        # Data rows
        ('ALIGN', (0, 1), (0, -1), 'LEFT'),
        ('ALIGN', (1, 1), (1, -1), 'CENTER'),
        ('ALIGN', (2, 1), (-1, -1), 'RIGHT'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('FONTSIZE', (0, 1), (-1, -1), 10),
        ('TOPPADDING', (0, 1), (-1, -1), 12),
        ('BOTTOMPADDING', (0, 1), (-1, -1), 12),
        ('LEFTPADDING', (0, 0), (-1, -1), 10),
        ('RIGHTPADDING', (0, 0), (-1, -1), 10),
        
        # Borders
        ('BOX', (0, 0), (-1, -1), 1, COLOR_BORDER),
        ('LINEBELOW', (0, 0), (-1, 0), 2, COLOR_PRIMARY),
        ('INNERGRID', (0, 1), (-1, -1), 0.5, COLOR_BORDER),
    ]
    
    # Add alternating row colors (subtle)
    for i in range(1, len(table_data)):
        if i % 2 == 0:
            table_style_commands.append(
                ('BACKGROUND', (0, i), (-1, i), COLOR_LIGHT_BG)
            )
    
    items_table.setStyle(TableStyle(table_style_commands))
    elements.append(items_table)
    elements.append(Spacer(1, 15))
    
    # ===== TOTALS SECTION =====
    totals_data = [
        [
            Paragraph("<font size='10' color='#6C757D'>Subtotal:</font>", styles['Normal']),
            Paragraph(f"<font size='10' color='#212529'>{format_currency(totals['subtotal'])}</font>", 
                     ParagraphStyle('Right', parent=styles['Normal'], alignment=TA_RIGHT))
        ],
        [
            Paragraph(f"<font size='10' color='#6C757D'>GST ({totals['gst_rate']:.0f}%):</font>", styles['Normal']),
            Paragraph(f"<font size='10' color='#212529'>{format_currency(totals['gst'])}</font>", 
                     ParagraphStyle('Right', parent=styles['Normal'], alignment=TA_RIGHT))
        ],
        [
            Paragraph("<font size='11' color='white'><b>TOTAL AMOUNT</b></font>", styles['Normal']),
            Paragraph(f"<font size='13' color='white'><b>{format_currency(totals['total'])}</b></font>", 
                     ParagraphStyle('Right', parent=styles['Normal'], alignment=TA_RIGHT))
        ]
    ]
    
    totals_table = Table(totals_data, colWidths=[1.8*inch, 1.5*inch])
    totals_table.setStyle(TableStyle([
        # Subtotal and GST rows
        ('ALIGN', (0, 0), (0, 1), 'RIGHT'),
        ('ALIGN', (1, 0), (1, 1), 'RIGHT'),
        ('TOPPADDING', (0, 0), (-1, 1), 8),
        ('BOTTOMPADDING', (0, 0), (-1, 1), 8),
        ('LINEBELOW', (0, 1), (-1, 1), 1, COLOR_BORDER),
        
        # Total row
        ('BACKGROUND', (0, 2), (-1, 2), COLOR_PRIMARY),
        ('TEXTCOLOR', (0, 2), (-1, 2), colors.white),
        ('ALIGN', (0, 2), (-1, 2), 'RIGHT'),
        ('TOPPADDING', (0, 2), (-1, 2), 12),
        ('BOTTOMPADDING', (0, 2), (-1, 2), 12),
        
        # Overall box
        ('BOX', (0, 0), (-1, -1), 1, COLOR_BORDER),
        ('LEFTPADDING', (0, 0), (-1, -1), 10),
        ('RIGHTPADDING', (0, 0), (-1, -1), 10),
    ]))
    
    # Right-align totals
    totals_wrapper = Table([[totals_table]], colWidths=[7*inch])
    totals_wrapper.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'RIGHT'),
        ('LEFTPADDING', (0, 0), (-1, -1), 0),
        ('RIGHTPADDING', (0, 0), (-1, -1), 0),
    ]))
    elements.append(totals_wrapper)
    elements.append(Spacer(1, 25))
    
    # ===== PAYMENT INSTRUCTIONS =====
    payment_title = Paragraph(
        "<font size='11' color='#212529'><b>Payment Information</b></font>",
        styles['Normal']
    )
    elements.append(payment_title)
    elements.append(Spacer(1, 10))
    
    # QR Code and Payment Details side by side
    import base64
    qr_image_data = qr_code_base64.split(',')[1] if ',' in qr_code_base64 else qr_code_base64
    qr_image_bytes = BytesIO(base64.b64decode(qr_image_data))
    qr_img = Image(qr_image_bytes, width=1.8*inch, height=1.8*inch)
    
    # QR Code box
    qr_content = [
        [qr_img],
        [Paragraph(
            "<font size='8' color='#6C757D'>Scan to Pay via UPI</font>",
            ParagraphStyle('Center', parent=styles['Normal'], alignment=TA_CENTER)
        )]
    ]
    
    qr_table = Table(qr_content, colWidths=[2*inch])
    qr_table.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('PADDING', (0, 0), (-1, -1), 10),
        ('BOX', (0, 0), (-1, -1), 1, COLOR_BORDER),
        ('BACKGROUND', (0, 0), (-1, -1), COLOR_LIGHT_BG),
    ]))
    
    # Payment details
    payment_info = Paragraph(
        f"<font size='10' color='#212529'>"
        f"<b>Pay via UPI</b><br/><br/>"
        f"<font size='9' color='#6C757D'>UPI ID: </font><b>{invoice_data['upi_id']}</b><br/>"
        f"<font size='9' color='#6C757D'>Payee: </font><b>{invoice_data['business_name']}</b><br/>"
        f"<font size='9' color='#6C757D'>Amount: </font><b>{format_currency(totals['total'])}</b><br/><br/>"
        f"<font size='8' color='#6C757D'>"
        f"Scan the QR code using any UPI app<br/>"
        f"(GooglePay, PhonePe, Paytm, etc.)</font>"
        f"</font>",
        styles['Normal']
    )
    
    payment_info_box = Table([[payment_info]], colWidths=[4.5*inch])
    payment_info_box.setStyle(TableStyle([
        ('PADDING', (0, 0), (-1, -1), 15),
        ('BOX', (0, 0), (-1, -1), 1, COLOR_BORDER),
        ('BACKGROUND', (0, 0), (-1, -1), colors.white),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
    ]))
    
    # Combine QR and details
    payment_row = Table([[qr_table, payment_info_box]], 
                        colWidths=[2.2*inch, 4.8*inch])
    payment_row.setStyle(TableStyle([
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('LEFTPADDING', (0, 0), (-1, -1), 0),
        ('RIGHTPADDING', (0, 0), (-1, -1), 0),
    ]))
    elements.append(payment_row)
    elements.append(Spacer(1, 25))
    
    # ===== TERMS AND CONDITIONS =====
    terms_title = Paragraph(
        "<font size='10' color='#212529'><b>Terms & Conditions</b></font>",
        styles['Normal']
    )
    elements.append(terms_title)
    elements.append(Spacer(1, 5))
    
    terms_text = Paragraph(
        f"<font size='8' color='#6C757D'>"
        f"• Payment is due within 7 days from the invoice date.<br/>"
        f"• Please include the invoice number when making payment.<br/>"
        f"• Late payments may incur additional charges.<br/>"
        f"• For any queries regarding this invoice, please contact us at {invoice_data['business_email']} or {invoice_data['business_phone']}."
        f"</font>",
        ParagraphStyle('Terms', parent=styles['Normal'], alignment=TA_JUSTIFY)
    )
    
    terms_box = Table([[terms_text]], colWidths=[7*inch])
    terms_box.setStyle(TableStyle([
        ('PADDING', (0, 0), (-1, -1), 12),
        ('BOX', (0, 0), (-1, -1), 1, COLOR_BORDER),
        ('BACKGROUND', (0, 0), (-1, -1), COLOR_LIGHT_BG),
    ]))
    elements.append(terms_box)
    elements.append(Spacer(1, 20))
    
    # ===== THANK YOU MESSAGE =====
    thank_you = Paragraph(
        "<font size='14' color='#2C3E50'><b>Thank You for Your Business!</b></font>",
        ParagraphStyle('ThankYou', parent=styles['Normal'], alignment=TA_CENTER)
    )
    elements.append(thank_you)
    elements.append(Spacer(1, 15))
    
    # ===== FOOTER =====
    footer_text = Paragraph(
        f"<font size='8' color='#ADB5BD'>"
        f"This is a computer-generated invoice and does not require a physical signature.<br/>"
        f"Generated on {datetime.now().strftime('%B %d, %Y at %I:%M %p')}<br/>"
        f"{invoice_data['business_name']} | {invoice_data['business_email']} | {invoice_data['business_phone']}"
        f"</font>",
        ParagraphStyle('Footer', parent=styles['Normal'], alignment=TA_CENTER)
    )
    
    footer_box = Table([[footer_text]], colWidths=[7*inch])
    footer_box.setStyle(TableStyle([
        ('PADDING', (0, 0), (-1, -1), 10),
        ('LINEABOVE', (0, 0), (-1, -1), 0.5, COLOR_BORDER),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
    ]))
    elements.append(footer_box)
    
    # Build PDF
    doc.build(elements)
    
    # Get PDF bytes
    pdf_bytes = buffer.getvalue()
    buffer.close()
    
    return pdf_bytes
