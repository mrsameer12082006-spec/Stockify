import pandas as pd
from .sales_schema import SALES_SCHEMA


def validate_sales_schema(df):
    """Validate sales DataFrame columns and basic types.

    - ensures required columns exist
    - coerces date to datetime
    - ensures quantity is integer-like
    - ensures revenue is numeric
    """
    missing = [c for c in SALES_SCHEMA if c not in df.columns]
    if missing:
        raise ValueError(f"Missing sales columns: {missing}")

    # coerce date
    df["date"] = pd.to_datetime(df["date"], errors="coerce")
    if df["date"].isna().any():
        # show sample bad rows
        bad_idx = df[df["date"].isna()].index.tolist()[:5]
        raise ValueError(f"Invalid date values in rows: {bad_idx}")

    # quantity
    qty = pd.to_numeric(df["quantity"], errors="coerce")
    bad_qty = qty.isna() & df["quantity"].notna()
    if bad_qty.any():
        raise ValueError("Non-numeric values in 'quantity' column")
    # ensure integers (no fractional parts)
    if not (qty.dropna() % 1 == 0).all():
        raise ValueError("Fractional values present in integer 'quantity' column")
    df["quantity"] = qty.astype("Int64")

    # revenue
    rev = pd.to_numeric(df["revenue"], errors="coerce")
    bad_rev = rev.isna() & df["revenue"].notna()
    if bad_rev.any():
        raise ValueError("Non-numeric values in 'revenue' column")
    df["revenue"] = rev.astype("float64")

    # product and category: ensure string-like
    df["product"] = df["product"].astype(str).str.strip()
    df["category"] = df["category"].astype(str).str.strip()

    return True
