import os
import json
from dotenv import load_dotenv
import openai
import re
import logging

# Load environment variables
load_dotenv()

# Initialize OpenAI client with API key
openai.api_key = os.getenv('OPENAI_KEY')

logger = logging.getLogger(__name__)

class OpenAIUtils:
    """
    Utility class for interacting with OpenAI's APIs.
    """
    
    @staticmethod
    def extract_product_data(merchant_name, product, product_category, target_market, unique_selling_points, price_range, purchase_context):
        """
        Identify key customer segments for a given merchant and product using OpenAI.

        Args:
            merchant_name (str): The name of the merchant.
            product_name (str): The specific product being analyzed.
            product_category (str): The broader category this product belongs to.
            target_market (str, optional): The geographic region or demographic focus.
            unique_selling_points (list, optional): Key differentiators of the product.
            price_range (str, optional): The pricing tier (e.g., budget, mid-tier, premium).
            purchase_context (str, optional): Typical buying scenarios (e.g., impulse buy, planned purchase).
            
        Returns:
            dict: Customer segmentation data
        """
        system_prompt = """You are an expert in market segmentation and consumer behavior analysis. Your task is to analyze a given product from a specific merchant and identify key customer segments based on demographic, psychographic, and behavioral factors. Provide structured customer segmentation insights in the following JSON format:

        {
            "merchant": "The name of the merchant",
            "product": "The product being analyzed",
            "product_category": "The general category of the product",
            "customer_segments": [
                {
                    "segment_name": "A descriptive name for the customer segment",
                    "demographics": {
                        "age_range": "Typical age range of customers",
                        "income_level": "Low, middle, or high income",
                        "location": "Urban, suburban, or rural",
                        "occupation": "Common professions for this segment"
                    },
                    "psychographics": {
                        "lifestyle": "Hobbies, interests, and values",
                        "purchasing_behavior": "How they typically buy this type of product",
                        "brand_affinity": "Level of loyalty to brands"
                    },
                    "pain_points": "Key challenges or needs this segment faces",
                    "marketing_strategy": "Recommended approach to engage this segment"
                }
            ]
        }

        Ensure the segmentation is detailed and actionable. If the product serves multiple distinct groups, provide multiple customer segments. If information is not explicitly available, make data-driven assumptions based on typical industry trends.
        """


        try:
            response = openai.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                response_format={"type": "json_object"}
            )
            
            # Extract the JSON content from the response
            content = response.choices[0].message.content
            try:
                # First try to parse the entire response as JSON
                case_data = json.loads(content)
            except json.JSONDecodeError:
                # If that fails, try to extract JSON from the response
                json_match = re.search(r'\{.*\}', content, re.DOTALL)
                if json_match:
                    case_data = json.loads(json_match.group())
                else:
                    raise ValueError("No valid JSON found in response")
            
            # Ensure all required fields are present with at least empty strings
            required_fields = {
                'title': '',
                'situation': {
                    'negotiation_issue': '',
                    'constraints': '',
                    'priority_areas': ''
                },
                'party_profile': '',
                'party_goals': '',
                'party_risk': '',
                'party_batna': '',
                'counterparty_profile': '',
                'counterparty_goals': '',
                'counterparty_risk': '',
                'other_relevant_info': ''
            }
            
            # Update required fields with extracted data
            for field, default_value in required_fields.items():
                if field not in case_data:
                    case_data[field] = default_value
                elif isinstance(default_value, dict) and isinstance(case_data[field], dict):
                    for subfield, subdefault in default_value.items():
                        if subfield not in case_data[field]:
                            case_data[field][subfield] = subdefault
            
            return case_data
            
        except Exception as e:
            logger.error(f"Error extracting case data: {str(e)}")
            raise
    