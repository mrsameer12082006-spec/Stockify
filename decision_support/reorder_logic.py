import pandas as pd


def generate_reorder_recommendations(df: pd.DataFrame) -> pd.DataFrame:
    """
    Generate reorder quantity suggestions based on stock gap.
    """

    required_cols = {
        "Product Name",
        "Quantity On Hand",
        "Reorder Point"
    }

    if not required_cols.issubset(df.columns):
        raise ValueError("Inventory DataFrame missing required columns.")

    recommendations = []

    for _, row in df.iterrows():
        product = row["Product Name"]
        stock = row["Quantity On Hand"]
        reorder_point = row["Reorder Point"]

        if stock <= reorder_point:
            suggested_qty = (reorder_point * 2) - stock
        else:
            suggested_qty = 0

        recommendations.append({
            "Product Name": product,
            "Current Stock": stock,
            "Reorder Point": reorder_point,
            "Suggested Reorder Quantity": max(int(suggested_qty), 0)
        })

    return pd.DataFrame(recommendations)
