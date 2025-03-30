# import json
# import os
# import numpy as np
# from sklearn.preprocessing import StandardScaler, RobustScaler
# from sklearn.impute import SimpleImputer
# from sklearn.cluster import KMeans
# from sklearn.decomposition import PCA
# from collections import defaultdict, Counter
# import pandas as pd
# from datetime import datetime
# from typing import List, Dict, Any
# from sklearn.model_selection import train_test_split
# from sklearn.metrics import silhouette_score, calinski_harabasz_score, davies_bouldin_score
# import random
# from scipy.spatial.distance import pdist
# import requests

# class CustomerAnalyzer:
#     def __init__(self, data_dir: str = "data"):
#         self.data_dir = data_dir
#         self.customers_data = {}
#         self.features_df = None
#         self.clusters = None
#         self.cluster_profiles = {}
#         self.train_data = None
#         self.test_data = None
#         self.train_clusters = None
#         self.test_clusters = None
#         self.pca = None
#         self.amount_scaler = RobustScaler()  # For amount-based features
#         self.ratio_scaler = StandardScaler()  # For ratio-based features
#         self.imputer = SimpleImputer(strategy='mean')
#         self.llm_endpoint = "http://localhost:5001/api/generate-cluster-profile"
        
#     def load_data(self):
#         """Load customer data from files."""
#         try:
#             # Generate customer data if it doesn't exist
#             if not os.path.exists('customer_data.json'):
#                 print("Generating customer data...")
#                 from mock_customer_data import MockTransactionGenerator
#                 generator = MockTransactionGenerator()
#                 customer_files = generator.generate_diverse_customers(num_customers=100, transactions_per_customer=200)
#                 with open('customer_data.json', 'w') as f:
#                     json.dump(customer_files, f)
            
#             # Load customer data
#             with open('customer_data.json', 'r') as f:
#                 customer_files = json.load(f)
            
#             # Process customer data
#             self.data = []
#             for customer in customer_files:
#                 if not customer.get('data') or not customer['data'][0].get('transactions'):
#                     continue
                    
#                 customer_data = {
#                     'customer_id': customer['persona']['name'].split()[-1],  # Extract number from "Customer X"
#                     'transactions': customer['data'][0]['transactions']  # All transactions are in first merchant
#                 }
#                 self.data.append(customer_data)
            
#             if not self.data:
#                 raise ValueError("No valid customer data found")
                
#             print(f"Loaded data for {len(self.data)} customers")
            
#         except Exception as e:
#             print(f"Error loading data: {str(e)}")
#             raise

#     def extract_customer_features(self, customer_data):
#         """Extract features for a single customer."""
#         transactions = customer_data['transactions']
        
#         if not transactions:
#             return None
            
#         # Basic transaction metrics
#         amounts = [float(t['price']['total']) for t in transactions]
#         avg_amount = np.mean(amounts)
#         max_amount = np.max(amounts)
#         min_amount = np.min(amounts)
#         amount_std = np.std(amounts)
        
#         # Transaction frequency and timing patterns
#         dates = [datetime.strptime(t['datetime'], "%Y-%m-%dT%H:%M:%S+00:00") for t in transactions]
#         if len(dates) > 1:
#             date_range = (max(dates) - min(dates)).days + 1
#             frequency = len(transactions) / date_range if date_range > 0 else len(transactions)
            
#             # Calculate day-of-week preferences
#             day_counts = Counter(d.weekday() for d in dates)
#             weekend_ratio = (day_counts[5] + day_counts[6]) / len(dates)
            
#             # Calculate time-of-day preferences
#             hour_counts = Counter(d.hour for d in dates)
#             morning_ratio = sum(hour_counts[h] for h in range(6, 12)) / len(dates)
#             afternoon_ratio = sum(hour_counts[h] for h in range(12, 18)) / len(dates)
#             evening_ratio = sum(hour_counts[h] for h in range(18, 24)) / len(dates)
#         else:
#             frequency = 1
#             weekend_ratio = 0.5
#             morning_ratio = 0.33
#             afternoon_ratio = 0.33
#             evening_ratio = 0.34
        
#         # Category preferences
#         category_counts = defaultdict(int)
#         total_transactions = len(transactions)
        
#         for t in transactions:
#             product_name = t['products'][0]['name'].lower() if t.get('products') else ''
#             url = t.get('url', '').lower()
            
#             if any(term in product_name or term in url for term in ['electronics', 'tech', 'computer', 'phone']):
#                 category_counts['electronics'] += 1
#             elif any(term in product_name or term in url for term in ['grocery', 'mart', 'food', 'market']):
#                 category_counts['groceries'] += 1
#             elif any(term in product_name or term in url for term in ['fashion', 'clothing', 'apparel', 'boutique']):
#                 category_counts['fashion'] += 1
#             elif any(term in product_name or term in url for term in ['home', 'furnish', 'decor', 'garden']):
#                 category_counts['home'] += 1
#             elif any(term in product_name or term in url for term in ['restaurant', 'cafe', 'dining']):
#                 category_counts['dining'] += 1
#             elif any(term in product_name or term in url for term in ['pharmacy', 'drug', 'health']):
#                 category_counts['health'] += 1
#             elif any(term in product_name or term in url for term in ['travel', 'airline', 'hotel']):
#                 category_counts['travel'] += 1
#             elif any(term in product_name or term in url for term in ['entertainment', 'movie', 'game']):
#                 category_counts['entertainment'] += 1
        
#         # Normalize category ratios to percentages
#         category_ratios = {}
#         if total_transactions > 0:
#             for category, count in category_counts.items():
#                 category_ratios[category] = count / total_transactions
        
#         # Payment method preferences
#         payment_counts = defaultdict(int)
#         for t in transactions:
#             for pm in t['payment_methods']:
#                 payment_counts[pm['type']] += 1
        
#         # Normalize payment ratios
#         total_payments = sum(payment_counts.values())
#         payment_ratios = {}
#         if total_payments > 0:
#             for method, count in payment_counts.items():
#                 payment_ratios[method] = count / total_payments
        
#         # Feature vector with all metrics
#         feature_vector = [
#             avg_amount, max_amount, min_amount, amount_std,  # Amount metrics
#             frequency,  # Transaction frequency
#             weekend_ratio, morning_ratio, afternoon_ratio, evening_ratio,  # Timing patterns
#             *category_ratios.values(),  # Category preferences
#             *payment_ratios.values()  # Payment preferences
#         ]
        
