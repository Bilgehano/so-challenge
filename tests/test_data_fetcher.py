"""Tests for the data_fetcher module."""

from pathlib import Path
from unittest.mock import patch, MagicMock

import pandas as pd
import pytest

from so_challenge.data_fetcher import fetch_monthly_questions, CACHE_PATH


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _make_api_page(year: int, month: int, count: int) -> dict:
    """Return a minimal Stack Exchange API response item."""
    return {
        "items": [{"count": count, "year": year, "month": month}],
        "has_more": False,
    }


def _build_fake_responses(status_code: int = 200) -> list[MagicMock]:
    """Build one mock response per month from 2008-01 to 2024-12."""
    responses = []
    for year in range(2008, 2025):
        for month in range(1, 13):
            resp = MagicMock()
            resp.status_code = status_code
            resp.raise_for_status = MagicMock()
            resp.json.return_value = _make_api_page(year, month, 100)
            responses.append(resp)
    return responses


# ---------------------------------------------------------------------------
# FR-1 / FR-2: Successful fetch returns correct DataFrame
# ---------------------------------------------------------------------------

class TestSuccessfulFetch:
    """Verify that a successful API call returns the expected DataFrame."""

    @patch("so_challenge.data_fetcher.requests.get")
    def test_returns_dataframe(self, mock_get, tmp_path):
        mock_get.side_effect = _build_fake_responses()
        df = fetch_monthly_questions(cache_dir=tmp_path)
        assert isinstance(df, pd.DataFrame)

    @patch("so_challenge.data_fetcher.requests.get")
    def test_dataframe_columns(self, mock_get, tmp_path):
        mock_get.side_effect = _build_fake_responses()
        df = fetch_monthly_questions(cache_dir=tmp_path)
        assert list(df.columns) == ["year_month", "question_count"]

    @patch("so_challenge.data_fetcher.requests.get")
    def test_dataframe_row_count(self, mock_get, tmp_path):
        """2008-01 through 2024-12 = 17 years x 12 months = 204 rows."""
        mock_get.side_effect = _build_fake_responses()
        df = fetch_monthly_questions(cache_dir=tmp_path)
        assert len(df) == 204

    @patch("so_challenge.data_fetcher.requests.get")
    def test_year_month_format(self, mock_get, tmp_path):
        mock_get.side_effect = _build_fake_responses()
        df = fetch_monthly_questions(cache_dir=tmp_path)
        # Every value should look like "YYYY-MM"
        assert df["year_month"].str.match(r"^\d{4}-\d{2}$").all()

    @patch("so_challenge.data_fetcher.requests.get")
    def test_question_count_dtype(self, mock_get, tmp_path):
        mock_get.side_effect = _build_fake_responses()
        df = fetch_monthly_questions(cache_dir=tmp_path)
        assert pd.api.types.is_integer_dtype(df["question_count"])


# ---------------------------------------------------------------------------
# NFR-1: Cached data is returned without a network call
# ---------------------------------------------------------------------------

class TestCaching:
    """Verify local CSV caching behaviour."""

    @patch("so_challenge.data_fetcher.requests.get")
    def test_cache_file_created(self, mock_get, tmp_path):
        mock_get.side_effect = _build_fake_responses()
        fetch_monthly_questions(cache_dir=tmp_path)
        assert (tmp_path / CACHE_PATH).exists()

    @patch("so_challenge.data_fetcher.requests.get")
    def test_cached_data_returned_without_network(self, mock_get, tmp_path):
        """Second call should read from cache; requests.get must not be called again."""
        mock_get.side_effect = _build_fake_responses()
        df1 = fetch_monthly_questions(cache_dir=tmp_path)

        mock_get.reset_mock()
        df2 = fetch_monthly_questions(cache_dir=tmp_path)

        mock_get.assert_not_called()
        pd.testing.assert_frame_equal(df1, df2)


# ---------------------------------------------------------------------------
# NFR-2: Network errors trigger retry logic
# ---------------------------------------------------------------------------

class TestRetryLogic:
    """Verify graceful handling of transient network errors."""

    @patch("so_challenge.data_fetcher.requests.get")
    def test_retries_on_server_error(self, mock_get, tmp_path):
        """A 500 followed by a success should still return valid data."""
        fail = MagicMock()
        fail.status_code = 500
        fail.raise_for_status.side_effect = Exception("Server Error")

        success = MagicMock()
        success.status_code = 200
        success.raise_for_status = MagicMock()
        success.json.return_value = _make_api_page(2008, 1, 42)

        # First call fails, second succeeds, then the rest succeed normally
        mock_get.side_effect = [fail, success] + _build_fake_responses()[1:]
        df = fetch_monthly_questions(cache_dir=tmp_path)
        assert isinstance(df, pd.DataFrame)
        assert len(df) == 204

    @patch("so_challenge.data_fetcher.requests.get")
    def test_raises_after_max_retries(self, mock_get, tmp_path):
        """After exhausting retries the function should raise an exception."""
        fail = MagicMock()
        fail.status_code = 500
        fail.raise_for_status.side_effect = Exception("Server Error")
        mock_get.return_value = fail

        with pytest.raises(Exception):
            fetch_monthly_questions(cache_dir=tmp_path)
