"""
Analytics runner orchestrator - combines all analytics modules into a single result set.
This module runs the complete analytics pipeline when data is loaded.
"""

import pandas as pd
from pathlib import Path
import sys

# Ensure imports work
project_root = Path(__file__).resolve().parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

# Import all analytics modules
from analytics.demand_analysis import (
    aggregate_product_demand,
    aggregate_category_demand,
    aggregate_top_products
)
from analytics.trend_analysis import (
    aggregate_daily_trends,
    aggregate_category_time_series
)
from analytics.kpi_calculator import compute_kpi_summary
from decision_support.recommendations import generate_recommendations


def run_analytics() -> dict:
    """
    Run complete analytics pipeline and return consolidated results.
    
    This function:
    1. Loads inventory and sales data from processed files
    2. Runs all analytics aggregations
    3. Generates recommendations and alerts
    4. Returns all results as a single dictionary
    
    Returns:
        Dictionary with keys:
        - inventory_df: Cleaned inventory data
        - sales_df: Cleaned sales data
        - product_demand: Product-level aggregations
        - category_demand: Category-level aggregations
        - top_products: Top N products by revenue
        - daily_trends: Time-series trends
        - category_trends: Category-level trends (dict)
        - category_time_series: Category time-series (list)
        - kpis: High-level KPI summary
        - stock_recommendations: Combined alerts and reorder suggestions
    """
    
    results = {}

    def _zero_kpis() -> dict:
        return {
            "total_products": 0,
            "total_sales_quantity": 0,
            "top_selling_product": "",
            "slow_moving_count": 0,
        }

    def _pick_latest_available_file(candidates: list[Path]) -> Optional[Path]:
        existing = [p for p in candidates if p.exists()]
        if not existing:
            return None
        return max(existing, key=lambda p: p.stat().st_mtime_ns)

    def _source_label(file_path: Optional[Path]) -> str:
        if file_path is None:
            return "No data"
        path_str = str(file_path).replace("\\", "/").lower()
        if "/pos/" in path_str or path_str.endswith("clean_sales.csv") or path_str.endswith("clean_inventory.csv"):
            return "POS / canonical"
        if "/ingestion/" in path_str or "/ingestion" in path_str:
            return "Ingestion"
        return "Unknown"
    
    try:
        # Resolve data files from both POS and ingestion outputs.
        # We always pick the latest modified available file so uploads and POS
        # updates are reflected dynamically across all analytics pages.
        inventory_candidates = [
            project_root / "data" / "processed" / "clean_inventory.csv",
            project_root / "Ingestion" / "data" / "processed" / "inventory_cleaned.csv",
            project_root / "ingestion" / "data" / "processed" / "inventory_cleaned.csv",
        ]
        sales_candidates = [
            project_root / "data" / "processed" / "clean_sales.csv",
            project_root / "Ingestion" / "data" / "processed" / "sales_cleaned.csv",
            project_root / "ingestion" / "data" / "processed" / "sales_cleaned.csv",
        ]

        inventory_file = _pick_latest_available_file(inventory_candidates)
        sales_file = _pick_latest_available_file(sales_candidates)
        
        inventory_df = None
        sales_df = None
        
        # Load inventory if available
        if inventory_file and inventory_file.exists():
            try:
                inventory_df = pd.read_csv(inventory_file)
                results["inventory_df"] = inventory_df
            except Exception as e:
                print(f"Warning: Could not load inventory file: {e}")
                results["inventory_df"] = None
        else:
            results["inventory_df"] = None
        
        # Load sales if available
        if sales_file and sales_file.exists():
            try:
                sales_df = pd.read_csv(sales_file)
                results["sales_df"] = sales_df
            except Exception as e:
                print(f"Warning: Could not load sales file: {e}")
                results["sales_df"] = None
        else:
            results["sales_df"] = None
        
        # If no data, return empty results
        if sales_df is None or sales_df.empty:
            return {
                "inventory_df": inventory_df or pd.DataFrame(),
                "sales_df": sales_df or pd.DataFrame(),
                "product_demand": pd.DataFrame(),
                "category_demand": pd.DataFrame(),
                "top_products": pd.DataFrame(),
                "daily_trends": pd.DataFrame(),
                "category_trends": {},
                "category_time_series": [],
                "kpis": _zero_kpis(),
                "stock_recommendations": pd.DataFrame(),
                "data_sources": {
                    "inventory": {"path": str(inventory_file) if inventory_file else "", "label": _source_label(inventory_file)},
                    "sales": {"path": str(sales_file) if sales_file else "", "label": _source_label(sales_file)},
                },
            }
        
        # ===== RUN ANALYTICS ON SALES DATA =====
        
        # 1. Demand Analysis
        try:
            product_demand = aggregate_product_demand(sales_df)
            results["product_demand"] = product_demand
        except Exception as e:
            print(f"Error in product demand analysis: {e}")
            results["product_demand"] = pd.DataFrame()
        
        try:
            category_demand = aggregate_category_demand(sales_df)
            results["category_demand"] = category_demand
        except Exception as e:
            print(f"Error in category demand analysis: {e}")
            results["category_demand"] = pd.DataFrame()
        
        try:
            top_products = aggregate_top_products(sales_df, top_n=5)
            results["top_products"] = top_products
        except Exception as e:
            print(f"Error in top products analysis: {e}")
            results["top_products"] = pd.DataFrame()
        
        # 2. Trend Analysis
        try:
            daily_trends = aggregate_daily_trends(sales_df)
            results["daily_trends"] = daily_trends
        except Exception as e:
            print(f"Error in daily trends analysis: {e}")
            results["daily_trends"] = pd.DataFrame()
        
        try:
            category_trends = aggregate_category_time_series(sales_df)
            results["category_trends"] = category_trends if category_trends else {}
            
            # Also store as list format for charting
            if isinstance(category_trends, dict) and "data" in category_trends:
                results["category_time_series"] = category_trends["data"]
            else:
                results["category_time_series"] = []
        except Exception as e:
            print(f"Error in category time series analysis: {e}")
            results["category_trends"] = {}
            results["category_time_series"] = []
        
        # 3. KPI Calculation
        try:
            kpi_summary = compute_kpi_summary(sales_df)
            results["kpis"] = kpi_summary
        except Exception as e:
            print(f"Error in KPI calculation: {e}")
            results["kpis"] = {}
        
        # ===== DECISION SUPPORT =====
        
        # 4. Generate Stock Recommendations (requires inventory data)
        if inventory_df is not None and not inventory_df.empty:
            try:
                stock_recommendations = generate_recommendations(inventory_df)
                results["stock_recommendations"] = stock_recommendations
            except Exception as e:
                print(f"Error in generating recommendations: {e}")
                results["stock_recommendations"] = pd.DataFrame()
        else:
            results["stock_recommendations"] = pd.DataFrame()
        
        results["data_sources"] = {
            "inventory": {"path": str(inventory_file) if inventory_file else "", "label": _source_label(inventory_file)},
            "sales": {"path": str(sales_file) if sales_file else "", "label": _source_label(sales_file)},
        }

        return results
        
    except Exception as e:
        print(f"Critical error in analytics runner: {e}")
        return {
            "inventory_df": pd.DataFrame(),
            "sales_df": pd.DataFrame(),
            "product_demand": pd.DataFrame(),
            "category_demand": pd.DataFrame(),
            "top_products": pd.DataFrame(),
            "daily_trends": pd.DataFrame(),
            "category_trends": {},
            "category_time_series": [],
            "kpis": _zero_kpis(),
            "stock_recommendations": pd.DataFrame(),
            "data_sources": {
                "inventory": {"path": "", "label": "No data"},
                "sales": {"path": "", "label": "No data"},
            },
        }