#         return np.array(feature_vector)

#     def extract_features(self, data):
#         """Extract relevant features from transaction data for clustering."""
#         try:
#             features = []
#             labels = []
            
#             for customer_data in data:
#                 if not customer_data.get('transactions'):
#                     continue
                    
#                 customer_id = customer_data['customer_id']
#                 transactions = customer_data['transactions']
                
#                 # Basic transaction metrics
#                 amounts = []
#                 for t in transactions:
#                     try:
#                         amount = float(t['price']['total'])
#                         amounts.append(amount)
#                     except (ValueError, KeyError):
#                         continue
                
#                 if not amounts:
#                     continue
                    
#                 avg_amount = np.mean(amounts)
#                 max_amount = np.max(amounts)
#                 min_amount = np.min(amounts)
#                 amount_std = np.std(amounts)
                
#                 # Transaction frequency and timing patterns
#                 dates = []
#                 for t in transactions:
#                     try:
#                         date = datetime.strptime(t['datetime'], "%Y-%m-%dT%H:%M:%S+00:00")
#                         dates.append(date)
#                     except (ValueError, KeyError):
#                         continue
                
#                 if len(dates) > 1:
#                     date_range = (max(dates) - min(dates)).days + 1
#                     frequency = len(transactions) / date_range if date_range > 0 else len(transactions)
                    
#                     # Calculate day-of-week preferences
#                     day_counts = Counter(d.weekday() for d in dates)
#                     weekend_ratio = (day_counts[5] + day_counts[6]) / len(dates)
                    
#                     # Calculate time-of-day preferences
#                     hour_counts = Counter(d.hour for d in dates)
#                     morning_ratio = sum(hour_counts[h] for h in range(6, 12)) / len(dates)
#                     afternoon_ratio = sum(hour_counts[h] for h in range(12, 18)) / len(dates)
#                     evening_ratio = sum(hour_counts[h] for h in range(18, 24)) / len(dates)
#                 else:
#                     frequency = 1
#                     weekend_ratio = 0.5
#                     morning_ratio = 0.33
#                     afternoon_ratio = 0.33
#                     evening_ratio = 0.34
                
#                 # Category preferences
#                 category_counts = defaultdict(int)
#                 for t in transactions:
#                     try:
#                         product_name = t['products'][0]['name'].lower() if t.get('products') else ''
#                         url = t.get('url', '').lower()
                        
#                         if any(term in product_name or term in url for term in ['electronics', 'tech', 'computer', 'phone']):
#                             category_counts['electronics'] += 1
#                         elif any(term in product_name or term in url for term in ['grocery', 'mart', 'food', 'market']):
#                             category_counts['groceries'] += 1
#                         elif any(term in product_name or term in url for term in ['fashion', 'clothing', 'apparel', 'boutique']):
#                             category_counts['fashion'] += 1
#                         elif any(term in product_name or term in url for term in ['home', 'furnish', 'decor', 'garden']):
#                             category_counts['home'] += 1
#                         elif any(term in product_name or term in url for term in ['restaurant', 'cafe', 'dining']):
#                             category_counts['dining'] += 1
#                         elif any(term in product_name or term in url for term in ['pharmacy', 'drug', 'health']):
#                             category_counts['health'] += 1
#                         elif any(term in product_name or term in url for term in ['travel', 'airline', 'hotel']):
#                             category_counts['travel'] += 1
#                         elif any(term in product_name or term in url for term in ['entertainment', 'movie', 'game']):
#                             category_counts['entertainment'] += 1
#                     except (KeyError, IndexError):
#                         continue
                
#                 total_transactions = len(transactions)
#                 if total_transactions == 0:
#                     continue
                    
#                 category_ratios = {
#                     'electronics': category_counts['electronics'] / total_transactions,
#                     'groceries': category_counts['groceries'] / total_transactions,
#                     'fashion': category_counts['fashion'] / total_transactions,
#                     'home': category_counts['home'] / total_transactions,
#                     'dining': category_counts['dining'] / total_transactions,
#                     'health': category_counts['health'] / total_transactions,
#                     'travel': category_counts['travel'] / total_transactions,
#                     'entertainment': category_counts['entertainment'] / total_transactions
#                 }
                
#                 # Feature vector with all metrics
#                 feature_vector = [
#                     avg_amount, max_amount, min_amount, amount_std,  # Amount metrics
#                     frequency,  # Transaction frequency
#                     weekend_ratio, morning_ratio, afternoon_ratio, evening_ratio,  # Timing patterns
#                     *category_ratios.values()  # Category preferences
#                 ]
                
#                 features.append(feature_vector)
#                 labels.append(customer_id)
            
#             if not features:
#                 raise ValueError("No valid features extracted from data")
                
#             return np.array(features), labels
            
#         except Exception as e:
#             print(f"Error extracting features: {str(e)}")
#             raise

#     def split_data(self, test_size: float = 0.2) -> None:
#         """Split data into training and test sets."""
#         if not hasattr(self, 'data') or not self.data:
#             raise ValueError("No data available for splitting")
            
#         # Get indices for all customers
#         indices = list(range(len(self.data)))
#         if not indices:
#             raise ValueError("No customers found in data")
            
#         # Calculate split sizes
#         train_size = int((1 - test_size) * len(indices))
#         if train_size == 0:
#             raise ValueError("Not enough data to split")
            
#         # Randomly shuffle indices
#         random.shuffle(indices)
        
#         # Split indices
#         train_indices = indices[:train_size]
#         test_indices = indices[train_size:]
        
#         # Create train and test lists
#         self.train_data = [self.data[i] for i in train_indices]
#         self.test_data = [self.data[i] for i in test_indices]
        
#         print(f"\nSplitting data into train and test sets...")
#         print(f"Training set size: {len(self.train_data)}")
#         print(f"Test set size: {len(self.test_data)}")

#     def find_optimal_clusters(self, scaled_features: np.ndarray) -> int:
#         """Find optimal number of clusters using multiple metrics."""
#         # Allow more clusters based on data size
#         max_clusters = min(10, len(scaled_features) // 5)
#         min_clusters = 2
        
