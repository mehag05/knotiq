from mock_customer_data import MockTransactionGenerator
import json
import os

def generate_merchant_data():
    # Initialize the generator
    generator = MockTransactionGenerator()
    
    # Generate merchant list
    merchants = generator.generate_merchant_list(num_merchants=100)
    
    # Create data directory if it doesn't exist
    if not os.path.exists('data'):
        os.makedirs('data')
    
    # Save merchants to a file
    with open('data/merchants.json', 'w') as f:
        json.dump({
            'status': 'success',
            'merchants': merchants
        }, f, indent=2)
    
    print(f"Generated {len(merchants)} merchants")
    print("Sample merchant:", merchants[0])
    return merchants

if __name__ == "__main__":
    generate_merchant_data() 