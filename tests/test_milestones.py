"""Tests for the milestones module."""

from datetime import datetime

import pytest

from so_challenge.milestones import MILESTONES

REQUIRED_LABELS = [
    "Transformer",
    "ChatGPT",
    "GPT-4",
    "Cursor & AI IDEs",
    "Claude Code",
    "GitHub Copilot Agent Mode",
]


# ---------------------------------------------------------------------------
# Test: Returns a collection of milestones
# ---------------------------------------------------------------------------

class TestMilestoneCollection:
    """MILESTONES should be a non-empty sequence."""

    def test_is_list(self):
        assert isinstance(MILESTONES, list)

    def test_not_empty(self):
        assert len(MILESTONES) >= len(REQUIRED_LABELS)


# ---------------------------------------------------------------------------
# Test: Each milestone has the expected structure
# ---------------------------------------------------------------------------

class TestMilestoneStructure:
    """Every entry must have 'date', 'label', and 'description' keys."""

    @pytest.mark.parametrize("key", ["date", "label", "description"])
    def test_required_keys_present(self, key):
        for ms in MILESTONES:
            assert key in ms, f"Milestone {ms} missing key '{key}'"

    def test_values_are_strings(self):
        for ms in MILESTONES:
            assert isinstance(ms["date"], str)
            assert isinstance(ms["label"], str)
            assert isinstance(ms["description"], str)


# ---------------------------------------------------------------------------
# Test: All required milestone labels are present
# ---------------------------------------------------------------------------

class TestRequiredLabels:
    """The predefined AI-breakthrough milestones must all appear."""

    def test_all_required_labels_present(self):
        labels = {ms["label"] for ms in MILESTONES}
        for expected in REQUIRED_LABELS:
            assert expected in labels, f"Missing milestone label: '{expected}'"


# ---------------------------------------------------------------------------
# Test: Milestone dates are parseable
# ---------------------------------------------------------------------------

class TestMilestoneDates:
    """Dates should be valid 'YYYY-MM' strings within the 2008-2024 range."""

    def test_dates_parseable(self):
        for ms in MILESTONES:
            parsed = datetime.strptime(ms["date"], "%Y-%m")
            assert parsed is not None, f"Could not parse date: {ms['date']}"

    def test_dates_within_range(self):
        for ms in MILESTONES:
            parsed = datetime.strptime(ms["date"], "%Y-%m")
            assert 2008 <= parsed.year <= 2024, (
                f"Milestone '{ms['label']}' date {ms['date']} outside 2008-2024"
            )
