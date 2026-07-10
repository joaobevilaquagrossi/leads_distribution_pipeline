from pathlib import Path

import pandas as pd


CSV_FILE = Path("data/raw/distribuicaosharepoint.csv")


def main():
    print("Starting CSV inspection script...")

    if not CSV_FILE.exists():
        raise FileNotFoundError(f"CSV file not found: {CSV_FILE}")

    print(f"CSV file found: {CSV_FILE}")
    print("Reading CSV file...")

    df = pd.read_csv(
        CSV_FILE,
        encoding="latin1",
        sep=";"
    )

    print("CSV loaded successfully.")
    print(f"Rows: {len(df)}")
    print(f"Columns: {len(df.columns)}")
    print()

    print("Column names:")
    print("-" * 40)

    for column in df.columns:
        print(column)

    print()
    print("First 5 rows:")
    print("-" * 40)
    print(df.head())


if __name__ == "__main__":
    main()