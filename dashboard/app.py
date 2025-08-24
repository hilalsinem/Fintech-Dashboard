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

def validate_data(df):
    """Validate the uploaded data has required columns"""
    required_columns = ['transaction_id', 'customer_id', 'transaction_date', 'amount', 
                       'transaction_type', 'merchant_category', 'status']
    
    missing_columns = [col for col in required_columns if col not in df.columns]
    if missing_columns:
        st.error(f"Missing required columns: {', '.join(missing_columns)}")
        st.info("Please make sure your file contains these columns: " + ", ".join(required_columns))
        return False
    
    # Convert date column if it exists
    if 'transaction_date' in df.columns:
        try:
            df['transaction_date'] = pd.to_datetime(df['transaction_date'])
        except:
            st.error("Could not parse transaction_date column. Please ensure it's in a valid date format.")
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
    # File upload section
    st.sidebar.header("Data Upload")
    
    st.markdown("""
    <div class="upload-section">
        <h2>📤 Upload Your Transaction Data</h2>
        <p>Upload an Excel or CSV file with transaction data to analyze it in the dashboard.</p>
    </div>
    """, unsafe_allow_html=True)
    
    uploaded_file = st.file_uploader(
        "Choose a file", 
        type=['csv', 'xlsx', 'xls'],
        help="Upload a CSV or Excel file with transaction data. Required columns: transaction_id, customer_id, transaction_date, amount, transaction_type, merchant_category, status"
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
                st.success("File uploaded successfully!")
                create_dashboard(df)
                
        except Exception as e:
            st.error(f"Error reading file: {str(e)}")
            st.info("Please make sure you're uploading a valid CSV or Excel file.")
    else:
        st.info("👆 Upload a file to get started or use sample data below.")
        
        if st.button("Use Sample Data"):
            with st.spinner("Generating sample data..."):
                df = generate_sample_data()
                create_dashboard(df)

if __name__ == "__main__":
    main()
