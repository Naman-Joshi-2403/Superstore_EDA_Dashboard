import logging
import pandas as pd

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from config import DISCOUNT_BINS, DISCOUNT_LABELS

logger = logging.getLogger(__name__)


def add_time_features(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df["Order Year"]    = df["Order Date"].dt.year
    df["Order Month"]   = df["Order Date"].dt.month
    df["Order Quarter"] = df["Order Date"].dt.quarter
    df["Month Name"]    = df["Order Date"].dt.strftime("%b")
    df["Month Year"]    = df["Order Date"].dt.to_period("M").astype(str)
    df["Day Of Week"]   = df["Order Date"].dt.day_name()
    logger.info("Added time features: Year, Month, Quarter, Month Name, Month Year, Day Of Week")
    return df

def add_shipping_days(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df["Shipping Days"] = (df["Ship Date"] - df["Order Date"]).dt.days
    neg = (df["Shipping Days"] < 0).sum()
    if neg:
        logger.warning(f"{neg} rows have negative Shipping Days — check date consistency.")
    logger.info(
        f"Shipping Days → min={df['Shipping Days'].min()}  "
        f"max={df['Shipping Days'].max()}  "
        f"mean={df['Shipping Days'].mean():.1f}"
    )
    return df

def add_profit_margin(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df["Profit Margin %"] = df.apply(
        lambda r: round((r["Profit"] / r["Sales"]) * 100, 2) if r["Sales"] != 0 else 0.0,
        axis=1,
    )
    logger.info(
        f"Profit Margin % → mean={df['Profit Margin %'].mean():.2f}%  "
        f"median={df['Profit Margin %'].median():.2f}%"
    )
    return df

def add_loss_flag(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df["Is Loss"] = df["Profit"] < 0
    loss_count = df["Is Loss"].sum()
    loss_pct   = loss_count / len(df) * 100
    logger.info(f"Loss-making rows: {loss_count:,} ({loss_pct:.1f}% of total orders)")
    return df

def add_discount_bins(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df["Discount Tier"] = pd.cut(
        df["Discount"],
        bins=DISCOUNT_BINS,
        labels=DISCOUNT_LABELS,
    )
    logger.info("Discount tiers distribution:")
    logger.info(df["Discount Tier"].value_counts().to_string())
    return df

def add_revenue_band(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    bins   = [-0.01, 50, 500, 2000, df["Sales"].max() + 1]
    labels = ["Low (<$50)", "Medium ($50-500)", "High ($500-2K)", "Very High (>$2K)"]
    df["Revenue Band"] = pd.cut(df["Sales"], bins=bins, labels=labels)
    return df

def run_feature_pipeline(df: pd.DataFrame) -> pd.DataFrame:
    logger.info("=" * 55)
    logger.info("Starting feature engineering pipeline …")
    logger.info("=" * 55)

    df = add_time_features(df)
    df = add_shipping_days(df)
    df = add_profit_margin(df)
    df = add_loss_flag(df)
    df = add_discount_bins(df)
    df = add_revenue_band(df)

    logger.info(f"Feature engineering complete → {df.shape[1]} total columns")
    return df
