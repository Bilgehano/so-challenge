"""Main entry point for the so-challenge project.

Fetches (or loads cached) monthly Stack Overflow question counts,
overlays AI milestone markers, and saves the resulting plot.
"""

import matplotlib.pyplot as plt

from so_challenge.data_fetcher import fetch_monthly_questions
from so_challenge.milestones import MILESTONES
from so_challenge.plotter import plot_monthly_questions


def main() -> None:
    df = fetch_monthly_questions()
    fig = plot_monthly_questions(df, MILESTONES)
    fig.savefig("so_trends.png", dpi=150)
    print("Saved so_trends.png")
    plt.show()


if __name__ == "__main__":
    main()
