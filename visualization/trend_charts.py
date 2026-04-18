import streamlit as st
import pandas as pd
import plotly.express as px


def plot_sales_trend(trend_df, chart_key="sales_trend_chart"):
    """
    Visualizes sales trend over time with an interactive line chart (Plotly).
    
    Accepts DataFrame with:
    - date
    - quantity (or total_quantity)
    - revenue (optional)
    
    Args:
        trend_df: DataFrame with date and quantity/revenue columns
        chart_key: Unique key for the Plotly chart (default: "sales_trend_chart")
    
    Safety:
    - Checks for None and empty DataFrame
    - Validates required columns exist
    - Handles date conversion gracefully
    - Graceful error handling
    """
    
    # Safety check 1: None or empty
    if trend_df is None or trend_df.empty:
        st.info(" No trend data available for visualization")
        return
    
    try:
        st.markdown("###  Sales Trend")
        st.caption("Daily sales movement to understand demand patterns over time")
        
        # Safety check 2: Column validation
        date_col = "date"
        quantity_cols = ["quantity", "total_quantity"]
        quantity_col = next((col for col in quantity_cols if col in trend_df.columns), None)
        
        if date_col not in trend_df.columns or quantity_col is None:
            st.warning(f" Expected columns not found. Available: {trend_df.columns.tolist()}")
            return
        
        # Prepare data
        plot_df = trend_df[[date_col, quantity_col]].copy()
        
        # Safety check 3: Date conversion
        try:
            plot_df[date_col] = pd.to_datetime(plot_df[date_col])
        except Exception:
            st.warning(" Could not parse dates. Proceeding with raw date values.")
        
        plot_df = plot_df.sort_values(date_col)
        
        # Create interactive line chart with Plotly
        fig = px.line(
            plot_df,
            x=date_col,
            y=quantity_col,
            title="Daily Sales Trend",
            labels={
                date_col: "Date",
                quantity_col: "Quantity Sold (Units)"
            },
            markers=True,
            line_shape="linear",
            hover_data={
                date_col: True,
                quantity_col: ":.0f"
            }
        )
        
        # Professional layout
        fig.update_traces(
            marker=dict(
                size=8,
                color="#1f77b4",
                line=dict(width=2, color="white")
            ),
            line=dict(width=3, color="#1f77b4"),
            hovertemplate="<b>%{x|%Y-%m-%d}</b><br>Quantity: %{y:,.0f} units<extra></extra>"
        )
        
        fig.update_layout(
            xaxis_title="Date",
            yaxis_title="Quantity Sold (Units)",
            template="plotly_white",
            hovermode="x unified",
            height=450,
            margin=dict(l=50, r=50, t=80, b=80),
            font=dict(size=11, family="Arial"),
            showlegend=False,
            xaxis=dict(
                tickformat="%Y-%m-%d",
                tickmode="auto",
                nticks=10
            )
        )
        
        st.plotly_chart(fig, use_container_width=True, key=chart_key)
        
    except Exception as e:
        st.error(f" Error generating sales trend chart: {str(e)}")