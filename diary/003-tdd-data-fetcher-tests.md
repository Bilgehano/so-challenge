# 003 — TDD Tests for data_fetcher

**Date**: 2026-03-23
**Tool**: GitHub Copilot (VS Code)
**Model**: Claude Opus 4.6
**Iterations**: 1

## Prompt

**2026-03-23 00:00**

Write pytest tests for `data_fetcher.py`. The module should:
- Fetch monthly SO question counts (2008-2024)
- Return a pandas DataFrame with columns: year_month, question_count
- Cache results locally as CSV
- Handle network errors gracefully

Write the tests BEFORE the implementation. Use unittest.mock to
mock API/network calls in tests. Include tests for:
- Successful data fetch returns correct DataFrame shape
- Cached data is returned without network call
- Network error triggers retry logic

Save the diary entry and commit everything with a proper commit
message describing what was added.
