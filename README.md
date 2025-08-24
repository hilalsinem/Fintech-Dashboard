# Fintech Transaction Dashboard

A comprehensive financial transaction analysis and visualization platform.
<img width="2736" height="1660" alt="image" src="https://github.com/user-attachments/assets/a5961c08-1d15-4700-9b80-838cdcd52cb0" />

<img width="2736" height="1494" alt="image" src="https://github.com/user-attachments/assets/fbbc1d26-ac9a-4899-b83c-7c9c8ab8fb07" />

<img width="2736" height="1650" alt="image" src="https://github.com/user-attachments/assets/04b185a7-660f-45e8-9006-883244172ed6" />


---

## 🚀 Features
- Synthetic transaction data generation  
- PostgreSQL database with optimized schema  
- Advanced SQL analytics  
- Interactive Streamlit dashboard  
- Fraud detection system  
- Business intelligence visualizations  

---

## 🛠️ Installation

### 1. Clone the repository
```bash
git clone https://github.com/your-username/fintech-dashboard.git
cd fintech-dashboard
```

### 2. Create virtual environment
```bash
python -m venv venv
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate
```

### 3. Install dependencies
```bash
pip install -r dashboard/requirements.txt
```

### 4. Generate sample data
```bash
python scripts/data_generator.py
```


## ▶️ Running the Dashboard
```bash
streamlit run dashboard/app.py
```
Access at: http://localhost:8501


## 📂 Project Structure
fintech-dashboard/

├── data/

│   └── transactions.csv

├── sql/

│   ├── schema.sql

│   └── queries.sql

├── scripts/

│   ├── data_generator.py

│   └── analysis.py

├── dashboard/

│   ├── app.py

│   └── requirements.txt

├── config.py

└── README.md


## 🗄️ Database Setup (Optional)

### 1. Create PostgreSQL database
CREATE DATABASE fintech_dashboard;

CREATE USER fintech_user WITH PASSWORD 'your_password';

GRANT ALL PRIVILEGES ON DATABASE fintech_dashboard TO fintech_user;


### 2. Import schema and data
psql -U fintech_user -d fintech_dashboard -f sql/schema.sql

psql -U fintech_user -d fintech_dashboard -c "\copy transactions FROM 'data/transactions.csv' CSV HEADER"


### 3. Update .env file
Add your database credentials in the .env file.


DB_NAME=fintech_dashboard

DB_USER=fintech_user

DB_PASSWORD=your_password

DB_HOST=localhost

DB_PORT=5432



## 📊 Usage

- Filter by date range, merchant category, transaction status

- View key metrics and visualizations

- Analyze transaction patterns and detect anomalies

- Explore business intelligence insights


## 🧰 Technologies Used

- Python, Pandas, SQLAlchemy

- PostgreSQL
  
- Streamlit

- Plotly, Matplotlib

- SQL
