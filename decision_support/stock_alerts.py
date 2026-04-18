import pandas as pd
import streamlit as st


def generate_stock_alerts(df: pd.DataFrame) -> pd.DataFrame:
    """
    Generate inventory health alerts based on stock levels and cost structure.

    Expected columns:
    - Product Name
    - Quantity On Hand
    - Reorder Point
    - Unit Cost
    - Selling Price
    """

    required_cols = {
        "Product Name",
        "Quantity On Hand",
        "Reorder Point",
        "Unit Cost",
        "Selling Price"
    }

    if not required_cols.issubset(df.columns):
        raise ValueError("Inventory DataFrame missing required columns.")

    alerts = []

    for _, row in df.iterrows():
        product = row["Product Name"]
        stock = row["Quantity On Hand"]
        reorder_point = row["Reorder Point"]
        unit_cost = row["Unit Cost"]
        selling_price = row["Selling Price"]

        stock_value = stock * unit_cost
        potential_revenue = stock * selling_price
        profit_margin = (
            ((selling_price - unit_cost) / selling_price) * 100
            if selling_price > 0 else 0
        )

        # ----------------------------
        # Alert Logic
        # ----------------------------

        if stock <= reorder_point:
            alert_type = "Low Stock"
            risk_level = "High"
            recommendation = "Reorder immediately to avoid stock-out."

        elif stock > reorder_point * 3:
            alert_type = "Overstock"
            risk_level = "Medium"
            recommendation = "Reduce next purchase or consider promotional discount."

        else:
            alert_type = "Healthy"
            risk_level = "Low"
            recommendation = "Stock level is optimal."

        alerts.append({
            "Product Name": product,
            "Current Stock": stock,
            "Reorder Point": reorder_point,
            "Alert Type": alert_type,
            "Risk Level": risk_level,
            "Stock Value": round(stock_value, 2),
            "Potential Revenue": round(potential_revenue, 2),
            "Profit Margin (%)": round(profit_margin, 2),
            "Recommendation": recommendation
        })

    return pd.DataFrame(alerts)


def show_stock_alerts():
    """Display stock alerts page with inventory health overview."""
    
    results = st.session_state.get("analytics_results", {})
    stock_recommendations = results.get("stock_recommendations", pd.DataFrame())
    
    st.markdown('<div class="page-title">🚨 Stock Alerts & Recommendations</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="page-subtitle">Real-time inventory health alerts and actionable recommendations</div>',
        unsafe_allow_html=True,
    )
    
    if stock_recommendations.empty:
        st.markdown("""
        <div style="text-align:center; padding:60px 20px; color:#9AA0A6;">
            <div style="font-size:44px; margin-bottom:10px;">📭</div>
            <div style="font-size:15px; font-weight:600; color:#5F6368; margin-bottom:4px;">No Stock Data Available</div>
            <div style="font-size:12px;">Upload inventory and sales data to see stock alerts</div>
        </div>
        """, unsafe_allow_html=True)
        return
    
    # ===== ALERT SUMMARY =====
    if "Alert Type" in stock_recommendations.columns:
        st.markdown('<div class="section-header">📊 Alert Summary</div>', unsafe_allow_html=True)
        
        low_stock = len(stock_recommendations[stock_recommendations["Alert Type"] == "Low Stock"])
        healthy = len(stock_recommendations[stock_recommendations["Alert Type"] == "Healthy"])
        overstock = len(stock_recommendations[stock_recommendations["Alert Type"] == "Overstock"])
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown(f"""
            <div class="glass-card" style="text-align:center; padding:20px 16px; background:rgba(217,48,37,0.06);">
                <div style="font-size:28px; margin-bottom:4px;">🔴</div>
                <div style="font-size:20px; font-weight:700; color:#D93025;">{low_stock}</div>
                <div style="font-size:11px; color:#5F6368; text-transform:uppercase; letter-spacing:1px; font-weight:600;">Low Stock</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div class="glass-card" style="text-align:center; padding:20px 16px; background:rgba(30,142,62,0.06);">
                <div style="font-size:28px; margin-bottom:4px;">✅</div>
                <div style="font-size:20px; font-weight:700; color:#1E8E3E;">{healthy}</div>
                <div style="font-size:11px; color:#5F6368; text-transform:uppercase; letter-spacing:1px; font-weight:600;">Healthy</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown(f"""
            <div class="glass-card" style="text-align:center; padding:20px 16px; background:rgba(249,171,0,0.06);">
                <div style="font-size:28px; margin-bottom:4px;">📦</div>
                <div style="font-size:20px; font-weight:700; color:#F9AB00;">{overstock}</div>
                <div style="font-size:11px; color:#5F6368; text-transform:uppercase; letter-spacing:1px; font-weight:600;">Overstock</div>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("<div style='height:32px'></div>", unsafe_allow_html=True)
        
        # ===== ALERTS BY TYPE =====
        low_stock_items = stock_recommendations[stock_recommendations["Alert Type"] == "Low Stock"]
        if not low_stock_items.empty:
            st.markdown('<div class="section-header">⚠️ Low Stock Items (Priority Action)</div>', unsafe_allow_html=True)
            st.markdown('<div class="chart-container">', unsafe_allow_html=True)
            st.dataframe(low_stock_items, use_container_width=True, hide_index=True)
            st.markdown('</div>', unsafe_allow_html=True)
            st.markdown("<div style='height:20px'></div>", unsafe_allow_html=True)
        
        overstock_items = stock_recommendations[stock_recommendations["Alert Type"] == "Overstock"]
        if not overstock_items.empty:
            st.markdown('<div class="section-header">📦 Overstock Items (Optimization Opportunity)</div>', unsafe_allow_html=True)
            st.markdown('<div class="chart-container">', unsafe_allow_html=True)
            st.dataframe(overstock_items, use_container_width=True, hide_index=True)
            st.markdown('</div>', unsafe_allow_html=True)
            st.markdown("<div style='height:20px'></div>", unsafe_allow_html=True)
    
    # ===== FULL ALERTS TABLE =====
    st.markdown('<div class="section-header">📋 Complete Stock Status</div>', unsafe_allow_html=True)
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    st.dataframe(stock_recommendations, use_container_width=True, hide_index=True)
    st.markdown('</div>', unsafe_allow_html=True)

