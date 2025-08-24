import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import io
import os

# Page configuration
st.set_page_config(
    page_title="Fintech Transaction Dashboard",
    page_icon="💳",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f8f9fa;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #1f77b4;
        margin-bottom: 1rem;
    }
    .upload-section {
        background-color: #f0f2f6;
        padding: 20px;
        border-radius: 10px;
        margin-bottom: 20px;
    }
    .requirements-box {
        background-color: #fff3cd;
        border-left: 4px solid #ffc107;
        padding: 15px;
        border-radius: 5px;
        margin: 15px 0;
    }
    .column-table {
        width: 100%;
        border-collapse: collapse;
        margin: 10px 0;
    }
    .column-table th, .column-table td {
        border: 1px solid #ddd;
        padding: 8px;
        text-align: left;
    }
    .column-table th {
        background-color: #f2f2f2;
    }
    .example-table {
        font-size: 0.9em;
        margin: 15px 0;
    }
</style>
""", unsafe_allow_html=True)

def generate_sample_data():
    """Generate sample data if no file is uploaded"""
    np.random.seed(42)
    random.seed(42)
    
    customer_ids = [f'CUST_{i:05d}' for i in range(1, 101)]
    merchant_categories = ['GROCERIES', 'ENTERTAINMENT', 'UTILITIES', 'SHOPPING', 
                          'DINING', 'TRANSPORT', 'HEALTHCARE', 'TRAVEL', 'EDUCATION']
    
    transaction_types = ['DEBIT', 'CREDIT', 'TRANSFER', 'PAYMENT', 'REFUND']
    status_types = ['SUCCESS', 'FAILED', 'PENDING', 'FRAUD_DETECTED']
    
    start_date = datetime(2023, 1, 1)
    end_date = datetime(2024, 1, 1)
    
    data = []
    for i in range(1000):
        customer_id = np.random.choice(customer_ids)
        transaction_date = start_date + timedelta(
            days=np.random.randint(0, (end_date - start_date).days),
            hours=np.random.randint(0, 23),
            minutes=np.random.randint(0, 59)
        )
        
        amount = round(np.random.lognormal(mean=3, sigma=1.5), 2)
        if np.random.random() < 0.05:
            amount = round(amount * np.random.uniform(5, 20), 2)
        
        transaction_type = np.random.choice(transaction_types)
        merchant_category = np.random.choice(merchant_categories)
        
        if np.random.random() < 0.03:
            status = 'FAILED'
        elif np.random.random() < 0.01:
            status = 'FRAUD_DETECTED'
        elif np.random.random() < 0.02:
            status = 'PENDING'
        else:
            status = 'SUCCESS'
        
        merchant_id = f'MERC_{np.random.randint(1000, 9999)}'
        
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
            'location': np.random.choice(['NY', 'CA', 'TX', 'FL', 'IL', 'WA'])
        })
    
    return pd.DataFrame(data)

def show_data_requirements():
    """Display data format requirements"""
    st.markdown("""
    <div class="requirements-box">
        <h3>📋 Data Format Requirements</h3>
        <p>Your file must include these columns with the exact names:</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Create a table of required columns
    requirements_data = {
        'Column Name': [
            'transaction_id', 
            'customer_id', 
            'transaction_date', 
            'amount', 
            'transaction_type', 
            'merchant_category', 
            'status'
        ],
        'Description': [
            'Unique identifier for each transaction (text)',
            'Identifier for the customer (text)',
            'Date of the transaction (date format)',
            'Transaction amount (numeric)',
            'Type of transaction (DEBIT, CREDIT, TRANSFER, PAYMENT, REFUND)',
            'Category of the merchant (text)',
            'Status of the transaction (SUCCESS, FAILED, PENDING, FRAUD_DETECTED)'
        ],
        'Required': ['Yes'] * 7
    }
    
    requirements_df = pd.DataFrame(requirements_data)
    st.table(requirements_df)
    
    # Show example data
    st.markdown("""
    <div class="requirements-box">
        <h4>📝 Example Data Format</h4>
        <p>Your data should look like this:</p>
    </div>
    """, unsafe_allow_html=True)
    
    example_data = {
        'transaction_id': ['TXN_000001', 'TXN_000002'],
        'customer_id': ['CUST_00001', 'CUST_00002'],
        'transaction_date': ['2023-01-15', '2023-01-16'],
        'amount': [125.50, 89.99],
        'transaction_type': ['DEBIT', 'CREDIT'],
        'merchant_category': ['GROCERIES', 'ENTERTAINMENT'],
        'status': ['SUCCESS', 'SUCCESS']
    }
    
    example_df = pd.DataFrame(example_data)
    st.dataframe(example_df, use_container_width=True)
    
    # Download template button
    st.download_button(
        label="📥 Download CSV Template",
        data=pd.DataFrame(columns=requirements_data['Column Name']).to_csv(index=False),
        file_name="transaction_data_template.csv",
        mime="text/csv",
        help="Download a template CSV file with the required column headers"
    )

