import logging
import pandas as pd
import numpy as np

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from config import (
    DATE_FORMAT, NUMERIC_COLS, CAT_COLS,
    DISCOUNT_MIN, DISCOUNT_MAX, CLEAN_DATA_PATH
)

logger = logging.getLogger(__name__)


def parse_dates(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    for col in ["Order Date", "Ship Date"]:
        df[col] = pd.to_datetime(df[col], format=DATE_FORMAT)
        logger.info(f"Parsed '{col}' → dtype: {df[col].dtype}")
    return df

def check_missing(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    null_counts = df.isnull().sum()
    null_cols   = null_counts[null_counts > 0]

    if null_cols.empty:
        logger.info("No missing values found in any column.")
        return df

    logger.warning(f"Missing values detected:\n{null_cols}")

    critical = ["Sales", "Profit"]
    before = len(df)
    df.dropna(subset=critical, inplace=True)
    dropped = before - len(df)
    if dropped:
        logger.warning(f"Dropped {dropped} rows with null Sales/Profit.")

    for col in NUMERIC_COLS:
        if df[col].isnull().sum() > 0:
            median_val = df[col].median()
            df[col].fillna(median_val, inplace=True)
            logger.info(f"Filled '{col}' nulls with median={median_val:.2f}")

    for col in CAT_COLS:
        if col in df.columns and df[col].isnull().sum() > 0:
            df[col].fillna("Unknown", inplace=True)
            logger.info(f"Filled '{col}' nulls with 'Unknown'")

    return df

def remove_duplicates(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    before = len(df)

    df.drop_duplicates(subset=["Row ID"], keep="first", inplace=True)
    after_rowid = len(df)

    df.drop_duplicates(keep="first", inplace=True)
    after_full = len(df)

    removed = before - after_full
    if removed:
        logger.warning(f"Removed {removed} duplicate row(s).")
    else:
        logger.info("No duplicate rows found.")
    return df

def flag_outliers(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    for col in ["Sales", "Profit", "Discount"]:
        Q1  = df[col].quantile(0.25)
        Q3  = df[col].quantile(0.75)
        IQR = Q3 - Q1
        lower = Q1 - 1.5 * IQR
        upper = Q3 + 1.5 * IQR
        flag_col = f"{col}_outlier"
        df[flag_col] = (df[col] < lower) | (df[col] > upper)
        count = df[flag_col].sum()
        logger.info(
            f"Outliers in '{col}': {count} rows "
            f"(bounds: [{lower:.2f}, {upper:.2f}])"
        )
    return df

def validate_discount(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    violations = ((df["Discount"] < DISCOUNT_MIN) | (df["Discount"] > DISCOUNT_MAX)).sum()
    if violations:
        logger.warning(
            f"{violations} Discount value(s) outside [0, 1]. Clipping to valid range."
        )
        df["Discount"] = df["Discount"].clip(DISCOUNT_MIN, DISCOUNT_MAX)
    else:
        logger.info("All Discount values are within valid range [0, 1].")
    return df

def standardize_categoricals(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    for col in CAT_COLS:
        if col in df.columns:
            df[col] = df[col].astype(str).str.strip().str.title()
    logger.info("Standardised casing for all categorical columns.")
    return df

def run_cleaning_pipeline(df: pd.DataFrame, save: bool = True) -> pd.DataFrame:
    logger.info("=" * 55)
    logger.info("Starting cleaning pipeline …")
    logger.info("=" * 55)

    df = parse_dates(df)
    df = check_missing(df)
    df = remove_duplicates(df)
    df = flag_outliers(df)
    df = validate_discount(df)
    df = standardize_categoricals(df)

    logger.info(f"Cleaning complete → {df.shape[0]:,} rows  ×  {df.shape[1]} columns")

    if save:
        os.makedirs(os.path.dirname(CLEAN_DATA_PATH), exist_ok=True)
        df.to_csv(CLEAN_DATA_PATH, index=False)
        logger.info(f"Cleaned data saved → {CLEAN_DATA_PATH}")

    return df
