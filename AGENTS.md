# Repository Guidelines

This repository is currently a minimal scaffold (only `.gitignore`, `.specstory`, and `prompt_history.md` exist). Use this guide to keep contributions consistent as code is added.

## Project Structure & Module Organization

- Root: configuration and project docs (e.g., `AGENTS.md`, `.gitignore`).
- `.specstory/`: local tooling artifacts; do not edit manually unless you know the format.
- When adding code, prefer a conventional layout such as `src/` for application code and `tests/` for test suites. If the project is a single script, keep it at the root and document it here.

## Build, Test, and Development Commands

- No build or run commands are defined yet.
- When you introduce tooling, add commands to this section (examples):
  - `npm run dev` for local development
  - `npm test` or `pytest` for running tests
  - `npm run lint` or `ruff check .` for linting

## Coding Style & Naming Conventions

- Use 2 spaces for JSON/YAML and 4 spaces for Python unless the project adopts a formatter.
- Prefer descriptive, lowercase file and folder names (e.g., `time_tracker.py`, `src/time_tracker/`).
- If you add a formatter/linter (e.g., Prettier, Black, Ruff), include the config and update this section with the exact command.
- Keep each file focused on a single purpose and keep methods under 30–40 lines.
- Do not add code comments.
- Prefer the latest stable versions of libraries; avoid backward-compatibility workarounds.

## Testing Guidelines

- No testing framework is configured yet.
- When adding tests, colocate in `tests/` and use clear naming (e.g., `test_time_entry.py`, `timeEntry.spec.ts`).
- Document how to run the test suite and any required environment variables.

## Commit & Pull Request Guidelines

- Current Git history contains only two setup commits and does not establish a convention.
- Until a convention is adopted, use concise, imperative messages (e.g., `Add time entry model`).
- PRs should include a brief summary, testing notes, and screenshots or logs when changes are user-facing.

## Security & Configuration Tips

- Do not commit secrets. Use `.env` for local configuration; it is already ignored in `.gitignore`.
- If you add configuration templates, provide `.env.example` with safe defaults.
- For Streamlit, keep secrets in `.streamlit/secrets.toml` and share `.streamlit/secrets.toml.example` instead.
