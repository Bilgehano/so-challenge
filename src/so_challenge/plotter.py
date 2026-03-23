"""Visualization module.

Provides functions for plotting and charting Stack Overflow data using matplotlib.
Consumes data prepared by data_fetcher and annotates plots with milestone markers.
"""

from __future__ import annotations

from datetime import datetime

import matplotlib
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import pandas as pd

matplotlib.use("Agg")  # non-interactive backend for headless environments


def plot_monthly_questions(
    df: pd.DataFrame,
    milestones: list[dict],
) -> matplotlib.figure.Figure:
    """Create a time-series plot of monthly SO question counts.

    Parameters
    ----------
    df:
        DataFrame with columns ``year_month`` (str) and ``question_count`` (int).
    milestones:
        List of dicts, each with ``date`` (str "YYYY-MM"), ``label``, and
        ``description``.

    Returns
    -------
    matplotlib.figure.Figure
    """
    fig, ax = plt.subplots(figsize=(14, 6))

    dates = [datetime.strptime(ym, "%Y-%m") for ym in df["year_month"]]
    y = df["question_count"].values

    # Primary series
    ax.plot(dates, y, label="Monthly questions", alpha=0.7)

    # 12-month rolling average
    rolling = df["question_count"].rolling(window=12, min_periods=1).mean()
    ax.plot(dates, rolling.values, label="12-month rolling average", linewidth=2)

    # Milestone markers
    for ms in milestones:
        ms_date = datetime.strptime(ms["date"], "%Y-%m")
        ax.axvline(ms_date, color="red", linestyle="--", alpha=0.6)
        ax.text(
            ms_date,
            ax.get_ylim()[1],
            ms["label"],
            rotation=90,
            verticalalignment="top",
            fontsize=8,
        )

    ax.xaxis.set_major_locator(mdates.YearLocator())
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y"))
    fig.autofmt_xdate()

    ax.set_xlabel("Year")
    ax.set_ylabel("Question Count")
    ax.set_title("Monthly Stack Overflow Question Counts (2008–2024)")
    ax.legend()

    fig.tight_layout()
    return fig
