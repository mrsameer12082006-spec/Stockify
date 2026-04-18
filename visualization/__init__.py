"""
Visualization module for Stockify.
Modern interactive charts using Plotly Express.

Functions:
- render_kpi_cards(): Display key metrics
- plot_top_products(): Interactive bar chart (Plotly)
- plot_sales_trend(): Interactive line chart (Plotly)
- show_alerts(): Alert table with risk highlighting
"""

from .alert_visuals import show_alerts
from .demand_charts import plot_top_products
from .trend_charts import plot_sales_trend
from .kpi_cards import render_kpi_cards

__all__ = [
    "show_alerts",
    "plot_top_products",
    "plot_sales_trend",
    "render_kpi_cards",
]
