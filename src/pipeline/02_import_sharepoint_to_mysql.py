import os
import math
from pathlib import Path

import pandas as pd
import mysql.connector
from dotenv import load_dotenv


CSV_FILE = Path("data/raw/distribuicaosharepoint.csv")
MYSQL_TABLE = "stg_leads_sharepoint"


COLUMNS_TO_INSERT = [
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


def read_csv_file():
    if not CSV_FILE.exists():
        raise FileNotFoundError(f"CSV file not found: {CSV_FILE}")

    df = pd.read_csv(
        CSV_FILE,
        encoding="latin1",
        sep=";"
    )

    return df


def parse_portuguese_datetime(value):
    if pd.isna(value):
        return None

    value = str(value).strip()

    if value == "":
        return None

    value = value.replace(" às ", " ")
    value = value.replace("h", ":")

    return pd.to_datetime(
        value,
        format="%d/%m/%Y %H:%M",
        errors="coerce"
    )


def clean_dataframe(df):
    if "Unnamed: 19" in df.columns:
        df = df.drop(columns=["Unnamed: 19"])

    df = df.rename(columns={
        "Lead foi repassado": "repassado",
        "Lead chegou represado": "represado",
        "Distribuído em": "distribuido_em",
        "Comunicador": "comunicador",
    })

    flag_columns = ["repassado", "represado", "comunicador"]

    for column in flag_columns:
        df[column] = df[column].replace({
            "Sim": "S",
            "Não": "N",
            "sim": "S",
            "não": "N",
            "SIM": "S",
            "NÃO": "N",
        })

    df["referencia"] = None
    df["ativo"] = None

    df = df[df["id_log"].notnull()].copy()

    df["referencia_data"] = pd.to_datetime(
        df["referencia_data"],
        format="%d/%m/%Y %H:%M",
        errors="coerce"
    )

    df["recebido_em"] = pd.to_datetime(
        df["recebido_em"],
        format="%d/%m/%Y %H:%M",
        errors="coerce"
    )

    df["distribuido_em"] = df["distribuido_em"].apply(
        parse_portuguese_datetime
    )

    text_columns_to_trim = [
        "nome_fila",
        "nome_grupo",
        "lead_nome",
        "gestor",
        "corretor",
        "imobiliaria",
        "repassado",
        "represado",
        "comunicador",
    ]

    for column in text_columns_to_trim:
        df[column] = df[column].apply(
            lambda value: value[:255] if isinstance(value, str) else value
        )

    numeric_columns = ["id_log", "id_fila", "idlead"]

    for column in numeric_columns:
        df[column] = pd.to_numeric(df[column], errors="coerce")

    df = df[df["id_log"].notnull()].copy()

    df = df.astype(object)
    df = df.where(pd.notnull(df), None)

    return df[COLUMNS_TO_INSERT]


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

    columns_sql = ", ".join(COLUMNS_TO_INSERT)
    placeholders = ", ".join(["%s"] * len(COLUMNS_TO_INSERT))

    insert_sql = f"""
        INSERT INTO {MYSQL_TABLE} ({columns_sql})
        VALUES ({placeholders})
    """

    rows = []

    for _, row in df.iterrows():
        values = tuple(
            convert_value(row[column])
            for column in COLUMNS_TO_INSERT
        )
        rows.append(values)

    cursor.executemany(insert_sql, rows)
    conn.commit()

    print(f"Rows inserted into {MYSQL_TABLE}: {cursor.rowcount}")

    cursor.close()
    conn.close()


def main():
    print("Reading SharePoint CSV...")
    df = read_csv_file()

    print(f"Rows read from CSV: {len(df)}")

    print("Cleaning SharePoint data...")
    df = clean_dataframe(df)

    print(f"Rows after cleaning: {len(df)}")

    print("Inserting into MySQL staging table...")
    insert_into_mysql(df)

    print("SharePoint import completed successfully.")


if __name__ == "__main__":
    main()