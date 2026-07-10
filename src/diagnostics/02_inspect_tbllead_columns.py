import pyodbc
from pathlib import Path


ACCESS_FILE = Path("data/raw/distribuicao.accdb")
TABLE_NAME = "tblLead"


def main():
    if not ACCESS_FILE.exists():
        raise FileNotFoundError(f"Access file not found: {ACCESS_FILE}")

    conn_str = (
        r"DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};"
        rf"DBQ={ACCESS_FILE};"
    )

    conn = pyodbc.connect(conn_str)
    cursor = conn.cursor()

    print(f"Columns in Access table: {TABLE_NAME}")
    print("-" * 60)

    for column in cursor.columns(table=TABLE_NAME):
        print(f"{column.column_name} | {column.type_name}")

    cursor.close()
    conn.close()


if __name__ == "__main__":
    main()