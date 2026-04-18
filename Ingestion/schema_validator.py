# ingestion/schema_validator.py
import pandas as pd


REQUIRED_COLUMNS = {
    "Product ID": "object",
    "Product Name": "object",
    "Category": "object",
    "Quantity On Hand": "int64",
    "Reorder Point": "int64",
    "Unit Cost": "float64",
    "Selling Price": "float64",
    "Last Purchase Date": "datetime64[ns]"
}


def _format_bad_samples(series, max_samples=5):
    samples = []
    for idx, val in series.items():
        samples.append(f"(row {idx}: {val})")
        if len(samples) >= max_samples:
            break
    return ", ".join(samples)


def validate_schema(df):
    """
    Validate required columns and data types.

    Numeric columns are validated by attempting a safe coercion; if any
    non-convertible values are present, a ValueError is raised with examples
    of the offending rows to aid debugging.
    """

    # Check missing columns
    missing_cols = [col for col in REQUIRED_COLUMNS if col not in df.columns]
    if missing_cols:
        raise ValueError(f"Missing columns: {missing_cols}")

    # Convert date column (coerce invalid dates to NaT)
    df["Last Purchase Date"] = pd.to_datetime(df["Last Purchase Date"], errors="coerce")

    # Validate each required column's type
    for col, dtype in REQUIRED_COLUMNS.items():
        if col == "Last Purchase Date":
            continue

        # object (string-like) columns: ensure presence
        if dtype.startswith("object"):
            # coerce to string to avoid weird types
            df[col] = df[col].astype(str)
            continue

        # numeric columns: attempt safe coercion
        if dtype.startswith("int") or dtype.startswith("float"):
            coerced = pd.to_numeric(df[col], errors="coerce")

            # Identify values that were non-null originally but failed conversion
            bad_mask = coerced.isna() & df[col].notna()
            if bad_mask.any():
                bad_series = df.loc[bad_mask, col]
                samples = _format_bad_samples(bad_series)
                raise ValueError(f"Invalid numeric values in column '{col}': {samples}")

            # If dtype is integer but values are floats (after coercion),
            # attempt to convert to integer if no fractional parts remain.
            if dtype.startswith("int"):
                # check for fractional parts
                if not (coerced.dropna() % 1 == 0).all():
                    raise ValueError(f"Non-integer values present in integer column '{col}'")
                # safe to convert to integer dtype
                df[col] = coerced.astype("Int64")
            else:
                df[col] = coerced.astype("float64")

    return True