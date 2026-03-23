# 005 — TDD Tests for plotter

**Date**: 2026-03-23
**Tool**: GitHub Copilot (VS Code)
**Model**: Claude Opus 4.6
**Iterations**: 1

## Prompt

**2026-03-23 00:00**

Write pytest tests for plotter.py. The module should:

Accept a pandas DataFrame with columns year_month and question_count
Create a time series plot of monthly Stack Overflow question counts
Add a 12-month rolling average line
Overlay milestone markers as vertical lines with labels
Return a matplotlib figure object without calling plt.show()

Write the tests BEFORE the implementation.

Include tests for:

Returning a valid matplotlib figure object
Plotting the main question count series
Plotting the 12-month rolling average
Rendering milestone markers on the chart

Save the diary entry and commit everything with a proper commit
message describing what was added.
