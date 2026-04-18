import streamlit as st
import pandas as pd


def show_alerts(alert_df):
    """
    Displays inventory alerts in a professional, interactive table format.
    
    Accepts alerts DataFrame with columns such as:
    - Alert Type (or alert_type)
    - Product Name (or product)
    - Risk Level
    - Recommendation
    - Stock value info
    
    Safety:
    - Checks for None and empty DataFrame
    - Provides helpful messages when no alerts
    - Color-coded display for risk levels
    - Error handling with user-friendly messages
    """
    
    st.markdown("###  Inventory Alerts")
    
    # Safety check 1: None or empty
    if alert_df is None or alert_df.empty:
        st.caption(" No inventory alerts. Stock levels are healthy.")
        return
    
    try:
        # Display the full dataframe with formatting
        st.dataframe(
            alert_df,
            use_container_width=True,
            hide_index=False
        )
        
        # Safety check 2: Highlight critical alerts if Risk Level exists
        if "Risk Level" in alert_df.columns:
            high_risk = alert_df[alert_df["Risk Level"] == "High"]
            if not high_risk.empty:
                st.warning(
                    f" **{len(high_risk)} product(s) at HIGH RISK** - Immediate action required!"
                )
                
                # Show priority list for high-risk items
                with st.expander(" View High-Risk Products"):
                    for _, row in high_risk.iterrows():
                        product_name = row.get("Product Name", "Unknown")
                        current_stock = row.get("Current Stock", "N/A")
                        reorder = row.get("Reorder Point", "N/A")
                        recommendation = row.get("Recommendation", "Take action")
                        
                        st.markdown(
                            f"**{product_name}**\n"
                            f"- Current: {current_stock} | Reorder Point: {reorder}\n"
                            f"- Action: {recommendation}"
                        )
        
        # Display summary statistics
        with st.expander(" Alert Summary"):
            if "Alert Type" in alert_df.columns:
                alert_counts = alert_df["Alert Type"].value_counts()
                st.write(alert_counts)
            
            if "Risk Level" in alert_df.columns:
                risk_counts = alert_df["Risk Level"].value_counts()
                st.write("**Risk Distribution:**")
                st.write(risk_counts)
            
    except Exception as e:
        st.error(f" Error displaying alerts: {str(e)}")