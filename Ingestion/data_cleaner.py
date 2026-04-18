# ingestion/cleaner.py

import pandas as pd


def clean_data(df):
    """
    Clean dataset:
    - Drop duplicates
    - Handle missing values
    - Trim strings
    """

    # Remove duplicates and operate on a copy to avoid SettingWithCopyWarning
    df = df.drop_duplicates().copy()

    # Trim string columns
    string_cols = ["Product ID", "Product Name", "Category"]
    for col in string_cols:
        df[col] = df[col].astype(str).str.strip()

    # Coerce numeric columns to appropriate numeric dtypes and fill missing values
    int_cols = ["Quantity On Hand", "Reorder Point"]
    float_cols = ["Unit Cost", "Selling Price"]

    for col in int_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")
            df[col] = df[col].fillna(0).astype("Int64")

    for col in float_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")
            df[col] = df[col].fillna(0.0).astype("float64")

    # Drop rows with missing critical identifiers
    df = df.dropna(subset=["Product ID", "Product Name"])

    return df
