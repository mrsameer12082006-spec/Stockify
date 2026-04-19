"""
Consolidated visualizations module - renders all visualization functions.
"""

import streamlit as st
import pandas as pd

from utils.helpers import format_currency
from utils.data_source_widget import render_data_source_status


def show_visualizations():
    """Display all available visualizations for the data."""
    
    results = st.session_state.get("analytics_results", {})
    
    st.markdown('<div class="page-title">📉 Visualizations</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="page-subtitle">Comprehensive charts and analytics visualizations</div>',
        unsafe_allow_html=True,
    )
    render_data_source_status(results)
    
    # Get data from results
    daily_trends = results.get("daily_trends", pd.DataFrame())
    product_demand = results.get("product_demand", pd.DataFrame())
    category_demand = results.get("category_demand", pd.DataFrame())
    stock_recommendations = results.get("stock_recommendations", pd.DataFrame())

    # Visualization tab styling (pill buttons)
    st.markdown(
        """
        <style>
        div[data-baseweb="tab-list"] {
            gap: 8px;
            border-bottom: 1px solid rgba(17, 24, 39, 0.08);
            padding-bottom: 8px;
            margin-bottom: 8px;
            flex-wrap: wrap;
        }
        div[data-baseweb="tab-list"] button {
            border: 1px solid rgba(50, 121, 249, 0.16) !important;
            background: rgba(255, 255, 255, 0.82) !important;
            color: #4b5563 !important;
            border-radius: 9999px !important;
            padding: 8px 16px !important;
            font-size: 15px !important;
            font-weight: 600 !important;
            line-height: 1.1 !important;
            min-height: 40px !important;
            transition: all 0.24s cubic-bezier(.23, 1, .32, 1) !important;
            box-shadow: 0 2px 8px rgba(17, 24, 39, 0.06);
        }
        div[data-baseweb="tab-list"] button:hover {
            transform: translateY(-1px);
            color: #1f2937 !important;
            border-color: rgba(50, 121, 249, 0.34) !important;
            box-shadow: 0 8px 18px rgba(50, 121, 249, 0.16);
        }
        div[data-baseweb="tab-list"] button[aria-selected="true"] {
            background: linear-gradient(90deg, #4f8dff, #3279f9) !important;
            color: #ffffff !important;
            border-color: transparent !important;
            box-shadow: 0 10px 24px rgba(50, 121, 249, 0.34);
            transform: translateY(-1px);
        }
        div[data-baseweb="tab-highlight"] {
            display: none !important;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )
    
    # ===== TAB LAYOUT FOR DIFFERENT VISUALIZATIONS =====
    tab1, tab2, tab3, tab4 = st.tabs(["📈 Sales Trends", "📦 Products", "🏷️ Categories", "🚨 Stock Alerts"])
    
    # ===== TAB 1: SALES TRENDS =====
    with tab1:
        st.markdown('<div class="section-header">Revenue & Volume Trends</div>', unsafe_allow_html=True)
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        
        if not daily_trends.empty:
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("**Daily Revenue**")
                if "revenue" in daily_trends.columns:
                    st.line_chart(daily_trends.set_index("date")[["revenue"]])
                else:
                    st.info("Revenue data not available")
            
            with col2:
                st.markdown("**Daily Sales Volume**")
                if "quantity" in daily_trends.columns:
                    st.bar_chart(daily_trends.set_index("date")[["quantity"]])
                else:
                    st.info("Quantity data not available")
            
            # Summary metrics
            if "revenue" in daily_trends.columns or "quantity" in daily_trends.columns:
                col1, col2, col3 = st.columns(3)
                
                if "revenue" in daily_trends.columns:
                    total_rev = daily_trends["revenue"].sum()
                    avg_rev = daily_trends["revenue"].mean()
                    with col1:
                        st.metric("Total Revenue", format_currency(total_rev))
                    with col2:
                        st.metric("Avg Daily Revenue", format_currency(avg_rev))
                
                if "quantity" in daily_trends.columns:
                    total_qty = daily_trends["quantity"].sum()
                    with col3:
                        st.metric("Total Units Sold", f"{total_qty:,}")
        else:
            st.markdown("""
            <div style="text-align:center; padding:40px 20px; color:#9AA0A6;">
                <div style="font-size:36px; margin-bottom:8px;">📭</div>
                <div style="font-size:13px;">Upload sales data to see trends</div>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # ===== TAB 2: PRODUCT ANALYSIS =====
    with tab2:
        st.markdown('<div class="section-header">Product Performance Analysis</div>', unsafe_allow_html=True)
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        
        if not product_demand.empty:
            # Demand classification
            if "totalQuantity" in product_demand.columns:
                avg_qty = product_demand["totalQuantity"].mean()
                high_demand = product_demand[product_demand["totalQuantity"] > avg_qty * 1.5]
                medium_demand = product_demand[
                    (product_demand["totalQuantity"] <= avg_qty * 1.5) & 
                    (product_demand["totalQuantity"] >= avg_qty * 0.5)
                ]
                low_demand = product_demand[product_demand["totalQuantity"] < avg_qty * 0.5]
                
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("🔥 High Demand", len(high_demand))
                with col2:
                    st.metric("⚡ Medium Demand", len(medium_demand))
                with col3:
                    st.metric("❄️ Low Demand", len(low_demand))
            
            st.markdown("**Product Details**")
            st.dataframe(product_demand, use_container_width=True)
        else:
            st.info("No product data available. Upload sales and inventory data first.")
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # ===== TAB 3: CATEGORY ANALYSIS =====
    with tab3:
        st.markdown('<div class="section-header">Category Performance</div>', unsafe_allow_html=True)
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        
        if not category_demand.empty:
            # Revenue by category
            if "revenue" in category_demand.columns and "category" in category_demand.columns:
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown("**Revenue by Category**")
                    chart_data = category_demand.set_index("category")["revenue"]
                    st.bar_chart(chart_data)
                
                with col2:
                    st.markdown("**Category Details**")
                    st.dataframe(category_demand, use_container_width=True)
            else:
                st.dataframe(category_demand, use_container_width=True)
        else:
            st.info("No category data available")
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # ===== TAB 4: STOCK ALERTS =====
    with tab4:
        st.markdown('<div class="section-header">Inventory Health & Alerts</div>', unsafe_allow_html=True)
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        
        if not stock_recommendations.empty:
            if "Alert Type" in stock_recommendations.columns:
                # Alert summary
                low_count = len(stock_recommendations[stock_recommendations["Alert Type"] == "Low Stock"])
                healthy_count = len(stock_recommendations[stock_recommendations["Alert Type"] == "Healthy"])
                overstock_count = len(stock_recommendations[stock_recommendations["Alert Type"] == "Overstock"])
                
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("🔴 Low Stock", low_count)
                with col2:
                    st.metric("✅ Healthy", healthy_count)
                with col3:
                    st.metric("📦 Overstock", overstock_count)
            
            st.markdown("**Stock Alert Details**")
            st.dataframe(stock_recommendations, use_container_width=True)
        else:
            st.info("No inventory data available. Upload inventory data to see stock alerts.")
        
        st.markdown('</div>', unsafe_allow_html=True)
