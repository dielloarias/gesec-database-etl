import os
import json
import pyodbc
import mysql.connector
from dotenv import load_dotenv

# -------------------------------------------------------------------
# Carrega variáveis de ambiente do arquivo .env
# -------------------------------------------------------------------
def carregar_variaveis():
    load_dotenv()
    return {
        "MYSQL_HOST": os.getenv("MYSQL_HOST"),
        "MYSQL_DB": os.getenv("MYSQL_DB"),
        "MYSQL_USER": os.getenv("MYSQL_USER"),
        "MYSQL_PASS": os.getenv("MYSQL_PASS"),
        "SQLSERVER_CONN": os.getenv("SQLSERVER_CONN"),
        "CONFIG_FILE": os.getenv("CONFIG_FILE", "config.json")
    }

# -------------------------------------------------------------------
# Lê o arquivo JSON de configuração que contém mapeamento origem->destino
# -------------------------------------------------------------------
def carregar_config(caminho_config):
    with open(caminho_config, "r", encoding="utf-8") as f:
        return json.load(f)

# -------------------------------------------------------------------
# Conecta ao MySQL
# -------------------------------------------------------------------
def conectar_mysql(host, database, user, password):
    return mysql.connector.connect(
        host=host,
        database=database,
        user=user,
        password=password
    )

# -------------------------------------------------------------------
# Conecta ao SQL Server
# -------------------------------------------------------------------
def conectar_sqlserver(conn_str):
    return pyodbc.connect(conn_str)

# -------------------------------------------------------------------
# Extrai dados da tabela no MySQL
# -------------------------------------------------------------------
def extrair_dados_mysql(conn, tabela_origem, colunas):
    cursor = conn.cursor()
    query = f"SELECT {', '.join(colunas)} FROM {tabela_origem}"
    cursor.execute(query)
    rows = cursor.fetchall()
    cursor.close()
    return rows

# -------------------------------------------------------------------
# Transforma dados (exemplo simples - pode ser adaptado)
# -------------------------------------------------------------------
def transformar_dados(rows):
    return [tuple(str(item).strip() if isinstance(item, str) else item for item in row) for row in rows]

# -------------------------------------------------------------------
# Carrega dados no SQL Server
# -------------------------------------------------------------------
def carregar_dados_sqlserver(conn, tabela_destino, colunas_destino, dados):
    cursor = conn.cursor()
    placeholders = ", ".join("?" for _ in colunas_destino)
    query = f"INSERT INTO {tabela_destino} ({', '.join(colunas_destino)}) VALUES ({placeholders})"
    cursor.executemany(query, dados)
    conn.commit()
    cursor.close()

# -------------------------------------------------------------------
# Orquestra o processo ETL
# -------------------------------------------------------------------
def executar_etl():
    env = carregar_variaveis()
    config = carregar_config(env["CONFIG_FILE"])

    conn_mysql = conectar_mysql(env["MYSQL_HOST"], env["MYSQL_DB"], env["MYSQL_USER"], env["MYSQL_PASS"])
    conn_sql = conectar_sqlserver(env["SQLSERVER_CONN"])

    for job in config["jobs"]:
        origem = job["origem"]
        destino = job["destino"]

        rows = extrair_dados_mysql(conn_mysql, origem["tabela"], origem["colunas"])
        dados_transformados = transformar_dados(rows)
        carregar_dados_sqlserver(conn_sql, destino["tabela"], destino["colunas"], dados_transformados)

    conn_mysql.close()
    conn_sql.close()

# -------------------------------------------------------------------
# Execução principal
# -------------------------------------------------------------------
if __name__ == "__main__":
    executar_etl()
