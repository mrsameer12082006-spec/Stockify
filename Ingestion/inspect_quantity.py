import pandas as pd
from pathlib import Path


def main():
    p = Path("sample_inventory.csv")
    print(f"Inspecting: {p.resolve()}")
    df = pd.read_csv(p)
    print("\nDataFrame info:")
    print(df.info())

    col = "Quantity On Hand"
    if col not in df.columns:
        print(f"Column '{col}' not found in CSV")
        return

    print(f"\nSample values for '{col}':")
    print(df[col].head(30).to_string(index=False))

    numeric = pd.to_numeric(df[col], errors='coerce')
    bad = df[numeric.isna()]
    print(f"\nRows with non-numeric or missing '{col}' ({len(bad)} rows):")
    if not bad.empty:
        print(bad.to_string(index=False))
    else:
        print('None')


if __name__ == '__main__':
    main()