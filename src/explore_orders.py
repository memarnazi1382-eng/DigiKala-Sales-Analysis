import pandas as pd

df = pd.read_csv("data/raw/orders.csv", low_memory=False)
df["DateTime_CartFinalize"] = pd.to_datetime(
    df["DateTime_CartFinalize"], errors="coerce"
)

print("--- Date range ---")
print(df["DateTime_CartFinalize"].min(), "->", df["DateTime_CartFinalize"].max())
print("Unparsed dates:", df["DateTime_CartFinalize"].isna().sum())

print("\n--- Unique counts ---")
print("Rows:", len(df))
print("Unique orders:", df["ID_Order"].nunique())
print("Unique customers:", df["ID_Customer"].nunique())
print("Unique items:", df["ID_Item"].nunique())
print("Unique cities:", df["city_name_fa"].nunique())

print("\n--- Rows per order ---")
print(df.groupby("ID_Order").size().describe())

print("\n--- Amount_Gross_Order ---")
print(df["Amount_Gross_Order"].describe())
print("Zero or negative amounts:", (df["Amount_Gross_Order"] <= 0).sum())

print("\n--- Quantity_item ---")
print(df["Quantity_item"].describe())
print(df["Quantity_item"].value_counts().head(10))

print("\n--- Top 10 cities ---")
print(df["city_name_fa"].value_counts().head(10))

print("\n--- Orders per year ---")
print(df.groupby(df["DateTime_CartFinalize"].dt.year)["ID_Order"].nunique())

print("\n--- Is amount repeated within an order? ---")
multi = df.groupby("ID_Order").filter(lambda g: len(g) > 1)
print(multi.sort_values("ID_Order").head(10).to_string())