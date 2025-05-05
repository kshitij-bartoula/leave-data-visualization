import pandas as pd
from typing import List, Optional

class DataProcessor:
    @staticmethod
    def filter_data(df: pd.DataFrame, column: str, value: str) -> pd.DataFrame:
        if df is None or df.empty:
            print(f"[Warning] DataFrame is empty or None.")
            return pd.DataFrame()
        if column not in df.columns:
            print(f"[Warning] Column '{column}' not found in DataFrame.")
            return df  # or return pd.DataFrame() depending on your use case
        return df if value == "All" else df[df[column] == value]

    @staticmethod
    def validate_data(df: pd.DataFrame, required_cols: List[str]) -> bool:
        if df is None:
            print("[Warning] DataFrame is None.")
            return False
        missing_cols = [col for col in required_cols if col not in df.columns]
        if missing_cols:
            print(f"[Warning] Missing columns: {missing_cols}")
            return False
        return True
