from pathlib import Path
import pandas as pd

raw_path = Path("data/raw/orders.csv")
out_dir = Path("data/processed")
out_dir.mkdir(parents=True, exist_ok=True)

df = pd.read_csv(raw_path, low_memory=False)
rows_before = len(df)

# 1. Rename columns to simple names
df = df.rename(columns={
    "ID_Order": "order_id",
    "ID_Customer": "customer_id",
    "ID_Item": "item_id",
    "DateTime_CartFinalize": "order_datetime",
    "Amount_Gross_Order": "amount",
    "city_name_fa": "city",
    "Quantity_item": "quantity",
})

# 2. Fix data types
df["order_datetime"] = pd.to_datetime(df["order_datetime"], errors="coerce")
df["quantity"] = df["quantity"].astype(int)

# 3. Add time columns
df["order_date"] = df["order_datetime"].dt.normalize()
df["year"] = df["order_datetime"].dt.year
df["month"] = df["order_datetime"].dt.month
df["year_month"] = df["order_datetime"].dt.to_period("M").astype(str)

# 4. Remove rows with zero or negative amount
bad_amount = df["amount"] <= 0
print("Rows with zero/negative amount removed:", bad_amount.sum())
df = df[~bad_amount]

# 5. Flag (do NOT delete) unusual values
amount_limit = df["amount"].quantile(0.99)
df["is_high_amount"] = df["amount"] > amount_limit
df["is_high_quantity"] = df["quantity"] >= 50

# 6. Save
out_path = out_dir / "orders_clean.csv"
df.to_csv(out_path, index=False, encoding="utf-8-sig")

print("Rows before:", rows_before)
print("Rows after:", len(df))
print("High amount rows flagged:", df["is_high_amount"].sum())
print("High quantity rows flagged:", df["is_high_quantity"].sum())
print("Saved to:", out_path)

# 7. Check: is amount per unit or total for the line?
single = df[df["quantity"] == 1].groupby("item_id")["amount"].median()
multi = df[df["quantity"] >= 2].copy()
multi["single_price"] = multi["item_id"].map(single)
multi = multi.dropna(subset=["single_price"])
multi = multi[multi["single_price"] > 0]
ratio = (multi["amount"] / multi["single_price"]).median()
print("\nMedian of (amount / single-unit price):", round(ratio, 2))
print("Median quantity of those rows:", multi["quantity"].median())