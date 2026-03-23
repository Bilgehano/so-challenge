"""Data collection module.

Responsible for fetching data from external sources (e.g. the Stack Overflow API)
and returning it in a pandas-friendly format for downstream analysis.
"""

from __future__ import annotations

import time
from pathlib import Path

import pandas as pd
import requests

API_BASE = "https://api.stackexchange.com/2.3"
CACHE_PATH = "so_questions.csv"
MAX_RETRIES = 3
BACKOFF_BASE = 1  # seconds


def _fetch_month(year: int, month: int) -> dict:
    """Fetch question count for a single month with retry logic."""
    from calendar import monthrange

    import datetime as dt

    from_date = int(dt.datetime(year, month, 1, tzinfo=dt.timezone.utc).timestamp())
    last_day = monthrange(year, month)[1]
    to_date = int(dt.datetime(year, month, last_day, 23, 59, 59, tzinfo=dt.timezone.utc).timestamp())

    params = {
        "site": "stackoverflow",
        "fromdate": from_date,
        "todate": to_date,
        "filter": "total",
    }

    for attempt in range(MAX_RETRIES):
        resp = requests.get(f"{API_BASE}/questions", params=params)
        try:
            resp.raise_for_status()
        except Exception:
            if attempt == MAX_RETRIES - 1:
                raise
            time.sleep(BACKOFF_BASE * 2**attempt)
            continue
        data = resp.json()
        items = data.get("items", [])
        count = items[0]["count"] if items else 0
        return {"year": year, "month": month, "count": count}

    raise RuntimeError(f"Failed to fetch data for {year}-{month:02d}")


def fetch_monthly_questions(cache_dir: Path | None = None) -> pd.DataFrame:
    """Fetch monthly SO question counts for 2008-2024, with local CSV caching.

    Parameters
    ----------
    cache_dir:
        Directory for the CSV cache file. Defaults to the current directory.

    Returns
    -------
    pd.DataFrame
        Columns: year_month (str "YYYY-MM"), question_count (int).
    """
    if cache_dir is None:
        cache_dir = Path(".")
    cache_dir = Path(cache_dir)
    cache_file = cache_dir / CACHE_PATH

    if cache_file.exists():
        return pd.read_csv(cache_file)

    rows: list[dict] = []
    for year in range(2008, 2025):
        for month in range(1, 13):
            result = _fetch_month(year, month)
            rows.append(
                {
                    "year_month": f"{result['year']}-{result['month']:02d}",
                    "question_count": result["count"],
                }
            )

    df = pd.DataFrame(rows)
    df["question_count"] = df["question_count"].astype(int)
    cache_dir.mkdir(parents=True, exist_ok=True)
    df.to_csv(cache_file, index=False)
    return df
