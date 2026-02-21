"""
Chat Parser Service
Uses Google Gemini API to extract items, quantities, and prices from natural language chat messages.
"""

import json
import re
import logging
from typing import List, Dict
import google.generativeai as genai
from config import Config

logger = logging.getLogger(__name__)


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
        logger.error("Gemini API key not configured")
        raise Exception("Gemini API key not configured. Please set GEMINI_API_KEY in .env file. Get your free key from: https://makersuite.google.com/app/apikey")
    
    logger.info("Configuring Gemini API...")
    # Configure Gemini
    genai.configure(api_key=Config.GEMINI_API_KEY)
    
    # Combine all chat messages into a single context
    chat_context = "\n".join(chat_messages)
    logger.debug(f"Chat context prepared: {chat_context[:100]}...")
    
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
        logger.info("Calling Gemini API (gemini-2.0-flash-exp model)...")
        model = genai.GenerativeModel('gemini-2.0-flash-exp')
        response = model.generate_content(prompt)
        logger.info("Gemini API response received")
        
        # Extract response content
        content = response.text.strip()
        logger.debug(f"Raw Gemini response: {content[:200]}...")
        
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
        logger.info("Parsing JSON response from Gemini...")
        items = json.loads(content)
        logger.info(f"Successfully parsed {len(items)} items from JSON")
        
        # Validate structure
        if not isinstance(items, list):
            logger.error(f"Response is not a list: {type(items)}")
            raise ValueError("Response is not a list")
        
        for idx, item in enumerate(items):
            if not all(key in item for key in ['item', 'quantity', 'price']):
                logger.error(f"Invalid item structure at index {idx}: {item}")
                raise ValueError(f"Invalid item structure: {item}")
            
            # Ensure correct types
            item['quantity'] = int(item['quantity'])
            item['price'] = float(item['price'])
        
        logger.info(f"All items validated successfully: {[item['item'] for item in items]}")
        return items
        
    except json.JSONDecodeError as e:
        logger.error(f"JSON decode error: {str(e)}. Content: {content[:200]}...")
        raise Exception(f"Failed to parse Gemini response as JSON. Response: {content[:200]}... Error: {str(e)}")
    except Exception as e:
        logger.error(f"Error parsing chats with Gemini: {str(e)}", exc_info=True)
        raise Exception(f"Error parsing chats with Gemini: {str(e)}")


def calculate_totals(items: List[Dict]) -> Dict:
    """
    Calculate subtotal, GST, and total from items.
    
    Args:
        items: List of items with quantity and price
        
    Returns:
        Dict with subtotal, gst, and total
    """
    logger.info(f"Calculating totals for {len(items)} items...")
    subtotal = sum(item['quantity'] * item['price'] for item in items)
    gst = subtotal * Config.GST_RATE
    total = subtotal + gst
    
    logger.info(f"Totals calculated - Subtotal: {subtotal}, GST ({Config.GST_RATE*100}%): {gst}, Total: {total}")
    
    return {
        'subtotal': round(subtotal, 2),
        'gst': round(gst, 2),
        'gst_rate': Config.GST_RATE * 100,  # As percentage
        'total': round(total, 2)
    }
