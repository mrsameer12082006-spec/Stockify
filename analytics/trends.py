"""
Trends page UI - displays time-series trends for inventory and sales.
"""

import streamlit as st
import pandas as pd

from utils.helpers import format_currency
from utils.data_source_widget import render_data_source_status


def show_trends():
    """Display trends dashboard with daily trends and category time series."""
    
    results = st.session_state.get("analytics_results", {})
    
    st.markdown('<div class="page-title">📈 Trends & Analytics</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="page-subtitle">Track sales and inventory patterns over time</div>',
        unsafe_allow_html=True,
    )
    render_data_source_status(results)
    
    # Get trend data from analytics results
    daily_trends = results.get("daily_trends", pd.DataFrame())
    category_trends = results.get("category_trends", {})
    category_time_series = results.get("category_time_series", [])
    
    # ===== DAILY TRENDS CHART =====
    st.markdown('<div class="section-header">📈 Daily Sales Trend</div>', unsafe_allow_html=True)
    st.markdown('<div class="chart-container delay-1">', unsafe_allow_html=True)
    
    if not daily_trends.empty:
        # Line chart for revenue
        st.markdown("**Revenue Over Time**")
        st.line_chart(daily_trends.set_index("date")[["revenue"]] if "revenue" in daily_trends.columns else daily_trends.set_index("date"))
        
        # Additional stats
        col1, col2, col3 = st.columns(3)
        with col1:
            total_revenue = daily_trends["revenue"].sum() if "revenue" in daily_trends.columns else 0
            st.metric("Total Revenue", format_currency(total_revenue))
        with col2:
            total_quantity = daily_trends["quantity"].sum() if "quantity" in daily_trends.columns else 0
            st.metric("Total Units Sold", f"{total_quantity:,}")
        with col3:
            avg_daily_revenue = daily_trends["revenue"].mean() if "revenue" in daily_trends.columns and not daily_trends.empty else 0
            st.metric("Avg Daily Revenue", format_currency(avg_daily_revenue))
    else:
        st.markdown("""
        <div style="text-align:center; padding:40px 20px; color:#9AA0A6;">
            <div style="font-size:36px; margin-bottom:8px;">📭</div>
            <div style="font-size:13px;">Upload sales data to see trends</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown("<div style='height:32px'></div>", unsafe_allow_html=True)
    
    # ===== QUANTITY TRENDS =====
    st.markdown('<div class="section-header">📊 Sales Volume Trend</div>', unsafe_allow_html=True)
    st.markdown('<div class="chart-container delay-2">', unsafe_allow_html=True)
    
    if not daily_trends.empty and "quantity" in daily_trends.columns:
        st.bar_chart(daily_trends.set_index("date")[["quantity"]])
    else:
        st.info("No quantity data available")
    
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown("<div style='height:32px'></div>", unsafe_allow_html=True)
    
    # ===== CATEGORY TRENDS =====
    if category_time_series and len(category_time_series) > 0:
        st.markdown('<div class="section-header">🏷️ Category Performance Over Time</div>', unsafe_allow_html=True)
        st.markdown('<div class="chart-container delay-3">', unsafe_allow_html=True)
        
        # Convert to dataframe for easier visualization
        category_data = pd.DataFrame(category_time_series)
        
        if not category_data.empty and "date" in category_data.columns:
            # Get category columns (all except date)
            category_cols = [col for col in category_data.columns if col != "date"]
            
            if category_cols:
                display_df = category_data.set_index("date")[category_cols]
                st.line_chart(display_df)
        else:
            st.info("No category trend data available")
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown("<div style='height:32px'></div>", unsafe_allow_html=True)
    
    # ===== DATA TABLE =====
    with st.expander("📋 View Raw Trend Data"):
        if not daily_trends.empty:
            st.dataframe(daily_trends, use_container_width=True)
        else:
            st.info("No trend data available yet")
