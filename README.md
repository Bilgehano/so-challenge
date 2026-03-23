# so-challenge

Stack Overflow data collection and visualization project.

## Overview

This project fetches data from the Stack Overflow API, processes it with pandas, and produces matplotlib visualizations annotated with key milestone events.

## Project Structure

- `src/so_challenge/data_fetcher.py` — Data collection from external sources
- `src/so_challenge/plotter.py` — Visualization and charting
- `src/so_challenge/milestones.py` — Milestone event definitions
- `tests/` — pytest test suite

## Setup

```bash
uv sync
```

## Running Tests

```bash
uv run pytest
```
