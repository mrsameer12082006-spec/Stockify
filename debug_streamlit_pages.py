#!/usr/bin/env python3
"""
Comprehensive Streamlit page rendering debugger.
Diagnoses issues with missing or blank pages, import errors, and data pipeline issues.

Usage:
    python debug_streamlit_pages.py
"""

import sys
import os
from pathlib import Path
import traceback

# Add project root to path
project_root = Path(__file__).resolve().parent
sys.path.insert(0, str(project_root))

print("=" * 70)
print("STREAMLIT PAGE RENDERING DEBUGGER")
print("=" * 70)

# ============================================================================
# SECTION 1: Python Environment & Dependencies
# ============================================================================
print("\n[1] Python Environment")
print("-" * 70)
print(f"Python Version: {sys.version}")
print(f"Python Executable: {sys.executable}")
print(f"Project Root: {project_root}")

# Check virtual environment
if hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix):
    print(f"✓ Virtual Environment: Active ({sys.prefix})")
else:
    print("⚠ Virtual Environment: NOT ACTIVE (may cause import issues)")

# ============================================================================
# SECTION 2: Package Imports
# ============================================================================
print("\n[2] Checking Critical Imports")
print("-" * 70)

required_packages = {
    'streamlit': 'st',
    'pandas': 'pd',
    'numpy': 'np',
}

for package, alias in required_packages.items():
    try:
        __import__(package)
        print(f"✓ {package:<15} - OK")
    except ImportError as e:
        print(f"✗ {package:<15} - MISSING: {str(e)}")

# ============================================================================
# SECTION 3: Frontend Pages Import Test
# ============================================================================
print("\n[3] Testing Frontend Pages Imports")
print("-" * 70)

pages_to_test = {
    "Home": ("frontend.pages.home", "show_home"),
    "Upload": ("frontend.pages.upload", "show_upload"),
    "Dashboard (Overview)": ("frontend.pages.dashboard", "show_dashboard"),
    "Products": ("frontend.pages.products", "show_products"),
    "Trends": ("frontend.pages.trends", "show_trends"),
    "Insights": ("frontend.pages.insights", "show_insights"),
}

for page_name, (module_path, function_name) in pages_to_test.items():
    try:
        module = __import__(module_path, fromlist=[function_name])
        func = getattr(module, function_name)
        
        # Check if function is callable
        if callable(func):
            print(f"✓ {page_name:<25} - Module OK, Function callable")
        else:
            print(f"⚠ {page_name:<25} - Module OK, but {function_name} NOT callable")
    except ImportError as e:
        print(f"✗ {page_name:<25} - Import Error: {str(e)}")
        print(f"  └─ {traceback.format_exc().splitlines()[-1]}")
    except AttributeError as e:
        print(f"✗ {page_name:<25} - Function not found: {str(e)}")
    except Exception as e:
        print(f"✗ {page_name:<25} - Unexpected Error: {str(e)}")

# ============================================================================
# SECTION 4: Ingestion Pipeline Test
# ============================================================================
print("\n[4] Testing Ingestion Pipeline")
print("-" * 70)

try:
    from ingestion import process_inventory_file, process_sales_file
    print(f"✓ process_inventory_file - OK")
    print(f"✓ process_sales_file - OK")
except ImportError as e:
    print(f"✗ Ingestion import failed: {str(e)}")
    print("\nAttempting detailed import trace:")
    
    # Try importing intermediate modules
    try:
        from ingestion.inventory import inventory_pipeline
        print("  ✓ ingestion.inventory.inventory_pipeline - OK")
    except Exception as e:
        print(f"  ✗ ingestion.inventory.inventory_pipeline - {str(e)}")
    
    try:
        from ingestion.sales import sales_pipeline
        print("  ✓ ingestion.sales.sales_pipeline - OK")
    except Exception as e:
        print(f"  ✗ ingestion.sales.sales_pipeline - {str(e)}")

# ============================================================================
# SECTION 5: Data Availability Check
# ============================================================================
print("\n[5] Data Files & Processing Paths")
print("-" * 70)

data_paths = {
    "Sales Data": "data/processed/clean_sales.csv",
    "Inventory Data": "data/processed/clean_inventory.csv",
}

