# 001 — Project Setup

**Date**: 2026-03-23
**Tool**: GitHub Copilot (VS Code)
**Model**: Claude Opus 4.6
**Iterations**: 1

## Prompt

**2026-03-23 00:00**

Create a Python project called so-challenge using uv (from Astral)
for dependency management. The project should separate data
collection (data_fetcher.py) from visualization (plotter.py), with
a separate module for milestone definitions (milestones.py).

Set up pytest for testing with corresponding test files for each
module. Manage all dependencies through pyproject.toml — I'll need
pandas, matplotlib, requests, and pytest.

Include a README.md with a brief project description.

Create a diary/ folder for tracking AI interactions. For every
prompt cycle in this project, save the interaction record to this
folder as a numbered markdown file. Use this format:

# NNN — Short Title

**Date**: YYYY-MM-DD
**Tool**: [tool name]
**Model**: [model name]
**Iterations**: [number]

## Prompt

**YYYY-MM-DD HH:MM**

[The full prompt text as given by the user.]

If there were follow-up prompts (corrections, clarifications),
add each as a separate entry with its own timestamp under the
same Prompt section.

Save this initial setup prompt as diary/001-project-setup.md.

Do NOT implement any logic yet — just create the project structure,
configuration, and empty module files with docstrings describing
their purpose.

Initialize a git repository and create an initial commit with this
scaffolding. Then create a GitHub repository using the gh CLI and
push the initial commit.
