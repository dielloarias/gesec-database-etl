# Projeto ETL MySQL → SQL Server

Este projeto implementa um **pipeline ETL (Extract, Transform, Load)** em Python para migrar dados de um banco **MySQL** para um banco **SQL Server**.  
Ele utiliza um arquivo de configuração (`config.json`) para definir quais tabelas e colunas serão processadas.

---

## ✨ Funcionalidades

- Leitura de variáveis de ambiente a partir de um arquivo `.env`
- Extração de dados de tabelas no MySQL
- Transformação simples de dados (remoção de espaços, normalização)
- Carga dos dados em tabelas do SQL Server
- Arquitetura modular e extensível

---

## 📂 Estrutura do Projeto

```
.
├── etl.py              # Script principal com o processo ETL
├── config.json         # Configuração de tabelas origem e destino
├── .env                # Variáveis de ambiente (credenciais e conexões)
└── README.md           # Documentação do projeto
```

---

## ⚙️ Dependências

As dependências podem ser instaladas com:

```bash
pip install -r requirements.txt
```

### Pacotes principais

- `mysql-connector-python` → Conexão com MySQL  
- `pymssql` → Conexão com SQL Server (sem ODBC)  
- `python-dotenv` → Gerenciamento de variáveis de ambiente  
- `json` (built-in) → Manipulação do arquivo de configuração  

Crie um arquivo `requirements.txt` com o seguinte conteúdo:

```
mysql-connector-python
pymssql
python-dotenv
```

---

## 🚀 Execução

1. Configure o arquivo `.env` com as credenciais de banco e o caminho do arquivo de configuração:
   ```ini
   MYSQL_HOST=localhost
   MYSQL_DB=nome_do_banco_mysql
   MYSQL_USER=usuario_mysql
   MYSQL_PASS=senha_mysql

   MSSQL_HOST=localhost
   MSSQL_DB=nome_do_banco_sqlserver
   MSSQL_USER=usuario_sqlserver
   MSSQL_PASS=senha_sqlserver

   CONFIG_FILE=config.json
   ```

2. Defina os **jobs de ETL** no `config.json`, por exemplo:
   ```json
   {
     "jobs": [
       {
         "origem": {
           "tabela": "users",
           "colunas": ["username", "email", "password_hash", "salt", "created_at", "updated_at"]
         },
         "destino": {
           "tabela": "dbo.users",
           "colunas": ["username", "email", "password_hash", "salt", "created_at", "updated_at"]
         }
       }
     ]
   }
   ```

3. Execute o script:
   ```bash
   python etl.py
   ```

---

## 👤 Autor

**Diello Cardoso de La Paz Arias**

---

## 📜 Licença

Este projeto é de uso educacional e pode ser adaptado para necessidades específicas de ETL.
