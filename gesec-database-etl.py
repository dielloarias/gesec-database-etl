import os
import json
import mysql.connector
import pymssql
from dotenv import load_dotenv

def carregar_variaveis():
    """ -------------------------------------------------------------------
    Carrega variáveis de ambiente do arquivo .env
    """
    load_dotenv()
    return {
        "MYSQL_HOST": os.getenv("MYSQL_HOST"),
        "MYSQL_DB": os.getenv("MYSQL_DB"),
        "MYSQL_USER": os.getenv("MYSQL_USER"),
        "MYSQL_PASS": os.getenv("MYSQL_PASS"),
        "MSSQL_HOST": os.getenv("MSSQL_HOST"),
        "MSSQL_DB": os.getenv("MSSQL_DB"),
        "MSSQL_USER": os.getenv("MSSQL_USER"),
        "MSSQL_PASS": os.getenv("MSSQL_PASS"),
        "CONFIG_FILE": os.getenv("CONFIG_FILE", "config.json")
    }

def carregar_config(caminho_config):
    """ -------------------------------------------------------------------
    Lê o arquivo JSON de configuração
    """
    with open(caminho_config, "r", encoding="utf-8") as f:
        return json.load(f)

def conectar_mysql(host, database, user, password):
    """ 
    Conecta ao MySQL
    """
    return mysql.connector.connect(
        host=host,
        database=database,
        user=user,
        password=password
    )

def conectar_sqlserver(host, database, user, password):
    """
    # Conecta ao SQL Server (sem ODBC, via pymssql)
    """
    return pymssql.connect(
        server=host,
        user=user,
        password=password,
        database=database
    )

def extrair_dados_mysql(conn, tabela_origem, colunas):
    """
    Extrai dados da tabela no MySQL
    """
    cursor = conn.cursor()
    query = f"SELECT {', '.join(colunas)} FROM {tabela_origem}"
    cursor.execute(query)
    rows = cursor.fetchall()
    cursor.close()
    return rows

def transformar_dados(rows):
    """ -------------------------------------------------------------------
    # Transforma dados
    """ 
    return [tuple(str(item).strip() if isinstance(item, str) else item for item in row) for row in rows]

def carregar_dados_sqlserver(conn, tabela_destino, colunas_destino, dados):
    """ -------------------------------------------------------------------
    # Carrega dados no SQL Server
    """ 
    cursor = conn.cursor()
    placeholders = ", ".join("%s" for _ in colunas_destino)  # pymssql usa %s
    query = f"INSERT INTO {tabela_destino} ({', '.join(colunas_destino)}) VALUES ({placeholders})"
    cursor.executemany(query, dados)
    conn.commit()
    cursor.close()

def executar_etl():
    """
    Orquestra o processo ETL
    """ 
    env = carregar_variaveis()
    config = carregar_config(env["CONFIG_FILE"])

    conn_mysql = conectar_mysql(env["MYSQL_HOST"], env["MYSQL_DB"], env["MYSQL_USER"], env["MYSQL_PASS"])
    conn_sql = conectar_sqlserver(env["MSSQL_HOST"], env["MSSQL_DB"], env["MSSQL_USER"], env["MSSQL_PASS"])

    for job in config["jobs"]:
        origem = job["origem"]
        destino = job["destino"]

        rows = extrair_dados_mysql(conn_mysql, origem["tabela"], origem["colunas"])
        dados_transformados = transformar_dados(rows)
        carregar_dados_sqlserver(conn_sql, destino["tabela"], destino["colunas"], dados_transformados)

    conn_mysql.close()
    conn_sql.close()

if __name__ == "__main__":
    """ -------------------------------------------------------------------
    Execução principal
    """
    executar_etl()
