import streamlit as st
from pathlib import Path
import sys


PROJECT_ROOT = Path(__file__).resolve().parents[1]
CANONICAL_DATA_DIR = PROJECT_ROOT / "data" / "processed"
CANONICAL_INVENTORY_FILE = CANONICAL_DATA_DIR / "clean_inventory.csv"
CANONICAL_SALES_FILE = CANONICAL_DATA_DIR / "clean_sales.csv"
CANONICAL_DB_FILE = CANONICAL_DATA_DIR / "stockify.db"
INGESTION_INVENTORY_FILE = PROJECT_ROOT / "Ingestion" / "data" / "processed" / "inventory_cleaned.csv"
INGESTION_SALES_FILE = PROJECT_ROOT / "Ingestion" / "data" / "processed" / "sales_cleaned.csv"
INGESTION_LOWER_INVENTORY_FILE = PROJECT_ROOT / "ingestion" / "data" / "processed" / "inventory_cleaned.csv"
INGESTION_LOWER_SALES_FILE = PROJECT_ROOT / "ingestion" / "data" / "processed" / "sales_cleaned.csv"


def _ensure_paths_in_sys():
    project_dir = Path(__file__).resolve().parent
    project_root = Path(__file__).resolve().parents[1]
    for p in [str(project_dir), str(project_root)]:
        if p not in sys.path:
            sys.path.insert(0, p)


_ensure_paths_in_sys()

# Import pipeline modules — gracefully handle missing ingestion package (e.g. on Vercel)
process_inventory_file = None
process_sales_file = None
run_analytics = None

try:
    from ingestion.inventory.inventory_pipeline import process_inventory_file
    from ingestion.sales.sales_pipeline import process_sales_file
except Exception:
    try:
        from Ingestion.inventory.inventory_pipeline import process_inventory_file
        from Ingestion.sales.sales_pipeline import process_sales_file
    except Exception:
        pass

try:
    from analytics.analytics_runner import run_analytics
except Exception:
    pass


def show_upload():
    st.markdown('<div class="page-title">📂 Upload Data</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="page-subtitle">Import your inventory and sales CSV/Excel files for instant analysis</div>',
        unsafe_allow_html=True,
    )

    # Info about POS system
    st.info(
        "💡 **Tip**: Use the **💳 POS** page for real-time sales entry with barcode scanning. "
        "Both CSV upload and POS automatically sync to your dashboard.",
        icon="ℹ️"
    )

    with st.expander("🧹 Reset all POS + ingestion data"):
        st.caption("Use this to force all analytics pages back to zero state.")
        if st.button("Reset data now", key="reset_all_data_btn", type="secondary"):
            files_to_remove = [
                CANONICAL_INVENTORY_FILE,
                CANONICAL_SALES_FILE,
                CANONICAL_DB_FILE,
                INGESTION_INVENTORY_FILE,
                INGESTION_SALES_FILE,
                INGESTION_LOWER_INVENTORY_FILE,
                INGESTION_LOWER_SALES_FILE,
            ]
            removed = 0
            for target in files_to_remove:
                try:
                    if target.exists():
                        target.unlink()
                        removed += 1
                except Exception:
                    pass

            if run_analytics:
                st.session_state.analytics_results = run_analytics()
            st.session_state.live_data_signature = None
            st.success(f"✅ Reset complete. Removed {removed} data file(s). Analytics now reflects zero state until new POS/upload data arrives.")

    # ===== INVENTORY UPLOAD =====
    st.markdown('<div class="section-header">📦 Inventory File</div>', unsafe_allow_html=True)

    st.markdown("""
    <div class="upload-zone">
        <div style="text-align:center; margin-bottom:8px;">
            <span style="font-size:36px; filter:drop-shadow(0 0 12px rgba(50,121,249,0.2));">📁</span>
        </div>
        <div style="text-align:center; color:#9AA0A6; font-size:13px;">
            Drag & drop or browse to upload your inventory file
        </div>
    </div>
    """, unsafe_allow_html=True)

    inv_file = st.file_uploader(
        "Choose inventory file",
        type=["csv", "xlsx"],
        key="inventory_uploader",
        label_visibility="collapsed",
    )

    if inv_file is not None:
        if process_inventory_file is None:
            st.error("⚠️ Ingestion pipeline not available (import error).")
        else:
            try:
                cleaned = process_inventory_file(inv_file)
                CANONICAL_DATA_DIR.mkdir(parents=True, exist_ok=True)
                cleaned.to_csv(CANONICAL_INVENTORY_FILE, index=False)
                st.success("✅ Inventory file processed successfully!")
                st.markdown('<div class="chart-container">', unsafe_allow_html=True)
                st.dataframe(cleaned.head(10), use_container_width=True)
                st.markdown('</div>', unsafe_allow_html=True)
                if run_analytics:
                    st.session_state.analytics_results = run_analytics()
                    st.session_state.live_data_signature = None
                    st.success("📊 Analytics updated!")
            except Exception as e:
                st.error(f"❌ Error processing inventory file: {e}")

    with st.expander("📋 View Expected Inventory Columns"):
        st.table({
            "Product ID": ["P001", "P002"],
            "Product Name": ["Coffee Beans", "Green Tea"],
            "Category": ["Beverages", "Beverages"],
            "Quantity On Hand": [120, 80],
            "Reorder Point": [30, 20],
            "Unit Cost": [3.50, 2.00],
            "Selling Price": [5.99, 3.99],
            "Last Purchase Date": ["2026-01-10", "2026-01-12"],
        })

    st.markdown("<div style='height:32px'></div>", unsafe_allow_html=True)

    # ===== SALES UPLOAD =====
    st.markdown('<div class="section-header delay-2">💰 Sales File</div>', unsafe_allow_html=True)

    st.markdown("""
    <div class="upload-zone delay-2">
        <div style="text-align:center; margin-bottom:8px;">
            <span style="font-size:36px; filter:drop-shadow(0 0 12px rgba(50,121,249,0.2));">📊</span>
        </div>
        <div style="text-align:center; color:#9AA0A6; font-size:13px;">
            Drag & drop or browse to upload your sales file
        </div>
    </div>
    """, unsafe_allow_html=True)

    sales_file = st.file_uploader(
        "Choose sales file",
        type=["csv", "xlsx"],
        key="sales_uploader",
        label_visibility="collapsed",
    )

    if sales_file is not None:
        if process_sales_file is None:
            st.error("⚠️ Ingestion pipeline not available (import error).")
        else:
            try:
                cleaned = process_sales_file(sales_file)
                CANONICAL_DATA_DIR.mkdir(parents=True, exist_ok=True)
                cleaned.to_csv(CANONICAL_SALES_FILE, index=False)
                st.success("✅ Sales file processed successfully!")
                st.markdown('<div class="chart-container">', unsafe_allow_html=True)
                st.dataframe(cleaned.head(10), use_container_width=True)
                st.markdown('</div>', unsafe_allow_html=True)
                if run_analytics:
                    st.session_state.analytics_results = run_analytics()
                    st.session_state.live_data_signature = None
                    st.success("📊 Analytics updated!")
            except Exception as e:
                st.error(f"❌ Error processing sales file: {e}")

    with st.expander("📋 View Expected Sales Columns"):
        st.table({
            "product": ["Coffee Beans", "Green Tea"],
            "date": ["2026-01-15", "2026-01-15"],
            "quantity": [45, 30],
            "revenue": [675.0, 240.0],
            "category": ["Beverages", "Beverages"],
        })
