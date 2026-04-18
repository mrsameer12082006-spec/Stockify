import pandas as pd

# -----------------------------
# MOCK KPI DATA
# -----------------------------
mock_kpi_data = {
    "total_products": 25,
    "total_sales_quantity": 1420,
    "top_selling_product": "Rice",
    "low_stock_count": 3
}


# -----------------------------
# MOCK PRODUCT DEMAND DATA
# -----------------------------
mock_demand_df = pd.DataFrame({
    "product_name": [
        "Rice", "Wheat", "Sugar", "Oil",
        "Salt", "Tea", "Coffee", "Biscuits"
    ],
    "total_sales": [
        420, 300, 180, 160,
        140, 90, 80, 50
    ]
})

# -----------------------------
# MOCK SALES TREND DATA
# -----------------------------
mock_trend_df = pd.DataFrame({
    "date": pd.date_range(start="2025-01-01", periods=10, freq="D"),
    "total_quantity": [120, 135, 128, 150, 170, 160, 155, 180, 175, 190]
})

# -----------------------------
# MOCK ALERT DATA
# -----------------------------
mock_alert_df = pd.DataFrame({
    "product_name": ["Oil", "Coffee", "Biscuits"],
    "alert_type": ["LOW_STOCK", "LOW_STOCK", "OVERSTOCK"],
    "message": [
        "Stock below reorder level",
        "Stock critically low",
        "Sales very slow, consider reducing order"
    ]
})

