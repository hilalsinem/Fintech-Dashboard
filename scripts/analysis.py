import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sqlalchemy import create_engine
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import os

class TransactionAnalyzer:
    def __init__(self, connection_string=None):
        if connection_string:
            self.engine = create_engine(connection_string)
        else:
            # Fallback to CSV if no database connection
            self.engine = None
            self.csv_path = '../data/transactions.csv'
        
    def load_data(self):
        """Load data from database or CSV"""
        if self.engine:
            self.transactions = pd.read_sql('SELECT * FROM transactions', self.engine)
        else:
            self.transactions = pd.read_csv(self.csv_path)
            
        self.transactions['transaction_date'] = pd.to_datetime(self.transactions['transaction_date'])
        
    def generate_summary_stats(self):
        """Generate comprehensive summary statistics"""
        summary = {
            'total_transactions': len(self.transactions),
            'successful_transactions': len(self.transactions[self.transactions['status'] == 'SUCCESS']),
            'failed_transactions': len(self.transactions[self.transactions['status'] == 'FAILED']),
            'fraud_transactions': len(self.transactions[self.transactions['status'] == 'FRAUD_DETECTED']),
            'total_volume': self.transactions[self.transactions['status'] == 'SUCCESS']['amount'].sum(),
            'avg_transaction_size': self.transactions[self.transactions['status'] == 'SUCCESS']['amount'].mean(),
            'start_date': self.transactions['transaction_date'].min(),
            'end_date': self.transactions['transaction_date'].max()
        }
        return summary
    
    def plot_daily_volume(self):
        """Plot daily transaction volume"""
        daily_data = self.transactions.groupby(
            self.transactions['transaction_date'].dt.date
        ).agg({
            'transaction_id': 'count',
            'amount': 'sum'
        }).reset_index()
        
        fig = make_subplots(specs=[[{"secondary_y": True}]])
        
        fig.add_trace(
            go.Scatter(x=daily_data['transaction_date'], 
                      y=daily_data['transaction_id'],
                      name="Transaction Count",
                      line=dict(color='blue')),
            secondary_y=False,
        )
        
        fig.add_trace(
            go.Scatter(x=daily_data['transaction_date'], 
                      y=daily_data['amount'],
                      name="Transaction Volume",
                      line=dict(color='green')),
            secondary_y=True,
        )
        
        fig.update_layout(
            title='Daily Transaction Volume and Count',
            xaxis_title='Date',
            width=1000,
            height=500
        )
        
        fig.update_yaxes(title_text="Transaction Count", secondary_y=False)
        fig.update_yaxes(title_text="Transaction Volume ($)", secondary_y=True)
        
        return fig
    
    def plot_category_analysis(self):
        """Plot transaction analysis by category"""
        category_data = self.transactions.groupby('merchant_category').agg({
            'transaction_id': 'count',
            'amount': 'sum'
        }).reset_index()
        
        fig = make_subplots(rows=1, cols=2, subplot_titles=('Transaction Count by Category', 'Revenue by Category'))
        
        fig.add_trace(
            go.Bar(x=category_data['merchant_category'], 
                  y=category_data['transaction_id'],
                  name="Count"),
            row=1, col=1
        )
        
        fig.add_trace(
            go.Bar(x=category_data['merchant_category'], 
                  y=category_data['amount'],
                  name="Revenue"),
            row=1, col=2
        )
        
        fig.update_layout(height=500, width=1000, showlegend=False)
        return fig
    
    def detect_anomalies(self):
        """Simple anomaly detection using Z-score"""
        successful_txns = self.transactions[self.transactions['status'] == 'SUCCESS']
        
        # Calculate Z-scores
        mean_amount = successful_txns['amount'].mean()
        std_amount = successful_txns['amount'].std()
        
        successful_txns['z_score'] = (successful_txns['amount'] - mean_amount) / std_amount
        
        # Flag anomalies (Z-score > 3)
        anomalies = successful_txns[successful_txns['z_score'] > 3]
        
        return anomalies[['transaction_id', 'customer_id', 'amount', 'z_score', 'merchant_category']]
    
    def generate_report(self):
        """Generate comprehensive analysis report"""
        self.load_data()
        summary = self.generate_summary_stats()
        
        print("=== FINANCIAL TRANSACTION ANALYSIS REPORT ===")
        print(f"Analysis Period: {summary['start_date']} to {summary['end_date']}")
        print(f"Total Transactions: {summary['total_transactions']:,}")
        print(f"Successful Transactions: {summary['successful_transactions']:,}")
        print(f"Failed Transactions: {summary['failed_transactions']:,}")
        print(f"Fraudulent Transactions: {summary['fraud_transactions']:,}")
        print(f"Total Volume: ${summary['total_volume']:,.2f}")
        print(f"Average Transaction Size: ${summary['avg_transaction_size']:,.2f}")
        
        # Generate plots
        daily_fig = self.plot_daily_volume()
        category_fig = self.plot_category_analysis()
        
        # Detect anomalies
        anomalies = self.detect_anomalies()
        print(f"\nAnomalies Detected (Z-score > 3): {len(anomalies)} transactions")
        
        return {
            'summary': summary,
            'daily_fig': daily_fig,
            'category_fig': category_fig,
            'anomalies': anomalies
        }

# Usage
if __name__ == "__main__":
    # Try to connect to database, fall back to CSV
    db_connection = os.getenv('DATABASE_URL')
    analyzer = TransactionAnalyzer(db_connection)
    report = analyzer.generate_report()