#         if len(scaled_features) < 2:
#             return 2
        
#         results = []
#         for k in range(min_clusters, max_clusters + 1):
#             try:
#                 kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
#                 labels = kmeans.fit_predict(scaled_features)
                
#                 # Calculate clustering metrics
#                 silhouette = silhouette_score(scaled_features, labels)
#                 calinski = calinski_harabasz_score(scaled_features, labels)
#                 davies = davies_bouldin_score(scaled_features, labels)
#                 inertia = kmeans.inertia_
                
#                 results.append({
#                     'k': k,
#                     'silhouette': silhouette,
#                     'calinski': calinski,
#                     'davies': davies,
#                     'inertia': inertia
#                 })
                
#                 print(f"\nMetrics for k={k}:")
#                 print(f"Silhouette Score: {silhouette:.3f}")
#                 print(f"Calinski-Harabasz Score: {calinski:.3f}")
#                 print(f"Davies-Bouldin Score: {davies:.3f}")
                
#             except Exception as e:
#                 print(f"Error calculating metrics for k={k}: {str(e)}")
#                 continue
        
#         if not results:
#             print("Warning: No valid clustering results found, defaulting to 2 clusters")
#             return 2
        
#         # Convert to DataFrame for analysis
#         results_df = pd.DataFrame(results)
        
#         # Normalize metrics for comparison
#         for col in ['silhouette', 'calinski', 'davies', 'inertia']:
#             if results_df[col].max() != results_df[col].min():
#                 results_df[col + '_norm'] = (results_df[col] - results_df[col].min()) / (results_df[col].max() - results_df[col].min())
#             else:
#                 results_df[col + '_norm'] = 0.5
        
#         # Invert normalized scores where lower is better
#         results_df['davies_norm'] = 1 - results_df['davies_norm']
#         results_df['inertia_norm'] = 1 - results_df['inertia_norm']
        
#         # Calculate weighted score with emphasis on silhouette and calinski
#         results_df['score'] = (
#             results_df['silhouette_norm'] * 0.4 +     # Increased weight for silhouette
#             results_df['calinski_norm'] * 0.3 +       # Increased weight for calinski
#             results_df['davies_norm'] * 0.2 +         # Reduced weight for davies
#             results_df['inertia_norm'] * 0.1          # Reduced weight for inertia
#         )
        
#         # Add penalty for too few clusters
#         results_df['score'] = results_df['score'] * (1 + 0.1 * (results_df['k'] - 2))
        
#         # Find optimal k
#         optimal_k = results_df.loc[results_df['score'].idxmax(), 'k']
        
#         print("\nClustering Metrics Analysis:")
#         print(f"Optimal number of clusters: {int(optimal_k)}")
#         print("\nMetric ranges:")
#         print(f"Silhouette Score: {results_df['silhouette'].min():.3f} to {results_df['silhouette'].max():.3f}")
#         print(f"Calinski-Harabasz Score: {results_df['calinski'].min():.3f} to {results_df['calinski'].max():.3f}")
#         print(f"Davies-Bouldin Score: {results_df['davies'].min():.3f} to {results_df['davies'].max():.3f}")
        
#         return int(optimal_k)
        
#     def cluster_customers(self):
#         """Cluster customers based on their features and next brand predictions."""
#         try:
#             # Extract features first if not already done
#             if not hasattr(self, 'features') or self.features is None:
#                 print("Extracting features from customer data...")
#                 self.features, self.labels = self.extract_features(self.data)
                
#             if len(self.features) < 2:
#                 print("Not enough data points for clustering")
#                 return {
#                     'status': 'error',
#                     'message': 'Not enough data points for clustering'
#                 }
                
#             # Scale features
#             self.features_scaled = self.amount_scaler.fit_transform(self.features)
            
#             # Determine optimal number of clusters
#             self.n_clusters = self.find_optimal_clusters(self.features_scaled)
            
#             # Initialize and fit K-means
#             self.kmeans = KMeans(n_clusters=self.n_clusters, random_state=42)
#             self.kmeans.fit(self.features_scaled)
            
#             # Analyze clusters
#             cluster_analysis = {}
#             for cluster_id in range(self.n_clusters):
#                 # Get customers in this cluster
#                 cluster_customers = [cust for i, cust in enumerate(self.data) if self.kmeans.labels_[i] == cluster_id]
                
#                 # Calculate basic metrics
#                 cluster_size = len(cluster_customers)
#                 total_customers = len(self.data)
#                 percentage = round((cluster_size / total_customers) * 100, 1)
                
#                 # Calculate mean values for various features
#                 cluster_feature_values = self.features[self.kmeans.labels_ == cluster_id]
#                 mean_values = {
#                     'avg_transaction_amount': round(np.mean(cluster_feature_values[:, 0]), 2),
#                     'max_amount': round(np.mean(cluster_feature_values[:, 1]), 2),
#                     'min_amount': round(np.mean(cluster_feature_values[:, 2]), 2),
#                     'amount_std': round(np.mean(cluster_feature_values[:, 3]), 2),
#                     'transaction_frequency': round(np.mean(cluster_feature_values[:, 4]), 2),
#                     'weekend_ratio': round(np.mean(cluster_feature_values[:, 5]) * 100, 1),
#                     'morning_ratio': round(np.mean(cluster_feature_values[:, 6]) * 100, 1),
#                     'afternoon_ratio': round(np.mean(cluster_feature_values[:, 7]) * 100, 1),
#                     'evening_ratio': round(np.mean(cluster_feature_values[:, 8]) * 100, 1)
#                 }
                
#                 # Calculate category ratios
#                 category_counts = defaultdict(int)
#                 total_transactions = 0
                
#                 for customer in cluster_customers:
#                     for transaction in customer['transactions']:
#                         total_transactions += 1
#                         product_name = transaction['products'][0]['name'].lower() if transaction.get('products') else ''
#                         url = transaction.get('url', '').lower()
                        
