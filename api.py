from flask import Flask, request, jsonify, send_from_directory, render_template, send_file
from flask_cors import CORS
from clv_analyzer import CLVAnalyzer
import os
import openai
from dotenv import load_dotenv
import json
import numpy as np
from functools import wraps
from customer_profile_generator import CustomerProfileGenerator
import io
import modal
from text_to_image import Inference
import requests

# Load environment variables
load_dotenv()

app = Flask(__name__, template_folder='templates')
CORS(app)

# Initialize OpenAI client
openai.api_key = os.getenv('OPENAI_API_KEY')

# Initialize analyzer
clv_analyzer = CLVAnalyzer()
profile_generator = CustomerProfileGenerator()

# Initialize Modal client
stub = modal.Stub("text-to-image")

# Simple merchant authentication (in production, use proper auth)
MERCHANT_CREDENTIALS = {
    "merchant1": "password1",
    "merchant2": "password2"
}

def require_merchant_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth_header = request.headers.get('Authorization')
        if not auth_header:
            return jsonify({'error': 'No authorization header'}), 401
        
        try:
            merchant_id, password = auth_header.split(':')
            if merchant_id not in MERCHANT_CREDENTIALS or MERCHANT_CREDENTIALS[merchant_id] != password:
                return jsonify({'error': 'Invalid credentials'}), 401
            return f(*args, **kwargs)
        except:
            return jsonify({'error': 'Invalid authorization format'}), 401
    return decorated

# Load data at startup
print("Loading data at startup...")
try:
    clv_analyzer.load_data()
    print(f"Successfully loaded data for {len(clv_analyzer.data)} customers")
except Exception as e:
    print(f"Error loading data at startup: {str(e)}")

@app.route('/api/status', methods=['GET'])
def check_status():
    """Check if the API is ready and data is loaded."""
    try:
        if not hasattr(clv_analyzer, 'data') or not clv_analyzer.data:
            return jsonify({
                'status': 'error',
                'message': 'Data not loaded',
                'ready': False
            }), 503
        return jsonify({
            'status': 'success',
            'message': 'API is ready',
            'ready': True,
            'customers_loaded': len(clv_analyzer.data)
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e),
            'ready': False
        }), 500

@app.route('/api/merchant/<merchant_name>/top-customers', methods=['GET'])
def get_merchant_top_customers(merchant_name):
    """Get top CLV customers and their demographics for a specific merchant."""
    try:
        # Get merchant's top customers and insights
        rankings = clv_analyzer.get_merchant_customer_rankings(merchant_name)
        insights = clv_analyzer.get_merchant_insights(merchant_name)
        
        if not rankings or not insights:
            return jsonify({
                'status': 'error',
                'message': f'No data found for merchant {merchant_name}'
            }), 404
        
        # Get top 10 customers
        top_customers = rankings[:10]
        
        # Get demographic insights
        demographics = {
            'total_customers': insights['total_customers'],
            'average_transaction_value': insights['average_transaction_value'],
            'total_revenue': insights['total_revenue'],
            'average_monthly_frequency': insights['average_purchase_frequency'],
            'retention_metrics': insights['retention_metrics']
        }
        
        # Generate profile and ad suggestions
        profile = profile_generator.generate_customer_profile(merchant_name, top_customers)
        ad_suggestions = profile_generator.generate_ad_suggestions(merchant_name, top_customers)
        
        return jsonify({
            'status': 'success',
            'merchant_name': merchant_name,
            'top_customers': top_customers,
            'demographics': demographics,
            'profile': profile,
            'ad_suggestions': ad_suggestions
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

@app.route('/api/text_to_image', methods=['POST'])
def generate_image():
    try:
        data = request.get_json()
        prompt = data.get('prompt')
        
        if not prompt:
            return jsonify({'error': 'No prompt provided'}), 400

        print(f"Received prompt: {prompt}")
        print("Attempting to generate image using Modal server...")

        try:
            # Call the Modal server endpoint
            response = requests.post(
                'https://mehag05--example-text-to-image-ui-dev.modal.run/api/text_to_image',
                json={'prompt': prompt},
                headers={'Content-Type': 'application/json'}
            )
            
            print(f"Modal server response status: {response.status_code}")
            print(f"Modal server response headers: {dict(response.headers)}")
            
            if not response.ok:
                try:
                    error_msg = response.json().get('error', 'Unknown error occurred')
                except:
                    error_msg = response.text
                print(f"Modal server error response: {error_msg}")
                return jsonify({'error': f"Modal server error: {error_msg}"}), 500
            
            if not response.content:
                print("No content in response")
                return jsonify({'error': "No image data received from Modal server"}), 500
            
            print(f"Successfully received image data of size: {len(response.content)} bytes")
            
            # Return the image directly from Modal server
            return send_file(
                io.BytesIO(response.content),
                mimetype='image/png'
            )
            
        except requests.exceptions.RequestException as e:
            print(f"Request error during Modal server call: {str(e)}")
            return jsonify({'error': f"Failed to connect to Modal server: {str(e)}"}), 500
        except Exception as e:
            print(f"Unexpected error during Modal server call: {str(e)}")
            return jsonify({'error': f"Unexpected error: {str(e)}"}), 500
            
    except Exception as e:
        print(f"Error generating image: {str(e)}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5001) 