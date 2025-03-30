import json
import os
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.impute import SimpleImputer
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from collections import defaultdict, Counter
import pandas as pd
from datetime import datetime
from typing import List, Dict, Any
from sklearn.model_selection import train_test_split
from sklearn.metrics import silhouette_score, calinski_harabasz_score, davies_bouldin_score
import matplotlib.pyplot as plt
import seaborn as sns
import random

class CustomerAnalyzer:
    def __init__(self, data_dir: str = "data"):
        self.data_dir = data_dir
        self.customers_data = {}
        self.features_df = None
        self.clusters = None
        self.cluster_profiles = {}
        self.train_data = None
        self.test_data = None
        self.train_clusters = None
        self.test_clusters = None
        self.pca = None
        self.scaler = StandardScaler()
        self.imputer = SimpleImputer(strategy='mean')
        
    def load_data(self):
        """Load and preprocess customer transaction data."""
        # Example data structure
        self.data = {
            '1': [
                {'amount': 19.99, 'category': 'electronics', 'payment_method': 'visa'},
                {'amount': 29.99, 'category': 'accessories', 'payment_method': 'mastercard'},
            ],
            '2': [
                {'amount': 9.99, 'category': 'food', 'payment_method': 'cash'},
                {'amount': 39.99, 'category': 'clothing', 'payment_method': 'amex'},
            ],
            # Add more customers with their transactions
        }
        
        # Generate synthetic data for 100 customers
        categories = ['electronics', 'food', 'clothing', 'books', 'home', 'sports', 'beauty', 'toys']
        payment_methods = ['visa', 'mastercard', 'amex', 'paypal', 'cash', 'discover']
        
        for i in range(100):
            customer_id = str(i)
            num_transactions = random.randint(5, 20)
            transactions = []
            
            for _ in range(num_transactions):
                transaction = {
                    'amount': round(random.uniform(5.0, 200.0), 2),
                    'category': random.choice(categories),
                    'payment_method': random.choice(payment_methods)
                }
                transactions.append(transaction)
            
            self.data[customer_id] = transactions

    def extract_customer_features(self, customer_data, fit=True):
        """Extract features from customer transaction data."""
        features = []
        all_categories = set()
        all_payment_methods = set()
        
        # First pass: collect all possible categories and payment methods
        if fit:
            for transactions in customer_data:
                if not transactions:
                    continue
                for t in transactions:
                    all_categories.add(t['category'])
                    all_payment_methods.add(t['payment_method'])
            self.categories = sorted(list(all_categories))
            self.payment_methods = sorted(list(all_payment_methods))
        
        # Second pass: extract features
        for transactions in customer_data:
            if not transactions:
                continue
                
            # Transaction amount features
            amounts = [float(t['amount']) for t in transactions]
            avg_amount = np.mean(amounts)
            std_amount = np.std(amounts)
            max_amount = max(amounts)
            min_amount = min(amounts)
            
            # Create base feature dictionary
            customer_features = {
                'avg_amount': avg_amount,
                'std_amount': std_amount,
                'max_amount': max_amount,
                'min_amount': min_amount,
                'transaction_count': len(transactions),
                'unique_categories': len(set(t['category'] for t in transactions)),
                'unique_payments': len(set(t['payment_method'] for t in transactions))
            }
            
            # Add category frequencies
            category_counts = Counter(t['category'] for t in transactions)
            for category in (self.categories if hasattr(self, 'categories') else all_categories):
                customer_features[f'category_{category}'] = category_counts[category] / len(transactions)
                
            # Add payment method frequencies
            payment_counts = Counter(t['payment_method'] for t in transactions)
            for method in (self.payment_methods if hasattr(self, 'payment_methods') else all_payment_methods):
                customer_features[f'payment_{method}'] = payment_counts[method] / len(transactions)
            
            features.append(customer_features)
        
        # Convert to DataFrame
        features_df = pd.DataFrame(features)
        
        # Fill missing values with 0
        features_df = features_df.fillna(0)
        
        return features_df

    def split_data(self, test_size: float = 0.2) -> None:
        """Split data into training and test sets."""
        if not hasattr(self, 'data') or not self.data:
            raise ValueError("No data available for splitting")
            
        customer_ids = list(self.data.keys())
        if not customer_ids:
            raise ValueError("No customers found in data")
            
        train_size = int(0.8 * len(customer_ids))
        if train_size == 0:
            raise ValueError("Not enough data to split")
            
        # Randomly shuffle customer IDs
        random.shuffle(customer_ids)
        
        # Split customer IDs
        train_ids = customer_ids[:train_size]
        test_ids = customer_ids[train_size:]
        
        # Create train and test dictionaries
        self.train_data = {cid: self.data[cid] for cid in train_ids}
        self.test_data = {cid: self.data[cid] for cid in test_ids}
        
        print(f"\nSplitting data into train and test sets...")
        print(f"Training set size: {len(self.train_data)}")
        print(f"Test set size: {len(self.test_data)}")

    def find_optimal_clusters(self, scaled_features: np.ndarray) -> int:
        """Find optimal number of clusters using multiple metrics."""
        max_clusters = min(len(scaled_features) // 2, 50)  # Dynamic max clusters
        min_clusters = 2
        
        results = []
        for k in range(min_clusters, max_clusters + 1):
            kmeans = KMeans(n_clusters=k, random_state=42)
            labels = kmeans.fit_predict(scaled_features)
            
            # Calculate multiple clustering metrics
            silhouette = silhouette_score(scaled_features, labels)
            calinski = calinski_harabasz_score(scaled_features, labels)
            davies = davies_bouldin_score(scaled_features, labels)
            inertia = kmeans.inertia_
            
            results.append({
                'k': k,
                'silhouette': silhouette,
                'calinski': calinski,
                'davies': davies,
                'inertia': inertia
            })
        
        # Convert to DataFrame for analysis
        results_df = pd.DataFrame(results)
        
        # Plot metrics
        plt.figure(figsize=(15, 10))
        
        # Silhouette Score
        plt.subplot(2, 2, 1)
        plt.plot(results_df['k'], results_df['silhouette'], marker='o')
        plt.xlabel('Number of clusters (k)')
        plt.ylabel('Silhouette Score')
        plt.title('Silhouette Score vs. k')
        
        # Calinski-Harabasz Score
        plt.subplot(2, 2, 2)
        plt.plot(results_df['k'], results_df['calinski'], marker='o')
        plt.xlabel('Number of clusters (k)')
        plt.ylabel('Calinski-Harabasz Score')
        plt.title('Calinski-Harabasz Score vs. k')
        
        # Davies-Bouldin Score
        plt.subplot(2, 2, 3)
        plt.plot(results_df['k'], results_df['davies'], marker='o')
        plt.xlabel('Number of clusters (k)')
        plt.ylabel('Davies-Bouldin Score')
        plt.title('Davies-Bouldin Score vs. k')
        
        # Elbow Plot
        plt.subplot(2, 2, 4)
        plt.plot(results_df['k'], results_df['inertia'], marker='o')
        plt.xlabel('Number of clusters (k)')
        plt.ylabel('Inertia')
        plt.title('Elbow Plot')
        
        plt.tight_layout()
        os.makedirs('visualizations', exist_ok=True)
        plt.savefig('visualizations/clustering_metrics.png')
        plt.close()
        
        # Find optimal k using multiple criteria
        # Normalize metrics to [0,1] range for comparison
        normalized_df = results_df.copy()
        normalized_df['silhouette'] = (normalized_df['silhouette'] - normalized_df['silhouette'].min()) / (normalized_df['silhouette'].max() - normalized_df['silhouette'].min())
        normalized_df['calinski'] = (normalized_df['calinski'] - normalized_df['calinski'].min()) / (normalized_df['calinski'].max() - normalized_df['calinski'].min())
        normalized_df['davies'] = 1 - (normalized_df['davies'] - normalized_df['davies'].min()) / (normalized_df['davies'].max() - normalized_df['davies'].min())  # Invert as lower is better
        
        # Combine metrics with weights
        normalized_df['combined_score'] = (
            normalized_df['silhouette'] * 0.4 +  # Silhouette is most interpretable
            normalized_df['calinski'] * 0.3 +    # Good for well-defined clusters
            normalized_df['davies'] * 0.3        # Good for cluster separation
        )
        
        # Find k with highest combined score
        optimal_k = normalized_df.loc[normalized_df['combined_score'].idxmax(), 'k']
        
        print("\nClustering Metrics Analysis:")
        print(f"Optimal number of clusters: {optimal_k}")
        print("\nMetric ranges:")
        print(f"Silhouette Score: {results_df['silhouette'].min():.3f} to {results_df['silhouette'].max():.3f}")
        print(f"Calinski-Harabasz Score: {results_df['calinski'].min():.3f} to {results_df['calinski'].max():.3f}")
        print(f"Davies-Bouldin Score: {results_df['davies'].min():.3f} to {results_df['davies'].max():.3f}")
        
        return int(optimal_k)
        
    def cluster_customers(self):
        """Cluster customers based on their transaction patterns."""
        print("\nClustering Metrics Analysis:")
        
        # Extract features for all customers
        all_features = self.extract_customer_features(self.data.values(), fit=True)
        self.features = all_features
        
        # Scale features
        scaler = StandardScaler()
        features_scaled = scaler.fit_transform(all_features)
        self.scaler = scaler
        
        # Find optimal number of clusters
        max_clusters = min(50, len(all_features) // 2)  # Cap at 50 or half of samples
        silhouette_scores = []
        ch_scores = []
        db_scores = []
        
        for n_clusters in range(2, max_clusters + 1):
            kmeans = KMeans(n_clusters=n_clusters, random_state=42)
            labels = kmeans.fit_predict(features_scaled)
            
            silhouette_scores.append(silhouette_score(features_scaled, labels))
            ch_scores.append(calinski_harabasz_score(features_scaled, labels))
            db_scores.append(davies_bouldin_score(features_scaled, labels))
        
        # Print metric ranges
        print("\nMetric ranges:")
        print(f"Silhouette Score: {min(silhouette_scores):.3f} to {max(silhouette_scores):.3f}")
        print(f"Calinski-Harabasz Score: {min(ch_scores):.3f} to {max(ch_scores):.3f}")
        print(f"Davies-Bouldin Score: {min(db_scores):.3f} to {max(db_scores):.3f}")
        
        # Choose optimal number of clusters
        optimal_clusters = np.argmax(silhouette_scores) + 2
        print(f"\nOptimal number of clusters: {optimal_clusters}")
        
        # Fit final clustering model
        self.kmeans = KMeans(n_clusters=optimal_clusters, random_state=42)
        self.kmeans.fit(features_scaled)
        
        # Create mapping of customers to clusters
        customer_ids = list(self.data.keys())
        cluster_mapping = {customer_id: cluster_id for customer_id, cluster_id 
                         in zip(customer_ids, self.kmeans.labels_)}
        
        return cluster_mapping
    
    def evaluate_clustering(self) -> Dict[str, float]:
        """Evaluate clustering quality using multiple metrics."""
        if not hasattr(self, 'kmeans') or not hasattr(self, 'features'):
            raise ValueError("Must run clustering before evaluation")
        
        # Get scaled features
        features_scaled = self.scaler.transform(self.features)
        
        # Calculate metrics
        silhouette = silhouette_score(features_scaled, self.kmeans.labels_)
        calinski = calinski_harabasz_score(features_scaled, self.kmeans.labels_)
        davies = davies_bouldin_score(features_scaled, self.kmeans.labels_)
        
        return {
            'silhouette': silhouette,
            'calinski_harabasz': calinski,
            'davies_bouldin': davies
        }
    
    def analyze_clusters(self) -> None:
        """Analyze and print detailed information about each cluster."""
        if not hasattr(self, 'kmeans') or not hasattr(self, 'features'):
            print("Clustering must be run before analysis.")
            return

        # Get all customer IDs from training data
        customer_ids = list(self.train_data.keys())
        
        for cluster_id in range(self.kmeans.n_clusters):
            cluster_mask = self.kmeans.labels_ == cluster_id
            
            # Get indices where cluster_mask is True
            cluster_indices = np.where(cluster_mask)[0]
            
            # Get customer IDs for this cluster
            cluster_customers = [customer_ids[i] for i in cluster_indices if i < len(customer_ids)]
            
            if not cluster_customers:
                continue
                
            # Calculate cluster statistics
            amounts = []
            categories = []
            payment_methods = []
            
            for customer_id in cluster_customers:
                customer_data = self.train_data[customer_id]
                if isinstance(customer_data, dict):
                    # Single transaction
                    amounts.append(float(customer_data.get('amount', 0)))
                    categories.append(customer_data.get('category', ''))
                    payment_methods.append(customer_data.get('payment_method', ''))
                elif isinstance(customer_data, list):
                    # Multiple transactions
                    for transaction in customer_data:
                        if isinstance(transaction, dict):
                            amounts.append(float(transaction.get('amount', 0)))
                            categories.append(transaction.get('category', ''))
                            payment_methods.append(transaction.get('payment_method', ''))
            
            if not amounts:
                continue
                
            avg_amount = np.mean(amounts)
            avg_count = len(amounts) / len(cluster_customers)
            
            category_counts = Counter(categories).most_common(3)
            payment_counts = Counter(payment_methods).most_common(2)
            
            print(f"\nCluster {cluster_id}:")
            print(f"Size: {len(cluster_customers)} customers")
            print(f"Avg transaction amount: ${avg_amount:.2f}")
            print(f"Avg transaction count: {avg_count:.1f}")
            print(f"Common categories: {', '.join(cat for cat, _ in category_counts)}")
            print(f"Common payment methods: {', '.join(pm for pm, _ in payment_counts)}")

    def validate_predictions(self):
        """Validate predictions on test data and return accuracy metrics."""
        if not hasattr(self, 'test_data') or not self.test_data:
            print("No test data available for validation.")
            return None

        total_predictions = 0
        category_correct = 0
        payment_correct = 0

        for customer_id, transactions in self.test_data.items():
            if not isinstance(transactions, list) or not transactions:
                continue

            # Get the last few transactions for validation
            validation_transactions = transactions[-3:]  # Use last 3 transactions
            
            try:
                # Make prediction
                prediction = self.predict_next_purchase(str(customer_id))
                
                # Validate category prediction
                if prediction['predicted_categories']:
                    predicted_categories = [cat['category'] for cat in prediction['predicted_categories']]
                    for transaction in validation_transactions:
                        if transaction['category'] in predicted_categories:
                            category_correct += 1
                            break
                
                # Validate payment method prediction
                if prediction['likely_payment_methods']:
                    predicted_methods = [pm['method'] for pm in prediction['likely_payment_methods']]
                    for transaction in validation_transactions:
                        if transaction['payment_method'] in predicted_methods:
                            payment_correct += 1
                            break
                
                total_predictions += 1
            except Exception as e:
                print(f"Error validating predictions for customer {customer_id}: {str(e)}")
                continue

        # Calculate accuracy metrics
        category_accuracy = category_correct / total_predictions if total_predictions > 0 else 0
        payment_accuracy = payment_correct / total_predictions if total_predictions > 0 else 0

        return {
            'category_accuracy': category_accuracy,
            'payment_accuracy': payment_accuracy,
            'total_predictions': total_predictions
        }
    
    def predict_next_purchase(self, customer_id: str) -> Dict:
        """Predict the next purchase for a given customer."""
        if not hasattr(self, 'kmeans') or not hasattr(self, 'features'):
            raise ValueError("Must run clustering before prediction")
            
        if customer_id not in self.train_data and customer_id not in self.test_data:
            raise ValueError(f"Customer {customer_id} not found in dataset")
            
        # Get customer transactions
        transactions = self.train_data.get(customer_id, []) if customer_id in self.train_data else self.test_data.get(customer_id, [])
        if not transactions:
            raise ValueError(f"No transactions found for customer {customer_id}")
            
        # Extract customer features
        customer_features = self.extract_customer_features([[t for t in transactions]], fit=False)
        
        # Scale features
        customer_features_scaled = self.scaler.transform(customer_features)
        
        # Get cluster assignment
        cluster_label = self.kmeans.predict(customer_features_scaled)[0]
        
        # Get cluster data
        cluster_mask = self.kmeans.labels_ == cluster_label
        cluster_customers = [cid for cid, mask in zip(self.train_data.keys(), cluster_mask) if mask]
        
        # Collect all transactions from cluster
        cluster_transactions = []
        for cid in cluster_customers:
            cluster_transactions.extend(self.train_data[cid])
            
        # Calculate predictions
        recent_transactions = transactions[-5:]  # Look at last 5 transactions
        
        # Predict categories
        cluster_categories = Counter(t['category'] for t in cluster_transactions).most_common()
        recent_categories = Counter(t['category'] for t in recent_transactions).most_common()
        
        predicted_categories = []
        for category, count in cluster_categories:
            confidence = count / len(cluster_transactions)
            # Boost confidence if category appears in recent transactions
            for recent_cat, recent_count in recent_categories:
                if category == recent_cat:
                    confidence *= 1.5
            predicted_categories.append({
                'category': category,
                'confidence': min(confidence, 1.0)
            })
        
        # Predict payment methods
        cluster_payments = Counter(t['payment_method'] for t in cluster_transactions).most_common()
        recent_payments = Counter(t['payment_method'] for t in recent_transactions).most_common()
        
        likely_payment_methods = []
        for method, count in cluster_payments:
            confidence = count / len(cluster_transactions)
            # Boost confidence if method appears in recent transactions
            for recent_method, recent_count in recent_payments:
                if method == recent_method:
                    confidence *= 1.5
            likely_payment_methods.append({
                'method': method,
                'confidence': min(confidence, 1.0)
            })
        
        # Estimate amount
        cluster_amounts = [float(t['amount']) for t in cluster_transactions]
        recent_amounts = [float(t['amount']) for t in recent_transactions]
        
        estimated_amount = np.mean(cluster_amounts) * 0.7 + np.mean(recent_amounts) * 0.3
        
        # Calculate overall confidence score
        confidence_score = np.mean([cat['confidence'] for cat in predicted_categories[:3]] +
                                 [pm['confidence'] for pm in likely_payment_methods[:2]])
        
        return {
            'predicted_categories': sorted(predicted_categories, key=lambda x: x['confidence'], reverse=True)[:3],
            'likely_payment_methods': sorted(likely_payment_methods, key=lambda x: x['confidence'], reverse=True)[:2],
            'estimated_amount': estimated_amount,
            'confidence_score': confidence_score
        }

    def visualize_clusters(self, output_dir: str = "visualizations") -> None:
        """Create visualizations of the clustering results."""
        if not hasattr(self, 'kmeans') or not hasattr(self, 'features'):
            raise ValueError("Must run clustering before visualization")
        
        # Create output directory if it doesn't exist
        os.makedirs(output_dir, exist_ok=True)
        
        # Get scaled features
        features_scaled = self.scaler.transform(self.features)
        
        # 1. Perform PCA for visualization
        pca = PCA(n_components=2)
        features_2d = pca.fit_transform(features_scaled)
        
        # Plot clusters
        plt.figure(figsize=(10, 8))
        scatter = plt.scatter(features_2d[:, 0], features_2d[:, 1], 
                             c=self.kmeans.labels_, cmap='viridis', 
                             alpha=0.6)
        plt.colorbar(scatter)
        plt.title('Customer Clusters (PCA)')
        plt.xlabel('First Principal Component')
        plt.ylabel('Second Principal Component')
        plt.savefig(os.path.join(output_dir, 'clusters_pca.png'))
        plt.close()
        
        # 2. Feature correlation heatmap
        plt.figure(figsize=(12, 10))
        correlation_matrix = self.features.corr()
        sns.heatmap(correlation_matrix, annot=False, cmap='coolwarm', center=0)
        plt.title('Feature Correlation Heatmap')
        plt.tight_layout()
        plt.savefig(os.path.join(output_dir, 'feature_correlation.png'))
        plt.close()
        
        # 3. Elbow curve
        inertias = []
        silhouette_scores = []
        k_range = range(2, min(51, len(self.features)))
        
        for k in k_range:
            kmeans = KMeans(n_clusters=k, random_state=42)
            kmeans.fit(features_scaled)
            inertias.append(kmeans.inertia_)
            silhouette_scores.append(silhouette_score(features_scaled, kmeans.labels_))
        
        # Plot elbow curve
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 5))
        
        # Inertia plot
        ax1.plot(k_range, inertias, 'bx-')
        ax1.set_xlabel('k')
        ax1.set_ylabel('Inertia')
        ax1.set_title('Elbow Method for Optimal k')
        
        # Silhouette score plot
        ax2.plot(k_range, silhouette_scores, 'rx-')
        ax2.set_xlabel('k')
        ax2.set_ylabel('Silhouette Score')
        ax2.set_title('Silhouette Score vs k')
        
        plt.tight_layout()
        plt.savefig(os.path.join(output_dir, 'elbow_analysis.png'))
        plt.close()
        
        print(f"Visualizations saved in '{output_dir}' directory")

    def generate_synthetic_data(self, num_customers=100, seed=None):
        """Generate synthetic customer data with more realistic patterns."""
        if seed is not None:
            random.seed(seed)
            np.random.seed(seed)
            
        categories = ['electronics', 'food', 'clothing', 'books', 'home', 'sports', 'beauty', 'toys']
        payment_methods = ['visa', 'mastercard', 'amex', 'paypal', 'cash', 'discover']
        
        # Create customer segments with specific behaviors
        segments = [
            {
                'name': 'budget_shoppers',
                'size': 0.3,  # 30% of customers
                'amount_range': (5.0, 50.0),
                'preferred_categories': ['food', 'books'],
                'preferred_payments': ['cash', 'debit']
            },
            {
                'name': 'regular_shoppers',
                'size': 0.4,  # 40% of customers
                'amount_range': (20.0, 150.0),
                'preferred_categories': ['clothing', 'home', 'sports'],
                'preferred_payments': ['visa', 'mastercard']
            },
            {
                'name': 'premium_shoppers',
                'size': 0.3,  # 30% of customers
                'amount_range': (100.0, 500.0),
                'preferred_categories': ['electronics', 'beauty'],
                'preferred_payments': ['amex', 'visa']
            }
        ]
        
        data = {}
        for i in range(num_customers):
            # Assign customer to a segment
            segment = np.random.choice(segments, p=[s['size'] for s in segments])
            
            # Generate transactions with segment-specific patterns
            num_transactions = random.randint(5, 20)
            transactions = []
            
            for _ in range(num_transactions):
                # 70% chance to use preferred categories/payments
                if random.random() < 0.7:
                    category = random.choice(segment['preferred_categories'])
                    payment = random.choice(segment['preferred_payments'])
                else:
                    category = random.choice(categories)
                    payment = random.choice(payment_methods)
                
                amount = round(random.uniform(*segment['amount_range']), 2)
                
                transaction = {
                    'amount': amount,
                    'category': category,
                    'payment_method': payment
                }
                transactions.append(transaction)
            
            data[str(i)] = transactions
            
        return data

    def cross_validate(self, k_folds=5):
        """Perform k-fold cross-validation to assess model generalization."""
        if not hasattr(self, 'data') or not self.data:
            raise ValueError("No data available for cross-validation")
            
        customer_ids = list(self.data.keys())
        random.shuffle(customer_ids)
        
        # Split into k folds
        fold_size = len(customer_ids) // k_folds
        folds = [customer_ids[i:i + fold_size] for i in range(0, len(customer_ids), fold_size)]
        
        metrics = {
            'silhouette_scores': [],
            'category_accuracy': [],
            'payment_accuracy': [],
            'amount_rmse': []
        }
        
        print("\nPerforming cross-validation...")
        for i in range(k_folds):
            # Use fold i as test set, rest as training set
            test_ids = folds[i]
            train_ids = [cid for fold in folds[:i] + folds[i+1:] for cid in fold]
            
            # Split data
            self.train_data = {cid: self.data[cid] for cid in train_ids}
            self.test_data = {cid: self.data[cid] for cid in test_ids}
            
            # Extract features and cluster
            all_features = self.extract_customer_features(self.train_data.values(), fit=True)
            self.features = all_features
            
            # Scale features
            scaler = StandardScaler()
            features_scaled = scaler.fit_transform(all_features)
            self.scaler = scaler
            
            # Find optimal clusters and fit model
            optimal_clusters = self.find_optimal_clusters(features_scaled)
            self.kmeans = KMeans(n_clusters=optimal_clusters, random_state=42)
            self.kmeans.fit(features_scaled)
            
            # Calculate metrics
            metrics['silhouette_scores'].append(silhouette_score(features_scaled, self.kmeans.labels_))
            
            # Validate predictions
            validation_metrics = self.validate_predictions()
            if validation_metrics:
                metrics['category_accuracy'].append(validation_metrics['category_accuracy'])
                metrics['payment_accuracy'].append(validation_metrics['payment_accuracy'])
            
            print(f"\nFold {i+1}/{k_folds}:")
            print(f"Silhouette Score: {metrics['silhouette_scores'][-1]:.3f}")
            print(f"Category Accuracy: {metrics['category_accuracy'][-1]:.2%}")
            print(f"Payment Accuracy: {metrics['payment_accuracy'][-1]:.2%}")
        
        # Calculate and print average metrics
        print("\nCross-validation Results:")
        print(f"Average Silhouette Score: {np.mean(metrics['silhouette_scores']):.3f} ± {np.std(metrics['silhouette_scores']):.3f}")
        print(f"Average Category Accuracy: {np.mean(metrics['category_accuracy']):.2%} ± {np.std(metrics['category_accuracy']):.2%}")
        print(f"Average Payment Accuracy: {np.mean(metrics['payment_accuracy']):.2%} ± {np.std(metrics['payment_accuracy']):.2%}")
        
        return metrics

    def test_generalization(self, num_test_customers=100):
        """Test model generalization on completely new synthetic data."""
        print("\nTesting model generalization on new synthetic data...")
        
        # Generate new test data with different seed
        test_data = self.generate_synthetic_data(num_test_customers, seed=42)
        
        # Store original test data
        original_test_data = self.test_data
        
        # Use new data for testing
        self.test_data = test_data
        
        # Validate predictions on new data
        validation_metrics = self.validate_predictions()
        
        print("\nGeneralization Test Results:")
        print(f"Category Accuracy on New Data: {validation_metrics['category_accuracy']:.2%}")
        print(f"Payment Accuracy on New Data: {validation_metrics['payment_accuracy']:.2%}")
        print(f"Total Predictions: {validation_metrics['total_predictions']}")
        
        # Restore original test data
        self.test_data = original_test_data
        
        return validation_metrics