#                         if any(term in product_name or term in url for term in ['electronics', 'tech', 'computer', 'phone']):
#                             category_counts['electronics'] += 1
#                         elif any(term in product_name or term in url for term in ['grocery', 'mart', 'food', 'market']):
#                             category_counts['groceries'] += 1
#                         elif any(term in product_name or term in url for term in ['fashion', 'clothing', 'apparel', 'boutique']):
#                             category_counts['fashion'] += 1
#                         elif any(term in product_name or term in url for term in ['home', 'furnish', 'decor', 'garden']):
#                             category_counts['home'] += 1
#                         elif any(term in product_name or term in url for term in ['restaurant', 'cafe', 'dining']):
#                             category_counts['dining'] += 1
#                         elif any(term in product_name or term in url for term in ['pharmacy', 'drug', 'health']):
#                             category_counts['health'] += 1
#                         elif any(term in product_name or term in url for term in ['travel', 'airline', 'hotel']):
#                             category_counts['travel'] += 1
#                         elif any(term in product_name or term in url for term in ['entertainment', 'movie', 'game']):
#                             category_counts['entertainment'] += 1
                
#                 # Normalize category ratios to percentages
#                 category_ratios = {}
#                 if total_transactions > 0:
#                     for category, count in category_counts.items():
#                         category_ratios[category] = round((count / total_transactions) * 100, 1)
                
#                 # Calculate timing patterns
#                 timing = {
#                     'weekend_ratio': mean_values['weekend_ratio'],
#                     'morning_ratio': mean_values['morning_ratio'],
#                     'afternoon_ratio': mean_values['afternoon_ratio'],
#                     'evening_ratio': mean_values['evening_ratio']
#                 }
                
#                 # Ensure timing ratios sum to 100%
#                 total_timing = sum(timing.values())
#                 if total_timing > 0:
#                     timing = {k: round((v / total_timing) * 100, 1) for k, v in timing.items()}
                
#                 # Predict next brand for the cluster
#                 next_brand = self.predict_next_brand(cluster_customers[0])
                
#                 # Generate cluster label
#                 label = self.generate_cluster_label({
#                     'size': cluster_size,
#                     'percentage': percentage,
#                     'mean_values': mean_values,
#                     'category_ratios': category_ratios,
#                     'timing': timing,
#                     'next_brand': next_brand
#                 })
                
#                 # Store cluster analysis
#                 cluster_analysis[cluster_id] = {
#                     'label': label,
#                     'size': cluster_size,
#                     'percentage': percentage,
#                     'avg_transaction_amount': mean_values['avg_transaction_amount'],
#                     'timing': timing,
#                     'top_categories': category_ratios,
#                     'next_brand': next_brand
#                 }
            
#             # Calculate clustering metrics
#             metrics = {
#                 'silhouette': round(silhouette_score(self.features_scaled, self.kmeans.labels_), 3),
#                 'calinski_harabasz': round(calinski_harabasz_score(self.features_scaled, self.kmeans.labels_), 3),
#                 'davies_bouldin': round(davies_bouldin_score(self.features_scaled, self.kmeans.labels_), 3)
#             }
            
#             return {
#                 'status': 'success',
#                 'cluster_analysis': cluster_analysis,
#                 'metrics': metrics
#             }
            
#         except Exception as e:
#             print(f"Error in clustering: {str(e)}")
#             return {
#                 'status': 'error',
#                 'message': str(e)
#             }
    
#     def evaluate_clustering(self) -> Dict[str, float]:
#         """Evaluate clustering quality using multiple metrics."""
#         if not hasattr(self, 'kmeans') or not hasattr(self, 'features'):
#             raise ValueError("Must run clustering before evaluation")
        
#         # Get scaled features
#         features_scaled = self.amount_scaler.transform(self.features)
        
#         # Calculate metrics
#         silhouette = silhouette_score(features_scaled, self.kmeans.labels_)
#         calinski = calinski_harabasz_score(features_scaled, self.kmeans.labels_)
#         davies = davies_bouldin_score(features_scaled, self.kmeans.labels_)
        
#         return {
#             'silhouette': silhouette,
#             'calinski_harabasz': calinski,
#             'davies_bouldin': davies
#         }
    
#     def analyze_clusters(self):
#         """Analyze each cluster and generate insights"""
#         cluster_insights = {}
        
#         # Get unique cluster labels
#         unique_clusters = np.unique(self.kmeans.labels_)
        
#         for cluster_id in unique_clusters:
#             # Get customers in this cluster
#             cluster_customers = [cust for i, cust in enumerate(self.data) if self.kmeans.labels_[i] == cluster_id]
            
#             # Calculate basic metrics
#             cluster_size = len(cluster_customers)
#             total_customers = len(self.data)
#             percentage = round((cluster_size / total_customers) * 100, 1)
            
#             # Calculate mean values for various features
#             cluster_feature_values = self.features[self.kmeans.labels_ == cluster_id]
#             mean_values = {
#                 'Average Amount': round(np.mean(cluster_feature_values[:, 0]), 2),
#                 'Max Amount': round(np.mean(cluster_feature_values[:, 1]), 2),
#                 'Min Amount': round(np.mean(cluster_feature_values[:, 2]), 2),
#                 'Amount Std': round(np.mean(cluster_feature_values[:, 3]), 2),
#                 'Transaction Frequency': round(np.mean(cluster_feature_values[:, 4]), 2),
#                 'Weekend Ratio': round(np.mean(cluster_feature_values[:, 5]) * 100, 1),
#                 'Morning Ratio': round(np.mean(cluster_feature_values[:, 6]) * 100, 1),
#                 'Afternoon Ratio': round(np.mean(cluster_feature_values[:, 7]) * 100, 1),
#                 'Evening Ratio': round(np.mean(cluster_feature_values[:, 8]) * 100, 1)
#             }
            
#             # Calculate category ratios with proper normalization
#             category_counts = defaultdict(int)
#             total_transactions = 0
            
#             for customer in cluster_customers:
#                 for transaction in customer['transactions']:
#                     total_transactions += 1
#                     product_name = transaction['products'][0]['name'].lower() if transaction.get('products') else ''
#                     url = transaction.get('url', '').lower()
                    
