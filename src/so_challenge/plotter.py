"""Visualization module.

Provides functions for plotting and charting Stack Overflow data using matplotlib.
Consumes data prepared by data_fetcher and annotates plots with milestone markers.
"""

from __future__ import annotations

import matplotlib
import matplotlib.pyplot as plt
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

    x = range(len(df))
    y = df["question_count"].values

    # Primary series
    ax.plot(x, y, label="Monthly questions")

    # 12-month rolling average
    rolling = df["question_count"].rolling(window=12, min_periods=1).mean()
    ax.plot(x, rolling.values, label="12-month rolling average")

    # Milestone markers
    ym_to_x = {ym: i for i, ym in enumerate(df["year_month"])}
    for ms in milestones:
        xi = ym_to_x.get(ms["date"])
        if xi is not None:
            ax.axvline(xi, color="red", linestyle="--", alpha=0.6)
            ax.text(
                xi,
                ax.get_ylim()[1],
                ms["label"],
                rotation=90,
                verticalalignment="top",
                fontsize=8,
            )

    ax.set_xlabel("Year")
    ax.set_ylabel("Count")
    ax.set_title("Monthly Stack Overflow Question Counts")
    ax.legend()

    fig.tight_layout()
    return fig
