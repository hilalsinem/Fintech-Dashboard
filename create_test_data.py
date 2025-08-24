import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def create_test_excel_file():
    # Create sample data
    data = {
        'transaction_id': [f'TXN_{i:06d}' for i in range(1, 51)],
        'customer_id': [f'CUST_{i:05d}' for i in np.random.randint(1, 20, 50)],
        'transaction_date': [datetime(2023, 5, 1) + timedelta(days=np.random.randint(0, 30)) for _ in range(50)],
        'amount': [round(np.random.uniform(5, 1000), 2) for _ in range(50)],
        'transaction_type': np.random.choice(['DEBIT', 'CREDIT', 'TRANSFER', 'PAYMENT', 'REFUND'], 50),
        'merchant_category': np.random.choice(['GROCERIES', 'ENTERTAINMENT', 'UTILITIES', 'SHOPPING', 
                                              'DINING', 'TRANSPORT', 'HEALTHCARE', 'TRAVEL', 'EDUCATION'], 50),
        'status': np.random.choice(['SUCCESS', 'FAILED', 'PENDING', 'FRAUD_DETECTED'], 50, p=[0.85, 0.05, 0.05, 0.05]),
        'merchant_id': [f'MERC_{np.random.randint(1000, 9999)}' for _ in range(50)],
        'currency': ['USD'] * 50,
        'location': np.random.choice(['NY', 'CA', 'TX', 'FL', 'IL', 'WA'], 50)
    }
    
    # Create DataFrame
    df = pd.DataFrame(data)
    
    # Save to Excel
    df.to_excel('transaction_data_sample.xlsx', index=False)
    print("Sample Excel file created: transaction_data_sample.xlsx")
    
    # Also save as CSV for alternative testing
    df.to_csv('transaction_data_sample.csv', index=False)
    print("Sample CSV file created: transaction_data_sample.csv")
    
    return df

if __name__ == "__main__":
    create_test_excel_file()