#                     if any(term in product_name or term in url for term in ['electronics', 'tech', 'computer', 'phone']):
#                         category_counts['electronics'] += 1
#                     elif any(term in product_name or term in url for term in ['grocery', 'mart', 'food', 'market']):
#                         category_counts['groceries'] += 1
#                     elif any(term in product_name or term in url for term in ['fashion', 'clothing', 'apparel', 'boutique']):
#                         category_counts['fashion'] += 1
#                     elif any(term in product_name or term in url for term in ['home', 'furnish', 'decor', 'garden']):
#                         category_counts['home'] += 1
#                     elif any(term in product_name or term in url for term in ['restaurant', 'cafe', 'dining']):
#                         category_counts['dining'] += 1
#                     elif any(term in product_name or term in url for term in ['pharmacy', 'drug', 'health']):
#                         category_counts['health'] += 1
#                     elif any(term in product_name or term in url for term in ['travel', 'airline', 'hotel']):
#                         category_counts['travel'] += 1
#                     elif any(term in product_name or term in url for term in ['entertainment', 'movie', 'game']):
#                         category_counts['entertainment'] += 1
            
#             # Normalize category ratios to percentages
#             category_ratios = {}
#             if total_transactions > 0:
#                 for category, count in category_counts.items():
#                     category_ratios[category] = round((count / total_transactions) * 100, 1)
            
#             # Calculate timing patterns with proper normalization
#             timing = {
#                 'weekend_ratio': mean_values['Weekend Ratio'],
#                 'morning_ratio': mean_values['Morning Ratio'],
#                 'afternoon_ratio': mean_values['Afternoon Ratio'],
#                 'evening_ratio': mean_values['Evening Ratio']
#             }
            
#             # Ensure timing ratios sum to 100%
#             total_timing = sum(timing.values())
#             if total_timing > 0:
#                 timing = {k: round((v / total_timing) * 100, 1) for k, v in timing.items()}
            
#             # Calculate brand preferences and next brand recommendation
#             brand_counts = {}
#             brand_categories = {}
#             for customer in cluster_customers:
#                 for transaction in customer['transactions']:
#                     url = transaction.get('url', '')
#                     merchant = url.split('/')[2] if len(url.split('/')) > 2 else 'Unknown'
                    
#                     if merchant != 'Unknown':
#                         brand_counts[merchant] = brand_counts.get(merchant, 0) + 1
#                         product_name = transaction['products'][0]['name'].lower() if transaction.get('products') else ''
#                         if any(term in product_name for term in ['electronics', 'tech', 'computer', 'phone']):
#                             brand_categories[merchant] = brand_categories.get(merchant, {})
#                             brand_categories[merchant]['electronics'] = brand_categories[merchant].get('electronics', 0) + 1
#                         elif any(term in product_name for term in ['fashion', 'clothing', 'apparel']):
#                             brand_categories[merchant] = brand_categories.get(merchant, {})
#                             brand_categories[merchant]['fashion'] = brand_categories[merchant].get('fashion', 0) + 1
            
#             # Find the most likely next brand
#             next_brand = "Unknown"
#             if brand_counts:
#                 sorted_brands = sorted(brand_counts.items(), key=lambda x: x[1], reverse=True)
#                 top_brands = sorted_brands[:3]
                
#                 brand_scores = {}
#                 for brand, count in top_brands:
#                     score = round((count / cluster_size) * 100, 1)
#                     if brand in brand_categories:
#                         brand_cats = brand_categories[brand]
#                         cat_alignment = sum(min(brand_cats.get(cat, 0), int(ratio)) 
#                                          for cat, ratio in category_ratios.items())
#                         score += (cat_alignment / 100)
#                     brand_scores[brand] = score
                
#                 next_brand = max(brand_scores.items(), key=lambda x: x[1])[0]
            
#             # Store insights with properly formatted percentages
#             cluster_insights[cluster_id] = {
#                 'size': cluster_size,
#                 'percentage': percentage,
#                 'mean_values': mean_values,
#                 'category_ratios': category_ratios,
#                 'timing': timing,
#                 'brand_counts': brand_counts,
#                 'brand_categories': brand_categories,
#                 'next_brand': next_brand,
#                 'label': None  # Will be filled by generate_cluster_label
#             }
        
#         # Generate labels for each cluster
#         for cluster_id in cluster_insights:
#             cluster_insights[cluster_id]['label'] = self.generate_cluster_label(cluster_insights[cluster_id])
        
#         return cluster_insights

#     def validate_predictions(self):
#         """Validate clustering predictions using silhouette score and other metrics."""
#         if not hasattr(self, 'kmeans') or not hasattr(self, 'features'):
#             print("Error: Must run clustering before validation")
#             return
        
#         # Calculate silhouette score
#         silhouette_avg = silhouette_score(self.features, self.kmeans.labels_)
        
#         # Calculate inertia (within-cluster sum of squares)
#         inertia = self.kmeans.inertia_
        
#         # Calculate cluster sizes
#         cluster_sizes = Counter(self.kmeans.labels_)
        
#         # Calculate cluster centers
#         cluster_centers = self.kmeans.cluster_centers_
        
#         # Calculate inter-cluster distances
#         inter_cluster_distances = pdist(cluster_centers)
#         avg_inter_cluster_distance = np.mean(inter_cluster_distances)
#         min_inter_cluster_distance = np.min(inter_cluster_distances)
        
#         validation_metrics = {
#             'silhouette_score': round(silhouette_avg, 3),
#             'inertia': round(inertia, 3),
#             'cluster_sizes': dict(cluster_sizes),
#             'avg_inter_cluster_distance': round(avg_inter_cluster_distance, 3),
#             'min_inter_cluster_distance': round(min_inter_cluster_distance, 3)
#         }
        
#         print("\nClustering Validation Metrics:")
#         print(f"Silhouette Score: {validation_metrics['silhouette_score']}")
#         print(f"Inertia: {validation_metrics['inertia']}")
#         print("Cluster Sizes:", validation_metrics['cluster_sizes'])
#         print(f"Average Inter-cluster Distance: {validation_metrics['avg_inter_cluster_distance']}")
#         print(f"Minimum Inter-cluster Distance: {validation_metrics['min_inter_cluster_distance']}")
        
#         return validation_metrics
    
#     def predict_next_purchase(self, customer_id):
#         """Predict characteristics of next purchase for a customer."""
#         # Find customer in test data
#         customer_data = None
#         for cust in self.test_data:
#             if str(cust['customer_id']) == str(customer_id):
#                 customer_data = cust
#                 break
            
#         if not customer_data:
#             raise ValueError(f"Customer {customer_id} not found in test data")
        
#         # Get customer's cluster
#         customer_features = self.extract_customer_features(customer_data)
#         if customer_features is None:
#             return None
            
