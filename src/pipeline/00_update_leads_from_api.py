import requests
import mysql.connector
from datetime import datetime
import time

API_URL = "https://brio.cvcrm.com.br/api/v1/cvdw/distribuicao/leads"
API_TOKEN = "09e9f9c82f8483d4d14d8eae6dc2928c0f1748dd"
API_EMAIL = "joao.grossi@briovendas.com.br"

headers = {
    "token": API_TOKEN,
    "email": API_EMAIL,
    "Accept": "application/json"
}

conn = mysql.connector.connect(
    host="10.100.100.209",
    port=3306,
    user="joao_grossi",
    password="brio@2026",
    database="cvdw"
)

cursor = conn.cursor()


def treat_date(valor):
    if valor in [None, "", "null"]:
        return None

    try:
        return datetime.strptime(valor, "%Y-%m-%d %H:%M:%S")
    except:
        return None


sql = """
INSERT INTO leads_distribuicao (
    id_log,
    referencia,
    referencia_data,
    ativo,
    recebido_em,
    id_fila,
    nome_fila,
    nome_grupo,
    idlead,
    lead_nome,
    empreendimento,
    gestor,
    corretor,
    imobiliaria,
    repassado,
    represado,
    distribuido_em,
    comunicador
)
VALUES (
    %(id_log)s,
    %(referencia)s,
    %(referencia_data)s,
    %(ativo)s,
    %(recebido_em)s,
    %(id_fila)s,
    %(nome_fila)s,
    %(nome_grupo)s,
    %(idlead)s,
    %(lead_nome)s,
    %(empreendimento)s,
    %(gestor)s,
    %(corretor)s,
    %(imobiliaria)s,
    %(repassado)s,
    %(represado)s,
    %(distribuido_em)s,
    %(comunicador)s
)
ON DUPLICATE KEY UPDATE
    referencia = VALUES(referencia),
    referencia_data = VALUES(referencia_data),
    ativo = VALUES(ativo),
    recebido_em = VALUES(recebido_em),
    id_fila = VALUES(id_fila),
    nome_fila = VALUES(nome_fila),
    nome_grupo = VALUES(nome_grupo),
    idlead = VALUES(idlead),
    lead_nome = VALUES(lead_nome),
    empreendimento = VALUES(empreendimento),
    gestor = VALUES(gestor),
    corretor = VALUES(corretor),
    imobiliaria = VALUES(imobiliaria),
    repassado = VALUES(repassado),
    represado = VALUES(represado),
    distribuido_em = VALUES(distribuido_em),
    comunicador = VALUES(comunicador),
    data_importacao = CURRENT_TIMESTAMP
"""

pagina = 1
total_paginas = 1

while pagina <= total_paginas:
    print(f"Extracting page {pagina}...")

    params = {
        "pagina": pagina,
        "registros_por_pagina": 500
    }

    response = requests.get(API_URL, headers=headers, params=params)

    if response.status_code ==429:
        print("Erro 429: muitas requisições. Aguardando para tentar novamente...")
        time.sleep(60)
        continue

    if response.status_code != 200:
        print("Erro na API")
        print("Status:", response.status_code)
        print("Resposta:", response.text)
        break

    json_data = response.json()

    total_paginas = json_data.get("total_de_paginas", 1)
    dados = json_data.get("dados", [])

    print("Total de páginas:", total_paginas)
    print("Registros nesta página:", len(dados))

    for item in dados:
        valores = {
            "id_log": item.get("id_log"),
            "referencia": item.get("referencia"),
            "referencia_data": treat_date(item.get("referencia_data")),
            "ativo": item.get("ativo"),
            "recebido_em": treat_date(item.get("recebido_em")),
            "id_fila": item.get("id_fila"),
            "nome_fila": item.get("nome_fila"),
            "nome_grupo": item.get("nome_grupo"),
            "idlead": item.get("idlead"),
            "lead_nome": item.get("lead_nome"),
            "empreendimento": item.get("empreendimento"),
            "gestor": item.get("gestor"),
            "corretor": item.get("corretor"),
            "imobiliaria": item.get("imobiliaria"),
            "repassado": item.get("repassado"),
            "represado": item.get("represado"),
            "distribuido_em": treat_date(item.get("distribuido_em")),
            "comunicador": item.get("comunicador")
        }

        cursor.execute(sql, valores)

    conn.commit()

    print(f"Página {pagina} importada com sucesso.")

    pagina += 1

    time.sleep(1)

cursor.close()
conn.close()

print("Extraction successfully completed!")