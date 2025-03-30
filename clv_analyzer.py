import pandas as pd
import numpy as np
from datetime import datetime
import json
from typing import Dict, List, Tuple
import os

class CLVAnalyzer:
    def __init__(self):
        self.data = []
        self.customer_metrics = {}
        self.merchant_metrics = {}
        
    def load_data(self, data_dir: str = 'data'):
        """Load transaction data from the specified directory."""
        self.data = []
        for filename in os.listdir(data_dir):
            if filename.endswith('.txt'):
                with open(os.path.join(data_dir, filename), 'r') as f:
                    try:
                        customer_data = json.load(f)
                        self.data.append(customer_data)
                    except json.JSONDecodeError:
                        print(f"Error reading {filename}")
                        continue
    
    def normalize_merchant_name(self, url: str) -> str:
        """Extract merchant name from URL."""
        # Remove http(s):// and www.
        url = url.lower().replace('https://', '').replace('http://', '').replace('www.', '')
        # Get the domain part
        domain = url.split('/')[0]
        # Remove .com and similar endings
        merchant = domain.split('.')[0]
        return merchant

    def calculate_merchant_specific_metrics(self, merchant_name: str) -> Dict:
        """Calculate customer metrics specific to a merchant."""
        merchant_customers = {}
        
        # Convert merchant name to lowercase for matching
        merchant_match = merchant_name.lower()
        
        for customer in self.data:
            customer_id = customer['customer_type']
            
            # Filter transactions for this merchant based on URL
            merchant_transactions = [
                t for t in customer['transactions'] 
                if merchant_match == self.normalize_merchant_name(t['url'])
            ]
            
            if not merchant_transactions:
                continue
                
            # Convert transaction dates to datetime objects (timezone-naive)
            dates = [datetime.fromisoformat(t['datetime'].replace('Z', '+00:00')).replace(tzinfo=None) 
                    for t in merchant_transactions]
            
            # Calculate merchant-specific metrics
            total_spend = sum(float(t['price']['total']) for t in merchant_transactions)
            num_transactions = len(merchant_transactions)
            first_purchase = min(dates)
            last_purchase = max(dates)
            
            # Calculate months between first and last purchase
            months_active = max(1, (last_purchase - first_purchase).days / 30.0)
            
            # Calculate monthly purchase frequency
            monthly_frequency = num_transactions / months_active
            
            # Calculate CLV score
            clv_score = (
                0.4 * total_spend +  # 40% weight on total spend
                0.3 * (num_transactions * 100) +  # 30% weight on frequency
                0.3 * (months_active * 1000)  # 30% weight on longevity
            )
            
            merchant_customers[customer_id] = {
                'total_spend': total_spend,
                'num_transactions': num_transactions,
                'avg_transaction_value': total_spend / num_transactions if num_transactions > 0 else 0,
                'purchase_frequency': monthly_frequency,  # transactions per month
                'months_active': months_active,
                'clv_score': clv_score,
                'first_purchase': first_purchase.isoformat(),
                'last_purchase': last_purchase.isoformat()
            }
            
        return merchant_customers
    
    def get_merchant_customer_rankings(self, merchant_id: str) -> List[Dict]:
        """Get ranked list of customers for a specific merchant based on their CLV."""
        if merchant_id not in self.merchant_metrics:
            self.merchant_metrics[merchant_id] = self.calculate_merchant_specific_metrics(merchant_id)
        
        # Convert to list and sort by CLV score
        customer_rankings = [
            {
                'customer_id': customer_id,
                **metrics
            }
            for customer_id, metrics in self.merchant_metrics[merchant_id].items()
        ]
        
        # Sort by CLV score in descending order
        customer_rankings.sort(key=lambda x: x['clv_score'], reverse=True)
        
        return customer_rankings
    
    def get_merchant_insights(self, merchant_id: str) -> Dict:
        """Get detailed insights about customers for a specific merchant."""
        if merchant_id not in self.merchant_metrics:
            self.merchant_metrics[merchant_id] = self.calculate_merchant_specific_metrics(merchant_id)
        
        merchant_customers = self.merchant_metrics[merchant_id]
        
        if not merchant_customers:
            return {}
        
        # Calculate merchant-level metrics
        total_customers = len(merchant_customers)
        total_spend = sum(c['total_spend'] for c in merchant_customers.values())
        avg_transaction_value = np.mean([c['avg_transaction_value'] for c in merchant_customers.values()])
        avg_purchase_frequency = np.mean([c['purchase_frequency'] for c in merchant_customers.values()])
        
        # Calculate retention metrics
        repeat_customers = sum(1 for c in merchant_customers.values() if c['num_transactions'] > 1)
        retention_rate = (repeat_customers / total_customers) * 100 if total_customers > 0 else 0
        
        # Calculate average time between purchases
        time_between_purchases = []
        for customer in self.data:
            merchant_transactions = [
                t for t in customer['transactions'] 
                if self.normalize_merchant_name(t['url']) == merchant_id.lower()
            ]
            if len(merchant_transactions) > 1:
                dates = sorted([datetime.fromisoformat(t['datetime'].replace('Z', '+00:00')).replace(tzinfo=None) 
                              for t in merchant_transactions])
                for i in range(1, len(dates)):
                    time_between_purchases.append((dates[i] - dates[i-1]).days)
        
        avg_time_between_purchases = np.mean(time_between_purchases) if time_between_purchases else 0
        
        # Calculate churn rate (customers who haven't purchased in last 30 days)
        current_date = datetime.now().replace(tzinfo=None)  # Make current date timezone-naive
        churned_customers = sum(1 for c in merchant_customers.values() 
                              if (current_date - datetime.fromisoformat(c['last_purchase'].replace('Z', '+00:00')).replace(tzinfo=None)).days > 30)
        churn_rate = (churned_customers / total_customers) * 100 if total_customers > 0 else 0
        
        # Get top customers
        top_customers = self.get_merchant_customer_rankings(merchant_id)[:5]
        
        return {
            'merchant_id': merchant_id,
            'total_customers': total_customers,
            'total_revenue': total_spend,
            'average_transaction_value': avg_transaction_value,
            'average_purchase_frequency': avg_purchase_frequency,
            'retention_metrics': {
                'retention_rate': round(retention_rate, 2),
                'repeat_customers': repeat_customers,
                'avg_time_between_purchases': round(avg_time_between_purchases, 1),
                'churn_rate': round(churn_rate, 2),
                'churned_customers': churned_customers
            },
            'top_customers': top_customers
        }
    
    def get_similar_merchant_customers(self, merchant_id: str, top_n: int = 5) -> List[Dict]:
        """Find customers who haven't purchased from this merchant but are similar to existing customers."""
        if merchant_id not in self.merchant_metrics:
            self.merchant_metrics[merchant_id] = self.calculate_merchant_specific_metrics(merchant_id)
        
        merchant_customers = self.merchant_metrics[merchant_id]
        
        if not merchant_customers:
            return []
        
        # Calculate average metrics for merchant's current customers
        avg_metrics = {
            'total_spend': np.mean([c['total_spend'] for c in merchant_customers.values()]),
            'monthly_frequency': np.mean([c['purchase_frequency'] for c in merchant_customers.values()]),
            'avg_transaction': np.mean([c['avg_transaction_value'] for c in merchant_customers.values()])
        }
        
        # Find similar customers who haven't purchased from this merchant
        recommendations = []
        for customer in self.data:
            customer_id = customer['customer_type']
            if customer_id not in merchant_customers:
                # Calculate customer's overall metrics
                transactions = customer['transactions']
                if not transactions:
                    continue
                    
                total_spend = sum(float(t['amount']) for t in transactions)
                num_transactions = len(transactions)
                dates = [datetime.fromisoformat(t['date'].replace('Z', '+00:00')) for t in transactions]
                days_active = (max(dates) - min(dates)).days
                months_active = max(1, days_active / 30)
                monthly_frequency = num_transactions / months_active
                avg_transaction = total_spend / num_transactions
                
                # Calculate similarity score
                similarity_score = (
                    0.4 * (total_spend / avg_metrics['total_spend']) +
                    0.3 * (monthly_frequency / avg_metrics['monthly_frequency']) +
                    0.3 * (avg_transaction / avg_metrics['avg_transaction'])
                )
                
                recommendations.append({
                    'customer_id': customer_id,
                    'similarity_score': similarity_score,
                    'total_spend': total_spend,
                    'monthly_frequency': monthly_frequency,
                    'avg_transaction': avg_transaction
                })
        
        # Sort by similarity score and return top N
        recommendations.sort(key=lambda x: x['similarity_score'], reverse=True)
        return recommendations[:top_n] 