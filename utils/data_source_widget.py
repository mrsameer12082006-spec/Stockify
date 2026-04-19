import streamlit as st


def render_data_source_status(results: dict) -> None:
    """Render a tiny source badge showing whether POS or ingestion drives the data."""

    sources = results.get("data_sources", {}) if isinstance(results, dict) else {}
    inventory = sources.get("inventory", {}) if isinstance(sources, dict) else {}
    sales = sources.get("sales", {}) if isinstance(sources, dict) else {}

    inventory_label = inventory.get("label", "No data")
    sales_label = sales.get("label", "No data")
    inventory_path = inventory.get("path", "")
    sales_path = sales.get("path", "")

    st.markdown(
        f"""
        <div style="
            display:flex;
            align-items:center;
            justify-content:space-between;
            gap:12px;
            padding:10px 12px;
            margin:8px 0 18px 0;
            border-radius:14px;
            background: rgba(50, 121, 249, 0.05);
            border: 1px solid rgba(50, 121, 249, 0.12);
            font-size:12px;
            color:#4b5563;
        ">
            <div style="font-weight:700; color:#1f2937;">Data source status</div>
            <div style="display:flex; flex-wrap:wrap; gap:8px; justify-content:flex-end;">
                <span style="padding:4px 10px; border-radius:9999px; background:#fff; border:1px solid rgba(0,0,0,0.06);">
                    Inventory: <strong>{inventory_label}</strong>
                </span>
                <span style="padding:4px 10px; border-radius:9999px; background:#fff; border:1px solid rgba(0,0,0,0.06);">
                    Sales: <strong>{sales_label}</strong>
                </span>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    with st.expander("View source files", expanded=False):
        st.code(f"Inventory: {inventory_path or 'No file'}\nSales: {sales_path or 'No file'}", language="text")