#         # Scale features before prediction
#         customer_features_scaled = self.amount_scaler.transform([customer_features])[0]
#         cluster_id = self.kmeans.predict([customer_features_scaled])[0]
        
#         # Get cluster insights
#         cluster_insights = self.analyze_clusters()
#         if cluster_id not in cluster_insights:
#             raise ValueError(f"No insights available for cluster {cluster_id}")
            
#         insights = cluster_insights[cluster_id]
        
#         # Get customer's transaction history
#         transactions = customer_data['transactions']
#         if not transactions:
#             return None
        
#         # Calculate merchant scores with recency weighting
#         merchant_scores = defaultdict(float)
#         now = pd.to_datetime(max(t['datetime'] for t in transactions))
        
#         for t in transactions:
#             # Get merchant name from URL
#             url = t.get('url', '')
#             merchant = url.split('/')[2] if len(url.split('/')) > 2 else 'Unknown'
            
#             transaction_date = pd.to_datetime(t['datetime'])
#             days_ago = (now - transaction_date).days
            
#             # Exponential decay based on recency
#             recency_weight = np.exp(-0.1 * days_ago)
            
#             # Consider transaction amount in scoring
#             amount_weight = float(t['price']['total']) / max(float(t['price']['total']) for t in transactions)
            
#             # Seasonal adjustment
#             month = transaction_date.month
#             if month in [11, 12]:  # Holiday season
#                 seasonal_weight = 1.2
#             elif month in [6, 7, 8]:  # Summer
#                 seasonal_weight = 1.1
#             else:
#                 seasonal_weight = 1.0
            
#             merchant_scores[merchant] += recency_weight * amount_weight * seasonal_weight
        
#         # Normalize scores
#         total_score = sum(merchant_scores.values())
#         if total_score > 0:
#             merchant_scores = {m: s/total_score for m, s in merchant_scores.items()}
        
#         # Get top merchants
#         top_merchants = [
#             {'merchant': merchant, 'score': score}
#             for merchant, score in sorted(merchant_scores.items(), key=lambda x: x[1], reverse=True)[:5]
#         ]
        
#         # Calculate likely amount range
#         recent_amounts = [float(t['price']['total']) for t in sorted(transactions, key=lambda x: x['datetime'], reverse=True)[:5]]
#         likely_min = np.percentile(recent_amounts, 25) if recent_amounts else 0
#         likely_max = np.percentile(recent_amounts, 75) if recent_amounts else 0
        
#         # Get payment method preferences
#         payment_counts = defaultdict(int)
#         for t in transactions:
#             for pm in t['payment_methods']:
#                 payment_counts[pm['type']] += 1
#         total_payments = sum(payment_counts.values())
#         payment_preferences = [
#             {'method': method, 'confidence': count/total_payments}
#             for method, count in payment_counts.items()
#         ] if total_payments > 0 else []
        
#         # Get category preferences
#         category_counts = defaultdict(int)
#         for t in transactions:
#             product_name = t['products'][0]['name'].lower() if t.get('products') else ''
#             url = t.get('url', '').lower()
            
#             if any(term in product_name or term in url for term in ['electronics', 'tech', 'computer', 'phone']):
#                 category_counts['Electronics'] += 1
#             elif any(term in product_name or term in url for term in ['grocery', 'mart', 'food', 'market']):
#                 category_counts['Groceries'] += 1
#             elif any(term in product_name or term in url for term in ['fashion', 'clothing', 'apparel', 'boutique']):
#                 category_counts['Shopping'] += 1
#             elif any(term in product_name or term in url for term in ['restaurant', 'cafe', 'dining']):
#                 category_counts['Dining'] += 1
#             elif any(term in product_name or term in url for term in ['entertainment', 'movie', 'game']):
#                 category_counts['Entertainment'] += 1
#             elif any(term in product_name or term in url for term in ['travel', 'airline', 'hotel']):
#                 category_counts['Travel'] += 1
#             else:
#                 category_counts['Other'] += 1
        
#         total_categories = sum(category_counts.values())
#         category_preferences = [
#             {'category': category, 'confidence': count/total_categories}
#             for category, count in sorted(category_counts.items(), key=lambda x: x[1], reverse=True)
#         ] if total_categories > 0 else []
        
#         # Extract cluster label components
#         label_parts = insights['label'].split()
        
#         return {
#             'cluster_label': insights['label'],
#             'spending_level': label_parts[0],
#             'frequency': label_parts[1],
#             'timing': label_parts[2],
#             'category': label_parts[3],
#             'size': label_parts[4],
#             'predicted_categories': category_preferences,
#             'likely_amount_range': {
#                 'min': likely_min,
#                 'max': likely_max
#             },
#             'likely_payment_methods': payment_preferences,
#             'top_merchants': top_merchants,
#             'next_brand': insights['next_brand']
#         }

#     def visualize_clusters(self, output_dir: str = "visualizations") -> None:
#         """Create visualizations of the clustering results."""
#         if not hasattr(self, 'kmeans') or not hasattr(self, 'features'):
#             raise ValueError("Must run clustering before visualization")
        
#         # Create output directory if it doesn't exist
#         os.makedirs(output_dir, exist_ok=True)
#         print(f"Visualizations saved in '{output_dir}' directory")

#     def cross_validate(self, k_folds=5):
#         """Perform k-fold cross-validation."""
#         # Get customer indices
#         customer_indices = list(range(len(self.data)))
#         random.shuffle(customer_indices)
        
#         # Split into folds
#         fold_size = len(customer_indices) // k_folds
#         folds = []
#         for i in range(k_folds):
#             start_idx = i * fold_size
#             end_idx = start_idx + fold_size if i < k_folds - 1 else len(customer_indices)
#             folds.append(customer_indices[start_idx:end_idx])
        
#         # Store metrics for each fold
#         validation_metrics = []
        
#         # For each fold
#         for fold_idx, test_indices in enumerate(folds, 1):
#             print(f"\nFold {fold_idx}/{k_folds}:")
            
#             # Split data into train and test sets
#             train_indices = [i for fold in folds if fold != test_indices for i in fold]
            
#             # Extract features for train and test sets
#             train_features = []
#             for idx in train_indices:
#                 features = self.extract_customer_features(self.data[idx])
#                 train_features.append(features)
                
