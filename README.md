# TrendPulse

A 4-stage Python data pipeline that collects current Google Trends data for India, cleans it, analyses it, and creates visualizations.

## Files

- `task1_data_collection.py` — fetches current Google Trends RSS data
- `task2_data_processing.py` — cleans and transforms the data
- `task3_analysis.py` — produces an analysis report
- `task4_visualization.py` — creates PNG charts

## Setup

```bash
pip install -r requirements.txt
```

## Run

Run the scripts in this order:

```bash
python task1_data_collection.py
python task2_data_processing.py
python task3_analysis.py
python task4_visualization.py
```

The scripts create:

- `data/raw_trends.csv`
- `data/processed_trends.csv`
- `data/analysis_report.txt`
- `visualizations/*.png`

## Data source

Google Trends RSS, India (`geo=IN`).

Because trending data changes over time, the exact output will depend on when Task 1 is executed.
