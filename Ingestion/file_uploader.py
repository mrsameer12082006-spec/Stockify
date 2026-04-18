# ingestion/uploader.py

import pandas as pd
from pathlib import Path


SUPPORTED_FORMATS = [".csv", ".xlsx"]


def load_file(file):
    """
    Load CSV or Excel file into pandas DataFrame
    """
    if file is None:
        raise ValueError("No file provided")

    file_name = file.name
    extension = Path(file_name).suffix.lower()

    if extension not in SUPPORTED_FORMATS:
        raise ValueError("Unsupported file format. Use CSV or Excel.")

    try:
        if extension == ".csv":
            df = pd.read_csv(file)
        else:
            df = pd.read_excel(file)

        return df

    except Exception as e:
        raise ValueError(f"Error reading file: {str(e)}")
