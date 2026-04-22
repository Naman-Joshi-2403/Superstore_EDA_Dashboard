# 🛒 Superstore EDA Dashboard

An interactive Exploratory Data Analysis dashboard built on the Kaggle Global Superstore dataset. Explore sales trends, profitability, regional performance, customer segments, and shipping operations — all through a clean dark-themed Streamlit interface.

---

## 🔗 Live Demo

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://superstore-data-eda.streamlit.app/)

👉 **[https://superstore-data-eda.streamlit.app/](https://superstore-data-eda.streamlit.app/)**

---

## 📋 Requirements & Setup

### Prerequisites
- Python 3.10+
- pip

### Installation

```bash
# 1. Clone the repository
git clone https://github.com/Naman-Joshi-2403/Superstore_EDA_Dashboard.git
cd superstore-eda

# 2. Create and activate a virtual environment
python -m venv env
env\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run the app
streamlit run app.py
```

The app will open at `http://localhost:8501`

### Dependencies

```
streamlit>=1.32.0
pandas>=2.0.0
matplotlib
```

---

## 🛠️ Tech Stack

| Tool | Purpose |
|---|---|
| **Python** | Core language |
| **Pandas** | Data cleaning, feature engineering, aggregations |
| **Streamlit** | Dashboard UI and native charts |
| **Matplotlib** | Correlation heatmap styling |
| **Streamlit Cloud** | Deployment and hosting |

---

## 📁 Project Structure

```
superstore-eda/
│
├── app.py                  # Main Streamlit app — UI, filters, KPIs, tabs
├── config.py               # Paths, column names, discount bin settings
├── requirements.txt        # Python dependencies
│
├── src/
│   ├── data_loader.py      # Reads raw CSV with correct encoding
│   ├── data_cleaner.py     # Handles nulls, types, duplicates, outlier flags
│   ├── feature_engineer.py # Derives time features, shipping days, profit margin
│   └── visualizer.py       # Groupby aggregations returning chart-ready DataFrames
│
├── data/
│   ├── raw/                # Original superstore.csv
│   └── processed/          # Cleaned superstore_clean.csv (auto-generated)
│
└── .streamlit/
    └── config.toml         # Dark theme configuration
```

---

## 📊 Dashboard Tabs & Features

### 📈 Sales Trends
- Monthly sales by year — spot seasonality patterns
- Year-over-year sales growth broken down by category
- Quarterly profit trends across all categories

### 💰 Profitability
- Profit by sub-category — instantly see loss-makers vs top performers
- Average profit and loss rate by discount tier — reveals the discount tipping point
- Callout showing the top 3 loss-making sub-categories

### 🗺️ Regional
- Sales and profit comparison across all four regions
- State-level profit ranking (top 20 states)
- Region × Category profit breakdown table

### 👥 Customers
- Sales distribution by customer segment
- Average profit margin per segment
- Top N customers by total sales (adjustable slider)

### 📦 Operations
- Average shipping days per ship mode
- Average profit per ship mode
- Full shipping summary table with loss rate

### 🔬 Deep Dive
- Correlation matrix across all numeric variables
- Full filtered dataset viewer
- CSV download of filtered data

---

## 💡 Key Insights

- **Tables and Bookcases are loss-making** sub-categories despite high sales volume — driven by deep discounts
- **Discounts above 40% almost always result in a loss** — the discount tier analysis makes this pattern clear
- **Technology has the highest profit margin** across all categories and regions
- **The West region leads in both sales and profit**, while the Central region consistently underperforms
- **Same Day shipping has the highest average profit** but is used the least — an opportunity worth exploring
- **Consumer segment accounts for ~50% of sales** but Corporate has a slightly better profit margin

---

## 📦 Data Source

 [Superstore Dataset]

- 9,994 order lines
- 4 years of data (2014–2017)
- 21 columns covering orders, customers, products, geography, and financials

---

## 👤 Author

**Naman**
- GitHub: [@Naman-Joshi-2403](https://github.com/Naman-Joshi-2403)

---

