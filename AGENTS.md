# Repository Guidelines

## Project Structure & Module Organization
Plan for a small, clear layout. Specify UI requirements in `src/ui/README.md` (features, layout notes, UX constraints) and keep API requirements in `src/api/README.md` (endpoints, auth, rate limits):
- `src/` for Python source code
- `src/ui/` for Streamlit app modules
- `src/api/` for the non-UI API (e.g., FastAPI/Flask)
- `src/core/` for shared domain logic (timers, storage, validation)
- `tests/` for automated tests
- `scripts/` for developer utilities
- `configs/` for configuration templates and app settings
- `.github/workflows/` for CI pipelines

## Build, Test, and Development Commands
Define commands in `pyproject.toml` or `Makefile` and document them here. Suggested defaults:
- `python -m venv .venv && source .venv/bin/activate` to set up the environment
- `pip install -r requirements.txt` to install dependencies
- `streamlit run src/ui/app.py` to run the UI
- `uvicorn src.api.main:app --reload` to run the FastAPI server
- `pytest` to run tests

## Coding Style & Naming Conventions
Use Python 3.11+. Keep imports sorted and formatting consistent:
- Formatting: Black (`black src tests`)
- Linting: Ruff (`ruff check src tests`)
- Type checking: Mypy (`mypy src`)
Naming:
- Modules/files: `snake_case.py`
- Classes: `PascalCase`
- Functions/variables: `snake_case`
- Constants: `UPPER_SNAKE_CASE`

## Testing Guidelines
Use `pytest` with tests in `tests/` and names like `test_*.py`. Cover core timer logic and API endpoints. Prefer unit tests for `src/core/` and lightweight integration tests for API routes. Document testing requirements (coverage goals, fixtures, and mocks) in `tests/README.md`.

## Commit & Pull Request Guidelines
Use concise, imperative commit messages (e.g., `Add timer model`). For pull requests:
- Describe the change and scope
- Link related issues
- Include screenshots for UI changes
- Note any new environment variables

## Deployment Requirements
Document deployment requirements in `configs/DEPLOYMENT.md` (hosting, env vars, ports, and process manager). Use GitHub Actions for CI in `.github/workflows/`. Add scheduled CRON workflows only after the main code is shipped.

## Dependency Management
Use GitHub-native dependency updates (Dependabot). Configure `dependabot.yml` in `.github/` and keep updates grouped (e.g., `pip` weekly) to reduce PR noise.

## Security & Configuration Tips
Do not commit secrets. Store local config in `.env` and document required variables in `.env.example`. Keep API keys out of source and CI logs.

## Agent-Specific Notes
Maintain `prompt_history.md` as a running, verbatim log of every user request each session. Append new entries rather than replacing the file. If you add architecture changes or new tooling, update this guide alongside the code to keep onboarding friction low.
Automatically append every new user request/command to `prompt_history.md` as it comes in so the log stays complete without manual reminders.
