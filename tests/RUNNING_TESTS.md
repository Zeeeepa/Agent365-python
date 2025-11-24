# Running Unit Tests for Agent365-Python SDK

## Quick Start

```bash
# Install dependencies
uv pip install -e libraries/microsoft-agents-a365-runtime
uv pip install pytest pytest-cov pytest-asyncio

# Run all tests
python -m pytest tests/

# Run with coverage
python -m pytest tests/runtime/ --cov=microsoft_agents_a365.runtime --cov-report=html
```

---

## Current Test Status

| Module | Tests | Status |
|--------|-------|--------|
| Runtime | 53 | ✅ Complete |
| Observability | ~20 | ⚠️ Partial |
| Tooling | 0 | ❌ Not Started |
| Notifications | 0 | ❌ Not Started |

**Coverage Target:** 80%+ | See [TEST_PLAN.md](TEST_PLAN.md) for roadmap

---

## Installation

```bash
# Runtime module only
uv pip install -e libraries/microsoft-agents-a365-runtime
uv pip install pytest pytest-cov pytest-asyncio

# All modules
uv pip install -e libraries/microsoft-agents-a365-observability-core
uv pip install -e libraries/microsoft-agents-a365-tooling
uv pip install -e libraries/microsoft-agents-a365-notifications
```

---

## Running Tests

```bash
# All tests
python -m pytest tests/

# Specific module
python -m pytest tests/runtime/

# Specific file
python -m pytest tests/runtime/test_environment_utils.py

# Specific test
python -m pytest tests/runtime/test_environment_utils.py::TestEnvironmentUtils::test_constants

# With verbose output
python -m pytest tests/runtime/ -v

# Stop on first failure
python -m pytest tests/runtime/ -x

# Pattern matching
python -m pytest tests/runtime/ -k "environment"

# Re-run failed tests only
python -m pytest --lf
```

---

## Coverage Reports

```bash
# Terminal output
python -m pytest tests/runtime/ --cov=microsoft_agents_a365.runtime --cov-report=term-missing

# HTML report (opens htmlcov/index.html)
python -m pytest tests/runtime/ --cov=microsoft_agents_a365.runtime --cov-report=html

# XML report (for CI/CD tools)
python -m pytest tests/runtime/ --cov=microsoft_agents_a365.runtime --cov-report=xml
```

---

## Advanced Options

```bash
# Parallel execution
uv pip install pytest-xdist
python -m pytest tests/runtime/ -n auto

# JUnit XML report
python -m pytest tests/runtime/ --junitxml=test-results.xml
```

---

## Understanding Output

```
tests/runtime/test_environment_utils.py::TestEnvironmentUtils::test_constants PASSED [  1%]
=================================== 53 passed in 0.18s ===================================
```

| Status | Description |
|--------|-------------|
| **PASSED** | Test passed successfully |
| **FAILED** | Test failed (shows error details) |
| **SKIPPED** | Test skipped |
| **ERROR** | Error during collection/setup |

---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| `ModuleNotFoundError` | `uv pip install -e libraries/microsoft-agents-a365-runtime` |
| `pytest: command not found` | `uv pip install pytest` |
| `ERROR: unrecognized arguments: --cov` | `uv pip install pytest-cov` |

---

## Test Structure

```
tests/
├── README.md                          # Overview
├── RUNNING_TESTS.md                   # This file
├── TEST_PLAN.md                       # Test strategy
└── runtime/
    ├── test_environment_utils.py      # 16 tests
    ├── test_version_utils.py          # 12 tests
    ├── test_utility.py                # 13 tests
    └── test_power_platform_api_discovery.py  # 12 tests
```
