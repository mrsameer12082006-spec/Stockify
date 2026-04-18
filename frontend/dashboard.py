import streamlit as st
import pandas as pd

from utils.helpers import format_currency

def show_dashboard():
    results = st.session_state.get("analytics_results", {})

    st.markdown('<div class="page-title">📊 Overview Dashboard</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="page-subtitle">Your complete inventory performance at a glance</div>',
        unsafe_allow_html=True,
    )

    kpis = results.get("kpis", {})
    daily_trends = results.get("daily_trends", pd.DataFrame())
    category_demand = results.get("category_demand", pd.DataFrame())
    top_products = results.get("top_products", pd.DataFrame())

    # ===== KPI METRICS =====
    total_revenue = daily_trends["revenue"].sum() if not daily_trends.empty else 0
    total_quantity = kpis.get("total_sales_quantity", 0)
    total_products = kpis.get("total_products", 0)
    avg_transaction = total_revenue / max(
        daily_trends["transactions"].sum() if not daily_trends.empty else 1, 1
    )

    col1, col2, col3, col4 = st.columns(4)

    metrics = [
        ("💰", "Total Revenue", format_currency(total_revenue), "metric-blue", col1),
        ("📦", "Units Sold", f"{total_quantity:,}", "metric-green", col2),
        ("🏷️", "Products", f"{total_products:,}", "metric-purple", col3),
        ("🧾", "Avg Transaction", format_currency(avg_transaction), "metric-orange", col4),
    ]

    for i, (icon, label, value, color_class, col) in enumerate(metrics):
        with col:
            st.markdown(f"""
            <div class="metric-card {color_class} delay-{i+1}">
                <div class="metric-icon">{icon}</div>
                <div class="metric-value">{value}</div>
                <div class="metric-label">{label}</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<div style='height:32px'></div>", unsafe_allow_html=True)

    # ===== STOCK HEALTH SUMMARY =====
    stock_recs = results.get("stock_recommendations", pd.DataFrame())
    if not stock_recs.empty and "Alert Type" in stock_recs.columns:
        st.markdown('<div class="section-header">🏥 Stock Health Summary</div>', unsafe_allow_html=True)

        low = len(stock_recs[stock_recs["Alert Type"] == "Low Stock"])
        healthy = len(stock_recs[stock_recs["Alert Type"] == "Healthy"])
        over = len(stock_recs[stock_recs["Alert Type"] == "Overstock"])

        h_col1, h_col2, h_col3 = st.columns(3)
        health_items = [
            ("🔻", "Low Stock", str(low), "#D93025", "rgba(217,48,37,0.06)", h_col1),
            ("✅", "Healthy", str(healthy), "#1E8E3E", "rgba(30,142,62,0.06)", h_col2),
            ("📦", "Overstock", str(over), "#F9AB00", "rgba(249,171,0,0.06)", h_col3),
        ]

        for i, (icon, label, val, color, bg, col) in enumerate(health_items):
            with col:
                st.markdown(f"""
                <div class="glass-card delay-{i+2}" style="text-align:center; padding:20px 16px;">
                    <div style="font-size:24px; margin-bottom:4px;">{icon}</div>
                    <div style="font-size:24px; font-weight:700; color:{color};">{val}</div>
                    <div style="font-size:11px; color:#9AA0A6; text-transform:uppercase;
                                letter-spacing:1px; font-weight:600; margin-top:4px;">{label}</div>
                </div>
                """, unsafe_allow_html=True)

        st.markdown("<div style='height:28px'></div>", unsafe_allow_html=True)
    else:
        st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)

    # ===== CHARTS =====
    colA, colB = st.columns(2)

    with colA:
        st.markdown('<div class="section-header">📈 Revenue Over Time</div>', unsafe_allow_html=True)
        st.markdown('<div class="chart-container delay-2">', unsafe_allow_html=True)
        if not daily_trends.empty:
            st.line_chart(daily_trends.set_index("date")["revenue"])
        else:
            st.markdown("""
            <div style="text-align:center; padding:40px 20px; color:#9AA0A6;">
                <div style="font-size:36px; margin-bottom:8px;">📭</div>
                <div style="font-size:13px;">Upload sales data to see revenue trends</div>
            </div>
            """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with colB:
        st.markdown('<div class="section-header">📊 Category Distribution</div>', unsafe_allow_html=True)
        st.markdown('<div class="chart-container delay-3">', unsafe_allow_html=True)
        if not category_demand.empty:
            st.bar_chart(category_demand.set_index("category")["revenue"])
        else:
            st.markdown("""
            <div style="text-align:center; padding:40px 20px; color:#9AA0A6;">
                <div style="font-size:36px; margin-bottom:8px;">📭</div>
                <div style="font-size:13px;">Upload data to see category distribution</div>
            </div>
            """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("<div style='height:28px'></div>", unsafe_allow_html=True)

    # ===== TOP PRODUCTS =====
    st.markdown('<div class="section-header">🏆 Top Products by Revenue</div>', unsafe_allow_html=True)
    st.markdown('<div class="chart-container delay-4">', unsafe_allow_html=True)
    if not top_products.empty:
        st.dataframe(top_products, use_container_width=True)
    else:
        st.markdown("""
        <div style="text-align:center; padding:40px 20px; color:#9AA0A6;">
            <div style="font-size:36px; margin-bottom:8px;">📭</div>
            <div style="font-size:13px;">Upload data to see top performing products</div>
        </div>
        """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
