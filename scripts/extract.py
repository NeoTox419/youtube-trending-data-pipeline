import requests
import pandas as pd
from datetime import datetime
from config.config import YOUTUBE_API_KEY, REGION_CODE

URL = "https://www.googleapis.com/youtube/v3/videos"

params = {
    "part": "snippet,statistics",
    "chart": "mostPopular",
    "regionCode": REGION_CODE,
    "maxResults": 50,
    "key": YOUTUBE_API_KEY
}

response = requests.get(URL, params=params)
data = response.json()

videos = []

for item in data.get("items", []):
    snippet = item["snippet"]
    stats = item.get("statistics", {})

    videos.append({
        "video_id": item["id"],
        "title": snippet["title"],
        "channel_title": snippet["channelTitle"],
        "category_id": snippet["categoryId"],
        "published_at": snippet["publishedAt"],
        "views": stats.get("viewCount", 0),
        "likes": stats.get("likeCount", 0),
        "comments": stats.get("commentCount", 0),
        "trending_date": datetime.today().strftime("%Y-%m-%d")
    })

df = pd.DataFrame(videos)

file_name = f"data/raw/trending_{datetime.today().strftime('%Y%m%d')}.csv"
df.to_csv(file_name, index=False)

print(f"Saved {len(df)} records to {file_name}")
