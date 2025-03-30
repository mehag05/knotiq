import json
import random
import uuid
from datetime import datetime, timedelta
import copy
import os
import argparse

class MockTransactionGenerator:
    def __init__(self):
        """Initialize the transaction generator with all necessary data"""
        # Set up customer personas
        self.define_customer_personas()
        
        # Set up product catalog
        self.product_catalog = self.generate_product_catalog()
        
        # Set up merchants
        self.merchants = self.generate_merchant_list()
        
        # Set up payment methods
        self.define_payment_methods()
        
        # Set up order statuses
        self.define_order_statuses()
    
    def define_customer_personas(self):
        """Define various customer persona types"""
        # Basic demographic archetypes with varied spending patterns
        self.basic_personas = [
            {
                "name": "Budget Conscious Parent",
                "income_range": (35000, 65000),
                "avg_transactions_per_month": (12, 18),
                "avg_transaction_amount": (45, 85),
                "payment_preferences": {
                    "VISA": 0.4, "MASTERCARD": 0.2, "DEBIT": 0.2, "EBT": 0.2
                },
                "category_preferences": {
                    "Groceries": 0.5, "Household": 0.2, "Children": 0.2, "Personal Care": 0.1
                },
                "preferred_merchants": ["Walmart", "Target", "Kroger", "Aldi", "Amazon", "Dollar General"]
            },
            {
                "name": "Young Professional",
                "income_range": (70000, 110000),
                "avg_transactions_per_month": (20, 30),
                "avg_transaction_amount": (35, 65),
                "payment_preferences": {
                    "AMEX": 0.7, "VISA": 0.2, "APPLE PAY": 0.1
                },
                "category_preferences": {
                    "Groceries": 0.3, "Dining": 0.3, "Household": 0.2, "Personal Care": 0.1, "Clothing": 0.1
                },
                "preferred_merchants": ["Whole Foods", "Trader Joe's", "Amazon", "Target", "Starbucks"]
            },
            {
                "name": "Retiree",
                "income_range": (40000, 80000),
                "avg_transactions_per_month": (8, 16),
                "avg_transaction_amount": (65, 95),
                "payment_preferences": {
                    "MASTERCARD": 0.6, "DISCOVER": 0.3, "VISA": 0.1
                },
                "category_preferences": {
                    "Groceries": 0.4, "Pharmacy": 0.3, "Household": 0.2, "Dining": 0.1
                },
                "preferred_merchants": ["CVS", "Walgreens", "Publix", "Kroger", "Walmart", "Costco"]
            },
            {
                "name": "College Student",
                "income_range": (15000, 35000),
                "avg_transactions_per_month": (15, 25),
                "avg_transaction_amount": (15, 35),
                "payment_preferences": {
                    "DEBIT": 0.7, "VISA": 0.2, "VENMO": 0.1
                },
                "category_preferences": {
                    "Fast Food": 0.4, "Groceries": 0.3, "Electronics": 0.1, "Education": 0.2
                },
                "preferred_merchants": ["McDonald's", "Taco Bell", "Amazon", "Target", "Uber Eats"]
            },
            {
                "name": "High-Income Professional",
                "income_range": (150000, 300000),
                "avg_transactions_per_month": (25, 40),
                "avg_transaction_amount": (100, 250),
                "payment_preferences": {
                    "AMEX": 0.8, "VISA": 0.15, "APPLE PAY": 0.05
                },
                "category_preferences": {
                    "Electronics": 0.3, "Groceries": 0.2, "Dining": 0.2, "Clothing": 0.2, "Home Goods": 0.1
                },
                "preferred_merchants": ["Whole Foods", "Apple", "Best Buy", "Nordstrom", "Amazon"]
            }
        ]

        # Extended unique personas with more specific traits
        self.extended_personas = [
            {
                "name": "Health-Conscious Millennial",
                "income_range": (55000, 90000),
                "avg_transactions_per_month": (20, 30),
                "avg_transaction_amount": (40, 70),
                "payment_preferences": {
                    "VISA": 0.5, "APPLE PAY": 0.3, "MASTERCARD": 0.2
                },
                "category_preferences": {
                    "Organic Food": 0.4, "Health & Wellness": 0.3, "Fitness": 0.2, "Sustainable Products": 0.1
                },
                "preferred_merchants": ["Whole Foods", "Trader Joe's", "Lululemon", "REI", "Sprouts"]
            },
            {
                "name": "Tech Enthusiast",
                "income_range": (85000, 140000),
                "avg_transactions_per_month": (15, 25),
                "avg_transaction_amount": (80, 250),
                "payment_preferences": {
                    "VISA": 0.4, "MASTERCARD": 0.3, "BITCOIN": 0.1, "PAYPAL": 0.2
                },
                "category_preferences": {
                    "Electronics": 0.5, "Software": 0.2, "Gaming": 0.2, "Tech Accessories": 0.1
                },
                "preferred_merchants": ["Best Buy", "Amazon", "Apple", "Newegg", "Micro Center"]
            },
            {
                "name": "Suburban Parent",
                "income_range": (80000, 130000),
                "avg_transactions_per_month": (25, 40),
                "avg_transaction_amount": (50, 120),
                "payment_preferences": {
                    "VISA": 0.5, "MASTERCARD": 0.3, "DISCOVER": 0.2
                },
                "category_preferences": {
                    "Groceries": 0.3, "Children's Items": 0.3, "Home Improvement": 0.2, "Entertainment": 0.1, "Pet Supplies": 0.1
                },
                "preferred_merchants": ["Target", "Costco", "Amazon", "Walmart", "Home Depot"]
            },
            {
                "name": "Rural Homeowner",
                "income_range": (45000, 85000),
                "avg_transactions_per_month": (10, 20),
                "avg_transaction_amount": (60, 150),
                "payment_preferences": {
                    "DEBIT": 0.4, "VISA": 0.4, "CASH": 0.2
                },
                "category_preferences": {
                    "Home Improvement": 0.3, "Automotive": 0.2, "Groceries": 0.2, "Outdoor Equipment": 0.2, "Farm Supplies": 0.1
                },
                "preferred_merchants": ["Walmart", "Tractor Supply", "Home Depot", "AutoZone", "NAPA Auto Parts"]
            },
            {
                "name": "Urban Minimalist",
                "income_range": (70000, 120000),
                "avg_transactions_per_month": (15, 22),
                "avg_transaction_amount": (40, 90),
                "payment_preferences": {
                    "MASTERCARD": 0.4, "APPLE PAY": 0.4, "VENMO": 0.2
                },
                "category_preferences": {
                    "Dining": 0.3, "Transportation": 0.2, "Groceries": 0.2, "Entertainment": 0.2, "Home Goods": 0.1
                },
                "preferred_merchants": ["Trader Joe's", "Amazon", "Uber", "Lyft", "Seamless"]
            },
            {
                "name": "Luxury Shopper",
                "income_range": (200000, 500000),
                "avg_transactions_per_month": (15, 30),
                "avg_transaction_amount": (200, 1000),
                "payment_preferences": {
                    "AMEX": 0.7, "VISA": 0.2, "MASTERCARD": 0.1
                },
                "category_preferences": {
                    "Designer Clothing": 0.3, "Fine Dining": 0.2, "Jewelry": 0.2, "Travel": 0.2, "Home Decor": 0.1
                },
                "preferred_merchants": ["Nordstrom", "Bloomingdale's", "Saks Fifth Avenue", "Neiman Marcus", "Williams-Sonoma"]
            },
            {
                "name": "Budget Traveler",
                "income_range": (35000, 70000),
                "avg_transactions_per_month": (20, 30),
                "avg_transaction_amount": (30, 100),
                "payment_preferences": {
                    "VISA": 0.4, "MASTERCARD": 0.3, "PAYPAL": 0.2, "VENMO": 0.1
                },
                "category_preferences": {
                    "Travel": 0.4, "Fast Food": 0.2, "Transportation": 0.2, "Accommodations": 0.1, "Entertainment": 0.1
                },
                "preferred_merchants": ["Southwest Airlines", "Airbnb", "Expedia", "McDonald's", "Uber"]
            },
            {
                "name": "DIY Enthusiast",
                "income_range": (50000, 90000),
                "avg_transactions_per_month": (12, 25),
                "avg_transaction_amount": (50, 150),
                "payment_preferences": {
                    "VISA": 0.4, "MASTERCARD": 0.3, "DISCOVER": 0.2, "PAYPAL": 0.1
                },
                "category_preferences": {
                    "Home Improvement": 0.4, "Crafts": 0.3, "Tools": 0.2, "Garden": 0.1
                },
                "preferred_merchants": ["Home Depot", "Lowe's", "Michaels", "Joann", "Harbor Freight"]
            },
            {
                "name": "Fitness Enthusiast",
                "income_range": (60000, 100000),
                "avg_transactions_per_month": (18, 30),
                "avg_transaction_amount": (40, 120),
                "payment_preferences": {
                    "VISA": 0.5, "MASTERCARD": 0.3, "APPLE PAY": 0.2
                },
                "category_preferences": {
                    "Fitness Equipment": 0.3, "Supplements": 0.2, "Activewear": 0.2, "Health Food": 0.2, "Gym Memberships": 0.1
                },
                "preferred_merchants": ["Nike", "Lululemon", "GNC", "Vitamin Shoppe", "Amazon"]
            },
            {
                "name": "New Parent",
                "income_range": (60000, 120000),
                "avg_transactions_per_month": (25, 40),
                "avg_transaction_amount": (50, 150),
                "payment_preferences": {
                    "VISA": 0.5, "MASTERCARD": 0.3, "DISCOVER": 0.2
                },
                "category_preferences": {
                    "Baby Supplies": 0.4, "Groceries": 0.3, "Household": 0.2, "Healthcare": 0.1
                },
                "preferred_merchants": ["Target", "Amazon", "Buy Buy Baby", "Walmart", "Carter's"]
            },
            {
                "name": "Pet Owner",
                "income_range": (45000, 90000),
                "avg_transactions_per_month": (15, 25),
                "avg_transaction_amount": (40, 100),
                "payment_preferences": {
                    "VISA": 0.4, "MASTERCARD": 0.3, "DISCOVER": 0.2, "PAYPAL": 0.1
                },
                "category_preferences": {
                    "Pet Food": 0.4, "Pet Supplies": 0.3, "Veterinary Care": 0.2, "Pet Toys": 0.1
                },
                "preferred_merchants": ["Chewy", "PetSmart", "Petco", "Amazon", "Walmart"]
            },
            {
                "name": "Gamer",
                "income_range": (30000, 80000),
                "avg_transactions_per_month": (10, 20),
                "avg_transaction_amount": (30, 150),
                "payment_preferences": {
                    "VISA": 0.4, "MASTERCARD": 0.3, "PAYPAL": 0.2, "BITCOIN": 0.1
                },
                "category_preferences": {
                    "Video Games": 0.5, "Electronics": 0.2, "Digital Content": 0.2, "Fast Food": 0.1
                },
                "preferred_merchants": ["GameStop", "Steam", "Best Buy", "Amazon", "PlayStation Store"]
            },
            {
                "name": "Remote Worker",
                "income_range": (70000, 120000),
                "avg_transactions_per_month": (20, 35),
                "avg_transaction_amount": (40, 120),
                "payment_preferences": {
                    "VISA": 0.4, "MASTERCARD": 0.3, "AMEX": 0.2, "APPLE PAY": 0.1
                },
                "category_preferences": {
                    "Home Office": 0.3, "Coffee Shops": 0.2, "Electronics": 0.2, "Food Delivery": 0.2, "Digital Subscriptions": 0.1
                },
                "preferred_merchants": ["Amazon", "Best Buy", "Starbucks", "Office Depot", "DoorDash"]
            },
            {
                "name": "Senior Fixed Income",
                "income_range": (25000, 45000),
                "avg_transactions_per_month": (8, 15),
                "avg_transaction_amount": (30, 70),
                "payment_preferences": {
                    "VISA": 0.5, "MASTERCARD": 0.3, "CASH": 0.2
                },
                "category_preferences": {
                    "Groceries": 0.4, "Pharmacy": 0.3, "Household": 0.2, "Healthcare": 0.1
                },
                "preferred_merchants": ["Walmart", "CVS", "Walgreens", "Kroger", "Dollar Tree"]
            }
        ]
        
        # Combine all personas
        self.all_personas = self.basic_personas + self.extended_personas
    
    def define_payment_methods(self):
        """Define available payment methods"""
        self.payment_methods = [
            {"type": "CARD", "brand": "VISA", "last_four": "4242"},
            {"type": "CARD", "brand": "VISA", "last_four": "1234"},
            {"type": "CARD", "brand": "VISA", "last_four": "5678"},
            {"type": "CARD", "brand": "MASTERCARD", "last_four": "9876"},
            {"type": "CARD", "brand": "MASTERCARD", "last_four": "5432"},
            {"type": "CARD", "brand": "MASTERCARD", "last_four": "8765"},
            {"type": "CARD", "brand": "AMEX", "last_four": "1111"},
            {"type": "CARD", "brand": "AMEX", "last_four": "3333"},
            {"type": "CARD", "brand": "AMEX", "last_four": "8888"},
            {"type": "CARD", "brand": "DISCOVER", "last_four": "9999"},
            {"type": "CARD", "brand": "DISCOVER", "last_four": "6789"},
            {"type": "CARD", "brand": "DISCOVER", "last_four": "4321"},
            {"type": "CARD", "brand": "DEBIT", "last_four": "4747"},
            {"type": "CARD", "brand": "DEBIT", "last_four": "1357"},
            {"type": "CARD", "brand": "DEBIT", "last_four": "2468"},
            {"type": "CARD", "brand": "EBT", "last_four": "2222"},
            {"type": "CARD", "brand": "EBT", "last_four": "7777"},
            {"type": "CARD", "brand": "EBT", "last_four": "5555"},
            {"type": "CARD", "brand": "APPLE PAY", "last_four": "3456"},
            {"type": "CARD", "brand": "APPLE PAY", "last_four": "7890"},
            {"type": "CARD", "brand": "GOOGLE PAY", "last_four": "1598"},
            {"type": "CARD", "brand": "GOOGLE PAY", "last_four": "7531"},
            {"type": "CARD", "brand": "PAYPAL", "last_four": "6543"},
            {"type": "CARD", "brand": "PAYPAL", "last_four": "1472"},
            {"type": "CARD", "brand": "VENMO", "last_four": "8642"},
            {"type": "CARD", "brand": "VENMO", "last_four": "3579"},
            {"type": "CARD", "brand": "STORE CREDIT", "last_four": "0000"},
            {"type": "CARD", "brand": "STORE CREDIT", "last_four": "9090"},
            {"type": "CARD", "brand": "FSA", "last_four": "6655"},
            {"type": "CARD", "brand": "HSA", "last_four": "4433"},
            {"type": "CARD", "brand": "GIFT CARD", "last_four": "1212"},
            {"type": "CARD", "brand": "REWARD POINTS", "last_four": "3434"}
        ]
    
    def define_order_statuses(self):
        """Define order statuses with weights for likelihood"""
        self.order_statuses = [
            {"status": "ORDERED", "weight": 0.1},
            {"status": "SHIPPED", "weight": 0.15},
            {"status": "DELIVERED", "weight": 0.15},
            {"status": "COMPLETED", "weight": 0.55},
            {"status": "CANCELLED", "weight": 0.05}
        ]
    
    def generate_product_catalog(self):
        """Generate a comprehensive product catalog across multiple categories"""
        return {
            "Groceries": [
                {"name": "Organic Bananas, 2 lb", "price_range": (2.99, 5.99), "eligibility": [], "brand": "Fresh Farms", "unit": "lb"},
                {"name": "Freshness Guaranteed Hawaiian Dinner Rolls, 16 oz, 12 Count", "price_range": (3.99, 6.99), "eligibility": [], "brand": "King's Bakery", "unit": "pack"},
                {"name": "Organic Whole Milk, 1 Gallon", "price_range": (4.99, 7.99), "eligibility": [], "brand": "Dairy Pure", "unit": "gallon"},
                {"name": "Large Cage-Free Brown Eggs, 12 Count", "price_range": (3.99, 7.99), "eligibility": [], "brand": "Happy Hens", "unit": "dozen"},
                {"name": "Organic Baby Spinach, 5 oz", "price_range": (3.49, 5.99), "eligibility": [], "brand": "Earth's Best", "unit": "bag"},
                {"name": "Sliced White Bread, 20 oz Loaf", "price_range": (2.79, 4.99), "eligibility": [], "brand": "Wonder Bread", "unit": "loaf"},
                {"name": "Red Delicious Apples, 3 lb Bag", "price_range": (3.99, 6.99), "eligibility": [], "brand": "Washington Apples", "unit": "bag"},
                {"name": "Ground Beef, 80% Lean, 1 lb", "price_range": (4.99, 8.99), "eligibility": [], "brand": "Premium Meats", "unit": "lb"},
                {"name": "Pasta, Spaghetti, 16 oz", "price_range": (1.19, 2.99), "eligibility": [], "brand": "Barilla", "unit": "box"},
                {"name": "Cereal, Honey Nut Cheerios, 18 oz Box", "price_range": (3.99, 5.99), "eligibility": [], "brand": "General Mills", "unit": "box"},
                {"name": "Greek Yogurt, Plain, 32 oz", "price_range": (4.99, 7.99), "eligibility": [], "brand": "Chobani", "unit": "container"},
                {"name": "Fresh Atlantic Salmon Fillet, 1 lb", "price_range": (12.99, 19.99), "eligibility": [], "brand": "Ocean Fresh", "unit": "lb"},
                {"name": "Organic Quinoa, 16 oz", "price_range": (5.99, 8.99), "eligibility": [], "brand": "Ancient Harvest", "unit": "bag"},
                {"name": "Mixed Berries, Frozen, 16 oz", "price_range": (4.99, 7.99), "eligibility": [], "brand": "Nature's Best", "unit": "bag"},
                {"name": "Fresh Basil, 1 oz", "price_range": (2.99, 4.99), "eligibility": [], "brand": "Herb Garden", "unit": "bunch"}
            ],
            "Household": [
                {"name": "Paper Towels, 6 Mega Rolls", "price_range": (8.99, 12.99), "eligibility": [], "brand": "Bounty", "unit": "pack"},
                {"name": "Toilet Paper, 12 Double Rolls", "price_range": (9.99, 14.99), "eligibility": [], "brand": "Charmin", "unit": "pack"},
                {"name": "Laundry Detergent, 100 fl oz", "price_range": (10.99, 16.99), "eligibility": [], "brand": "Tide", "unit": "bottle"},
                {"name": "Disinfectant Wipes, 75 Count", "price_range": (4.99, 7.99), "eligibility": [], "brand": "Lysol", "unit": "container"},
                {"name": "Dish Soap, 24 fl oz", "price_range": (2.99, 4.99), "eligibility": [], "brand": "Dawn", "unit": "bottle"},
                {"name": "Trash Bags, 45 Count", "price_range": (7.99, 12.99), "eligibility": [], "brand": "Glad", "unit": "box"},
                {"name": "Air Freshener Spray, 8.8 oz", "price_range": (3.99, 6.99), "eligibility": [], "brand": "Febreze", "unit": "bottle"},
                {"name": "Glass Cleaner, 32 fl oz", "price_range": (3.99, 6.99), "eligibility": [], "brand": "Windex", "unit": "bottle"},
                {"name": "Bathroom Cleaner, 32 fl oz", "price_range": (3.99, 6.99), "eligibility": [], "brand": "Clorox", "unit": "bottle"},
                {"name": "All-Purpose Cleaner, 32 fl oz", "price_range": (3.99, 6.99), "eligibility": [], "brand": "Method", "unit": "bottle"}
            ],
            "Personal Care": [
                {"name": "Toothpaste, 5.2 oz", "price_range": (2.99, 5.99), "eligibility": ["FSA/HSA"], "brand": "Crest", "unit": "tube"},
                {"name": "Shampoo, 24 fl oz", "price_range": (4.99, 8.99), "eligibility": [], "brand": "Pantene", "unit": "bottle"},
                {"name": "Conditioner, 24 fl oz", "price_range": (4.99, 8.99), "eligibility": [], "brand": "Pantene", "unit": "bottle"},
                {"name": "Body Wash, 18 fl oz", "price_range": (3.99, 7.99), "eligibility": [], "brand": "Dove", "unit": "bottle"},
                {"name": "Deodorant, 2.6 oz", "price_range": (3.49, 5.99), "eligibility": ["FSA/HSA"], "brand": "Dove", "unit": "stick"},
                {"name": "Pain Relief Tablets, 200 Count", "price_range": (12.99, 18.99), "eligibility": ["FSA/HSA"], "brand": "Aleve", "unit": "bottle"},
                {"name": "Face Moisturizer, 1.7 fl oz", "price_range": (8.99, 15.99), "eligibility": [], "brand": "Neutrogena", "unit": "bottle"},
                {"name": "Hand Lotion, 16.9 fl oz", "price_range": (5.99, 9.99), "eligibility": [], "brand": "Aveeno", "unit": "bottle"},
                {"name": "Sunscreen SPF 50, 8 fl oz", "price_range": (7.99, 12.99), "eligibility": [], "brand": "Neutrogena", "unit": "bottle"},
                {"name": "Hand Soap, 12 fl oz", "price_range": (3.99, 6.99), "eligibility": [], "brand": "Softsoap", "unit": "bottle"}
            ],
            "Children": [
                {"name": "Diapers, Size 4, 144 Count", "price_range": (29.99, 39.99), "eligibility": [], "brand": "Pampers", "unit": "box"},
                {"name": "Baby Wipes, Unscented, 576 Count", "price_range": (12.99, 18.99), "eligibility": [], "brand": "Huggies", "unit": "box"},
                {"name": "Children's Multivitamin Gummies, 120 Count", "price_range": (8.99, 14.99), "eligibility": ["FSA/HSA"], "brand": "Flintstones", "unit": "bottle"},
                {"name": "Baby Formula, 30.8 oz", "price_range": (24.99, 39.99), "eligibility": [], "brand": "Similac", "unit": "container"},
                {"name": "Baby Food Pouches, 4 oz, 12 Count", "price_range": (12.99, 18.99), "eligibility": [], "brand": "Gerber", "unit": "pack"},
                {"name": "Baby Bottles, 8 oz, 3 Pack", "price_range": (14.99, 24.99), "eligibility": [], "brand": "Dr. Brown's", "unit": "pack"},
                {"name": "Baby Shampoo, 8 fl oz", "price_range": (4.99, 7.99), "eligibility": [], "brand": "Johnson's", "unit": "bottle"},
                {"name": "Baby Lotion, 13 fl oz", "price_range": (5.99, 9.99), "eligibility": [], "brand": "Johnson's", "unit": "bottle"},
                {"name": "Baby Wash, 13 fl oz", "price_range": (5.99, 9.99), "eligibility": [], "brand": "Johnson's", "unit": "bottle"},
                {"name": "Baby Powder, 14 oz", "price_range": (4.99, 7.99), "eligibility": [], "brand": "Johnson's", "unit": "bottle"}
            ],
            "Pharmacy": [
                {"name": "Multivitamin Tablets, 130 Count", "price_range": (9.99, 15.99), "eligibility": ["FSA/HSA"], "brand": "One A Day", "unit": "bottle"},
                {"name": "Blood Pressure Monitor", "price_range": (29.99, 49.99), "eligibility": ["FSA/HSA"], "brand": "Omron", "unit": "unit"},
                {"name": "Reading Glasses, +2.00", "price_range": (12.99, 24.99), "eligibility": ["FSA/HSA"], "brand": "Foster Grant", "unit": "pair"},
                {"name": "Allergy Relief Tablets, 70 Count", "price_range": (14.99, 24.99), "eligibility": ["FSA/HSA"], "brand": "Zyrtec", "unit": "bottle"},
                {"name": "First Aid Kit, 100 Pieces", "price_range": (19.99, 29.99), "eligibility": ["FSA/HSA"], "brand": "Johnson & Johnson", "unit": "kit"},
                {"name": "Thermometer, Digital", "price_range": (8.99, 14.99), "eligibility": ["FSA/HSA"], "brand": "Vicks", "unit": "unit"},
                {"name": "Bandages, Assorted Sizes, 100 Count", "price_range": (5.99, 9.99), "eligibility": ["FSA/HSA"], "brand": "Band-Aid", "unit": "box"},
                {"name": "Antibiotic Ointment, 1 oz", "price_range": (4.99, 7.99), "eligibility": ["FSA/HSA"], "brand": "Neosporin", "unit": "tube"},
                {"name": "Hand Sanitizer, 8 fl oz", "price_range": (3.99, 6.99), "eligibility": ["FSA/HSA"], "brand": "Purell", "unit": "bottle"},
                {"name": "Pain Relief Cream, 2 oz", "price_range": (6.99, 10.99), "eligibility": ["FSA/HSA"], "brand": "Bengay", "unit": "tube"}
            ],
            "Fast Food": [
                {"name": "Burger Meal Deal", "price_range": (7.99, 12.99), "eligibility": [], "brand": "McDonald's", "unit": "meal"},
                {"name": "Chicken Sandwich Combo", "price_range": (8.99, 13.99), "eligibility": [], "brand": "Chick-fil-A", "unit": "meal"},
                {"name": "Breakfast Sandwich Meal", "price_range": (5.99, 9.99), "eligibility": [], "brand": "McDonald's", "unit": "meal"},
                {"name": "Pizza, Large Pepperoni", "price_range": (9.99, 15.99), "eligibility": [], "brand": "Domino's", "unit": "pizza"},
                {"name": "Taco Combo Box", "price_range": (8.99, 13.99), "eligibility": [], "brand": "Taco Bell", "unit": "meal"},
                {"name": "Chicken Nuggets Meal", "price_range": (6.99, 10.99), "eligibility": [], "brand": "McDonald's", "unit": "meal"},
                {"name": "Sub Sandwich Combo", "price_range": (8.99, 13.99), "eligibility": [], "brand": "Subway", "unit": "meal"},
                {"name": "Burger King Whopper Meal", "price_range": (8.99, 13.99), "eligibility": [], "brand": "Burger King", "unit": "meal"},
                {"name": "Wendy's Chicken Sandwich Meal", "price_range": (7.99, 12.99), "eligibility": [], "brand": "Wendy's", "unit": "meal"},
                {"name": "KFC Bucket Meal", "price_range": (19.99, 29.99), "eligibility": [], "brand": "KFC", "unit": "meal"}
            ],
            "Dining": [
                {"name": "Restaurant Meal Delivery - Italian", "price_range": (15.99, 29.99), "eligibility": [], "brand": "Olive Garden", "unit": "meal"},
                {"name": "Restaurant Meal Delivery - Chinese", "price_range": (14.99, 27.99), "eligibility": [], "brand": "P.F. Chang's", "unit": "meal"},
                {"name": "Restaurant Meal Delivery - Mexican", "price_range": (13.99, 25.99), "eligibility": [], "brand": "Chipotle", "unit": "meal"},
                {"name": "Coffee Shop - Specialty Drinks and Pastries", "price_range": (7.99, 15.99), "eligibility": [], "brand": "Starbucks", "unit": "order"},
                {"name": "Sushi Roll Platter", "price_range": (24.99, 39.99), "eligibility": [], "brand": "Sushi Express", "unit": "platter"},
                {"name": "Steakhouse Dinner for Two", "price_range": (49.99, 79.99), "eligibility": [], "brand": "Outback Steakhouse", "unit": "meal"},
                {"name": "Pizza Delivery - Family Size", "price_range": (19.99, 29.99), "eligibility": [], "brand": "Pizza Hut", "unit": "pizza"},
                {"name": "Thai Food Delivery", "price_range": (16.99, 29.99), "eligibility": [], "brand": "Thai Express", "unit": "meal"},
                {"name": "Mediterranean Platter", "price_range": (18.99, 32.99), "eligibility": [], "brand": "Mediterranean Grill", "unit": "platter"},
                {"name": "BBQ Family Pack", "price_range": (39.99, 59.99), "eligibility": [], "brand": "Texas Roadhouse", "unit": "meal"}
            ],
            "Electronics": [
                {"name": "Wireless Earbuds", "price_range": (29.99, 159.99), "eligibility": [], "brand": "Apple", "unit": "pair"},
                {"name": "USB-C Charging Cable, 6ft", "price_range": (9.99, 19.99), "eligibility": [], "brand": "Anker", "unit": "cable"},
                {"name": "Portable Power Bank, 10000mAh", "price_range": (19.99, 39.99), "eligibility": [], "brand": "Anker", "unit": "unit"},
                {"name": "Bluetooth Speaker", "price_range": (29.99, 99.99), "eligibility": [], "brand": "JBL", "unit": "unit"},
                {"name": "Smart TV, 43-inch 4K", "price_range": (249.99, 499.99), "eligibility": [], "brand": "Samsung", "unit": "unit"},
                {"name": "Wireless Mouse", "price_range": (19.99, 39.99), "eligibility": [], "brand": "Logitech", "unit": "unit"},
                {"name": "Mechanical Keyboard", "price_range": (49.99, 129.99), "eligibility": [], "brand": "Razer", "unit": "unit"},
                {"name": "Webcam HD", "price_range": (29.99, 59.99), "eligibility": [], "brand": "Logitech", "unit": "unit"},
                {"name": "External SSD, 1TB", "price_range": (89.99, 159.99), "eligibility": [], "brand": "Samsung", "unit": "unit"},
                {"name": "Smart Watch", "price_range": (199.99, 399.99), "eligibility": [], "brand": "Apple", "unit": "unit"}
            ],
            "Education": [
                {"name": "Notebook, College Ruled, 5-pack", "price_range": (8.99, 15.99), "eligibility": [], "brand": "Mead", "unit": "pack"},
                {"name": "Mechanical Pencils, 24 Count", "price_range": (6.99, 12.99), "eligibility": [], "brand": "Paper Mate", "unit": "pack"},
                {"name": "Backpack, 15-inch Laptop Compatible", "price_range": (29.99, 59.99), "eligibility": [], "brand": "Jansport", "unit": "unit"},
                {"name": "Scientific Calculator", "price_range": (19.99, 39.99), "eligibility": [], "brand": "Texas Instruments", "unit": "unit"},
                {"name": "Printer Paper, 5000 Sheets", "price_range": (39.99, 59.99), "eligibility": [], "brand": "HP", "unit": "ream"},
                {"name": "Whiteboard, 24x36 inches", "price_range": (19.99, 39.99), "eligibility": [], "brand": "Expo", "unit": "board"},
                {"name": "Markers, Assorted Colors, 12 Pack", "price_range": (4.99, 9.99), "eligibility": [], "brand": "Crayola", "unit": "pack"},
                {"name": "Stapler, Heavy Duty", "price_range": (12.99, 24.99), "eligibility": [], "brand": "Swingline", "unit": "unit"},
                {"name": "Sticky Notes, 12 Pads", "price_range": (5.99, 9.99), "eligibility": [], "brand": "Post-it", "unit": "pack"},
                {"name": "Index Cards, 1000 Count", "price_range": (7.99, 12.99), "eligibility": [], "brand": "Oxford", "unit": "box"}
            ],
            "Clothing": [
                {"name": "Men's T-Shirt, Medium", "price_range": (14.99, 29.99), "eligibility": [], "brand": "Nike", "unit": "shirt"},
                {"name": "Women's Jeans, Size 8", "price_range": (29.99, 79.99), "eligibility": [], "brand": "Levi's", "unit": "pair"},
                {"name": "Athletic Socks, 6 Pairs", "price_range": (12.99, 24.99), "eligibility": [], "brand": "Nike", "unit": "pack"},
                {"name": "Winter Coat", "price_range": (59.99, 199.99), "eligibility": [], "brand": "North Face", "unit": "coat"},
                {"name": "Running Shoes", "price_range": (79.99, 149.99), "eligibility": [], "brand": "Nike", "unit": "pair"},
                {"name": "Dress Shirt, Men's", "price_range": (29.99, 59.99), "eligibility": [], "brand": "Ralph Lauren", "unit": "shirt"},
                {"name": "Yoga Pants, Women's", "price_range": (39.99, 79.99), "eligibility": [], "brand": "Lululemon", "unit": "pair"},
                {"name": "Hoodie, Unisex", "price_range": (34.99, 69.99), "eligibility": [], "brand": "Champion", "unit": "piece"},
                {"name": "Swim Shorts, Men's", "price_range": (24.99, 49.99), "eligibility": [], "brand": "Speedo", "unit": "pair"},
                {"name": "Summer Dress, Women's", "price_range": (39.99, 89.99), "eligibility": [], "brand": "Free People", "unit": "dress"}
            ],
            "Home Goods": [
                {"name": "Decorative Throw Pillow", "price_range": (19.99, 39.99), "eligibility": [], "brand": "Threshold", "unit": "pillow"},
                {"name": "Bed Sheets, Queen Size", "price_range": (29.99, 79.99), "eligibility": [], "brand": "Threshold", "unit": "set"},
                {"name": "Bath Towel Set, 4 Piece", "price_range": (24.99, 49.99), "eligibility": [], "brand": "Fieldcrest", "unit": "set"},
                {"name": "Table Lamp", "price_range": (29.99, 69.99), "eligibility": [], "brand": "Project 62", "unit": "lamp"},
                {"name": "Area Rug, 5x7", "price_range": (49.99, 129.99), "eligibility": [], "brand": "NuLoom", "unit": "rug"},
                {"name": "Wall Art, Canvas Print", "price_range": (39.99, 89.99), "eligibility": [], "brand": "Project 62", "unit": "piece"},
                {"name": "Coffee Table", "price_range": (99.99, 299.99), "eligibility": [], "brand": "Project 62", "unit": "table"},
                {"name": "Throw Blanket", "price_range": (19.99, 39.99), "eligibility": [], "brand": "Threshold", "unit": "blanket"},
                {"name": "Picture Frame, 8x10", "price_range": (14.99, 29.99), "eligibility": [], "brand": "Project 62", "unit": "frame"},
                {"name": "Vase, Decorative", "price_range": (24.99, 49.99), "eligibility": [], "brand": "Threshold", "unit": "vase"}
            ],
            "Pet Food": [
                {"name": "Dry Dog Food, Adult, 24 lb Bag", "price_range": (24.99, 59.99), "eligibility": [], "brand": "Purina", "unit": "bag"},
                {"name": "Wet Cat Food, 24 Cans", "price_range": (14.99, 34.99), "eligibility": [], "brand": "Friskies", "unit": "pack"},
                {"name": "Dog Treats, Assorted, 1 lb", "price_range": (7.99, 19.99), "eligibility": [], "brand": "Milk-Bone", "unit": "bag"},
                {"name": "Cat Litter, Clumping, 40 lb", "price_range": (14.99, 29.99), "eligibility": [], "brand": "Tidy Cats", "unit": "box"},
                {"name": "Pet Food Storage Container", "price_range": (19.99, 39.99), "eligibility": [], "brand": "IRIS", "unit": "container"},
                {"name": "Dog Food, Grain-Free, 20 lb", "price_range": (39.99, 69.99), "eligibility": [], "brand": "Blue Buffalo", "unit": "bag"},
                {"name": "Cat Food, Indoor Formula, 15 lb", "price_range": (29.99, 49.99), "eligibility": [], "brand": "Purina", "unit": "bag"},
                {"name": "Pet Food Mat", "price_range": (9.99, 19.99), "eligibility": [], "brand": "Gorilla Grip", "unit": "mat"},
                {"name": "Pet Food Scoop", "price_range": (4.99, 9.99), "eligibility": [], "brand": "IRIS", "unit": "scoop"},
                {"name": "Pet Food Storage Bin", "price_range": (24.99, 49.99), "eligibility": [], "brand": "Gamma2", "unit": "bin"}
            ],
            "Pet Supplies": [
                {"name": "Dog Bed, Medium", "price_range": (19.99, 69.99), "eligibility": [], "brand": "Furhaven", "unit": "bed"},
                {"name": "Cat Litter Box", "price_range": (14.99, 29.99), "eligibility": [], "brand": "IRIS", "unit": "box"},
                {"name": "Pet Carrier", "price_range": (29.99, 79.99), "eligibility": [], "brand": "Sherpa", "unit": "carrier"},
                {"name": "Dog Leash, 6 ft", "price_range": (9.99, 19.99), "eligibility": [], "brand": "PetSafe", "unit": "leash"},
                {"name": "Cat Scratching Post", "price_range": (24.99, 49.99), "eligibility": [], "brand": "SmartCat", "unit": "post"},
                {"name": "Pet Grooming Kit", "price_range": (19.99, 39.99), "eligibility": [], "brand": "Hertzko", "unit": "kit"},
                {"name": "Dog Harness", "price_range": (14.99, 29.99), "eligibility": [], "brand": "PetSafe", "unit": "harness"},
                {"name": "Cat Tree", "price_range": (49.99, 99.99), "eligibility": [], "brand": "Go Pet Club", "unit": "tree"},
                {"name": "Pet Water Fountain", "price_range": (24.99, 49.99), "eligibility": [], "brand": "Veken", "unit": "fountain"},
                {"name": "Pet First Aid Kit", "price_range": (19.99, 39.99), "eligibility": [], "brand": "Pet First Aid", "unit": "kit"}
            ],
            "Home Office": [
                {"name": "Office Chair, Ergonomic", "price_range": (99.99, 299.99), "eligibility": [], "brand": "Herman Miller", "unit": "chair"},
                {"name": "Desk, Computer", "price_range": (149.99, 399.99), "eligibility": [], "brand": "Bush Business", "unit": "desk"},
                {"name": "Printer, All-in-One", "price_range": (99.99, 299.99), "eligibility": [], "brand": "HP", "unit": "printer"},
                {"name": "Monitor, 24-inch", "price_range": (129.99, 249.99), "eligibility": [], "brand": "Dell", "unit": "monitor"},
                {"name": "Wireless Keyboard", "price_range": (29.99, 59.99), "eligibility": [], "brand": "Logitech", "unit": "keyboard"},
                {"name": "Desk Lamp", "price_range": (19.99, 39.99), "eligibility": [], "brand": "TaoTronics", "unit": "lamp"},
                {"name": "File Cabinet, 2-Drawer", "price_range": (49.99, 99.99), "eligibility": [], "brand": "HON", "unit": "cabinet"},
                {"name": "Desk Organizer", "price_range": (14.99, 29.99), "eligibility": [], "brand": "SimpleHouseware", "unit": "organizer"},
                {"name": "Monitor Stand", "price_range": (19.99, 39.99), "eligibility": [], "brand": "VIVO", "unit": "stand"},
                {"name": "Cable Management Kit", "price_range": (9.99, 19.99), "eligibility": [], "brand": "JOTO", "unit": "kit"}
            ],
            "Sports & Outdoors": [
                {"name": "Yoga Mat", "price_range": (19.99, 39.99), "eligibility": [], "brand": "Gaiam", "unit": "mat"},
                {"name": "Dumbbell Set, 20 lb", "price_range": (49.99, 99.99), "eligibility": [], "brand": "CAP", "unit": "set"},
                {"name": "Running Shoes", "price_range": (79.99, 149.99), "eligibility": [], "brand": "Nike", "unit": "pair"},
                {"name": "Basketball", "price_range": (19.99, 39.99), "eligibility": [], "brand": "Spalding", "unit": "ball"},
                {"name": "Tennis Racket", "price_range": (49.99, 99.99), "eligibility": [], "brand": "Wilson", "unit": "racket"},
                {"name": "Golf Balls, 12 Pack", "price_range": (19.99, 39.99), "eligibility": [], "brand": "Titleist", "unit": "pack"},
                {"name": "Soccer Ball", "price_range": (14.99, 29.99), "eligibility": [], "brand": "Adidas", "unit": "ball"},
                {"name": "Swimming Goggles", "price_range": (14.99, 29.99), "eligibility": [], "brand": "Speedo", "unit": "pair"},
                {"name": "Jump Rope", "price_range": (9.99, 19.99), "eligibility": [], "brand": "Crossrope", "unit": "rope"},
                {"name": "Resistance Bands Set", "price_range": (19.99, 39.99), "eligibility": [], "brand": "TheraBand", "unit": "set"}
            ],
            "Beauty": [
                {"name": "Face Moisturizer, 1.7 oz", "price_range": (8.99, 15.99), "eligibility": [], "brand": "Neutrogena", "unit": "bottle"},
                {"name": "Mascara, Black", "price_range": (6.99, 12.99), "eligibility": [], "brand": "Maybelline", "unit": "tube"},
                {"name": "Lipstick, Matte", "price_range": (4.99, 9.99), "eligibility": [], "brand": "Revlon", "unit": "tube"},
                {"name": "Foundation, 1 oz", "price_range": (12.99, 24.99), "eligibility": [], "brand": "L'Oreal", "unit": "bottle"},
                {"name": "Eye Shadow Palette", "price_range": (14.99, 29.99), "eligibility": [], "brand": "NYX", "unit": "palette"},
                {"name": "Hair Dryer", "price_range": (29.99, 59.99), "eligibility": [], "brand": "Conair", "unit": "unit"},
                {"name": "Hair Straightener", "price_range": (39.99, 79.99), "eligibility": [], "brand": "Remington", "unit": "unit"},
                {"name": "Makeup Brushes Set", "price_range": (19.99, 39.99), "eligibility": [], "brand": "Real Techniques", "unit": "set"},
                {"name": "Facial Cleanser", "price_range": (7.99, 14.99), "eligibility": [], "brand": "CeraVe", "unit": "bottle"},
                {"name": "Nail Polish Set", "price_range": (9.99, 19.99), "eligibility": [], "brand": "OPI", "unit": "set"}
            ],
            "Books": [
                {"name": "Hardcover Fiction Book", "price_range": (19.99, 39.99), "eligibility": [], "brand": "Random House", "unit": "book"},
                {"name": "Paperback Fiction Book", "price_range": (9.99, 19.99), "eligibility": [], "brand": "Penguin", "unit": "book"},
                {"name": "Children's Picture Book", "price_range": (12.99, 24.99), "eligibility": [], "brand": "Scholastic", "unit": "book"},
                {"name": "Cookbook, Hardcover", "price_range": (24.99, 49.99), "eligibility": [], "brand": "Chronicle Books", "unit": "book"},
                {"name": "Self-Help Book", "price_range": (14.99, 29.99), "eligibility": [], "brand": "Simon & Schuster", "unit": "book"},
                {"name": "Coloring Book", "price_range": (9.99, 19.99), "eligibility": [], "brand": "Dover", "unit": "book"},
                {"name": "Journal, Hardcover", "price_range": (12.99, 24.99), "eligibility": [], "brand": "Moleskine", "unit": "book"},
                {"name": "Comic Book", "price_range": (3.99, 7.99), "eligibility": [], "brand": "Marvel", "unit": "book"},
                {"name": "Textbook, Hardcover", "price_range": (49.99, 99.99), "eligibility": [], "brand": "Pearson", "unit": "book"},
                {"name": "Coffee Table Book", "price_range": (29.99, 59.99), "eligibility": [], "brand": "Taschen", "unit": "book"}
            ],
            "Toys & Games": [
                {"name": "Board Game", "price_range": (19.99, 39.99), "eligibility": [], "brand": "Hasbro", "unit": "game"},
                {"name": "LEGO Set", "price_range": (29.99, 99.99), "eligibility": [], "brand": "LEGO", "unit": "set"},
                {"name": "Puzzle, 1000 Pieces", "price_range": (14.99, 29.99), "eligibility": [], "brand": "Ravensburger", "unit": "puzzle"},
                {"name": "Remote Control Car", "price_range": (24.99, 49.99), "eligibility": [], "brand": "Hot Wheels", "unit": "car"},
                {"name": "Action Figure Set", "price_range": (19.99, 39.99), "eligibility": [], "brand": "Marvel", "unit": "set"},
                {"name": "Building Blocks Set", "price_range": (14.99, 29.99), "eligibility": [], "brand": "Mega Bloks", "unit": "set"},
                {"name": "Card Game", "price_range": (9.99, 19.99), "eligibility": [], "brand": "Mattel", "unit": "game"},
                {"name": "Science Kit", "price_range": (24.99, 49.99), "eligibility": [], "brand": "National Geographic", "unit": "kit"},
                {"name": "Art Set", "price_range": (19.99, 39.99), "eligibility": [], "brand": "Crayola", "unit": "set"},
                {"name": "Educational Game", "price_range": (14.99, 29.99), "eligibility": [], "brand": "Learning Resources", "unit": "game"}
            ],
            "Garden & Outdoor": [
                {"name": "Garden Tool Set", "price_range": (29.99, 59.99), "eligibility": [], "brand": "Fiskars", "unit": "set"},
                {"name": "Plant Pot Set", "price_range": (19.99, 39.99), "eligibility": [], "brand": "Bloem", "unit": "set"},
                {"name": "Garden Hose, 50 ft", "price_range": (24.99, 49.99), "eligibility": [], "brand": "Flexzilla", "unit": "hose"},
                {"name": "Garden Gloves", "price_range": (9.99, 19.99), "eligibility": [], "brand": "Pine Tree Tools", "unit": "pair"},
                {"name": "Plant Food", "price_range": (7.99, 14.99), "eligibility": [], "brand": "Miracle-Gro", "unit": "bottle"},
                {"name": "Garden Kneeler", "price_range": (19.99, 39.99), "eligibility": [], "brand": "Garden Genie", "unit": "unit"},
                {"name": "Pruning Shears", "price_range": (14.99, 29.99), "eligibility": [], "brand": "Fiskars", "unit": "pair"},
                {"name": "Garden Trowel", "price_range": (9.99, 19.99), "eligibility": [], "brand": "Fiskars", "unit": "tool"},
                {"name": "Plant Seeds Pack", "price_range": (4.99, 9.99), "eligibility": [], "brand": "Burpee", "unit": "pack"},
                {"name": "Garden Cart", "price_range": (49.99, 99.99), "eligibility": [], "brand": "Gorilla Carts", "unit": "cart"}
            ],
            "Automotive": [
                {"name": "Car Battery", "price_range": (89.99, 159.99), "eligibility": [], "brand": "DieHard", "unit": "battery"},
                {"name": "Motor Oil, 5 qt", "price_range": (24.99, 39.99), "eligibility": [], "brand": "Mobil 1", "unit": "bottle"},
                {"name": "Windshield Wipers", "price_range": (19.99, 39.99), "eligibility": [], "brand": "Rain-X", "unit": "pair"},
                {"name": "Air Filter", "price_range": (14.99, 29.99), "eligibility": [], "brand": "FRAM", "unit": "filter"},
                {"name": "Tire Pressure Gauge", "price_range": (9.99, 19.99), "eligibility": [], "brand": "Accutire", "unit": "gauge"},
                {"name": "Car Wash Kit", "price_range": (19.99, 39.99), "eligibility": [], "brand": "Chemical Guys", "unit": "kit"},
                {"name": "Jump Starter", "price_range": (49.99, 99.99), "eligibility": [], "brand": "NOCO", "unit": "unit"},
                {"name": "Car Vacuum", "price_range": (29.99, 59.99), "eligibility": [], "brand": "Bissell", "unit": "vacuum"},
                {"name": "Tire Inflator", "price_range": (24.99, 49.99), "eligibility": [], "brand": "AstroAI", "unit": "unit"},
                {"name": "Car Emergency Kit", "price_range": (19.99, 39.99), "eligibility": [], "brand": "First Secure", "unit": "kit"}
            ],
            "Tools & Hardware": [
                {"name": "Cordless Drill Set", "price_range": (79.99, 159.99), "eligibility": [], "brand": "DeWalt", "unit": "set"},
                {"name": "Tool Set, 200 Pieces", "price_range": (49.99, 99.99), "eligibility": [], "brand": "Craftsman", "unit": "set"},
                {"name": "Circular Saw", "price_range": (59.99, 119.99), "eligibility": [], "brand": "Skil", "unit": "saw"},
                {"name": "Hammer Set", "price_range": (19.99, 39.99), "eligibility": [], "brand": "Stanley", "unit": "set"},
                {"name": "Socket Set", "price_range": (29.99, 59.99), "eligibility": [], "brand": "Craftsman", "unit": "set"},
                {"name": "Power Sander", "price_range": (39.99, 79.99), "eligibility": [], "brand": "Black & Decker", "unit": "sander"},
                {"name": "Work Light", "price_range": (19.99, 39.99), "eligibility": [], "brand": "Stanley", "unit": "light"},
                {"name": "Tool Box", "price_range": (29.99, 59.99), "eligibility": [], "brand": "Craftsman", "unit": "box"},
                {"name": "Safety Glasses", "price_range": (9.99, 19.99), "eligibility": [], "brand": "3M", "unit": "pair"},
                {"name": "Work Gloves", "price_range": (14.99, 29.99), "eligibility": [], "brand": "Mechanix", "unit": "pair"}
            ]
        }
    
    def generate_merchant_list(self, num_merchants=100):
        """Generate a list of merchants"""
        # Define merchant categories
        grocery_merchants = ["Kroger", "Walmart", "Target", "Safeway", "Whole Foods", "Trader Joe's", "Publix", "Albertsons", 
                            "Aldi", "H-E-B", "Meijer", "Food Lion", "Costco", "Sam's Club", "Wegmans", "Sprouts", "Harris Teeter",
                            "Giant Eagle", "ShopRite", "Stop & Shop", "Hy-Vee", "Ralphs", "Vons", "Pavilions", "King Soopers"]
        
        pharmacy_merchants = ["CVS", "Walgreens", "Rite Aid", "GNC", "Vitamin Shoppe", "Walmart Pharmacy", "Kroger Pharmacy",
                            "Target Pharmacy", "Costco Pharmacy", "Publix Pharmacy", "Walgreens Pharmacy", "CVS Pharmacy",
                            "Rite Aid Pharmacy", "Duane Reade", "Bartell Drugs", "Longs Drugs", "Thrifty White"]
        
        electronics_merchants = ["Best Buy", "Apple", "Microsoft Store", "GameStop", "Office Depot", "Staples", 
                                "Dell", "Samsung", "Sony", "AT&T", "Verizon", "T-Mobile", "Sprint", "Micro Center",
                                "Fry's Electronics", "B&H Photo", "Newegg", "TigerDirect", "Crutchfield", "Abt Electronics"]
        
        fashion_merchants = ["Macy's", "Nordstrom", "JCPenney", "Kohl's", "TJ Maxx", "Ross", "Gap", "Old Navy", 
                            "Nike", "Adidas", "Foot Locker", "H&M", "Zara", "Uniqlo", "Forever 21", "Victoria's Secret",
                            "Lululemon", "Under Armour", "Puma", "Reebok", "Levi's", "Ralph Lauren", "Tommy Hilfiger",
                            "Calvin Klein", "American Eagle", "Urban Outfitters", "Anthropologie", "Free People"]
        
        home_merchants = ["Home Depot", "Lowe's", "Ace Hardware", "Bed Bath & Beyond", "IKEA", "Pottery Barn", 
                         "HomeGoods", "Wayfair", "Ashley HomeStore", "Crate & Barrel", "Williams-Sonoma", "West Elm",
                         "Pier 1", "At Home", "Kirkland's", "Tuesday Morning", "Big Lots", "Marshalls", "HomeGoods",
                         "Tuesday Morning", "Kirkland's", "At Home", "Big Lots", "Marshalls", "HomeGoods"]
        
        online_merchants = ["Amazon", "eBay", "Etsy", "Overstock", "Chewy", "Zappos", "Instacart", "DoorDash",
                           "Walmart.com", "Target.com", "Jet.com", "Wish", "Groupon", "LivingSocial", "Rakuten",
                           "Poshmark", "Mercari", "Depop", "ThredUp", "Rent the Runway", "Stitch Fix", "Trunk Club"]
        
        restaurant_merchants = ["McDonald's", "Starbucks", "Subway", "Taco Bell", "Burger King", "Wendy's", "Chick-fil-A", 
                               "Chipotle", "Panera Bread", "Domino's", "KFC", "Olive Garden", "Outback Steakhouse", "Chili's",
                               "Pizza Hut", "Papa John's", "Little Caesars", "Dunkin'", "Dairy Queen", "Five Guys",
                               "In-N-Out Burger", "Shake Shack", "Culver's", "Whataburger", "Jack in the Box", "Arby's",
                               "Popeyes", "Wingstop", "Buffalo Wild Wings", "Red Robin", "Texas Roadhouse", "LongHorn Steakhouse"]
        
        specialty_merchants = ["REI", "Bass Pro Shops", "PetSmart", "Petco", "Michaels", "Hobby Lobby", 
                              "Barnes & Noble", "Guitar Center", "Dick's Sporting Goods", "Academy Sports",
                              "Cabela's", "Orvis", "Patagonia", "The North Face", "Columbia Sportswear",
                              "L.L.Bean", "Eddie Bauer", "Joann", "AC Moore", "HobbyTown", "GameStop",
                              "ThinkGeek", "Hot Topic", "Spencer's", "Build-A-Bear Workshop", "LEGO Store"]
        
        travel_merchants = ["Expedia", "Booking.com", "Airbnb", "Hotels.com", "Southwest Airlines", 
                           "Delta Airlines", "American Airlines", "Uber", "Lyft", "United Airlines",
                           "JetBlue", "Alaska Airlines", "Hilton", "Marriott", "Hyatt", "InterContinental",
                           "Holiday Inn", "Best Western", "Travelocity", "Priceline", "Kayak", "Orbitz",
                           "Hotwire", "Vrbo", "TripAdvisor", "Skyscanner", "Kiwi.com", "Hopper"]
        
        subscription_merchants = ["Netflix", "Hulu", "Disney+", "Spotify", "Apple Music", "Xbox Game Pass", 
                                 "PlayStation Plus", "Adobe Creative Cloud", "Microsoft 365", "Amazon Prime",
                                 "YouTube Premium", "Pandora", "SiriusXM", "Audible", "Kindle Unlimited",
                                 "Amazon Music", "Google Play Music", "Tidal", "Deezer", "Crunchyroll",
                                 "Funimation", "HBO Max", "Peacock", "Paramount+", "Discovery+", "ESPN+"]
        
        automotive_merchants = ["AutoZone", "O'Reilly Auto Parts", "NAPA Auto Parts", "Advance Auto Parts",
                               "Pep Boys", "CarMax", "AutoNation", "Carvana", "Vroom", "Carvana",
                               "Midas", "Jiffy Lube", "Firestone", "Goodyear", "Discount Tire",
                               "Les Schwab", "Tire Rack", "CarParts.com", "RockAuto", "1A Auto"]
        
        beauty_merchants = ["Sephora", "Ulta Beauty", "MAC Cosmetics", "Lush", "The Body Shop",
                           "Bath & Body Works", "L'Occitane", "Kiehl's", "Origins", "Clinique",
                           "Estée Lauder", "Lancôme", "Shiseido", "Bobbi Brown", "NARS",
                           "Benefit Cosmetics", "Too Faced", "Urban Decay", "Tarte", "Fenty Beauty"]
        
        # Combine all merchant categories
        all_merchants = (grocery_merchants + pharmacy_merchants + electronics_merchants + fashion_merchants + 
                         home_merchants + online_merchants + restaurant_merchants + specialty_merchants + 
                         travel_merchants + subscription_merchants + automotive_merchants + beauty_merchants)
        
        # Remove duplicates and shuffle
        unique_merchants = list(set(all_merchants))
        random.shuffle(unique_merchants)
        
        # Generate merchant IDs and limit to requested number
        merchants = []
        for i, name in enumerate(unique_merchants[:num_merchants]):
            merchants.append({
                "id": i + 1,
                "name": name
            })
        
        return merchants
    
    def weighted_choice(self, choices):
        """Choose an item from a list of choices with weights"""
        total = sum(choice['weight'] for choice in choices)
        r = random.random() * total
        upto = 0
        for choice in choices:
            upto += choice['weight']
            if upto >= r:
                return choice
        return choices[-1]  # Fallback
    
    def generate_random_date(self, start_date, end_date):
        """Generate a random date between start_date and end_date"""
        time_between_dates = end_date - start_date
        days_between_dates = time_between_dates.days
        random_number_of_days = random.randrange(days_between_dates)
        return start_date + timedelta(days=random_number_of_days)
    
    def select_payment_methods_for_customer(self, customer_persona, num_methods=2):
        """Select payment methods for a customer based on their preferences"""
        payment_methods = []
        
        # Select primary methods based on preferences
        primary_methods = []
        for brand, weight in customer_persona["payment_preferences"].items():
            matching_methods = [pm for pm in self.payment_methods if pm["brand"] == brand]
            if matching_methods:
                for _ in range(int(weight * 10)):  # Convert weight to frequency
                    primary_methods.append(random.choice(matching_methods))
        
        # Ensure we have at least one primary method
        if not primary_methods:
            primary_methods = [random.choice(self.payment_methods)]
        
        # Select a subset of these primary methods
        num_primary = min(num_methods, len(primary_methods))
        selected_primary = random.sample(primary_methods, num_primary)
        payment_methods.extend(selected_primary)
        
        # If we need more methods, add some random ones
        if len(payment_methods) < num_methods:
            remaining_methods = [m for m in self.payment_methods if m not in payment_methods]
            if remaining_methods:
                additional_methods = random.sample(remaining_methods, min(num_methods - len(payment_methods), len(remaining_methods)))
                payment_methods.extend(additional_methods)
        
        return payment_methods
    
    def get_seasonal_adjustment(self, date, category):
        """Apply seasonal adjustments to purchase probabilities"""
        month = date.month
        
        # Define seasonal categories
        holiday_categories = ["Clothing", "Electronics", "Jewelry", "Home Goods", "Home Decor"]
        summer_categories = ["Outdoor Equipment", "Garden", "Travel", "Accommodations"]
        winter_categories = ["Clothing", "Home Improvement", "Entertainment"]
        spring_categories = ["Garden", "Home Improvement", "Clothing"]
        back_to_school = ["Education", "Electronics", "Clothing", "Children"]
        
        # Apply seasonal adjustments
        if month in [11, 12] and category in holiday_categories:
            return 2.0
        
        if month in [6, 7, 8] and category in summer_categories:
            return 1.5
        
        if month in [12, 1, 2] and category in winter_categories:
            return 1.5
        
        if month in [3, 4, 5] and category in spring_categories:
            return 1.3
        
        if month in [8, 9] and category in back_to_school:
            return 1.7
        
        # Default: no adjustment
        return 1.0
    
    def handle_payment_split(self, payment_methods, customer_payment_methods, total, num_payment_methods, include_transaction_amount):
        """Handle splitting payments between multiple payment methods"""
        if num_payment_methods == 2 and include_transaction_amount:
            # Random split between 20/80 and 80/20
            split_ratio = random.uniform(0.2, 0.8)
            amount1 = round(total * split_ratio, 2)
            amount2 = round(total - amount1, 2)  # Ensure they sum exactly to total
            
            if len(customer_payment_methods) >= 2:
                # Select two different payment methods if possible
                methods = random.sample(customer_payment_methods, 2)
                
                # First payment method
                payment_methods.append({
                    "external_id": str(random.randint(100000, 999999)),
                    "type": methods[0]['type'],
                    "brand": methods[0]['brand'],
                    "last_four": methods[0]['last_four'],
                    "name": None,
                    "transaction_amount": amount1
                })
                
                # Second payment method
                payment_methods.append({
                    "external_id": str(random.randint(100000, 999999)),
                    "type": methods[1]['type'],
                    "brand": methods[1]['brand'],
                    "last_four": methods[1]['last_four'],
                    "name": None,
                    "transaction_amount": amount2
                })
            else:
                # If only one method available, use it twice (different transactions)
                method = customer_payment_methods[0]
                
                # First payment
                payment_methods.append({
                    "external_id": str(random.randint(100000, 999999)),
                    "type": method['type'],
                    "brand": method['brand'],
                    "last_four": method['last_four'],
                    "name": None,
                    "transaction_amount": amount1
                })
                
                # Second payment (same method, different transaction ID)
                payment_methods.append({
                    "external_id": str(random.randint(100000, 999999)),
                    "type": method['type'],
                    "brand": method['brand'],
                    "last_four": method['last_four'],
                    "name": None,
                    "transaction_amount": amount2
                })
        else:
            # Just one payment method
            method = random.choice(customer_payment_methods)
            payment_methods.append({
                "external_id": str(random.randint(100000, 999999)),
                "type": method['type'],
                "brand": method['brand'],
                "last_four": method['last_four'],
                "name": None,
                "transaction_amount": total if include_transaction_amount else None
            })
    
    def generate_transaction(self, merchant_id, merchant_name, customer_persona, transaction_date, customer_payment_methods):
        """Generate a single transaction for a customer"""
        # Determine number of products (1 to 5, weighted toward lower numbers)
        num_products = random.choices([1, 2, 3, 4, 5], weights=[0.2, 0.3, 0.3, 0.15, 0.05])[0]
        
        # Determine order status
        order_status = self.weighted_choice(self.order_statuses)['status']
        
        # Select product categories based on persona weights
        selected_categories = []
        for _ in range(num_products):
            # Weighted random choice for category
            r = random.random()
            cumulative = 0
            selected = next(iter(customer_persona['category_preferences']))  # Default
            
            for category, weight in customer_persona['category_preferences'].items():
                # Apply seasonal adjustment
                adjusted_weight = weight * self.get_seasonal_adjustment(transaction_date, category)
                cumulative += adjusted_weight
                if r <= cumulative:
                    selected = category
                    break
            
            selected_categories.append(selected)
        
        # Select actual products from those categories
        products = []
        sub_total = 0
        
        for category in selected_categories:
            # Skip if we've reached target number of products
            if len(products) >= num_products:
                break
            
            # Find available products in this category
            available_products = self.product_catalog.get(category, [])
            if available_products:  # Skip empty categories
                # Choose a random product from this category
                product = random.choice(available_products)
                
                # Determine price within the product's range
                min_price, max_price = product['price_range']
                unit_price = round(random.uniform(min_price, max_price), 2)
                
                # Determine quantity (most often 1, occasionally more)
                quantity = random.choices([1, 2, 3], weights=[0.8, 0.15, 0.05])[0]
                
                # Calculate total for this product
                product_total = round(unit_price * quantity, 2)
                sub_total += product_total
                
                # Add product to the transaction
                products.append({
                    "external_id": str(random.randint(10000000, 999999999)),
                    "name": product['name'],
                    "url": f"https://www.{merchant_name.lower().replace(' ', '')}.com/ip/{random.randint(100000000, 999999999)}",
                    "quantity": quantity,
                    "eligibility": product['eligibility'],
                    "price": {
                        "sub_total": product_total,
                        "total": product_total,
                        "unit_price": unit_price
                    }
                })
        
        # If no products were added, ensure we add at least one fallback product
        if not products:
            # Find any category with products
            for category, products_list in self.product_catalog.items():
                if products_list:
                    product = random.choice(products_list)
                    
                    unit_price = round(random.uniform(product['price_range'][0], product['price_range'][1]), 2)
                    product_total = unit_price
                    sub_total = product_total
                    
                    products.append({
                        "external_id": str(random.randint(10000000, 999999999)),
                        "name": product['name'],
                        "url": f"https://www.{merchant_name.lower().replace(' ', '')}.com/ip/{random.randint(100000000, 999999999)}",
                        "quantity": 1,
                        "eligibility": product['eligibility'],
                        "price": {
                            "sub_total": product_total,
                            "total": product_total,
                            "unit_price": unit_price
                        }
                    })
                    break
        
        # Round the total to nearest cent
        total = round(sub_total, 2)
        
        # Determine payment methods
        payment_methods = []
        
        # For cancelled orders, maybe don't include transaction amounts
        if order_status == "CANCELLED":
            # 80% chance of having null transaction amounts for cancelled orders
            include_transaction_amount = random.random() > 0.8
        else:
            include_transaction_amount = True
        
        # Determine number of payment methods
        if total > 100:
            num_payment_methods_probability = [0.7, 0.3]  # 30% chance of using 2 payment methods
        elif total > 50:
            num_payment_methods_probability = [0.8, 0.2]  # 20% chance of using 2 payment methods
        else:
            num_payment_methods_probability = [0.9, 0.1]  # 10% chance of using 2 payment methods
        
        num_payment_methods = random.choices([1, 2], weights=num_payment_methods_probability)[0]
        
        # Check if any products are FSA/HSA eligible
        has_fsa_eligible = any("FSA/HSA" in product["eligibility"] for product in products)
        
        # If using two payment methods and some items are FSA eligible, consider using FSA/HSA
        if num_payment_methods == 2 and has_fsa_eligible and include_transaction_amount and random.random() < 0.7:
            # Find FSA eligible items total
            fsa_eligible_total = sum(product["price"]["total"] for product in products 
                                   if any(elig in product["eligibility"] for elig in ["FSA/HSA"]))
            
            # Non-FSA eligible total
            non_fsa_total = total - fsa_eligible_total
            
            # Use FSA/HSA card for eligible items
            fsa_method = next((m for m in customer_payment_methods if m["brand"] in ["FSA", "HSA"]), None)
            
            if fsa_method:
                payment_methods.append({
                    "external_id": str(random.randint(100000, 999999)),
                    "type": fsa_method['type'],
                    "brand": fsa_method['brand'],
                    "last_four": fsa_method['last_four'],
                    "name": None,
                    "transaction_amount": round(fsa_eligible_total, 2)
                })
                
                # Use regular payment method for non-FSA items
                regular_methods = [m for m in customer_payment_methods if m["brand"] not in ["FSA", "HSA"]]
                if regular_methods:
                    regular_method = random.choice(regular_methods)
                    payment_methods.append({
                        "external_id": str(random.randint(100000, 999999)),
                        "type": regular_method['type'],
                        "brand": regular_method['brand'],
                        "last_four": regular_method['last_four'],
                        "name": None,
                        "transaction_amount": round(non_fsa_total, 2)
                    })
            else:
                # Fall back to regular payment methods
                self.handle_payment_split(payment_methods, customer_payment_methods, total, num_payment_methods, include_transaction_amount)
        else:
            # Regular payment method handling
            self.handle_payment_split(payment_methods, customer_payment_methods, total, num_payment_methods, include_transaction_amount)
        
        # Build the complete transaction
        transaction = {
            "id": str(uuid.uuid4()),
            "external_id": str(uuid.uuid4()),
            "datetime": transaction_date.strftime("%Y-%m-%dT%H:%M:%S+00:00"),
            "url": f"https://www.{merchant_name.lower().replace(' ', '')}.com/orders/{random.randint(100000000, 999999999)}rand",
            "order_status": order_status,
            "payment_methods": payment_methods,
            "price": {
                "sub_total": sub_total,
                "adjustments": [],
                "total": total,
                "currency": "USD"
            },
            "products": products
        }
        
        return transaction
    
    def generate_customer_transactions(self, customer_persona, num_transactions, start_date, end_date):
        """Generate a set of transactions for a customer over a time period"""
        all_transactions = []
        
        # Determine transaction frequency
        min_per_month, max_per_month = customer_persona.get('avg_transactions_per_month', (15, 30))
        
        # Calculate date ranges
        days_in_range = (end_date - start_date).days
        months_in_range = days_in_range / 30.0  # approximate
        
        # Calculate transactions per month
        avg_per_month = random.uniform(min_per_month, max_per_month)
        
        # Total expected transactions over the time period
        expected_transactions = int(avg_per_month * months_in_range)
        
        # Adjust for requested number if different
        if num_transactions > 0:
            expected_transactions = num_transactions
        
        # Select preferred merchants based on persona
        preferred_merchant_names = customer_persona.get('preferred_merchants', [])
        
        # Find matching merchants from our list
        preferred_merchants = []
        for name in preferred_merchant_names:
            matching = [m for m in self.merchants if m["name"] == name]
            if matching:
                preferred_merchants.extend(matching)
        
        # Add some random merchants
        if len(preferred_merchants) < 10:
            remaining = [m for m in self.merchants if m not in preferred_merchants]
            additional_count = min(10 - len(preferred_merchants), len(remaining))
            preferred_merchants.extend(random.sample(remaining, additional_count))
        
        # Select payment methods for this customer
        customer_payment_methods = self.select_payment_methods_for_customer(customer_persona, 
                                                                         num_methods=random.randint(2, 4))
        
        # Generate transaction dates
        transaction_dates = []
        for _ in range(expected_transactions):
            random_date = self.generate_random_date(start_date, end_date)
            transaction_dates.append(random_date)
        
        # Sort dates chronologically
        transaction_dates.sort()
        
        # Generate transactions
        for transaction_date in transaction_dates:
            # Decide on merchant - more likely to use preferred merchants
            if random.random() < 0.8 and preferred_merchants:  # 80% chance to use preferred
                merchant = random.choice(preferred_merchants)
            else:
                merchant = random.choice(self.merchants)
            
            # Generate the transaction
            transaction = self.generate_transaction(
                merchant["id"],
                merchant["name"],
                customer_persona,
                transaction_date,
                customer_payment_methods
            )
            
            all_transactions.append((transaction, merchant))
        
        # Sort by date (most recent first)
        all_transactions.sort(key=lambda x: x[0]["datetime"], reverse=True)
        
        return all_transactions
    
    def generate_customer_data(self, customer_persona, num_transactions_per_file=200, start_date=None, end_date=None):
        """Generate customer data files organized by merchant"""
        # Use last ~12 months as default date range
        if end_date is None:
            end_date = datetime.now()
        if start_date is None:
            start_date = end_date - timedelta(days=365)
        
        # Generate transactions for this customer
        all_transactions = self.generate_customer_transactions(
            customer_persona, 
            num_transactions_per_file, 
            start_date, 
            end_date
        )
        
        # Group transactions by merchant
        merchant_transactions = {}
        for transaction, merchant in all_transactions:
            merchant_id = merchant["id"]
            if merchant_id not in merchant_transactions:
                merchant_transactions[merchant_id] = {
                    "merchant": merchant,
                    "transactions": []
                }
            merchant_transactions[merchant_id]["transactions"].append(transaction)
        
        # Create a file for each merchant
        result_files = []
        for merchant_id, data in merchant_transactions.items():
            # Only include merchants with transactions
            if data["transactions"]:
                # Add pagination fields
                result = copy.deepcopy(data)
                result["next_cursor"] = "eyJpZCI6MTI3NjEsIl9wb2ludHNUb05leHRJdGVtcyI6dHJ1ZX0"
                result["limit"] = len(result["transactions"])
                
                result_files.append(result)
        
        return result_files
    
    def generate_diverse_customers(self, num_customers=100, transactions_per_customer=200):
        """Generate data for a diverse set of customers"""
        # Start with all base personas
        self.all_personas = self.basic_personas + self.extended_personas
        
        # Generate unique personas for each customer
        selected_personas = []
        for i in range(num_customers):
            # Choose a random base persona to modify
            base_persona = copy.deepcopy(random.choice(self.all_personas))
            
            # Modify attributes to create unique variation
            # Adjust income range
            income_min, income_max = base_persona["income_range"]
            income_adjustment = random.uniform(0.8, 1.2)
            new_income_min = max(15000, int(income_min * income_adjustment))
            new_income_max = max(new_income_min + 10000, int(income_max * income_adjustment))
            base_persona["income_range"] = (new_income_min, new_income_max)
            
            # Adjust transaction frequency
            tx_min, tx_max = base_persona["avg_transactions_per_month"]
            tx_adjustment = random.uniform(0.8, 1.2)
            new_tx_min = max(5, int(tx_min * tx_adjustment))
            new_tx_max = max(new_tx_min + 5, int(tx_max * tx_adjustment))
            base_persona["avg_transactions_per_month"] = (new_tx_min, new_tx_max)
            
            # Adjust payment preferences
            for brand in list(base_persona["payment_preferences"].keys()):
                base_persona["payment_preferences"][brand] *= random.uniform(0.8, 1.2)
            
            # Normalize payment preferences
            total = sum(base_persona["payment_preferences"].values())
            for brand in base_persona["payment_preferences"]:
                base_persona["payment_preferences"][brand] /= total
            
            # Add more overlap between customer types
            self.adjust_preferences(base_persona)
            
            # Give it a unique name
            base_persona["name"] = f"Customer {i+1}"
            
            selected_personas.append(base_persona)
        
        # Use last 12 months as date range
        end_date = datetime.now()
        start_date = end_date - timedelta(days=365)
        
        # Generate data for each customer
        customer_files = []
        for i, persona in enumerate(selected_personas):
            print(f"Generating data for customer {i+1}/{num_customers}")
            
            # Generate customer data
            customer_data = self.generate_customer_data(
                persona, 
                num_transactions_per_file=transactions_per_customer,
                start_date=start_date,
                end_date=end_date
            )
            
            # Combine all transactions
            all_transactions = []
            for merchant_data in customer_data:
                all_transactions.extend(merchant_data["transactions"])
            
            # Add splurge transactions
            self.add_splurge_transactions(all_transactions, persona)
            
            # Apply seasonal patterns
            self.apply_seasonal_patterns(all_transactions)
            
            # Sort transactions by date
            all_transactions.sort(key=lambda x: x["datetime"], reverse=True)
            
            customer_files.append({
                "persona": persona,
                "data": [{
                    "merchant": {"id": 1, "name": "Customer"},
                    "transactions": all_transactions
                }]
            })
        
        return customer_files
    
    def save_customer_files(self, customer_files, output_dir):
        """Save generated customer files to disk"""
        # Create output directory if it doesn't exist
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        
        # Save each customer's data
        for i, customer in enumerate(customer_files):
            # Use simple numbered filename
            customer_filename = os.path.join(output_dir, f"{i+1}.txt")
            
            # Combine all transactions from all merchants into one list
            all_transactions = []
            for merchant_data in customer["data"]:
                all_transactions.extend(merchant_data["transactions"])
            
            # Sort transactions by date (most recent first)
            all_transactions.sort(key=lambda x: x["datetime"], reverse=True)
            
            # Create the combined data structure
            combined_data = {
                "customer_type": customer["persona"]["name"],  # Store customer type in the data
                "merchant": {
                    "id": 1,  # Using a single merchant ID for the customer
                    "name": "Customer"  # Generic name since we're using numbered files
                },
                "transactions": all_transactions,
                "next_cursor": "eyJpZCI6MTI3NjEsIl9wb2ludHNUb05leHRJdGVtcyI6dHJ1ZX0",
                "limit": len(all_transactions)
            }
            
            # Save the combined data to a single file
            with open(customer_filename, 'w') as f:
                json.dump(combined_data, f, indent=4)
            
            print(f"Generated {len(all_transactions)} transactions for customer {i+1}")
        
        print(f"Successfully generated data for {len(customer_files)} customers in '{output_dir}' directory.")
    
    def adjust_preferences(self, base_persona):
        """Add more overlap between customer types by mixing preferences"""
        # Add some random categories from other personas
        all_categories = set()
        for persona in self.all_personas:
            all_categories.update(persona["category_preferences"].keys())
        
        # Add 2-3 random categories with lower weights
        for _ in range(random.randint(2, 3)):
            new_category = random.choice(list(all_categories))
            if new_category not in base_persona["category_preferences"]:
                base_persona["category_preferences"][new_category] = random.uniform(0.05, 0.15)
        
        # Normalize category preferences
        total = sum(base_persona["category_preferences"].values())
        for category in base_persona["category_preferences"]:
            base_persona["category_preferences"][category] /= total

    def add_splurge_transactions(self, transactions, persona):
        """Add random splurge transactions to make spending patterns more realistic"""
        # 10% chance of a splurge transaction
        if random.random() < 0.1:
            # Create a transaction 2-3x their normal spending
            normal_max = persona["avg_transaction_amount"][1]
            splurge_amount = random.uniform(normal_max * 2, normal_max * 3)
            
            # Find a suitable merchant for the splurge
            splurge_merchant = random.choice(self.merchants)
            
            # Get a random date from existing transactions
            random_transaction = random.choice(transactions)
            transaction_date = datetime.strptime(random_transaction["datetime"], "%Y-%m-%dT%H:%M:%S+00:00")
            
            # Create a splurge transaction
            splurge_transaction = self.generate_transaction(
                splurge_merchant["id"],
                splurge_merchant["name"],
                persona,
                transaction_date,
                self.select_payment_methods_for_customer(persona)
            )
            
            # Adjust the transaction amount
            splurge_transaction["price"]["total"] = splurge_amount
            splurge_transaction["price"]["sub_total"] = splurge_amount
            for product in splurge_transaction["products"]:
                product["price"]["total"] = splurge_amount / len(splurge_transaction["products"])
                product["price"]["sub_total"] = product["price"]["total"]
                product["price"]["unit_price"] = product["price"]["total"]
            
            transactions.append(splurge_transaction)

    def apply_seasonal_patterns(self, transactions):
        """Add seasonal variations to spending patterns"""
        for transaction in transactions:
            month = datetime.strptime(transaction["datetime"], "%Y-%m-%dT%H:%M:%S+00:00").month
            
            # Holiday shopping spikes (Nov-Dec)
            if month in [11, 12]:
                transaction["price"]["total"] *= random.uniform(1.2, 1.5)
                transaction["price"]["sub_total"] = transaction["price"]["total"]
                for product in transaction["products"]:
                    product["price"]["total"] *= random.uniform(1.2, 1.5)
                    product["price"]["sub_total"] = product["price"]["total"]
                    product["price"]["unit_price"] = product["price"]["total"]
            
            # Summer spending (Jun-Aug)
            elif month in [6, 7, 8]:
                transaction["price"]["total"] *= random.uniform(1.1, 1.3)
                transaction["price"]["sub_total"] = transaction["price"]["total"]
                for product in transaction["products"]:
                    product["price"]["total"] *= random.uniform(1.1, 1.3)
                    product["price"]["sub_total"] = product["price"]["total"]
                    product["price"]["unit_price"] = product["price"]["total"]

def main():
    """Main entry point for the script"""
    # Parse command line arguments
    parser = argparse.ArgumentParser(description='Generate mock transaction data for multiple customers')
    parser.add_argument('--customers', type=int, default=5, help='Number of customers to generate')
    parser.add_argument('--transactions', type=int, default=200, help='Approximate transactions per customer')
    parser.add_argument('--outdir', type=str, default='mock_data', help='Output directory')
    args = parser.parse_args()
    
    # Create the transaction generator
    generator = MockTransactionGenerator()
    
    # Generate diverse customer data
    customer_files = generator.generate_diverse_customers(args.customers, args.transactions)
    
    # Save the files
    generator.save_customer_files(customer_files, args.outdir)

if __name__ == "__main__":
    main()



    