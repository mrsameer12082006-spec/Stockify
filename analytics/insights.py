"""
Insights page UI - displays actionable recommendations and stock alerts.
"""

import streamlit as st
import pandas as pd

from utils.helpers import format_currency
from utils.data_source_widget import render_data_source_status


def show_insights():
    """Display actionable insights including stock alerts and recommendations."""
    
    results = st.session_state.get("analytics_results", {})
    
    st.markdown('<div class="page-title">💡 Smart Insights & Recommendations</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="page-subtitle">AI-powered recommendations to optimize your inventory</div>',
        unsafe_allow_html=True,
    )
    render_data_source_status(results)
    
    # Get recommendation data from analytics results
    stock_recommendations = results.get("stock_recommendations", pd.DataFrame())
    
    if stock_recommendations.empty:
        st.markdown("""
        <div style="text-align:center; padding:60px 20px; color:#9AA0A6;">
            <div style="font-size:44px; margin-bottom:10px;">🤔</div>
            <div style="font-size:15px; font-weight:600; color:#5F6368; margin-bottom:4px;">No Insights Available Yet</div>
            <div style="font-size:12px;">Upload inventory and sales data to get personalized recommendations</div>
        </div>
        """, unsafe_allow_html=True)
        return
    
    # ===== ALERT SUMMARY CARDS =====
    st.markdown('<div class="section-header">🚨 Stock Health Overview</div>', unsafe_allow_html=True)
    
    low_stock_count = len(stock_recommendations[stock_recommendations["Alert Type"] == "Low Stock"]) if "Alert Type" in stock_recommendations.columns else 0
    overstock_count = len(stock_recommendations[stock_recommendations["Alert Type"] == "Overstock"]) if "Alert Type" in stock_recommendations.columns else 0
    healthy_count = len(stock_recommendations[stock_recommendations["Alert Type"] == "Healthy"]) if "Alert Type" in stock_recommendations.columns else 0
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown(f"""
        <div class="glass-card" style="text-align:center; padding:20px 16px; background:rgba(217,48,37,0.06);">
            <div style="font-size:28px; margin-bottom:4px;">🔴</div>
            <div style="font-size:20px; font-weight:700; color:#D93025;">{low_stock_count}</div>
            <div style="font-size:11px; color:#5F6368; text-transform:uppercase; letter-spacing:1px; font-weight:600;">Low Stock Items</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="glass-card" style="text-align:center; padding:20px 16px; background:rgba(249,171,0,0.06);">
            <div style="font-size:28px; margin-bottom:4px;">📦</div>
            <div style="font-size:20px; font-weight:700; color:#F9AB00;">{overstock_count}</div>
            <div style="font-size:11px; color:#5F6368; text-transform:uppercase; letter-spacing:1px; font-weight:600;">Overstock Items</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="glass-card" style="text-align:center; padding:20px 16px; background:rgba(30,142,62,0.06);">
            <div style="font-size:28px; margin-bottom:4px;">✅</div>
            <div style="font-size:20px; font-weight:700; color:#1E8E3E;">{healthy_count}</div>
            <div style="font-size:11px; color:#5F6368; text-transform:uppercase; letter-spacing:1px; font-weight:600;">Healthy Items</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<div style='height:32px'></div>", unsafe_allow_html=True)
    
    # ===== INSIGHTS BY CATEGORY =====
    if "Alert Type" in stock_recommendations.columns:
        # Low Stock Items - Priority 1
        low_stock_items = stock_recommendations[stock_recommendations["Alert Type"] == "Low Stock"]
        if not low_stock_items.empty:
            st.markdown('<div class="section-header">⚠️ Critical Action Required - Low Stock Items</div>', unsafe_allow_html=True)
            st.markdown('<div class="chart-container">', unsafe_allow_html=True)
            st.dataframe(
                low_stock_items[["Product Name", "Current Stock", "Reorder Point", "Recommendation"]] 
                if "Product Name" in low_stock_items.columns 
                else low_stock_items,
                use_container_width=True,
                hide_index=True
            )
            st.markdown('</div>', unsafe_allow_html=True)
            st.markdown("<div style='height:20px'></div>", unsafe_allow_html=True)
        
        # Overstock Items
        overstock_items = stock_recommendations[stock_recommendations["Alert Type"] == "Overstock"]
        if not overstock_items.empty:
            st.markdown('<div class="section-header">📦 Optimization Opportunity - Overstock Items</div>', unsafe_allow_html=True)
            st.markdown('<div class="chart-container">', unsafe_allow_html=True)
            st.dataframe(
                overstock_items[["Product Name", "Current Stock", "Reorder Point", "Recommendation"]] 
                if "Product Name" in overstock_items.columns 
                else overstock_items,
                use_container_width=True,
                hide_index=True
            )
            st.markdown('</div>', unsafe_allow_html=True)
            st.markdown("<div style='height:20px'></div>", unsafe_allow_html=True)
    
    # ===== FULL RECOMMENDATIONS TABLE =====
    st.markdown('<div class="section-header">📋 Complete Stock Analysis</div>', unsafe_allow_html=True)
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    st.dataframe(stock_recommendations, use_container_width=True, hide_index=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # ===== KEY METRICS =====
    if "Stock Value" in stock_recommendations.columns:
        st.markdown("<div style='height:32px'></div>", unsafe_allow_html=True)
        st.markdown('<div class="section-header">💰 Inventory Valuation</div>', unsafe_allow_html=True)
        
        total_stock_value = stock_recommendations["Stock Value"].sum()
        total_potential_revenue = stock_recommendations["Potential Revenue"].sum() if "Potential Revenue" in stock_recommendations.columns else 0
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Total Inventory Value", format_currency(total_stock_value))
        with col2:
            st.metric("Potential Revenue", format_currency(total_potential_revenue))
