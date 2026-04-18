import streamlit as st


def render_kpi_cards(kpi_data: dict):
    """
    Renders KPI summary cards for inventory dashboard using Streamlit metrics.
    
    Expected input:
    {
        'total_products': int,
        'total_sales_quantity': int,
        'top_selling_product': str,
        'low_stock_count': int
    }
    
    Safety:
    - Validates input is not None
    - Provides default values for missing keys
    - Error handling with user-friendly messages
    """
    
    if kpi_data is None:
        st.warning(" KPI data not available")
        return
    
    try:
        # Create a container for better visual organization
        st.markdown("###  Inventory Overview")
        
        # Use columns for layout
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric(
                label=" Total Products",
                value=kpi_data.get("total_products", 0),
                delta=None
            )
        
        with col2:
            st.metric(
                label=" Total Quantity",
                value=f"{kpi_data.get('total_sales_quantity', 0):,}",
                delta=None
            )
        
        with col3:
            top_product = str(kpi_data.get("top_selling_product", "N/A"))
            # Truncate long product names
            if len(top_product) > 20:
                top_product = top_product[:17] + "..."
            st.metric(
                label="⭐ Top Product",
                value=top_product,
                delta=None
            )
        
        with col4:
            low_stock = kpi_data.get("low_stock_count", 0)
            delta_color = "off" if low_stock == 0 else "inverse"
            st.metric(
                label=" Low Stock Count",
                value=low_stock,
                delta=None
            )
    
    except Exception as e:
        st.error(f" Error rendering KPI cards: {str(e)}")