#             test_features = []
#             for idx in test_indices:
#                 features = self.extract_customer_features(self.data[idx])
#                 test_features.append(features)
            
#             # Fit model on training data
#             kmeans = KMeans(n_clusters=self.n_clusters, random_state=42)
#             kmeans.fit(train_features)
            
#             # Predict on test data
#             test_labels = kmeans.predict(test_features)
            
#             # Calculate validation metrics
#             metrics = {
#                 'silhouette': silhouette_score(test_features, test_labels) if len(set(test_labels)) > 1 else -1,
#                 'inertia': kmeans.inertia_,
#                 'cluster_sizes': dict(Counter(test_labels)),
#                 'avg_inter_cluster_distance': self.calculate_inter_cluster_distance(test_features, test_labels),
#                 'min_inter_cluster_distance': self.calculate_min_inter_cluster_distance(test_features, test_labels)
#             }
            
#             # Print metrics
#             print(f"Silhouette Score: {metrics['silhouette']:.3f}")
#             print(f"Inertia: {metrics['inertia']:.3f}")
#             print(f"Cluster Sizes: {metrics['cluster_sizes']}")
#             print(f"Average Inter-cluster Distance: {metrics['avg_inter_cluster_distance']:.3f}")
#             print(f"Minimum Inter-cluster Distance: {metrics['min_inter_cluster_distance']:.3f}")
            
#             validation_metrics.append(metrics)
        
#         # Calculate and print average metrics across folds
#         avg_silhouette = np.mean([m['silhouette'] for m in validation_metrics])
#         std_silhouette = np.std([m['silhouette'] for m in validation_metrics])
        
#         avg_inertia = np.mean([m['inertia'] for m in validation_metrics])
#         std_inertia = np.std([m['inertia'] for m in validation_metrics])
        
#         avg_inter_cluster = np.mean([m['avg_inter_cluster_distance'] for m in validation_metrics])
#         std_inter_cluster = np.std([m['avg_inter_cluster_distance'] for m in validation_metrics])
        
#         avg_min_inter_cluster = np.mean([m['min_inter_cluster_distance'] for m in validation_metrics])
#         std_min_inter_cluster = np.std([m['min_inter_cluster_distance'] for m in validation_metrics])
        
#         print("\nCross-validation Results:")
#         print(f"Average Silhouette Score: {avg_silhouette:.3f} ± {std_silhouette:.3f}")
#         print(f"Average Inertia: {avg_inertia:.3f} ± {std_inertia:.3f}")
#         print(f"Average Inter-cluster Distance: {avg_inter_cluster:.3f} ± {std_inter_cluster:.3f}")
#         print(f"Average Min Inter-cluster Distance: {avg_min_inter_cluster:.3f} ± {std_min_inter_cluster:.3f}")
        
#         return validation_metrics

#     def generate_cluster_label(self, insights):
#         """Generate a descriptive label for a cluster based on its characteristics."""
#         # Get spending level
#         avg_amount = insights['mean_values'].get('Average Amount', 0)
#         if avg_amount > 100:
#             spending_level = "High-Value"
#         elif avg_amount > 50:
#             spending_level = "Mid-Range"
#         else:
#             spending_level = "Budget"
        
#         # Get timing preference
#         timing_ratios = insights['timing']
#         max_time = max(timing_ratios.items(), key=lambda x: x[1])
#         timing = max_time[0].replace('_ratio', '').title()
        
#         # Get frequency pattern
#         freq = insights['mean_values'].get('Transaction Frequency', 0)
#         if freq > 2:
#             frequency = "Frequent"
#         elif freq > 1:
#             frequency = "Regular"
#         else:
#             frequency = "Occasional"
        
#         # Get category preference
#         category_ratios = insights['category_ratios']
#         if category_ratios:
#             top_category = max(category_ratios.items(), key=lambda x: x[1])[0]
#             if top_category == 'Other':
#                 # Look for second highest category
#                 sorted_categories = sorted(category_ratios.items(), key=lambda x: x[1], reverse=True)
#                 if len(sorted_categories) > 1:
#                     top_category = sorted_categories[1][0]
#                 else:
#                     top_category = "General"
#         else:
#             top_category = "General"
        
#         # Create unique identifier based on cluster size
#         cluster_size = insights['size']
#         size_rank = "Large" if cluster_size > 40 else "Medium" if cluster_size > 20 else "Small"
        
#         # Combine components to create unique label
#         label_parts = [
#             spending_level,
#             frequency,
#             timing,
#             top_category,
#             size_rank
#         ]
        
#         return " ".join(label_parts)

#     def calculate_inter_cluster_distance(self, features, labels):
#         """Calculate average distance between cluster centers."""
#         features = np.array(features)
#         labels = np.array(labels)
        
#         if len(set(labels)) <= 1:
#             return 0.0
            
#         # Calculate cluster centers
#         cluster_centers = []
#         for cluster_id in set(labels):
#             cluster_points = features[np.where(labels == cluster_id)[0]]
#             if len(cluster_points) > 0:
#                 cluster_centers.append(np.mean(cluster_points, axis=0))
                
#         if len(cluster_centers) <= 1:
#             return 0.0
            
#         # Calculate pairwise distances between centers
#         cluster_centers = np.array(cluster_centers)
#         distances = pdist(cluster_centers)
#         return np.mean(distances)

#     def calculate_min_inter_cluster_distance(self, features, labels):
#         """Calculate minimum distance between cluster centers."""
#         features = np.array(features)
#         labels = np.array(labels)
        
#         if len(set(labels)) <= 1:
#             return 0.0
            
#         # Calculate cluster centers
#         cluster_centers = []
#         for cluster_id in set(labels):
#             cluster_points = features[np.where(labels == cluster_id)[0]]
#             if len(cluster_points) > 0:
#                 cluster_centers.append(np.mean(cluster_points, axis=0))
                
#         if len(cluster_centers) <= 1:
#             return 0.0
            
#         # Calculate pairwise distances between centers
#         cluster_centers = np.array(cluster_centers)
#         distances = pdist(cluster_centers)
#         return np.min(distances) if len(distances) > 0 else 0.0

#     def print_cluster_insights(self, cluster_insights):
#         """Print detailed insights for each cluster."""
#         print("\nCluster Analysis Results:")
#         print("=" * 50)
        
