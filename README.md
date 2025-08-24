# Fintech Transaction Dashboard

## A comprehensive financial transaction analysis and visualization platform.

<img width="2736" height="1564" alt="image" src="https://github.com/user-attachments/assets/761f88be-22be-4728-b05a-bfa9ac16005c" />

---

<img width="2736" height="1468" alt="image" src="https://github.com/user-attachments/assets/998e0057-e6fc-4b57-a122-66a1c4c52eff" />

---

<img width="2736" height="1618" alt="image" src="https://github.com/user-attachments/assets/678abee9-1e6c-45b9-b89d-1d36fac4dda1" />

---

<img width="2736" height="1624" alt="image" src="https://github.com/user-attachments/assets/ce83e137-935a-48eb-b2de-e5c1df7d8194" />


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
pip install -r requirements.txt
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
