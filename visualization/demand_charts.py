import streamlit as st
import pandas as pd
import plotly.express as px


def plot_top_products(demand_df, chart_key="top_products_chart"):
    """
    Visualizes top products using an interactive bar chart with Plotly.
    
    Accepts DataFrame with:
    - product (or product_name)
    - revenue (or total_sales, total_revenue)
    - quantity (optional)
    
    Args:
        demand_df: DataFrame with product and revenue columns
        chart_key: Unique key for the Plotly chart (default: "top_products_chart")
    
    Safety:
    - Checks for None and empty DataFrame
    - Validates required columns exist
    - Graceful error handling
    """
    
    # Safety check 1: None or empty
    if demand_df is None or demand_df.empty:
        st.info(" No product data available for visualization")
        return
    
    try:
        st.markdown("###  Top Products")
        st.caption("Product-wise sales performance to identify fast and slow movers")
        
        # Safety check 2: Column validation
        product_col = "product" if "product" in demand_df.columns else "product_name"
        revenue_cols = ["revenue", "total_revenue", "total_sales"]
        revenue_col = next((col for col in revenue_cols if col in demand_df.columns), None)
        
        if product_col not in demand_df.columns or revenue_col is None:
            st.warning(f" Expected columns not found. Available: {demand_df.columns.tolist()}")
            return
        
        # Prepare data
        plot_df = demand_df[[product_col, revenue_col]].copy()
        plot_df = plot_df.sort_values(revenue_col, ascending=False)
        plot_df[product_col] = plot_df[product_col].astype(str)
        
        # Create interactive bar chart with Plotly
        fig = px.bar(
            plot_df,
            x=product_col,
            y=revenue_col,
            title="Top Selling Products by Revenue",
            labels={
                product_col: "Product",
                revenue_col: "Revenue (₹)"
            },
            text=revenue_col,
            color=revenue_col,
            color_continuous_scale="Blues",
            hover_data={
                product_col: True,
                revenue_col: ":.2f"
            }
        )
        
        # Professional layout
        fig.update_traces(
            textposition="outside",
            texttemplate="₹ %{text:,.0f}",
            hovertemplate="<b>%{x}</b><br>Revenue: ₹%{y:,.2f}<extra></extra>"
        )
        
        fig.update_layout(
            xaxis_title="Product",
            yaxis_title="Revenue (₹)",
            template="plotly_white",
            hovermode="x unified",
            height=450,
            margin=dict(l=50, r=50, t=80, b=80),
            font=dict(size=11, family="Arial"),
            showlegend=False,
            coloraxis_showscale=False
        )
        
        st.plotly_chart(fig, use_container_width=True, key=chart_key)
        
    except Exception as e:
        st.error(f" Error generating product demand chart: {str(e)}")