import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from sqlalchemy import create_engine
from datetime import datetime, timedelta
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
</style>
""", unsafe_allow_html=True)

class FintechDashboard:
    def __init__(self):
        # Try to connect to database, fall back to CSV
        self.db_connection = os.getenv('DATABASE_URL')
        if self.db_connection:
            self.engine = create_engine(self.db_connection)
        else:
            self.engine = None
            self.csv_path = '../data/transactions.csv'
        
    def load_data(self):
        """Load transaction data from database or CSV"""
        if self.engine:
            query = "SELECT * FROM transactions"
            self.df = pd.read_sql(query, self.engine)
        else:
            self.df = pd.read_csv(self.csv_path)
            
        self.df['transaction_date'] = pd.to_datetime(self.df['transaction_date'])
        
    def create_dashboard(self):
        """Create the Streamlit dashboard"""
        st.title("💳 Fintech Transaction Dashboard")
        st.markdown("---")
        
        # Load data
        self.load_data()
        
        # Sidebar filters
        st.sidebar.header("Filters")
        
        date_range = st.sidebar.date_input(
            "Date Range",
            value=(self.df['transaction_date'].min().date(), 
                  self.df['transaction_date'].max().date()),
            min_value=self.df['transaction_date'].min().date(),
            max_value=self.df['transaction_date'].max().date()
        )
        
        selected_categories = st.sidebar.multiselect(
            "Merchant Categories",
            options=self.df['merchant_category'].unique(),
            default=self.df['merchant_category'].unique()
        )
        
        selected_status = st.sidebar.multiselect(
            "Transaction Status",
            options=self.df['status'].unique(),
            default=['SUCCESS']
        )
        
        # Filter data
        filtered_df = self.df[
            (self.df['transaction_date'].dt.date >= date_range[0]) &
            (self.df['transaction_date'].dt.date <= date_range[1]) &
            (self.df['merchant_category'].isin(selected_categories)) &
            (self.df['status'].isin(selected_status))
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
        st.subheader("Transaction Data")
        st.dataframe(filtered_df.head(100))

# Run the dashboard
if __name__ == "__main__":
    dashboard = FintechDashboard()
    dashboard.create_dashboard()