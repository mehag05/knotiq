import os
from dotenv import load_dotenv
import openai
import logging

load_dotenv()

# Initialize OpenAI client with API key
openai.api_key = os.getenv('OPENAI_KEY')

logger = logging.getLogger(__name__)


def generate_ad_prompt(segment):
    """
    Generate an engaging Instagram post for Uber targeting a specific customer segment.

    Args:
        segment (object): An object with 'name' and 'description' attributes.

    Returns:
        str: The generated Instagram post content.
    """
    system_prompt = """
    You are a professional designer and marketer tasked with creating an engaging Instagram post for Uber targeting a specific customer segment. 
    Your goal is to resonate with this audience while maintaining Uber's brand voice: professional yet approachable, innovative, and customer-focused. 

    Generate the following elements for the Instagram post:

    {
        "visual_description": "A compelling visual description (image/graphic concept)",
        "headline": "Attention-grabbing headline (max 70 characters)",
        "caption": "Engaging caption (include emojis, max 200 characters)",
        "hashtags": "3-5 relevant hashtags",
        "call_to_action": "A clear call-to-action"
    }

    Ensure that the content reflects the context provided about the segment, including its description and characteristics.
    """

    user_prompt = f"""Please create an engaging Instagram post for Uber targeting {segment.name}.

    Context: {segment.description}

    Provide a complete response with all the elements specified in the system prompt.
    """
    
    try:
        response = openai.ChatCompletion.create(  # Correct method for chat-based models
            model="gpt-4",  # Ensure you're using a valid model name
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ]
        )
        
        content = response.choices[0].message.content
        return content
    
    except Exception as e:
        logger.error(f"Error generating ad prompt: {str(e)}")
        raise