for data_name, relative_path in data_paths.items():
    full_path = project_root / relative_path
    if full_path.exists():
        size_mb = full_path.stat().st_size / (1024 * 1024)
        # Try to read the file
        try:
            import pandas as pd
            df = pd.read_csv(full_path)
            print(f"✓ {data_name:<20} - Found ({len(df)} rows, {size_mb:.2f} MB)")
        except Exception as e:
            print(f"⚠ {data_name:<20} - Found but error reading: {str(e)}")
    else:
        print(f"✗ {data_name:<20} - NOT FOUND at {relative_path}")

# ============================================================================
# SECTION 6: Frontend Layout & CSS Test
# ============================================================================
print("\n[6] Frontend Layout Module")
print("-" * 70)

try:
    from frontend.layout import inject_css
    print(f"✓ frontend.layout.inject_css - OK")
except ImportError as e:
    print(f"✗ frontend.layout.inject_css import failed: {str(e)}")

# ============================================================================
# SECTION 7: Navigation Sidebar Test
# ============================================================================
print("\n[7] Navigation & Configuration")
print("-" * 70)

try:
    from app import sidebar_navigation, load_data, compute_dashboard_metrics
    print(f"✓ sidebar_navigation - OK")
    print(f"✓ load_data - OK")
    print(f"✓ compute_dashboard_metrics - OK")
except ImportError as e:
    print(f"✗ App main functions import failed: {str(e)}")

# ============================================================================
# SECTION 8: Page Label Matching
# ============================================================================
print("\n[8] Page Selection Labels (Sidebar Navigation)")
print("-" * 70)

pages = [" Home", " Upload", " Overview", " Products", " Trends", " Insights"]
print("Expected page labels in radio selection:")
for page in pages:
    print(f"  • '{page}'")

print("\n⚠ Note: Page labels have leading space (e.g., ' Overview')")
print("Make sure your if/elif statements match these EXACTLY")

# ============================================================================
# SUMMARY
# ============================================================================
print("\n" + "=" * 70)
print("DEBUGGING CHECKLIST")
print("=" * 70)

checklist = """
If Overview page is blank:

☐ 1. Check if "Overview" page selection matches in app.py
     ├─ Look for: elif page == " Overview":
     └─ Ensure leading space: " Overview" (not "Overview")

☐ 2. Verify dashboard function is imported and called
     ├─ from frontend.pages.dashboard import show_dashboard
     └─ Call: show_dashboard()

☐ 3. Check for silent exceptions
     ├─ Add try/except blocks (now in dashboard.py)
     └─ Errors should display with st.error()

☐ 4. Test function directly in Python
     ├─ python -c "from frontend.pages.dashboard import show_dashboard; print(show_dashboard)"
     └─ Should return function object, not None/error

☐ 5. Check CSS injection (inject_css)
     ├─ Verify frontend/layout.py exists
     └─ Test: python -c "from frontend.layout import inject_css; print(inject_css)"

☐ 6. Review data dependencies
     ├─ Dashboard may fail if data/processed/clean_sales.csv missing
     ├─ Check load_data() in app.py
     └─ Upload sample data first, then check Overview

☐ 7. Check browser console
     ├─ Open Developer Tools (F12)
     ├─ Check Console tab for JavaScript errors
     └─ Check Network tab for failed requests

☐ 8. Restart Streamlit
     ├─ Stop: Ctrl+C in terminal
     ├─ Restart: streamlit run app.py
     └─ Clear cache: Delete .streamlit/cache if issues persist
"""

print(checklist)

# ============================================================================
# RECOMMENDED NEXT STEPS
# ============================================================================
print("\nRECOMMENDED NEXT STEPS:")
print("-" * 70)
print("1. Review the error output above for ✗ (failures)")
print("2. Run: streamlit run app.py")
print("3. Go to Upload page and upload sample CSV files")
print("4. Click Overview - errors should now display instead of blank page")
print("5. Check browser console (F12) for any JavaScript errors")
print("6. Check terminal where streamlit is running for Python errors")
print("\nFor detailed error logs, check the terminal output.")
print("=" * 70)
