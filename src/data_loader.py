import logging
import pandas as pd

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from config import RAW_DATA_PATH, ENCODING, EXPECTED_COLUMNS

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s  [%(levelname)s]  %(name)s — %(message)s",
    datefmt="%H:%M:%S",
)
logger = logging.getLogger(__name__)


def load_raw_data(path: str = RAW_DATA_PATH) -> pd.DataFrame:
    if not os.path.exists(path):
        raise FileNotFoundError(
            f"Raw data not found at '{path}'. "
            "Place superstore.csv in data/raw/ before running."
        )

    logger.info(f"Loading raw data from: {path}")

    df = pd.read_csv(path, encoding=ENCODING)

    logger.info(f"Loaded  → {df.shape[0]:,} rows  ×  {df.shape[1]} columns")
    logger.info(
        f"Memory  → {df.memory_usage(deep=True).sum() / 1024:.1f} KB"
    )

    validate_schema(df)
    return df

def validate_schema(df: pd.DataFrame) -> None:
    missing = [c for c in EXPECTED_COLUMNS if c not in df.columns]
    if missing:
        raise ValueError(
            f"Schema validation failed. Missing columns: {missing}\n"
            f"Found columns: {list(df.columns)}"
        )
    logger.info("Schema validation passed — all 21 columns present.")

def get_data_summary(df: pd.DataFrame) -> dict:
    return {
        "rows":       df.shape[0],
        "columns":    df.shape[1],
        "null_total": int(df.isnull().sum().sum()),
        "duplicates": int(df.duplicated().sum()),
        "dtypes":     df.dtypes.astype(str).to_dict(),
    }
