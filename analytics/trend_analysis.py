"""
Daily time-series aggregation.

This module handles STEP 4 of the analytics pipeline:
aggregating raw sales data to daily trend metrics.
"""

import pandas as pd


def aggregate_daily_trends(df: pd.DataFrame) -> pd.DataFrame:
    """
    Generate a daily time-series summary from raw sales data.

    INPUT:
    Expects a clean Pandas DataFrame with columns:
    - product (string)
    - date (string, format YYYY-MM-DD)
    - quantity (int > 0)
    - revenue (float)
    - category (string)

    OUTPUT:
    Returns a DataFrame with exactly these columns:
    - date (string, YYYY-MM-DD)
    - revenue (number) → total revenue for the date
    - quantity (number) → total quantity sold for the date
    - transactions (integer) → count of records for the date

    SORTING:
    - Output is sorted by date in ASCENDING order.

    ASSUMPTIONS:
    - Input DataFrame is already clean (schema validation handled by ingestion layer).
    - Date column is in YYYY-MM-DD format (no validation performed).
    - All rows are valid; no further validation performed.
    - Output is JSON-serializable (no NaN or Infinity).

    ARGS:
        df: Clean sales data DataFrame.

    RETURNS:
        Aggregated daily time-series DataFrame matching the output contract exactly.
    """
    # Group by date and aggregate metrics
    grouped = df.groupby("date", as_index=False).agg(
        revenue=("revenue", "sum"),
        quantity=("quantity", "sum"),
        transactions=("quantity", "count"),
    )

    # Sort by date in ascending order
    grouped = grouped.sort_values("date", ascending=True, ignore_index=True)

    # Ensure JSON-serializability by converting inf/NaN to safe values
    grouped = grouped.fillna(0).replace([float("inf"), float("-inf")], 0)

    return grouped


def aggregate_category_time_series(df: pd.DataFrame) -> dict:
    """
    Generate a category-level daily time-series for trend visualization.

    INPUT:
    Expects a clean Pandas DataFrame with columns:
    - product (string)
    - date (string, format YYYY-MM-DD)
    - quantity (int > 0)
    - revenue (float)
    - category (string; may be missing or empty)

    OUTPUT:
    Returns a dictionary with exactly this structure:
    {
      "categories": [<list of unique category names>],
      "data": [
        {
          "date": "YYYY-MM-DD",
          "<category_1>": revenue_value,
          "<category_2>": revenue_value,
          ...
        }
      ]
    }

    REQUIREMENTS:
    - Categories list contains unique, normalized category names (sorted alphabetically).
    - Categories normalized by trimming whitespace and replacing missing/empty with "Uncategorized".
    - Each row in `data` represents one date (sorted ascending).
    - Each category appears as a key in each data row.
    - Missing date-category combinations filled with 0.
    - Revenue values only (quantity not included).
    - Output is JSON-serializable.

    ASSUMPTIONS:
    - Input DataFrame is already clean (schema validation handled by ingestion layer).
    - Date column is in YYYY-MM-DD format (no validation performed).
    - All rows are valid; no further validation performed.
    - Output is JSON-serializable (no NaN or Infinity).

    ARGS:
        df: Clean sales data DataFrame.

    RETURNS:
        Dictionary with "categories" and "data" keys matching the output contract exactly.
    """
    # Normalize category values: trim whitespace and replace missing/empty with "Uncategorized"
    df_copy = df.copy()
    df_copy["category"] = df_copy["category"].fillna("").astype(str).str.strip()
    df_copy["category"] = df_copy["category"].replace("", "Uncategorized")

    # Group by date and category, sum revenue
    grouped = df_copy.groupby(["date", "category"], as_index=False).agg(
        revenue=("revenue", "sum")
    )

    # Get unique dates sorted ascending
    dates = sorted(df_copy["date"].unique())

    # Get unique categories sorted alphabetically
    categories = sorted(df_copy["category"].unique())

    # Create a dictionary for fast lookup: (date, category) -> revenue
    revenue_map = {}
    for _, row in grouped.iterrows():
        revenue_map[(row["date"], row["category"])] = float(row["revenue"])

    # Build data array with one row per date
    data = []
    for date in dates:
        row = {"date": date}
        # Add revenue for each category (0 if missing)
        for category in categories:
            revenue_val = revenue_map.get((date, category), 0.0)
            # Handle inf/NaN
            if pd.isna(revenue_val) or revenue_val == float("inf") or revenue_val == float("-inf"):
                revenue_val = 0.0
            row[category] = revenue_val
        data.append(row)

    result = {
        "categories": categories,
        "data": data
    }

    return result


def aggregate_top_product_time_series(df: pd.DataFrame, top_n: int = 5) -> dict:
    """
    Generate a daily time-series for top-N products based on quantity sold.

    INPUT:
    Expects a clean Pandas DataFrame with columns:
    - product (string)
    - date (string, format YYYY-MM-DD)
    - quantity (int > 0)
    - revenue (float)
    - category (string)

    OUTPUT:
    Returns a dictionary with exactly this structure:
    {
      "products": [<list of top-N product names>],
      "data": [
        {
          "date": "YYYY-MM-DD",
          "<product_1>": quantity_value,
          "<product_2>": quantity_value,
          ...
        }
      ]
    }

    REQUIREMENTS:
    - Top-N products are selected based on TOTAL quantity sold (not revenue).
    - Product list contains unique product names (sorted by total quantity DESC).
    - Each row in `data` represents one date (sorted ascending).
    - Each product appears as a key in each data row.
    - Missing date-product combinations filled with 0.
    - Quantity values only (no revenue included).
    - Output is JSON-serializable.

    ASSUMPTIONS:
    - Input DataFrame is already clean (schema validation handled by ingestion layer).
    - Date column is in YYYY-MM-DD format (no validation performed).
    - All rows are valid; no further validation performed.
    - Output is JSON-serializable (no NaN or Infinity).

    ARGS:
        df: Clean sales data DataFrame.
        top_n: Number of top products to include (default=5). Based on total quantity sold.

    RETURNS:
        Dictionary with "products" and "data" keys matching the output contract exactly.
    """
    # Compute total quantity per product
    product_totals = df.groupby("product", as_index=False).agg(
        total_quantity=("quantity", "sum")
    )

    # Sort by total quantity descending to identify top products
    product_totals = product_totals.sort_values("total_quantity", ascending=False, ignore_index=True)

    # Select top_n products
    top_products = product_totals.head(top_n)["product"].tolist()

    # Filter data to only include top products
    df_filtered = df[df["product"].isin(top_products)].copy()

    # Group by date and product, sum quantity
    grouped = df_filtered.groupby(["date", "product"], as_index=False).agg(
        quantity=("quantity", "sum")
    )

    # Get unique dates sorted ascending
    dates = sorted(df_filtered["date"].unique())

    # Create a dictionary for fast lookup: (date, product) -> quantity
    quantity_map = {}
    for _, row in grouped.iterrows():
        quantity_map[(row["date"], row["product"])] = float(row["quantity"])

    # Build data array with one row per date
    data = []
    for date in dates:
        row = {"date": date}
        # Add quantity for each product (0 if missing)
        for product in top_products:
            quantity_val = quantity_map.get((date, product), 0.0)
            # Handle inf/NaN
            if pd.isna(quantity_val) or quantity_val == float("inf") or quantity_val == float("-inf"):
                quantity_val = 0.0
            row[product] = quantity_val
        data.append(row)

    result = {
        "products": top_products,
        "data": data
    }

    return result
