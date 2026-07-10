import pyodbc
from pathlib import Path


ACCESS_FILE = Path("data/raw/distribuicao.accdb")


def main():
    if not ACCESS_FILE.exists():
        raise FileNotFoundError(f"Access file not found: {ACCESS_FILE}")

    conn_str = (
        r"DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};"
        rf"DBQ={ACCESS_FILE};"
    )

    conn = pyodbc.connect(conn_str)
    cursor = conn.cursor()

    print("Tables found in Access database:")
    print("-" * 40)

    for table_info in cursor.tables(tableType="TABLE"):
        table_name = table_info.table_name
        print(table_name)

    cursor.close()
    conn.close()


if __name__ == "__main__":
    main()