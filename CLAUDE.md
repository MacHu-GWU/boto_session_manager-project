# Project Guide for AI Assistants

This document guides AI assistants on how to navigate and work with this project.

## Project Overview

`boto_session_manager` is a high-level wrapper around boto3. The core class `BotoSesManager` manages the creation and caching of AWS Sessions, Clients, and Resources, and provides common session management features such as assume role (with optional auto-refreshing credentials), AWS CLI environment variable injection via context manager, and credential snapshot serialization. This saves users from repeatedly wiring up boto3 session and credential logic in multi-account, multi-role scenarios.

The project maintains all 400+ AWS service client IDs as class attributes in `AwsServiceEnum`, and generates a typed lazy property for each service in `ClientMixin` (e.g. `bsm.s3_client`, `bsm.ec2_client`). These properties leverage `mypy-boto3-*` stub packages for IDE autocomplete and static type checking with zero runtime overhead. None of this code is hand-written — a code-generation script crawls the official boto3 documentation to collect every service name and ID into a spec file, then renders `services.py` and `clients.py` through Jinja2 templates. Whenever AWS releases new services, re-running the script brings everything up to date.

The project is currently being upgraded from 1.x to 2.0 (a major version bump). Tests run against real AWS accounts (integration tests), not mocks.

## Core Configuration Files

### Tool & Dependency Management
- `mise.toml` - Task runner and tool version management (Python 3.12, uv, claude)
- `pyproject.toml` - Python dependencies and package metadata
- `.venv/` - Virtual environment directory (created by uv)

Use `mise ls python --current` to see the exact Python version in use.

### CI/CD & Testing
- `.github/workflows/main.yml` - GitHub Actions CI workflow
- `codecov.yml` + `.coveragerc` - Code coverage reporting (codecov.io)
- `.readthedocs.yml` - Documentation hosting (readthedocs.org)

### Documentation
- `docs/source/` - Sphinx documentation source files
- `docs/source/conf.py` - Sphinx configuration

## Development Workflow

### Task Management
List all available tasks:
```bash
mise tasks ls
```

Run a specific task:
```bash
mise run ${task_name}
```

**Key tasks:**
- `inst` - Install all dependencies using uv (fast package manager)
- `cov` - Run unit tests with coverage report
- `build-doc` - Build Sphinx documentation

For complete task reference, run `mise run list-tasks` to generate `.claude/mise-tasks.md`.

### Testing Philosophy
This project uses **pytest** with a special pattern that allows running individual test files as standalone scripts.

**Example:** See `tests/test_api.py` - the `if __name__ == "__main__":` block demonstrates this pattern. It runs pytest as a subprocess with coverage tracking for the specific module, enabling quick isolated testing during development.

## Working with This Project

**Approach:**
1. Don't load entire files unnecessarily - read specific files only when needed
2. Use task commands (`mise run`) instead of direct tool invocation
3. Follow the testing pattern when creating new test files
4. Reference configuration files for specific settings rather than assuming defaults

**Tools in use:**
- **mise-en-place** - Development tool management
- **uv** - Fast Python package management
- **pytest** - Unit testing framework
- **sphinx** - Documentation generation
