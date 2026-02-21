"""
Chat Parser Service
Uses Google Gemini API to extract items, quantities, and prices from natural language chat messages.
"""

import json
import re
from typing import List, Dict
from google import genai
from config import Config


def parse_chats(chat_messages: List[str]) -> List[Dict]:
    """
    Parse chat messages using Google Gemini to extract structured item data.
    
    Args:
        chat_messages: List of chat message strings
        
    Returns:
        List of dicts with structure: [{"item": str, "quantity": int, "price": float}]
        
    Raises:
        Exception: If Gemini API fails or returns invalid data
    """
    
    if not Config.GEMINI_API_KEY:
        raise Exception("Gemini API key not configured. Please set GEMINI_API_KEY in .env file. Get your free key from: https://makersuite.google.com/app/apikey")
    
    # Initialize Gemini client
    client = genai.Client(api_key=Config.GEMINI_API_KEY)
    
    # Combine all chat messages into a single context
    chat_context = "\n".join(chat_messages)
    
    # Create prompt for Gemini
    prompt = f"""You are an expert at extracting purchase information from chat messages.

Analyze the following chat messages and extract all items being purchased.
For each item, identify:
- item: The product/service name
- quantity: How many units (default to 1 if not mentioned)
- price: The price per unit in rupees

Chat messages:
{chat_context}

Return ONLY a valid JSON array with this exact structure (no markdown, no code blocks, just the JSON):
[
  {{
    "item": "Product Name",
    "quantity": 2,
    "price": 500.00
  }}
]

Rules:
- If quantity is not mentioned, assume 1
- Extract price per unit, not total
- Use descriptive item names
- Return empty array [] if no items found
- ONLY return the JSON array, no other text or explanation

JSON array:"""

    try:
        # Call Gemini API
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt
        )
        
        # Extract response content
        content = response.text.strip()
        
        # Remove markdown code blocks if present
        if "```json" in content:
            content = re.search(r'```json\s*(.*?)\s*```', content, re.DOTALL)
            if content:
                content = content.group(1).strip()
            else:
                content = response.text.strip()
        elif "```" in content:
            content = content.replace("```", "").strip()
        
        # Remove any leading/trailing text before/after JSON
        json_start = content.find('[')
        json_end = content.rfind(']')
        if json_start != -1 and json_end != -1:
            content = content[json_start:json_end + 1]
        
        # Parse JSON
        items = json.loads(content)
        
        # Validate structure
        if not isinstance(items, list):
            raise ValueError("Response is not a list")
        
        for item in items:
            if not all(key in item for key in ['item', 'quantity', 'price']):
                raise ValueError(f"Invalid item structure: {item}")
            
            # Ensure correct types
            item['quantity'] = int(item['quantity'])
            item['price'] = float(item['price'])
        
        return items
        
    except json.JSONDecodeError as e:
        raise Exception(f"Failed to parse Gemini response as JSON. Response: {content[:200]}... Error: {str(e)}")
    except Exception as e:
        raise Exception(f"Error parsing chats with Gemini: {str(e)}")


def calculate_totals(items: List[Dict]) -> Dict:
    """
    Calculate subtotal, GST, and total from items.
    
    Args:
        items: List of items with quantity and price
        
    Returns:
        Dict with subtotal, gst, and total
    """
    subtotal = sum(item['quantity'] * item['price'] for item in items)
    gst = subtotal * Config.GST_RATE
    total = subtotal + gst
    
    return {
        'subtotal': round(subtotal, 2),
        'gst': round(gst, 2),
        'gst_rate': Config.GST_RATE * 100,  # As percentage
        'total': round(total, 2)
    }
