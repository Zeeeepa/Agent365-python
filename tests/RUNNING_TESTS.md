# Running Unit Tests for Agent365-Python SDK

This guide covers setting up and running tests in Visual Studio Code.

---

## Prerequisites

- **Python 3.11+** installed
- **Visual Studio Code** with Python extension
- **Git** repository cloned locally

---

## Test Structure

> **Note:** This structure will be updated as new tests are added.

```plaintext
tests/
├── runtime/                           # Runtime tests
├── observability/                     # Observability tests
├── tooling/                           # Tooling tests
└── notifications/                     # Notifications tests
```

---

## Initial Setup

### 1. Configure Python Environment

1. Press `Ctrl+Shift+P`
2. Type "Python: Select Interpreter"
3. Choose your Python 3.11+ interpreter

### 2. Install Dependencies

```powershell
# Install test dependencies
uv pip install pytest pytest-asyncio pytest-mock pytest-cov pytest-html

# Install workspace packages
uv pip install -e .
```

---

## Running Tests in VS Code

### Test Explorer

1. Click the beaker icon in the Activity Bar or press `Ctrl+Shift+P` → "Test: Focus on Test Explorer View"
2. Click the play button to run tests (all/folder/file/individual)
3. Right-click → "Debug Test" to debug with breakpoints

### Command Palette

- `Test: Run All Tests`
- `Test: Run Tests in Current File`
- `Test: Debug Tests in Current File`

---

## Running Tests from Command Line

```powershell
# Run all tests
python -m pytest tests/

# Run specific module/file
python -m pytest tests/runtime/
python -m pytest tests/runtime/test_environment_utils.py

# Run with options
python -m pytest tests/ -v                    # Verbose
python -m pytest tests/ -x                    # Stop on first failure
python -m pytest tests/ -k "environment"      # Pattern matching
python -m pytest --lf                         # Re-run failed tests
```

---

## Generating Reports

### HTML Reports

```powershell
# Coverage report
python -m pytest tests/ --cov=libraries --cov-report=html
Invoke-Item htmlcov\index.html

# Test report
python -m pytest tests/ --html=test-report.html --self-contained-html
Invoke-Item test-report.html

# Combined
python -m pytest tests/ --cov=libraries --cov-report=html --html=test-report.html --self-contained-html -v
```

### CI/CD Reports

```powershell
# XML reports for CI/CD pipelines
python -m pytest tests/ --cov=libraries --cov-report=xml --junitxml=test-results.xml
```

---

## Troubleshooting

### Common Issues

| Issue | Solution |
|-------|----------|
| **Test loading failed** | Clean pyproject.toml, reinstall packages, restart VS Code |
| **ImportError: No module named 'pytest'** | `uv pip install pytest pytest-asyncio pytest-mock` |
| **ImportError: No module named 'microsoft_agents_a365'** | `uv pip install -e .` |
| **Tests not discovered** | Refresh Test Explorer or restart VS Code |

### Fix Steps

If tests fail to discover or import errors occur:

**1. Clean pyproject.toml**

```powershell
$content = Get-Content "pyproject.toml" -Raw
$fixed = $content -replace "`r`n", "`n"
$fixed | Set-Content "pyproject.toml" -NoNewline
```

**2. Reinstall packages**

```powershell
uv pip install -e .
```

**3. Restart VS Code**

- Close completely and reopen
- Wait for Python extension to reload
- Refresh Test Explorer
