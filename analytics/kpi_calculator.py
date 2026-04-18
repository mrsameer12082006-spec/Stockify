"""
High-level inventory KPI computation.

This module handles STEP 7 of the analytics pipeline:
computing high-level inventory KPIs from raw sales data.
"""

import pandas as pd


def compute_kpi_summary(df: pd.DataFrame) -> dict:
    """
    Compute high-level inventory KPIs from raw sales data.
              
    INPUT:
    Expects a clean Pandas DataFrame with columns:
    - product (string)
    - date (string, format YYYY-MM-DD)
    - quantity (int > 0)
    - revenue (float)
    - category (string)

    OUTPUT:
    Returns a dictionary with exactly these keys:
    {
      "total_products": int,
      "total_sales_quantity": int,
      "top_selling_product": string,
      "slow_moving_count": int
    }

    KPI DEFINITIONS:
    - total_products: Count of unique products.
    - total_sales_quantity: Sum of quantity across all records.
    - top_selling_product: Product with highest total quantity sold.
    - slow_moving_count: Number of products whose total quantity is below
                         the average total quantity per product.

    EDGE CASES:
    - Empty DataFrame: Returns total_products=0, total_sales_quantity=0,
                       top_selling_product="", slow_moving_count=0.

    ASSUMPTIONS:
    - Input DataFrame is already clean (schema validation handled by ingestion layer).
    - All rows are valid; no further validation performed.
    - Output is JSON-serializable (no NaN or Infinity).

    ARGS:
        df: Clean sales data DataFrame.

    RETURNS:
        Dictionary matching the output contract exactly.
    """
    # Handle empty DataFrame
    if df.empty:
        return {
            "total_products": 0,
            "total_sales_quantity": 0,
            "top_selling_product": "",
            "slow_moving_count": 0
        }

    # Compute per-product total quantity
    product_quantities = df.groupby("product", as_index=False).agg(
        total_quantity=("quantity", "sum")
    )

    # total_products: count of unique products
    total_products = len(product_quantities)

    # total_sales_quantity: sum of all quantities
    total_sales_quantity = int(product_quantities["total_quantity"].sum())

    # top_selling_product: product with highest total quantity
    top_product_row = product_quantities.loc[product_quantities["total_quantity"].idxmax()]
    top_selling_product = str(top_product_row["product"])

    # Calculate average quantity per product
    avg_quantity_per_product = product_quantities["total_quantity"].mean()

    # slow_moving_count: number of products below average quantity
    slow_moving_count = int((product_quantities["total_quantity"] < avg_quantity_per_product).sum())

    result = {
        "total_products": total_products,
        "total_sales_quantity": total_sales_quantity,
        "top_selling_product": top_selling_product,
        "slow_moving_count": slow_moving_count
    }

    return result
