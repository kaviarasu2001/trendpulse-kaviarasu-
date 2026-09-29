"""
Task 3 — Data Analysis
Analyses the processed trending dataset and prints a concise report.

Run Tasks 1 and 2 first.
"""

from pathlib import Path

import pandas as pd

INPUT_FILE = Path("data/processed_trends.csv")
REPORT_FILE = Path("data/analysis_report.txt")


def main():
    if not INPUT_FILE.exists():
        raise FileNotFoundError(
            f"{INPUT_FILE} not found. Run task2_data_processing.py first."
        )

    df = pd.read_csv(INPUT_FILE)

    if df.empty:
        print("No trend data available for analysis.")
        return

    top_by_traffic = df.sort_values("traffic_estimate", ascending=False).head(10)
    top_by_news = df.sort_values("related_news_count", ascending=False).head(10)

    avg_words = df["word_count"].mean()
    avg_news = df["related_news_count"].mean()
    median_traffic = df["traffic_estimate"].median()

    keyword_series = (
        df["trend"]
        .str.lower()
        .str.findall(r"\b[a-z0-9]{3,}\b")
        .explode()
        .dropna()
    )
    keyword_counts = keyword_series.value_counts().head(10)

    report_lines = [
        "TRENDPULSE — TREND ANALYSIS REPORT",
        "=" * 42,
        f"Total unique trends: {len(df)}",
        f"Average words per trend: {avg_words:.2f}",
        f"Average related news items: {avg_news:.2f}",
        f"Median estimated traffic: {median_traffic:,.0f}",
        "",
        "TOP 10 TRENDS BY ESTIMATED TRAFFIC",
        "-" * 42,
    ]

    for i, row in enumerate(top_by_traffic.itertuples(index=False), 1):
        report_lines.append(
            f"{i:>2}. {row.trend} — {row.traffic_estimate:,} estimated traffic"
        )

    report_lines += [
        "",
        "TOP 10 TRENDS BY RELATED NEWS COUNT",
        "-" * 42,
    ]

    for i, row in enumerate(top_by_news.itertuples(index=False), 1):
        report_lines.append(
            f"{i:>2}. {row.trend} — {row.related_news_count} related news items"
        )

    report_lines += [
        "",
        "MOST COMMON WORDS IN TREND TITLES",
        "-" * 42,
    ]

    for word, count in keyword_counts.items():
        report_lines.append(f"{word}: {count}")

    report = "\n".join(report_lines)

    print(report)

    REPORT_FILE.parent.mkdir(parents=True, exist_ok=True)
    REPORT_FILE.write_text(report, encoding="utf-8")
    print(f"\nSaved report to: {REPORT_FILE}")


if __name__ == "__main__":
    main()
