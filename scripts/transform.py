import pandas as pd
import json
from pathlib import Path

RAW_DIR = Path("data/raw")
PROCESSED_DIR = Path("data/processed")
CATEGORY_FILE = Path("config/video_categories.json")

PROCESSED_DIR.mkdir(exist_ok=True)

# Load latest raw file
latest_file = max(RAW_DIR.glob("trending_*.csv"))

df = pd.read_csv(latest_file)

# Enforce schema
df["views"] = pd.to_numeric(df["views"], errors="coerce").fillna(0).astype(int)
df["likes"] = pd.to_numeric(df["likes"], errors="coerce").fillna(0).astype(int)
df["comments"] = pd.to_numeric(df["comments"], errors="coerce").fillna(0).astype(int)

df["published_at"] = pd.to_datetime(df["published_at"])
df["trending_date"] = pd.to_datetime(df["trending_date"])

# Load category mapping
with open(CATEGORY_FILE, "r") as f:
    category_map = json.load(f)

df["category_name"] = df["category_id"].astype(str).map(category_map)
df["category_name"].fillna("Unknown", inplace=True)

# Save processed file
output_file = PROCESSED_DIR / latest_file.name.replace("trending", "processed")
df.to_csv(output_file, index=False)

print(f"Processed data saved to {output_file}")