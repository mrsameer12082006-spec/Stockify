import streamlit as st
import pandas as pd

def show_products():
    results = st.session_state.get("analytics_results", {})

    st.markdown('<div class="page-title">📦 Product Analysis</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="page-subtitle">Demand classification and product performance breakdown</div>',
        unsafe_allow_html=True,
    )

    product_demand = results.get("product_demand", pd.DataFrame())

    if not product_demand.empty:
        avg_quantity = product_demand["totalQuantity"].mean()
        high_demand = len(product_demand[product_demand["totalQuantity"] > avg_quantity * 1.5])
        medium_demand = len(
            product_demand[
                (product_demand["totalQuantity"] <= avg_quantity * 1.5)
                & (product_demand["totalQuantity"] >= avg_quantity * 0.5)
            ]
        )
        low_demand = len(product_demand[product_demand["totalQuantity"] < avg_quantity * 0.5])
    else:
        high_demand = 0
        medium_demand = 0
        low_demand = 0

    # ===== DEMAND CARDS =====
    col1, col2, col3 = st.columns(3)

    demand_cards = [
        ("🔥", "High Demand", str(high_demand), "metric-green", col1),
        ("⚡", "Medium Demand", str(medium_demand), "metric-orange", col2),
        ("❄️", "Low Demand", str(low_demand), "metric-red", col3),
    ]

    for i, (icon, label, value, color_class, col) in enumerate(demand_cards):
        with col:
            st.markdown(f"""
            <div class="metric-card {color_class} delay-{i+1}">
                <div class="metric-icon">{icon}</div>
                <div class="metric-value">{value}</div>
                <div class="metric-label">{label}</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<div style='height:32px'></div>", unsafe_allow_html=True)

    # ===== PRODUCT TABLE =====
    st.markdown('<div class="section-header">📋 Product Performance</div>', unsafe_allow_html=True)
    st.markdown('<div class="chart-container delay-4">', unsafe_allow_html=True)
    if not product_demand.empty:
        st.dataframe(product_demand, use_container_width=True)
    else:
        st.markdown("""
        <div style="text-align:center; padding:48px 20px; color:#9AA0A6;">
            <div style="font-size:44px; margin-bottom:10px;">📭</div>
            <div style="font-size:15px; font-weight:600; color:#5F6368; margin-bottom:4px;">No Product Data</div>
            <div style="font-size:12px;">Upload inventory and sales data to see performance</div>
        </div>
        """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
