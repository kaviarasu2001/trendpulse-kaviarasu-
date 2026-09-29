"""
Task 2 — Data Processing
Cleans the raw Google Trends data, converts traffic values into numbers,
removes duplicates, and saves the processed dataset.

Run Task 1 first.
"""

import re
from pathlib import Path

import pandas as pd

INPUT_FILE = Path("data/raw_trends.csv")
OUTPUT_FILE = Path("data/processed_trends.csv")


def parse_traffic(value):
    """Convert values such as '20K+' or '1M+' to numeric estimates."""
    if pd.isna(value):
        return 0

    text = str(value).upper().strip().replace(",", "")
    match = re.search(r"([\d.]+)\s*([KMB]?)", text)

    if not match:
        return 0

    number = float(match.group(1))
    multiplier = {"": 1, "K": 1_000, "M": 1_000_000, "B": 1_000_000_000}
    return int(number * multiplier.get(match.group(2), 1))


def main():
    if not INPUT_FILE.exists():
        raise FileNotFoundError(
            f"{INPUT_FILE} not found. Run task1_data_collection.py first."
        )

    df = pd.read_csv(INPUT_FILE)

    # Standardize text columns.
    df["trend"] = (
        df["trend"]
        .astype(str)
        .str.replace(r"\s+", " ", regex=True)
        .str.strip()
    )

    df["traffic_estimate"] = df["traffic"].apply(parse_traffic)
    df["published_at"] = pd.to_datetime(df["published_at"], errors="coerce", utc=True)
    df["collected_at"] = pd.to_datetime(df["collected_at"], errors="coerce", utc=True)

    # Remove empty topics and duplicate trends.
    df = df[df["trend"].notna() & (df["trend"] != "")]
    df = df.drop_duplicates(subset=["trend"], keep="first")

    # Useful derived fields.
    df["trend_length"] = df["trend"].str.len()
    df["word_count"] = df["trend"].str.split().str.len()
    df["has_number"] = df["trend"].str.contains(r"\d", regex=True)

    # Sort by estimated traffic.
    df = df.sort_values(
        by=["traffic_estimate", "related_news_count"],
        ascending=False,
    ).reset_index(drop=True)

    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(OUTPUT_FILE, index=False)

    print(f"Processed {len(df)} unique trends.")
    print(f"Saved processed data to: {OUTPUT_FILE}")
    print("\nTop 10 trends:")
    print(df[["trend", "traffic_estimate", "related_news_count"]].head(10).to_string(index=False))


if __name__ == "__main__":
    main()
