import os, sys
import pandas as pd
import streamlit as st

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from config import CLEAN_DATA_PATH, RAW_DATA_PATH
from src.data_loader      import load_raw_data
from src.data_cleaner     import run_cleaning_pipeline
from src.feature_engineer import run_feature_pipeline
from src.visualizer import (
    sales_by_month, sales_by_category_year, quarterly_profit,
    profit_by_subcategory, avg_profit_by_discount_tier, loss_rate_by_discount_tier,
    sales_profit_by_region, profit_by_state, sales_by_region_category,
    sales_by_segment, profit_margin_by_segment, top_customers,
    avg_shipping_days, avg_profit_by_ship_mode, shipping_summary_table,
    correlation_table,
)

st.set_page_config(
    page_title="Superstore EDA",
    page_icon="🛒",
    layout="wide",
    initial_sidebar_state="expanded",
)


@st.cache_data(show_spinner="Loading data …")
def load_data() -> pd.DataFrame:
    if os.path.exists(CLEAN_DATA_PATH):
        df = pd.read_csv(CLEAN_DATA_PATH, parse_dates=["Order Date", "Ship Date"])
    else:
        raw = load_raw_data(RAW_DATA_PATH)
        df  = run_cleaning_pipeline(raw, save=True)
    return run_feature_pipeline(df)

df_full = load_data()


with st.sidebar:
    st.header("🔍 Filters")

    sel_years    = st.multiselect("📅 Year",     sorted(df_full["Order Year"].unique()),    default=sorted(df_full["Order Year"].unique()))
    sel_regions  = st.multiselect("🗺️ Region",  sorted(df_full["Region"].unique()),        default=sorted(df_full["Region"].unique()))
    sel_segments = st.multiselect("👥 Segment",  sorted(df_full["Segment"].unique()),       default=sorted(df_full["Segment"].unique()))
    sel_cats     = st.multiselect("📦 Category", sorted(df_full["Category"].unique()),      default=sorted(df_full["Category"].unique()))
    show_outliers = st.checkbox("Include flagged outliers", value=True)


df = df_full.copy()
if sel_years:    df = df[df["Order Year"].isin(sel_years)]
if sel_regions:  df = df[df["Region"].isin(sel_regions)]
if sel_segments: df = df[df["Segment"].isin(sel_segments)]
if sel_cats:     df = df[df["Category"].isin(sel_cats)]
if not show_outliers:
    df = df[~(df["Sales_outlier"] | df["Profit_outlier"] | df["Discount_outlier"])]

if df.empty:
    st.warning("⚠️ No data for these filters.")
    st.stop()


st.title("🛒 Superstore EDA Dashboard")

total_sales  = df["Sales"].sum()
total_profit = df["Profit"].sum()
margin       = (total_profit / total_sales * 100) if total_sales else 0
total_orders = df["Order ID"].nunique()
loss_orders  = int(df["Is Loss"].sum())

k1, k2, k3, k4, k5 = st.columns(5)
k1.metric("💰 Total Sales",   f"${total_sales/1e6:.2f}M")
k2.metric("📈 Total Profit",  f"${total_profit/1e3:.1f}K", delta=f"{'+' if total_profit >= 0 else ''}{total_profit/1e3:.1f}K")
k3.metric("📊 Profit Margin", f"{margin:.1f}%")
k4.metric("🧾 Total Orders",  f"{total_orders:,}")
k5.metric("🔴 Loss Orders",   f"{loss_orders:,}", delta=f"-{loss_orders/len(df)*100:.1f}% of lines", delta_color="inverse")

st.divider()


tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "📈 Sales Trends", "💰 Profitability", "🗺️ Regional",
    "👥 Customers",    "📦 Operations",    "🔬 Deep Dive",
])

with tab1:
    st.subheader("Monthly Sales by Year")
    st.line_chart(sales_by_month(df), height=300)

    st.subheader("Year-over-Year Sales by Category")
    st.bar_chart(sales_by_category_year(df), height=280)

    st.subheader("Quarterly Profit by Category")
    st.line_chart(quarterly_profit(df), height=280)

with tab2:
    st.subheader("Total Profit by Sub-Category")
    st.bar_chart(profit_by_subcategory(df), horizontal=True, height=420)

    col_a, col_b = st.columns(2)
    with col_a:
        st.subheader("Avg Profit by Discount Tier")
        st.bar_chart(avg_profit_by_discount_tier(df), height=260)
    with col_b:
        st.subheader("Loss Rate % by Discount Tier")
        st.bar_chart(loss_rate_by_discount_tier(df), height=260)

    worst = df.groupby("Sub-Category")["Profit"].sum().nsmallest(3).reset_index()
    st.info("⚠️ **Top loss-making sub-categories:** " +
            "  |  ".join(f"{r['Sub-Category']}: ${r['Profit']:,.0f}" for _, r in worst.iterrows()))

with tab3:
    st.subheader("Sales & Profit by Region")
    st.bar_chart(sales_profit_by_region(df), height=280)

    col_a, col_b = st.columns(2)
    with col_a:
        st.subheader("Profit by State (Top 20)")
        st.bar_chart(profit_by_state(df).head(20), height=320)
    with col_b:
        st.subheader("Profit: Region × Category")
        st.dataframe(sales_by_region_category(df).style.format("${:,.0f}"),
                     use_container_width=True, height=320)

with tab4:
    col_a, col_b = st.columns(2)
    with col_a:
        st.subheader("Sales by Segment")
        st.bar_chart(sales_by_segment(df), height=260)
    with col_b:
        st.subheader("Avg Profit Margin % by Segment")
        st.bar_chart(profit_margin_by_segment(df), height=260)

    n = st.slider("Top N customers", 5, 20, 10)
    st.subheader(f"Top {n} Customers by Sales")
    st.bar_chart(top_customers(df, n), horizontal=True, height=350)

with tab5:
    col_a, col_b = st.columns(2)
    with col_a:
        st.subheader("Avg Shipping Days by Ship Mode")
        st.bar_chart(avg_shipping_days(df), height=260)
    with col_b:
        st.subheader("Avg Profit by Ship Mode")
        st.bar_chart(avg_profit_by_ship_mode(df), height=260)

    st.subheader("Shipping Summary")
    st.dataframe(shipping_summary_table(df), use_container_width=True)

with tab6:
    st.subheader("Correlation Matrix")
    st.dataframe(
        correlation_table(df),
        use_container_width=True,
    )

    st.subheader("Filtered Dataset")
    st.dataframe(
        df[["Order ID", "Order Date", "Customer Name", "Segment", "Category",
            "Sub-Category", "Region", "State", "Sales", "Profit", "Discount",
            "Quantity", "Profit Margin %", "Shipping Days", "Discount Tier", "Is Loss",
        ]].sort_values("Order Date", ascending=False),
        use_container_width=True,
        height=360,
    )
    st.download_button("⬇️ Download CSV",
                       df.to_csv(index=False).encode("utf-8"),
                       "superstore_filtered.csv", "text/csv")

