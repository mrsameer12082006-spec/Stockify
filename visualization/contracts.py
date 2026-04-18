"""
Visualization Data Contracts
----------------------------

This file defines the expected input formats for the visualization layer.
All analytics and decision-support modules must conform to these contracts.
"""

# KPI CONTRACT
# Dictionary format expected by KPI cards
KPI_CONTRACT = {
    "total_products": int,
    "total_sales_quantity": int,
    "top_selling_product": str,
    "low_stock_count": int
}


# PRODUCT DEMAND CONTRACT
# DataFrame columns expected for demand charts
PRODUCT_DEMAND_COLUMNS = [
    "product_name",
    "total_sales"
]

# SALES TREND CONTRACT
# DataFrame columns expected for trend charts
SALES_TREND_COLUMNS = [
    "date",
    "total_quantity"
]

# ALERTS CONTRACT
# DataFrame columns expected for alert visuals
ALERT_COLUMNS = [
    "product_name",
    "alert_type",      # e.g. LOW_STOCK / OVERSTOCK
    "message"
]