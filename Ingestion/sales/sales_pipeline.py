from pathlib import Path
from ..file_uploader import load_file
from .sales_validator import validate_sales_schema
from .sales_cleaner import clean_sales

PACKAGE_ROOT = Path(__file__).resolve().parent.parent
OUTPUT_PATH = PACKAGE_ROOT / "data" / "processed"
OUTPUT_FILE = OUTPUT_PATH / "sales_cleaned.csv"


def process_sales_file(file):
    """Full pipeline for sales files: load -> validate -> clean -> save"""
    df = load_file(file)
    validate_sales_schema(df)
    cleaned = clean_sales(df)

    OUTPUT_PATH.mkdir(parents=True, exist_ok=True)
    cleaned.to_csv(OUTPUT_FILE, index=False)

    return cleaned
