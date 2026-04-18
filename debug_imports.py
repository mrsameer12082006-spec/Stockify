"""
Debug script to test import issues in the Stockify app.
Run this before starting Streamlit to diagnose import problems.
"""

import sys
import os
from pathlib import Path

print("=" * 60)
print("STOCKIFY IMPORT DEBUGGING")
print("=" * 60)

# 1. Check Python version
print(f"\n✓ Python Version: {sys.version}")

# 2. Check project root
project_root = Path(__file__).resolve().parent
print(f"✓ Project Root: {project_root}")

# 3. Check PYTHONPATH
print(f"\n✓ Current sys.path:")
for i, path in enumerate(sys.path[:5], 1):
    print(f"  {i}. {path}")

# 4. Add project root if needed
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))
    print(f"\n→ Added project root to sys.path")

# 5. Test file existence
print(f"\n✓ Checking critical files:")
files_to_check = [
    "ingestion/__init__.py",
    "ingestion/file_uploader.py",
    "ingestion/inventory/inventory_pipeline.py",
    "ingestion/sales/sales_pipeline.py",
]

for file_path in files_to_check:
    full_path = project_root / file_path
    exists = "✓" if full_path.exists() else "✗"
    print(f"  {exists} {file_path}")

# 6. Test imports step-by-step
print(f"\n✓ Testing imports (step-by-step):")

try:
    print("  1. Importing pandas...")
    import pandas as pd
    print("     ✓ pandas imported")
except Exception as e:
    print(f"     ✗ Error: {e}")

try:
    print("  2. Importing file_uploader...")
    from ingestion.file_uploader import load_file
    print("     ✓ file_uploader.load_file imported")
except Exception as e:
    print(f"     ✗ Error: {e}")

try:
    print("  3. Importing inventory pipeline...")
    from ingestion.inventory.inventory_pipeline import process_inventory_file
    print("     ✓ process_inventory_file imported")
except Exception as e:
    print(f"     ✗ Error: {e}")

try:
    print("  4. Importing sales pipeline...")
    from ingestion.sales.sales_pipeline import process_sales_file
    print("     ✓ process_sales_file imported")
except Exception as e:
    print(f"     ✗ Error: {e}")

try:
    print("  5. Importing from ingestion package...")
    from ingestion import process_inventory_file, process_sales_file
    print("     ✓ Both functions imported from ingestion package")
except Exception as e:
    print(f"     ✗ Error: {e}")

print("\n" + "=" * 60)
print("If all checks passed, the import error is fixed!")
print("=" * 60)
