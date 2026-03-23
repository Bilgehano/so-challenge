"""Tests for the plotter module."""

import matplotlib
import matplotlib.pyplot as plt
import pandas as pd
import pytest

from so_challenge.plotter import plot_monthly_questions


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture()
def sample_df() -> pd.DataFrame:
    """A small DataFrame covering 24 months for fast, deterministic tests."""
    rows = [
        {"year_month": f"2020-{m:02d}", "question_count": 1000 + m * 10}
        for m in range(1, 13)
    ] + [
        {"year_month": f"2021-{m:02d}", "question_count": 1100 + m * 10}
        for m in range(1, 13)
    ]
    return pd.DataFrame(rows)


@pytest.fixture()
def milestones() -> list[dict]:
    """A pair of sample milestones that fall within the sample_df range."""
    return [
        {"date": "2020-06", "label": "Event A", "description": "First event"},
        {"date": "2021-03", "label": "Event B", "description": "Second event"},
    ]


# ---------------------------------------------------------------------------
# Test: Returns a valid matplotlib figure
# ---------------------------------------------------------------------------

class TestReturnsFigure:
    """The function must return a matplotlib Figure without calling plt.show()."""

    def test_returns_figure_object(self, sample_df, milestones):
        fig = plot_monthly_questions(sample_df, milestones)
        assert isinstance(fig, matplotlib.figure.Figure)
        plt.close(fig)

    def test_figure_has_axes(self, sample_df, milestones):
        fig = plot_monthly_questions(sample_df, milestones)
        assert len(fig.axes) >= 1
        plt.close(fig)


# ---------------------------------------------------------------------------
# Test: Main question-count series is plotted
# ---------------------------------------------------------------------------

class TestQuestionCountSeries:
    """The primary line should reflect the raw question_count data."""

    def test_main_line_exists(self, sample_df, milestones):
        fig = plot_monthly_questions(sample_df, milestones)
        ax = fig.axes[0]
        lines = ax.get_lines()
        assert len(lines) >= 1, "Expected at least one line on the axes"
        plt.close(fig)

    def test_main_line_data_length(self, sample_df, milestones):
        fig = plot_monthly_questions(sample_df, milestones)
        ax = fig.axes[0]
        # The first line should have as many points as the DataFrame rows
        main_line = ax.get_lines()[0]
        assert len(main_line.get_ydata()) == len(sample_df)
        plt.close(fig)


# ---------------------------------------------------------------------------
# Test: 12-month rolling average line
# ---------------------------------------------------------------------------

class TestRollingAverage:
    """A second line representing a 12-month rolling average should be present."""

    def test_rolling_average_line_exists(self, sample_df, milestones):
        fig = plot_monthly_questions(sample_df, milestones)
        ax = fig.axes[0]
        lines = ax.get_lines()
        assert len(lines) >= 2, "Expected at least two lines (raw + rolling avg)"
        plt.close(fig)

    def test_rolling_average_label(self, sample_df, milestones):
        fig = plot_monthly_questions(sample_df, milestones)
        ax = fig.axes[0]
        labels = [line.get_label() for line in ax.get_lines()]
        assert any("rolling" in lbl.lower() or "average" in lbl.lower() for lbl in labels), (
            f"No line labelled with 'rolling' or 'average'; got {labels}"
        )
        plt.close(fig)


# ---------------------------------------------------------------------------
# Test: Milestone markers rendered
# ---------------------------------------------------------------------------

class TestMilestoneMarkers:
    """Milestone dates should appear as vertical lines with text labels."""

    def test_vertical_lines_for_milestones(self, sample_df, milestones):
        fig = plot_monthly_questions(sample_df, milestones)
        ax = fig.axes[0]
        # axvline adds Line2D objects; we also accept collections from axvspan
        # Count vertical lines beyond the data lines (raw + rolling = 2)
        vlines = ax.get_lines()[2:]  # everything after the two data lines
        assert len(vlines) >= len(milestones), (
            f"Expected >= {len(milestones)} vertical milestone lines, got {len(vlines)}"
        )
        plt.close(fig)

    def test_milestone_text_labels(self, sample_df, milestones):
        fig = plot_monthly_questions(sample_df, milestones)
        ax = fig.axes[0]
        text_objects = [t.get_text() for t in ax.texts]
        for ms in milestones:
            assert any(ms["label"] in t for t in text_objects), (
                f"Milestone label '{ms['label']}' not found in axes texts: {text_objects}"
            )
        plt.close(fig)