def validate_data(df):
    """Validate the uploaded data has required columns"""
    required_columns = ['transaction_id', 'customer_id', 'transaction_date', 'amount', 
                       'transaction_type', 'merchant_category', 'status']
    
    missing_columns = [col for col in required_columns if col not in df.columns]
    if missing_columns:
        st.error(f"❌ Missing required columns: {', '.join(missing_columns)}")
        st.info("Please make sure your file contains these exact column names.")
        show_data_requirements()
        return False
    
    # Convert date column if it exists
    if 'transaction_date' in df.columns:
        try:
            df['transaction_date'] = pd.to_datetime(df['transaction_date'])
        except:
            st.error("Could not parse transaction_date column. Please ensure it's in a valid date format (YYYY-MM-DD).")
            return False
    
    # Ensure amount is numeric
    if 'amount' in df.columns:
        try:
            df['amount'] = pd.to_numeric(df['amount'])
        except:
            st.error("Could not convert amount column to numeric values.")
            return False
    
    return True

def create_dashboard(df):
    """Create the dashboard with the provided data"""
    st.title("💳 Fintech Transaction Dashboard")
    st.markdown("---")
    
    # Sidebar filters
    st.sidebar.header("Filters")
    
    # Date range filter
    min_date = df['transaction_date'].min().date()
    max_date = df['transaction_date'].max().date()
    
    date_range = st.sidebar.date_input(
        "Date Range",
        value=(min_date, max_date),
        min_value=min_date,
        max_value=max_date
    )
    
    # Category filter
    available_categories = df['merchant_category'].unique()
    selected_categories = st.sidebar.multiselect(
        "Merchant Categories",
        options=available_categories,
        default=available_categories
    )
    
    # Status filter
    available_statuses = df['status'].unique()
    selected_status = st.sidebar.multiselect(
        "Transaction Status",
        options=available_statuses,
        default=['SUCCESS']
    )
    
    # Filter data
    filtered_df = df[
        (df['transaction_date'].dt.date >= date_range[0]) &
        (df['transaction_date'].dt.date <= date_range[1]) &
        (df['merchant_category'].isin(selected_categories)) &
        (df['status'].isin(selected_status))
    ]
    
    # KPI Cards
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        total_volume = filtered_df[filtered_df['status'] == 'SUCCESS']['amount'].sum()
        st.metric("Total Volume", f"${total_volume:,.2f}")
        
    with col2:
        total_txns = len(filtered_df)
        st.metric("Total Transactions", f"{total_txns:,}")
        
    with col3:
        success_rate = (len(filtered_df[filtered_df['status'] == 'SUCCESS']) / len(filtered_df)) * 100
        st.metric("Success Rate", f"{success_rate:.1f}%")
        
    with col4:
        avg_txn_size = filtered_df[filtered_df['status'] == 'SUCCESS']['amount'].mean()
        st.metric("Avg Transaction", f"${avg_txn_size:,.2f}")
    
    # Main charts
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Daily Transaction Volume")
        daily_data = filtered_df[filtered_df['status'] == 'SUCCESS'].groupby(
            filtered_df['transaction_date'].dt.date
        )['amount'].sum().reset_index()
        
        fig = px.line(daily_data, x='transaction_date', y='amount',
                     labels={'transaction_date': 'Date', 'amount': 'Amount ($)'})
        st.plotly_chart(fig, use_container_width=True)
        
    with col2:
        st.subheader("Transactions by Category")
        category_data = filtered_df[filtered_df['status'] == 'SUCCESS'].groupby(
            'merchant_category'
        )['amount'].sum().reset_index()
        
        fig = px.pie(category_data, values='amount', names='merchant_category',
                    title='Revenue Distribution by Category')
        st.plotly_chart(fig, use_container_width=True)
    
    # Additional charts
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Transaction Status Distribution")
        status_counts = filtered_df['status'].value_counts()
        fig = px.bar(status_counts, x=status_counts.index, y=status_counts.values,
                    labels={'x': 'Status', 'y': 'Count'})
        st.plotly_chart(fig, use_container_width=True)
        
    with col2:
        st.subheader("Top Customers by Spending")
        top_customers = filtered_df[filtered_df['status'] == 'SUCCESS'].groupby(
            'customer_id'
        )['amount'].sum().nlargest(10).reset_index()
        
        fig = px.bar(top_customers, x='customer_id', y='amount',
                    labels={'customer_id': 'Customer ID', 'amount': 'Total Spent ($)'})
        st.plotly_chart(fig, use_container_width=True)
    
    # Fraud detection section
    if 'FRAUD_DETECTED' in df['status'].values:
        st.subheader("Fraud Detection Analysis")
        fraud_data = filtered_df[filtered_df['status'] == 'FRAUD_DETECTED']
        
        if not fraud_data.empty:
            col1, col2 = st.columns(2)
            
            with col1:
                fraud_by_category = fraud_data.groupby('merchant_category').size().reset_index(name='count')
                fig = px.bar(fraud_by_category, x='merchant_category', y='count',
                            title='Fraud Cases by Category')
                st.plotly_chart(fig, use_container_width=True)
                
            with col2:
                fraud_over_time = fraud_data.groupby(
                    fraud_data['transaction_date'].dt.date
                ).size().reset_index(name='count')
                fig = px.line(fraud_over_time, x='transaction_date', y='count',
                             title='Fraud Cases Over Time')
                st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No fraudulent transactions detected in the selected filters.")
    
    # Data table
    st.subheader("Transaction Data Preview")
    st.dataframe(filtered_df.head(100))

