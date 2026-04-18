# ingestion/pipeline.py

from pathlib import Path

# Support both package-mode (python -m ingestion.run_pipeline) and
# script-mode (python run_pipeline.py) by attempting package-relative imports
# and falling back to local imports when needed.
try:
    from .file_uploader import load_file
    from .schema_validator import validate_schema
    from .data_cleaner import clean_data
except Exception:
    import sys
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    from file_uploader import load_file
    from schema_validator import validate_schema
    from data_cleaner import clean_data


PACKAGE_ROOT = Path(__file__).resolve().parent
OUTPUT_PATH = PACKAGE_ROOT / "data" / "processed"
OUTPUT_FILE = OUTPUT_PATH / "inventory_cleaned.csv"


def process_inventory_file(file):
    """
    Complete ingestion pipeline
    """

    # Step 1: Load
    df = load_file(file)

    # Step 2: Validate
    validate_schema(df)

    # Step 3: Clean
    cleaned_df = clean_data(df)

    # Step 4: Save processed file
    OUTPUT_PATH.mkdir(parents=True, exist_ok=True)
    cleaned_df.to_csv(OUTPUT_FILE, index=False)

    return cleaned_df