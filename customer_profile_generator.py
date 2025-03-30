import openai
from datetime import datetime
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()
openai.api_key = os.getenv('OPENAI_API_KEY')

class CustomerProfileGenerator:
    def __init__(self):
        self.profile_cache = {}

    def analyze_spending_patterns(self, customers):
        """Analyze spending patterns of top customers"""
        avg_transaction = sum(c['avg_transaction_value'] for c in customers) / len(customers)
        avg_frequency = sum(c['purchase_frequency'] for c in customers) / len(customers)
        total_spend = sum(c['total_spend'] for c in customers)
        
        # Categorize spending behavior
        high_spenders = len([c for c in customers if c['avg_transaction_value'] > 100])
        moderate_spenders = len([c for c in customers if 50 <= c['avg_transaction_value'] <= 100])
        low_spenders = len([c for c in customers if c['avg_transaction_value'] < 50])
        
        return {
            'average_transaction': avg_transaction,
            'average_frequency': avg_frequency,
            'total_spend': total_spend,
            'spending_distribution': {
                'high_spenders': high_spenders,
                'moderate_spenders': moderate_spenders,
                'low_spenders': low_spenders
            }
        }

    def analyze_purchase_behavior(self, customers):
        """Analyze purchase behavior patterns"""
        avg_frequency = sum(c['purchase_frequency'] for c in customers) / len(customers)
        recent_shoppers = len([c for c in customers if (datetime.now() - datetime.fromisoformat(c['last_purchase'].replace('Z', '+00:00'))).days < 30])
        
        return {
            'average_frequency': avg_frequency,
            'recent_shoppers': recent_shoppers,
            'regular_shoppers': len([c for c in customers if c['purchase_frequency'] > 1.5])
        }

    def identify_customer_segments(self, customers):
        """Identify main customer segments"""
        segments = {
            'vip_customers': len([c for c in customers if c['clv_score'] > 1000 and c['purchase_frequency'] > 2]),
            'high_value_regulars': len([c for c in customers if c['clv_score'] > 500 and c['purchase_frequency'] > 1.5]),
            'mid_value_customers': len([c for c in customers if c['clv_score'] > 200]),
            'standard_customers': len([c for c in customers if c['clv_score'] <= 200])
        }
        return segments

    def generate_customer_profile(self, merchant_name, top_customers):
        """Generate a comprehensive customer profile using GPT"""
        if not top_customers:
            return None
            
        # Calculate metrics
        spending_patterns = self.analyze_spending_patterns(top_customers)
        purchase_behavior = self.analyze_purchase_behavior(top_customers)
        customer_segments = self.identify_customer_segments(top_customers)
        
        # Create prompt for GPT
        prompt = f"""Based on the following customer data for {merchant_name}, generate a detailed profile that focuses on specific, data-driven insights about their spending behavior and purchase patterns.

Key Metrics:
- Average Transaction Value: ${spending_patterns['average_transaction']:.2f}
- Average Monthly Frequency: {purchase_behavior['average_frequency']:.2f}
- Total Customer Spend: ${spending_patterns['total_spend']:.2f}

Customer Segments:
- VIP Customers: {customer_segments['vip_customers']}
- High-Value Regulars: {customer_segments['high_value_regulars']}
- Mid-Value Customers: {customer_segments['mid_value_customers']}
- Standard Customers: {customer_segments['standard_customers']}

Spending Distribution:
- High Spenders: {spending_patterns['spending_distribution']['high_spenders']}
- Moderate Spenders: {spending_patterns['spending_distribution']['moderate_spenders']}
- Low Spenders: {spending_patterns['spending_distribution']['low_spenders']}

Purchase Behavior:
- Regular Shoppers: {purchase_behavior['regular_shoppers']}
- Recent Shoppers: {purchase_behavior['recent_shoppers']}

Generate a profile that focuses on:
1. Specific spending patterns (e.g., "showing a preference for $100+ transactions", "maintaining $50-75 monthly spending")
2. Concrete purchase behaviors (e.g., "shopping 2-3 times per month", "making bulk purchases during holiday seasons")
3. Distinct customer characteristics based on data (e.g., "early morning shoppers", "weekend purchasers")
4. Specific engagement patterns (e.g., "responding to seasonal promotions", "participating in loyalty programs")

Avoid generic terms like "regular shoppers", "high loyalty", or "value-conscious". Instead, use specific data points and patterns.

Format: A single, detailed phrase that captures these specific insights, like "Customers averaging $120 transactions with 2.5 monthly visits, showing strong weekend shopping patterns and responding to seasonal promotions" or "Shoppers maintaining $60-80 monthly spend with 1.8 monthly visits, demonstrating preference for bulk purchases during holiday periods"."""

        try:
            response = openai.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a data-driven marketing analyst who creates specific, measurable customer profiles based on concrete spending and purchase patterns. Avoid generic terms and focus on specific data points and behaviors."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=100,
                temperature=0.7
            )
            
            profile = response.choices[0].message.content.strip()
            self.profile_cache[merchant_name] = profile
            return profile
            
        except Exception as e:
            print(f"Error generating profile: {str(e)}")
            return None

    def generate_ad_suggestions(self, merchant_name, top_customers):
        """Generate specific ad suggestions based on the customer profile"""
        profile = self.generate_customer_profile(merchant_name, top_customers)
        if not profile:
            return None
            
        prompt = f"""Based on the following customer profile for {merchant_name}, generate specific ad suggestions:

Customer Profile:
{profile}

Generate:
1. 3-4 specific ad headlines that would resonate with this customer base
2. Key messaging points to emphasize
3. Suggested visual elements or themes
4. Recommended call-to-action approaches

Format the response as structured ad suggestions."""

        try:
            response = openai.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are an advertising expert who creates targeted, effective ad suggestions based on customer profiles."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=400,
                temperature=0.7
            )
            
            return response.choices[0].message.content.strip()
            
        except Exception as e:
            print(f"Error generating ad suggestions: {str(e)}")
            return None

# Example usage:
if __name__ == "__main__":
    # This would be used with the existing CLVAnalyzer
    from clv_analyzer import CLVAnalyzer
    
    # Initialize analyzers
    clv_analyzer = CLVAnalyzer()
    profile_generator = CustomerProfileGenerator()
    
    # Load data
    clv_analyzer.load_data()
    
    # Example merchant
    merchant_name = "Carvana"
    
    # Get top customers
    top_customers = clv_analyzer.get_merchant_customer_rankings(merchant_name)[:10]
    
    # Generate profile and ad suggestions
    profile = profile_generator.generate_customer_profile(merchant_name, top_customers)
    ad_suggestions = profile_generator.generate_ad_suggestions(merchant_name, top_customers)
    
    # Print results
    print(f"\nCustomer Profile for {merchant_name}:")
    print(profile)
    print("\nAd Suggestions:")
    print(ad_suggestions) 