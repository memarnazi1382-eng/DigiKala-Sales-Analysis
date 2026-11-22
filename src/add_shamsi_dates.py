from pathlib import Path
import pandas as pd
from persiantools.jdatetime import JalaliDate

SRC = Path("data/processed/orders_clean.csv")
OUT = Path("data/processed/shamsi_columns.xlsx")

MONTHS = [
    "فروردین", "اردیبهشت", "خرداد", "تیر", "مرداد", "شهریور",
    "مهر", "آبان", "آذر", "دی", "بهمن", "اسفند",
]

df = pd.read_csv(SRC, usecols=["order_id", "order_date"], parse_dates=["order_date"])

# Convert each unique date once (faster than converting every row)
dates = df["order_date"].dt.normalize()
mapping = {}
for d in dates.unique():
    d = pd.Timestamp(d)
    mapping[d] = JalaliDate.to_jalali(d.year, d.month, d.day)

jalali = dates.map(mapping)

out = pd.DataFrame({"order_id": df["order_id"]})
out["shamsi_date"] = jalali.map(lambda j: f"{j.year}/{j.month:02d}/{j.day:02d}")
out["shamsi_year"] = jalali.map(lambda j: j.year)
out["shamsi_month"] = jalali.map(lambda j: j.month)
out["shamsi_month_name"] = jalali.map(lambda j: MONTHS[j.month - 1])
out["shamsi_year_month"] = jalali.map(lambda j: f"{j.year}-{j.month:02d}")

out.to_excel(OUT, index=False)

print("Rows:", len(out))
print(out.head())
print("Shamsi years:", sorted(out["shamsi_year"].unique()))
print("Saved to:", OUT)