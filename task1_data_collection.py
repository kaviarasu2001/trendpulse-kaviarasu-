"""
Task 1 — Data Collection
Fetches current Google Trends daily trending searches for India
and saves the raw results as data/raw_trends.csv.

Install:
    pip install requests
"""

import csv
import html
import re
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
from pathlib import Path

import requests

RSS_URL = "https://trends.google.com/trending/rss?geo=IN"
OUTPUT_DIR = Path("data")
OUTPUT_FILE = OUTPUT_DIR / "raw_trends.csv"


def clean_text(value: str) -> str:
    """Remove HTML and normalize whitespace."""
    value = html.unescape(value or "")
    value = re.sub(r"<[^>]+>", " ", value)
    return re.sub(r"\s+", " ", value).strip()


def fetch_trends():
    """Fetch and parse the Google Trends RSS feed."""
    response = requests.get(
        RSS_URL,
        timeout=20,
        headers={"User-Agent": "TrendPulse/1.0"},
    )
    response.raise_for_status()

    root = ET.fromstring(response.content)
    items = []

    for item in root.findall(".//item"):
        title = clean_text(item.findtext("title"))
        traffic = clean_text(item.findtext("ht:approx_traffic", namespaces={
            "ht": "https://trends.google.com/trending/rss"
        }))
        pub_date = clean_text(item.findtext("pubDate"))
        news_items = [
            clean_text(n.text)
            for n in item.findall("ht:news_item/ht:news_item_title",
                                  namespaces={"ht": "https://trends.google.com/trending/rss"})
            if n.text
        ]

        if title:
            items.append({
                "trend": title,
                "traffic": traffic,
                "published_at": pub_date,
                "related_news_count": len(news_items),
            })

    return items


def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    trends = fetch_trends()

    collected_at = datetime.now(timezone.utc).isoformat()

    with OUTPUT_FILE.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(
            file,
            fieldnames=[
                "trend",
                "traffic",
                "published_at",
                "related_news_count",
                "collected_at",
            ],
        )
        writer.writeheader()

        for row in trends:
            row["collected_at"] = collected_at
            writer.writerow(row)

    print(f"Collected {len(trends)} trending topics.")
    print(f"Saved raw data to: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