def main():
    # Header section
    st.markdown("""
    <div class="upload-section">
        <h1>💳 Fintech Transaction Dashboard</h1>
        <p>Upload your transaction data to analyze financial patterns, detect anomalies, and visualize trends.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Show data requirements
    with st.expander("📋 Click to view data format requirements", expanded=True):
        show_data_requirements()
    
    # File upload section
    st.markdown("### 📤 Upload Your Transaction Data")
    
    uploaded_file = st.file_uploader(
        "Choose a CSV or Excel file", 
        type=['csv', 'xlsx', 'xls'],
        help="Upload your transaction data file. Make sure it follows the format requirements above."
    )
    
    if uploaded_file is not None:
        try:
            # Read the file based on its type
            if uploaded_file.name.endswith('.csv'):
                df = pd.read_csv(uploaded_file)
            else:  # Excel file
                df = pd.read_excel(uploaded_file)
            
            # Validate the data
            if validate_data(df):
                st.success("✅ File uploaded successfully!")
                create_dashboard(df)
                
        except Exception as e:
            st.error(f"❌ Error reading file: {str(e)}")
            st.info("Please make sure you're uploading a valid CSV or Excel file.")
    else:
        st.info("👆 Upload a file to get started or use sample data below.")
        
        if st.button("Use Sample Data"):
            with st.spinner("Generating sample data..."):
                df = generate_sample_data()
                create_dashboard(df)

if __name__ == "__main__":
    main()
