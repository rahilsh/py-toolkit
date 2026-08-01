# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- `py_toolkit.git.github` module with `fork_repo`, `delete_repo`, and
  `read_repo_names` helpers (modernised from the original `github_create_fork.py`
  and `github_delete_repo.py` scripts).
- `py_toolkit.git.git_config` module with `find_git_configs`,
  `replace_in_git_config`, and `replace_username_in_configs` helpers (modernised
  from the original `replace_username_in_git_config.py` script).
- `GitError` exception for git/GitHub operation failures.
- `git-config-replace` CLI subcommand.
- `LICENSE` file (MIT).
- `py.typed` marker so type hints are exposed to consumers (PEP 561).
- Community health files: `CONTRIBUTING.md`, `CODE_OF_CONDUCT.md`,
  `SECURITY.md`, issue templates, and a pull request template.
- CI test matrix across Python 3.9–3.13.

### Changed
- Moved the changelog out of `README.md` into this file.
- Dropped support for Python 3.9 (minimum is now 3.10) to align with the
  `setuptools >= 83` build requirement.

### Removed
- Internal one-off scripts (`scripts/`) and `resources/` that were specific to
  the original author's environment.
- Zendesk integration module (`py_toolkit.zendesk`) and its tests.

## [0.2.0] - 2026-06-01

### Added
- Full type hints on all public functions.
- Proper logging (replaced all `print()` calls).
- Custom exception hierarchy.
- CLI entry point with `csv`, `serve`, and `xml2json` commands.
- Pre-commit hooks configuration.
- tox configuration for multi-version testing.
- Environment-variable-based configuration for secrets and paths.
- Docstrings on all public APIs.
- 95%+ test coverage.

### Changed
- Moved one-off scripts out of the published package.

## [0.1.0] - 2026-05-01

### Added
- Initial release with CSV, PDF, server, and HTTP utilities.
- Python-recommended `src/` layout.
- `pyproject.toml`-based packaging.

[Unreleased]: https://github.com/rahilsh/py-toolkit/compare/v0.2.0...HEAD
[0.2.0]: https://github.com/rahilsh/py-toolkit/compare/v0.1.0...v0.2.0
[0.1.0]: https://github.com/rahilsh/py-toolkit/releases/tag/v0.1.0
