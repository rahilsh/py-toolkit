# Contributing to py-toolkit

Thanks for your interest in contributing! This document explains how to set up
your environment, propose changes, and get them merged.

## Code of Conduct

This project and everyone participating in it is governed by our
[Code of Conduct](CODE_OF_CONDUCT.md). By participating, you are expected to
uphold it.

## Getting Started

1. Fork the repository and clone your fork.
2. Create a virtual environment and install the project in editable mode with
   development dependencies:

   ```bash
   python -m venv .venv
   source .venv/bin/activate
   pip install -e ".[dev,db,xml]"
   ```

3. Install the pre-commit hooks:

   ```bash
   pre-commit install
   ```

## Development Workflow

1. Create a branch off `main`:

   ```bash
   git checkout -b feature/my-change
   ```

2. Make your changes, keeping them focused and small where possible.
3. Add or update tests for any behavior you change.
4. Run the quality checks locally (see below).
5. Commit using clear, conventional messages (e.g. `feat: ...`, `fix: ...`,
   `docs: ...`, `test: ...`, `chore: ...`).
6. Push your branch and open a Pull Request against `main`.

## Quality Checks

All of these run in CI and must pass before a PR can be merged:

```bash
# Lint
ruff check src/ tests/

# Format check
ruff format --check src/ tests/

# Tests with coverage (must stay >= 85%)
pytest --cov --cov-report=term-missing --cov-fail-under=85

# Run against all supported Python versions
tox
```

The pre-commit hooks run a subset of these automatically on every commit.

## Testing Guidelines

- Every new feature or bug fix should include tests.
- Tests live in `tests/` and mirror the package layout.
- Aim to keep total coverage at or above 85%.
- Use `requests-mock` for HTTP, and `hypothesis` for property-based tests where
  it adds value.

## Pull Request Guidelines

- Keep PRs focused on a single concern.
- Update the `README.md` and `CHANGELOG.md` when behavior or the public API
  changes.
- Ensure CI is green.
- Link any related issues in the PR description.

## Reporting Bugs & Requesting Features

Please use the GitHub issue templates:

- [Bug report](https://github.com/rahilsh/py-toolkit/issues/new?template=bug_report.md)
- [Feature request](https://github.com/rahilsh/py-toolkit/issues/new?template=feature_request.md)

## License

By contributing, you agree that your contributions will be licensed under the
[MIT License](LICENSE).
