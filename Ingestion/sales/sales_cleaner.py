import pandas as pd


def clean_sales(df: pd.DataFrame) -> pd.DataFrame:
    """Perform lightweight cleaning for sales data."""
    df = df.copy()

    # Trim strings
    for col in ["product", "category"]:
        if col in df.columns:
            df[col] = df[col].astype(str).str.strip()

    # Fill missing numeric with sensible defaults
    if "quantity" in df.columns:
        df["quantity"] = pd.to_numeric(df["quantity"], errors="coerce").fillna(0).astype("Int64")

    if "revenue" in df.columns:
        df["revenue"] = pd.to_numeric(df["revenue"], errors="coerce").fillna(0.0).astype("float64")

    # Ensure date is datetime
    if "date" in df.columns:
        df["date"] = pd.to_datetime(df["date"], errors="coerce")

    # Drop exact duplicate rows
    df = df.drop_duplicates()

    return df
