from pathlib import Path
import sys

# Prefer package-relative imports when run as a module (python -m ingestion.run_pipeline).
# Fall back to local imports when the file is executed directly (python run_pipeline.py).
try:
    # package-mode
    from . import data_cleaner, file_uploader, schema_validator
    from .pipeline import process_inventory_file
    from . import pipeline
except Exception:
    # script-mode: ensure package folder is on sys.path so local imports work.
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    import file_uploader, data_cleaner, schema_validator, pipeline
    from pipeline import process_inventory_file


def main():
    # Allow passing a sample file path as the first CLI argument; otherwise use
    # the sample file bundled with the package (works regardless of CWD).
    sample = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).resolve().parent / "sample_inventory.csv"
    print(f"Using sample file: {sample.resolve()}")
    try:
        df = process_inventory_file(sample)
        print("Processed DataFrame shape:", df.shape)
        print("First 5 rows:\n", df.head().to_string(index=False))
    except ValueError as e:
        print("Pipeline validation failed:", e)
        print("Attempting: load -> clean -> validate -> save")
        df = file_uploader.load_file(sample)
        cleaned = data_cleaner.clean_data(df)
        try:
            schema_validator.validate_schema(cleaned)
        except Exception as e2:
            print("Validation still failing after cleaning:", e2)
            raise
        # Save cleaned output using pipeline constants
        pipeline.OUTPUT_PATH.mkdir(parents=True, exist_ok=True)
        cleaned.to_csv(pipeline.OUTPUT_FILE, index=False)
        print("Cleaned file saved to:", pipeline.OUTPUT_FILE)
        print("Processed DataFrame shape:", cleaned.shape)
        print("First 5 rows:\n", cleaned.head().to_string(index=False))


if __name__ == '__main__':
    main()