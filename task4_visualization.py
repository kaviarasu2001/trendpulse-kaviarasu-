"""
Task 4 — Data Visualization
Creates charts from the processed Google Trends data.

Charts:
1. Top trends by estimated traffic
2. Top trends by related news count
3. Distribution of trend title word counts

Run Tasks 1 and 2 first.
"""

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

INPUT_FILE = Path("data/processed_trends.csv")
OUTPUT_DIR = Path("visualizations")


def save_bar_chart(df, value_column, title, filename, xlabel):
    chart_df = df.sort_values(value_column, ascending=True).tail(10)

    plt.figure(figsize=(10, 6))
    plt.barh(chart_df["trend"], chart_df[value_column])
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel("Trend")
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / filename, dpi=150)
    plt.close()


def main():
    if not INPUT_FILE.exists():
        raise FileNotFoundError(
            f"{INPUT_FILE} not found. Run task2_data_processing.py first."
        )

    df = pd.read_csv(INPUT_FILE)

    if df.empty:
        print("No data available for visualization.")
        return

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    save_bar_chart(
        df,
        "traffic_estimate",
        "Top 10 Google Trends — Estimated Traffic",
        "top_trends_by_traffic.png",
        "Estimated traffic",
    )

    save_bar_chart(
        df,
        "related_news_count",
        "Top 10 Google Trends — Related News",
        "top_trends_by_news.png",
        "Number of related news items",
    )

    plt.figure(figsize=(9, 6))
    plt.hist(df["word_count"], bins=range(1, int(df["word_count"].max()) + 2))
    plt.title("Distribution of Trend Title Length")
    plt.xlabel("Number of words")
    plt.ylabel("Number of trends")
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / "trend_word_count_distribution.png", dpi=150)
    plt.close()

    print("Visualization files created:")
    for path in OUTPUT_DIR.glob("*.png"):
        print(f" - {path}")


if __name__ == "__main__":
    main()