#         for cluster_id, insights in cluster_insights.items():
#             print(f"\nCluster {cluster_id}:")
#             print(f"Size: {insights['size']} customers ({insights['percentage']:.2f}%)")
#             print(f"Label: {insights['label']}")
#             print(f"Average Transaction Amount: ${insights['mean_values']['Average Amount']:.2f}")
            
#             print("\nCategory Preferences:")
#             for category, ratio in sorted(insights['category_ratios'].items(), key=lambda x: x[1], reverse=True):
#                 print(f"- {category}: {ratio:.1%}")
                
#             print("\nShopping Timing:")
#             for time, ratio in insights['timing'].items():
#                 print(f"- {time.replace('_ratio', '')}: {ratio:.1%}")
                
#             print("\nTop Brands:")
#             for brand, count in sorted(insights['brand_counts'].items(), key=lambda x: x[1], reverse=True)[:3]:
#                 print(f"- {brand}: {count/insights['size']:.1%}")
                
#             print("\nNext Brand Recommendation:", insights['next_brand'])
#             print("-" * 50)

#     def predict_next_brand(self, customer_data):
#         """Predict the next brand a customer is likely to purchase from."""
#         transactions = customer_data['transactions']
#         if not transactions:
#             return "Unknown"
        
#         # Extract merchant information from transactions
#         merchants = [t.get('url', '').split('/')[2] for t in transactions if t.get('url')]
#         if not merchants:
#             return "Unknown"
        
#         # Count merchant frequencies
#         merchant_counts = Counter(merchants)
        
#         # Get the most common merchant
#         most_common_merchant = merchant_counts.most_common(1)[0][0]
        
#         # Map merchant to brand
#         merchant_to_brand = {
#             'amazon.com': 'Amazon',
#             'walmart.com': 'Walmart',
#             'target.com': 'Target',
#             'bestbuy.com': 'Best Buy',
#             'gamestop.com': 'GameStop',
#             'abtelectronics.com': 'ABT Electronics',
#             'newegg.com': 'Newegg',
#             'microcenter.com': 'Micro Center',
#             'bhphotovideo.com': 'B&H Photo',
#             'tigerdirect.com': 'TigerDirect',
#             'crutchfield.com': 'Crutchfield'
#         }
        
#         return merchant_to_brand.get(most_common_merchant, most_common_merchant)

#     def generate_cluster_profile(self, cluster_data):
#         """Generate a meaningful cluster profile using LLM."""
#         try:
#             # Prepare data for LLM
#             prompt = f"""Generate a unique and meaningful customer segment profile based on the following data:
            
#             Average Transaction Amount: ${cluster_data['avg_transaction_amount']:.2f}
#             Transaction Frequency: {cluster_data['frequency']:.2f} per day
#             Shopping Timing:
#             - Morning: {cluster_data['timing']['morning_ratio']*100:.1f}%
#             - Afternoon: {cluster_data['timing']['afternoon_ratio']*100:.1f}%
#             - Evening: {cluster_data['timing']['evening_ratio']*100:.1f}%
#             - Weekend: {cluster_data['timing']['weekend_ratio']*100:.1f}%
            
#             Top Categories:
#             {json.dumps(cluster_data['top_categories'], indent=2)}
            
#             Next Brand: {cluster_data['next_brand']}
            
#             Generate a unique and descriptive label for this customer segment that reflects their spending habits, shopping preferences, and likely next brand.
#             The label should be concise but informative."""
            
#             response = requests.post(
#                 self.llm_endpoint,
#                 json={"prompt": prompt}
#             )
            
#             if response.status_code == 200:
#                 return response.json()["content"]
#             else:
#                 return "Unknown Customer Segment"
#         except Exception as e:
#             print(f"Error generating cluster profile: {e}")
#             return "Unknown Customer Segment"

# def main():
#     """Main function to run the analysis."""
#     print("Loading customer data...")
#     analyzer = CustomerAnalyzer()
    
#     # Load existing data from files
#     analyzer.load_data()

#     print("Extracting features...")
#     cluster_mapping = analyzer.cluster_customers()

#     # Perform cross-validation
#     cv_metrics = analyzer.cross_validate(k_folds=5)

#     print("\nSplitting data into train and test sets...")
#     analyzer.split_data()

#     print("\nEvaluating clustering quality...")
#     metrics = analyzer.evaluate_clustering()
#     print(f"Silhouette Score: {metrics['silhouette']:.3f}")
#     print(f"Calinski-Harabasz Score: {metrics['calinski_harabasz']:.3f}")
#     print(f"Davies-Bouldin Score: {metrics['davies_bouldin']:.3f}")

#     print("\nCluster Profiles:")
#     cluster_analysis = analyzer.analyze_clusters()
#     analyzer.print_cluster_insights(cluster_analysis)

#     print("\nExample Predictions:")
#     test_customers = [customer['customer_id'] for customer in analyzer.test_data[:3]]
#     for customer_id in test_customers:
#         try:
#             prediction = analyzer.predict_next_purchase(str(customer_id))
#             if prediction:
#                 print(f"\nPredictions for Customer {customer_id}:")
#                 print("Cluster Characteristics:", ', '.join(prediction['cluster_characteristics']))
                
#                 print("\nPredicted Categories:")
#                 for cat in prediction['predicted_categories']:
#                     print(f"- {cat['category']}: {cat['confidence']:.1%}")
                
#                 print("\nLikely Amount Range:")
#                 print(f"${prediction['likely_amount_range']['min']:.2f} - ${prediction['likely_amount_range']['max']:.2f}")
                
#                 print("\nLikely Payment Methods:")
#                 for pm in prediction['likely_payment_methods']:
#                     print(f"- {pm['method']}: {pm['confidence']:.1%}")
                    
#                 print("\nTop Merchants:")
#                 for merchant in prediction['top_merchants']:
#                     print(f"- {merchant['merchant']}: {merchant['score']:.1%}")
                    
#                 print("\nFavorite Merchant:", prediction['favorite_merchant'])
#             else:
#                 print(f"\nNo predictions available for Customer {customer_id} (insufficient data)")
#         except Exception as e:
#             print(f"Error making prediction for customer {customer_id}: {str(e)}")

# if __name__ == "__main__":
#     main()
