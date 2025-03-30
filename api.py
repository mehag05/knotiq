from flask import Flask, request, jsonify, send_from_directory, render_template
from flask_cors import CORS
from clv_analyzer import CLVAnalyzer
import os
import openai
from dotenv import load_dotenv
import json
import numpy as np
from functools import wraps

# Load environment variables
load_dotenv()

app = Flask(__name__, template_folder='templates')
CORS(app)

# Initialize OpenAI client
openai.api_key = os.getenv('OPENAI_API_KEY')

# Initialize analyzer
clv_analyzer = CLVAnalyzer()

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
        
        return jsonify({
            'status': 'success',
            'merchant_name': merchant_name,
            'top_customers': top_customers,
            'demographics': demographics
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

if __name__ == '__main__':
    app.run(debug=True, port=5001) 