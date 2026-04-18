"""
Product-level demand analysis aggregation.

This module handles STEP 1 of the analytics pipeline:
aggregating raw sales data to product-level metrics.
"""

import pandas as pd


def aggregate_product_demand(df: pd.DataFrame) -> pd.DataFrame:
    """
    Aggregate raw sales data to product-level demand metrics.

    INPUT:
    Expects a clean Pandas DataFrame with columns:
    - product (string, non-empty)
    - date (string, format YYYY-MM-DD)
    - quantity (int > 0)
    - revenue (float)
    - category (string; may be missing or empty)

    OUTPUT:
    Returns a DataFrame with exactly these columns:
    - product (string)
    - category (string; defaults to "Uncategorized" if missing/empty)
    - totalQuantity (number) → sum of quantity per product
    - totalRevenue (number) → sum of revenue per product
    - salesCount (integer) → count of records per product
    - avgQuantityPerSale (float) → totalQuantity / salesCount

    CATEGORY HANDLING:
    - Per product, uses the first non-empty category value.
    - If all category values for a product are missing/empty, defaults to "Uncategorized".

    ASSUMPTIONS:
    - Input DataFrame is already clean (schema validation handled by ingestion layer).
    - All rows are valid; no further validation performed.
    - Output is JSON-serializable (no NaN or Infinity).

    ARGS:
        df: Clean sales data DataFrame.

    RETURNS:
        Aggregated product-level DataFrame matching the output contract exactly.
    """
    # Group by product and aggregate metrics
    grouped = df.groupby("product", as_index=False).agg(
        totalQuantity=("quantity", "sum"),
        totalRevenue=("revenue", "sum"),
        salesCount=("quantity", "count"),
        category=("category", lambda x: _get_first_valid_category(x)),
    )

    # Calculate average quantity per sale
    grouped["avgQuantityPerSale"] = grouped["totalQuantity"] / grouped["salesCount"]

    # Reorder columns to match output contract
    result = grouped[["product", "category", "totalQuantity", "totalRevenue", "salesCount", "avgQuantityPerSale"]]

    # Ensure JSON-serializability by converting inf/NaN to safe values
    result = result.fillna(0).replace([float("inf"), float("-inf")], 0)

    return result


def aggregate_category_demand(df: pd.DataFrame) -> pd.DataFrame:
    """
    Aggregate raw sales data to category-level demand metrics.

    INPUT:
    Expects a clean Pandas DataFrame with columns:
    - product (string, non-empty)
    - date (string, format YYYY-MM-DD)
    - quantity (int > 0)
    - revenue (float)
    - category (string; may be missing or empty)

    OUTPUT:
    Returns a DataFrame with exactly these columns:
    - category (string)
    - revenue (number) → sum of revenue per category
    - quantity (number) → sum of quantity per category

    CATEGORY HANDLING:
    - Normalizes category values by trimming whitespace.
    - Replaces missing, empty, or whitespace-only values with "Uncategorized".
    - Groups all normalized categories together.

    SORTING:
    - Output is sorted by revenue in DESCENDING order.

    ASSUMPTIONS:
    - Input DataFrame is already clean (schema validation handled by ingestion layer).
    - All rows are valid; no further validation performed.
    - Output is JSON-serializable (no NaN or Infinity).

    ARGS:
        df: Clean sales data DataFrame.

    RETURNS:
        Aggregated category-level DataFrame matching the output contract exactly.
    """
    # Normalize category values: trim whitespace and replace missing/empty with "Uncategorized"
    df_copy = df.copy()
    df_copy["category"] = df_copy["category"].fillna("").astype(str).str.strip()
    df_copy["category"] = df_copy["category"].replace("", "Uncategorized")

    # Group by category and aggregate metrics
    grouped = df_copy.groupby("category", as_index=False).agg(
        revenue=("revenue", "sum"),
        quantity=("quantity", "sum"),
    )

    # Sort by revenue in descending order
    grouped = grouped.sort_values("revenue", ascending=False, ignore_index=True)

    # Ensure JSON-serializability by converting inf/NaN to safe values
    grouped = grouped.fillna(0).replace([float("inf"), float("-inf")], 0)

    return grouped


def aggregate_top_products(df: pd.DataFrame, top_n: int = 5) -> pd.DataFrame:
    """
    Generate a top-N products summary based on revenue.

    INPUT:
    Expects a clean Pandas DataFrame with columns:
    - product (string, non-empty)
    - date (string, format YYYY-MM-DD)
    - quantity (int > 0)
    - revenue (float)
    - category (string)

    OUTPUT:
    Returns a DataFrame with exactly these columns:
    - product (string)
    - revenue (number) → total revenue per product
    - quantity (number) → total quantity per product

    LIMITING:
    - Output is sorted by revenue in DESCENDING order.
    - Returns the top `top_n` products by revenue.
    - If fewer than `top_n` products exist, returns all products.

    ASSUMPTIONS:
    - Input DataFrame is already clean (schema validation handled by ingestion layer).
    - All rows are valid; no further validation performed.
    - Output is JSON-serializable (no NaN or Infinity).

    ARGS:
        df: Clean sales data DataFrame.
        top_n: Number of top products to return (default=5). If fewer products exist, returns all.

    RETURNS:
        Aggregated top-N products DataFrame matching the output contract exactly.
    """
    # Group by product and aggregate revenue and quantity
    grouped = df.groupby("product", as_index=False).agg(
        revenue=("revenue", "sum"),
        quantity=("quantity", "sum"),
    )

    # Sort by revenue in descending order
    grouped = grouped.sort_values("revenue", ascending=False, ignore_index=True)

    # Limit to top_n products
    grouped = grouped.head(top_n)

    # Ensure JSON-serializability by converting inf/NaN to safe values
    grouped = grouped.fillna(0).replace([float("inf"), float("-inf")], 0)

    return grouped


def _get_first_valid_category(categories: pd.Series) -> str:
    """
    Extract the first non-empty category from a Series.

    If all values are None, NaN, or empty strings, returns "Uncategorized".

    ARGS:
        categories: Pandas Series of category values.

    RETURNS:
        First valid category string, or "Uncategorized" as default.
    """
    for value in categories:
        # Check for non-null and non-empty string
        if pd.notna(value) and str(value).strip():
            return str(value).strip()
    return "Uncategorized"
