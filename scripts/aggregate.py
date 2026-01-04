import pandas as pd
from pathlib import Path

PROCESSED_DIR = Path("data/processed")
AGG_DIR = Path("data/aggregated")

AGG_DIR.mkdir(exist_ok=True)

# Load latest processed file
latest_file = max(PROCESSED_DIR.glob("processed_*.csv"))
df = pd.read_csv(latest_file)

# 1. Top Creators (Channels)
top_creators = (
    df.groupby("channel_title")
    .agg(
        total_views=("views", "sum"),
        total_likes=("likes", "sum"),
        total_comments=("comments", "sum"),
        video_count=("video_id", "count")
    )
    .reset_index()
    .sort_values(by="total_views", ascending=False)
)

top_creators.to_csv(AGG_DIR / "top_creators.csv", index=False)

# 2. Top Categories
top_categories = (
    df.groupby("category_name")
    .agg(
        total_views=("views", "sum"),
        total_likes=("likes", "sum"),
        total_comments=("comments", "sum"),
        video_count=("video_id", "count")
    )
    .reset_index()
    .sort_values(by="total_views", ascending=False)
)

top_categories.to_csv(AGG_DIR / "top_categories.csv", index=False)

# 3. Top Videos
top_videos = (
    df.sort_values(by="views", ascending=False)
    .head(50)[
        [
            "video_id",
            "title",
            "channel_title",
            "category_name",
            "views",
            "likes",
            "comments"
        ]
    ]
)

top_videos.to_csv(AGG_DIR / "top_videos.csv", index=False)

print("Aggregation completed successfully.")