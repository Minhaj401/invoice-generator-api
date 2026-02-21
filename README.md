# Invoice Generator API

Flask API that generates PDF invoices from chat messages using AI parsing, with UPI QR code payment integration.

## Features

- 🤖 AI-powered chat parsing using Google Gemini (Free tier available!)
- 📄 Professional PDF invoice generation with HTML/CSS templates
- 💳 UPI QR code generation for seamless payments
- 🧮 Automatic GST (18%) calculation
- 📱 RESTful API with JSON input/output

## Setup

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure environment:**
   - Copy `.env.example` to `.env`
   - Get your free Gemini API key from: https://makersuite.google.com/app/apikey
   - Add the key to `.env`
   - Update business details

3. **Run the server:**
   ```bash
   python run.py
   ```

The API will be available at `http://localhost:5000`

## API Endpoint

### POST `/api/generate-invoice`

**Request Body:**
```json
{
  "chats": [
    "I'll take 2 pizzas",
    "Each pizza is 500 rupees",
    "Also need 3 cold drinks at 50 each"
  ],
  "upi_id": "merchant@paytm",
  "customer_name": "John Doe",
  "customer_phone": "+91-9876543210",
  "customer_email": "john@example.com",
  
  "_comment": "Optional: Override business details per request",
  "business_name": "Pizza Palace",
  "business_address": "456 Food Street, Bangalore - 560001",
  "business_phone": "+91-9988776655",
  "business_email": "orders@pizzapalace.com",
  "business_gst": "29ABCDE1234F1Z5"
}
```

**Optional Fields:**
- `business_name` - Override default business name
- `business_address` - Override default address  
- `business_phone` - Override default phone
- `business_email` - Override default email
- `business_gst` - Override default GST number

If not provided, defaults to values from `.env` file.

**Response:**
- PDF file download with `Content-Type: application/pdf`
- Filename: `invoice_INV-YYYYMM-XXXX.pdf`

## Example Usage

```bash
curl -X POST http://localhost:5000/api/generate-invoice \
  -H "Content-Type: application/json" \
  -d @sample_request.json \
  --output invoice.pdf
```

## Requirements

- Python 3.8+
- Google Gemini API key (Free tier available)
- ReportLab for PDF generation

## Deployment

See [DEPLOYMENT.md](DEPLOYMENT.md) for comprehensive deployment guides for:
- Render
- Railway  
- Heroku
- Docker
- PythonAnywhere
- AWS, GCP, Azure

## License

MIT