def main():
    """Main function to run the analysis."""
    print("Loading customer data...")
    analyzer = CustomerAnalyzer()
    analyzer.data = analyzer.generate_synthetic_data(num_customers=100, seed=42)

    print("Extracting features...")
    cluster_mapping = analyzer.cluster_customers()

    # Perform cross-validation
    cv_metrics = analyzer.cross_validate(k_folds=5)

    print("\nSplitting data into train and test sets...")
    analyzer.split_data()

    print("\nEvaluating clustering quality...")
    metrics = analyzer.evaluate_clustering()
    print(f"Silhouette Score: {metrics['silhouette']:.3f}")
    print(f"Calinski-Harabasz Score: {metrics['calinski_harabasz']:.3f}")
    print(f"Davies-Bouldin Score: {metrics['davies_bouldin']:.3f}")

    print("\nGenerating visualizations...")
    analyzer.visualize_clusters()

    print("\nCluster Profiles:")
    analyzer.analyze_clusters()

    # Test generalization on new data
    generalization_metrics = analyzer.test_generalization(num_test_customers=100)

    print("\nExample Predictions:")
    test_customers = list(analyzer.test_data.keys())[:3]
    for customer_id in test_customers:
        try:
            print(f"\nPredictions for Customer {customer_id}:")
            prediction = analyzer.predict_next_purchase(str(customer_id))
            print("Predicted categories (with confidence):")
            for cat in prediction['predicted_categories']:
                print(f"  - {cat['category']}: {cat['confidence']:.2%}")
            print(f"Estimated amount: ${prediction['estimated_amount']:.2f}")
            print("Likely payment methods (with confidence):")
            for pm in prediction['likely_payment_methods']:
                print(f"  - {pm['method']}: {pm['confidence']:.2%}")
            print(f"Overall confidence score: {prediction['confidence_score']:.2%}")
        except Exception as e:
            print(f"Error making prediction for customer {customer_id}: {str(e)}")

if __name__ == "__main__":
    main()
