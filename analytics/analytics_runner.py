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
    
    try:
        # Try to load processed data (support both Ingestion/ingestion casing)
        ingestion_candidates = [
            project_root / "Ingestion" / "data" / "processed",
            project_root / "ingestion" / "data" / "processed",
        ]
        ingestion_path = next((p for p in ingestion_candidates if p.exists()), ingestion_candidates[0])
        
        inventory_file = ingestion_path / "inventory_cleaned.csv"
        sales_file = ingestion_path / "sales_cleaned.csv"
        
        inventory_df = None
        sales_df = None
        
        # Load inventory if available
        if inventory_file.exists():
            try:
                inventory_df = pd.read_csv(inventory_file)
                results["inventory_df"] = inventory_df
            except Exception as e:
                print(f"Warning: Could not load inventory file: {e}")
                results["inventory_df"] = None
        else:
            results["inventory_df"] = None
        
        # Load sales if available
        if sales_file.exists():
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
                "kpis": {},
                "stock_recommendations": pd.DataFrame()
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
            "kpis": {},
            "stock_recommendations": pd.DataFrame()
        }
