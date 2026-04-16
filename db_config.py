# ─── Connexion SQL Server (Docker) ───────────────────────────
# Généré automatiquement par fix_sqlserver_docker.sh
# Conteneur : sql_server | Port hôte : 1433

import pyodbc
from sqlalchemy import create_engine, text

SA_PASSWORD = "MonMotDePasseFort123!"
DATABASE    = "master"
SERVER      = "localhost,1433"

# ── Chaîne de connexion pyodbc
CONN_STR = (
    "DRIVER={ODBC Driver 18 for SQL Server};"
    f"SERVER={SERVER};"
    f"DATABASE={DATABASE};"
    "UID=sa;"
    f"PWD={SA_PASSWORD};"
    "TrustServerCertificate=yes;"
)

def test_pyodbc():
    conn = pyodbc.connect(CONN_STR)
    cursor = conn.cursor()
    cursor.execute("SELECT @@VERSION")
    print("pyodbc OK :", cursor.fetchone()[0][:60])
    conn.close()

def get_engine():
    url = (
        f"mssql+pyodbc://sa:{SA_PASSWORD}@localhost:{PORT}/{DATABASE}"
        "?driver=ODBC+Driver+18+for+SQL+Server"
        "&TrustServerCertificate=yes"
    )
    return create_engine(url)

def test_sqlalchemy():
    engine = get_engine()
    with engine.connect() as conn:
        result = conn.execute(text("SELECT @@VERSION"))
        print("SQLAlchemy OK :", result.fetchone()[0][:60])

if __name__ == "__main__":
    test_pyodbc()
    # test_sqlalchemy()
