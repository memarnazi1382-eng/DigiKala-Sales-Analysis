from pathlib import Path
import pandas as pd

raw_dir = Path("data/raw")

print("--- Files in data/raw ---")
for f in sorted(raw_dir.iterdir()):
    print(f.name)

matches = [f for f in raw_dir.glob("orders.*")]
if not matches:
    raise FileNotFoundError("No file named orders.* in data/raw")

path = matches[0]
print(f"\nReading: {path.name}")

if path.suffix.lower() == ".csv":
    try:
        df = pd.read_csv(path, low_memory=False)
    except UnicodeDecodeError:
        df = pd.read_csv(path, encoding="utf-8-sig", low_memory=False)
else:
    df = pd.read_excel(path)

print("\n--- Shape ---")
print(df.shape)

print("\n--- Columns ---")
print(df.columns.tolist())

print("\n--- First 5 rows ---")
print(df.head().to_string())

print("\n--- Data types ---")
print(df.dtypes)

print("\n--- Missing values ---")
print(df.isna().sum().sort_values(ascending=False))

print("\n--- Duplicate rows ---")
print(df.duplicated().sum())