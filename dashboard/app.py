import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random
import os
import streamlit as st

# Add this function to generate data
def generate_transaction_data(num_records=10000):
    np.random.seed(42)
    random.seed(42)
    
    # Generate customer data
    customer_ids = [f'CUST_{i:05d}' for i in range(1, 501)]
    merchant_categories = ['GROCERIES', 'ENTERTAINMENT', 'UTILITIES', 'SHOPPING', 
                          'DINING', 'TRANSPORT', 'HEALTHCARE', 'TRAVEL', 'EDUCATION']
    
    transaction_types = ['DEBIT', 'CREDIT', 'TRANSFER', 'PAYMENT', 'REFUND']
    status_types = ['SUCCESS', 'FAILED', 'PENDING', 'FRAUD_DETECTED']
    
    # Generate dates
    start_date = datetime(2023, 1, 1)
    end_date = datetime(2024, 1, 1)
    
    data = []
    for i in range(num_records):
        customer_id = random.choice(customer_ids)
        transaction_date = start_date + timedelta(
            days=random.randint(0, (end_date - start_date).days),
            hours=random.randint(0, 23),
            minutes=random.randint(0, 59)
        )
        
        amount = round(np.random.lognormal(mean=3, sigma=1.5), 2)
        if random.random() < 0.05:  # 5% chance of large transaction
            amount = round(amount * random.uniform(5, 20), 2)
        
        transaction_type = random.choice(transaction_types)
        merchant_category = random.choice(merchant_categories)
        
        # Generate status with some failures and fraud
        if random.random() < 0.03:
            status = 'FAILED'
        elif random.random() < 0.01:
            status = 'FRAUD_DETECTED'
        elif random.random() < 0.02:
            status = 'PENDING'
        else:
            status = 'SUCCESS'
        
        # Generate merchant info
        merchant_id = f'MERC_{random.randint(1000, 9999)}'
        
        data.append({
            'transaction_id': f'TXN_{i:06d}',
            'customer_id': customer_id,
            'transaction_date': transaction_date,
            'amount': amount,
            'transaction_type': transaction_type,
            'merchant_category': merchant_category,
            'merchant_id': merchant_id,
            'status': status,
            'currency': 'USD',
            'location': random.choice(['NY', 'CA', 'TX', 'FL', 'IL', 'WA'])
        })
    
    df = pd.DataFrame(data)
    return df

class FintechDashboard:
    def __init__(self):
        self.csv_path = 'transactions.csv'
        
    def load_data(self):
        """Load transaction data from CSV, generate if doesn't exist"""
        # Check if file exists, if not generate data
        if not os.path.exists(self.csv_path):
            st.info("Generating sample transaction data...")
            self.df = generate_transaction_data(5000)  # Smaller dataset for deployment
            self.df.to_csv(self.csv_path, index=False)
            st.success("Data generated successfully!")
        else:
            self.df = pd.read_csv(self.csv_path)
            
        self.df['transaction_date'] = pd.to_datetime(self.df['transaction_date'])
    
    # Rest of your class methods remain the same...
