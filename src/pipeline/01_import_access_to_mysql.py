import os
import math
from pathlib import Path

import pandas as pd
import pyodbc
import mysql.connector
from dotenv import load_dotenv


ACCESS_FILE = Path("data/raw/distribuicao.accdb")
ACCESS_TABLE = "tblLead"
MYSQL_TABLE = "stg_leads_access"


COLUMNS_TO_IMPORT = [
    "id_log",
    "referencia",
    "referencia_data",
    "ativo",
    "recebido_em",
    "id_fila",
    "nome_fila",
    "nome_grupo",
    "idlead",
    "lead_nome",
    "empreendimento",
    "gestor",
    "corretor",
    "imobiliaria",
    "repassado",
    "represado",
    "distribuido_em",
    "comunicador",
]


def read_access_table():
    conn_str = (
        r"DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};"
        rf"DBQ={ACCESS_FILE};"
    )

    columns_sql = ", ".join(COLUMNS_TO_IMPORT)

    query = f"""
        SELECT {columns_sql}
        FROM {ACCESS_TABLE}
    """

    conn = pyodbc.connect(conn_str)

    try:
        df = pd.read_sql(query, conn)
    finally:
        conn.close()

    return df


def clean_dataframe(df):
    df = df[df["id_log"].notnull()].copy()

    df["lead_nome"] = df["lead_nome"].apply(
        lambda value: value[:255] if isinstance (value,str) else value
    )

    df = df.astype(object)

    df = df.where(pd.notnull(df), None)

    return df


def get_mysql_connection():
    load_dotenv()

    conn = mysql.connector.connect(
        host=os.getenv("MYSQL_HOST"),
        user=os.getenv("MYSQL_USER"),
        password=os.getenv("MYSQL_PASSWORD"),
        database=os.getenv("MYSQL_DATABASE"),
        use_pure=True,
    )

    return conn


def convert_value(value):
    """
    Converts problematic pandas/numpy values into normal Python values
    before sending them to MySQL.
    """

    if value is None:
        return None

    if isinstance(value, float) and math.isnan(value):
        return None

    if pd.isna(value):
        return None

    if isinstance(value, pd.Timestamp):
        return value.to_pydatetime()

    return value


def insert_into_mysql(df):
    if df.empty:
        print("No rows to insert.")
        return

    conn = get_mysql_connection()
    cursor = conn.cursor()

    columns_sql = ", ".join(COLUMNS_TO_IMPORT)
    placeholders = ", ".join(["%s"] * len(COLUMNS_TO_IMPORT))

    insert_sql = f"""
        INSERT INTO {MYSQL_TABLE} ({columns_sql})
        VALUES ({placeholders})
    """

    rows = []

    for _, row in df.iterrows():
        values = tuple(
            convert_value(row[column])
            for column in COLUMNS_TO_IMPORT
        )
        rows.append(values)

    cursor.executemany(insert_sql, rows)
    conn.commit()

    print(f"Rows inserted into {MYSQL_TABLE}: {cursor.rowcount}")

    cursor.close()
    conn.close()


def main():
    print("Reading Access data...")
    df = read_access_table()

    print(f"Rows read from Access: {len(df)}")

    print("Cleaning data...")
    df = clean_dataframe(df)

    print(f"Rows after cleaning: {len(df)}")

    print("Inserting into MySQL staging table...")
    insert_into_mysql(df)

    print("Access import completed successfully.")


if __name__ == "__main__":
    main()