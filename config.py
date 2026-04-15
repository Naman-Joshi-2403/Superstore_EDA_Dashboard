import os

BASE_DIR        = os.path.dirname(os.path.abspath(__file__))
RAW_DATA_PATH   = os.path.join(BASE_DIR, "data", "raw",       "superstore.csv")
CLEAN_DATA_PATH = os.path.join(BASE_DIR, "data", "processed", "superstore_clean.csv")

ENCODING    = "cp1252"
DATE_FORMAT = "%m/%d/%Y"

EXPECTED_COLUMNS = [
    "Row ID", "Order ID", "Order Date", "Ship Date", "Ship Mode",
    "Customer ID", "Customer Name", "Segment", "Country", "City",
    "State", "Postal Code", "Region", "Product ID", "Category",
    "Sub-Category", "Product Name", "Sales", "Quantity", "Discount", "Profit"
]

NUMERIC_COLS = ["Sales", "Quantity", "Discount", "Profit"]
CAT_COLS     = ["Ship Mode", "Segment", "Region", "Category", "Sub-Category", "State", "City"]
DATE_COLS    = ["Order Date", "Ship Date"]

DISCOUNT_MIN    = 0.0
DISCOUNT_MAX    = 1.0
DISCOUNT_BINS   = [-0.01, 0.0, 0.2, 0.4, 1.0]
DISCOUNT_LABELS = ["No Discount", "Low (0-20%)", "Medium (20-40%)", "High (>40%)"]
