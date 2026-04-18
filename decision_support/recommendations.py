import pandas as pd
from .stock_alerts import generate_stock_alerts
from .reorder_logic import generate_reorder_recommendations


def generate_recommendations(df: pd.DataFrame) -> pd.DataFrame:
    """
    Combine stock alerts with reorder suggestions
    into a final structured recommendation output.
    """

    # Generate alert dataframe
    alerts_df = generate_stock_alerts(df)

    # Generate reorder dataframe
    reorder_df = generate_reorder_recommendations(df)

    # Merge both outputs
    final_df = alerts_df.merge(
        reorder_df[["Product Name", "Suggested Reorder Quantity"]],
        on="Product Name",
        how="left"
    )

    return final_df
