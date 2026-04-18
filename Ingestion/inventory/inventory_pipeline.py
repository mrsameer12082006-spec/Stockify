from pathlib import Path
from ..file_uploader import load_file
from .inventory_validator import validate_inventory_schema
from .inventory_cleaner import clean_inventory

PACKAGE_ROOT = Path(__file__).resolve().parent.parent
OUTPUT_PATH = PACKAGE_ROOT / "data" / "processed"
OUTPUT_FILE = OUTPUT_PATH / "inventory_cleaned.csv"


def process_inventory_file(file):
    df = load_file(file)
    validate_inventory_schema(df)
    cleaned = clean_inventory(df)

    OUTPUT_PATH.mkdir(parents=True, exist_ok=True)
    cleaned.to_csv(OUTPUT_FILE, index=False)

    return cleaned
