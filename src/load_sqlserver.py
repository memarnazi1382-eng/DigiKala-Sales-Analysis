from pathlib import Path
import pandas as pd
from sqlalchemy import create_engine, text, types
from sqlalchemy.engine import URL

SERVER = "localhost"
DATABASE = "DigikalaDB"
DRIVER = "ODBC Driver 17 for SQL Server"
CSV_PATH = Path("data/processed/orders_clean.csv")


def make_url(db_name):
    odbc = (
        f"DRIVER={{{DRIVER}}};SERVER={SERVER};DATABASE={db_name};"
        "Trusted_Connection=yes;TrustServerCertificate=yes;"
    )
    return URL.create("mssql+pyodbc", query={"odbc_connect": odbc})


# 1. Create the database if it does not exist
master_engine = create_engine(make_url("master"), isolation_level="AUTOCOMMIT")
with master_engine.connect() as conn:
    conn.execute(text(
        f"IF DB_ID('{DATABASE}') IS NULL CREATE DATABASE {DATABASE}"
    ))
print("Database ready:", DATABASE)

# 2. Read the cleaned CSV
df = pd.read_csv(
    CSV_PATH,
    parse_dates=["order_datetime", "order_date"],
    low_memory=False,
)
print("Rows in CSV:", len(df))

# 3. Load into SQL Server
engine = create_engine(make_url(DATABASE), fast_executemany=True)

df.to_sql(
    "orders",
    engine,
    if_exists="replace",
    index=False,
    chunksize=10000,
    dtype={
        "city": types.NVARCHAR(100),
        "year_month": types.VARCHAR(7),
    },
)

# 4. Verify
with engine.connect() as conn:
    count = conn.execute(text("SELECT COUNT(*) FROM orders")).scalar()
print("Rows in SQL Server table 'orders':", count)