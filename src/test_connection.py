import pyodbc

DRIVER = "ODBC Driver 17 for SQL Server"

candidates = [
    "localhost",
    ".",
    r".\SQLEXPRESS",
    r"localhost\SQLEXPRESS",
    r"(localdb)\MSSQLLocalDB",
]

for server in candidates:
    conn_str = (
        f"DRIVER={{{DRIVER}}};"
        f"SERVER={server};"
        "DATABASE=master;"
        "Trusted_Connection=yes;"
        "TrustServerCertificate=yes;"
    )
    try:
        conn = pyodbc.connect(conn_str, timeout=5)
        print("WORKS:", server)
        conn.close()
    except Exception as e:
        print("failed:", server)