# Microsoft Agent 365 Package Build Script

This directory contains a build script to compile all Python packages in the Microsoft Agent 365 project. The script automatically discovers all `pyproject.toml` files and builds wheel packages from them using modern, fast build tools.

**Note: By default, the script excludes samples and test directories to focus on core packages. Use explicit include patterns to build samples or tests when needed.**

## Build Script

### Python Script (`build-packages.py`)
**Cross-platform solution with modern `uv` build system**

The build script uses the ultra-fast `uv build --wheel` command for significantly improved build performance and better dependency management.

```bash
# Basic usage - excludes samples and tests by default
python build-packages.py

# Clean build
python build-packages.py --clean

# Verbose output
python build-packages.py --verbose

# Custom output directory
python build-packages.py --output-dir my-dist

# Include only specific packages (overrides default exclusions)
python build-packages.py --include tooling observability

# Build samples explicitly (overrides default exclusion)
python build-packages.py --include samples

# Exclude additional packages beyond defaults
python build-packages.py --exclude wrappers
```

## Prerequisites

- Python 3.9 or higher
- `uv` package manager (automatically checked, install with `pip install uv`)

## Performance Benefits

The build script uses `uv build --wheel` which provides:
- **🚀 Significantly faster builds** - Up to 10x faster than traditional Python build tools
- **🔒 Better dependency isolation** - Built with Rust for improved reliability
- **🔧 Modern build system** - Uses latest Python packaging standards
- **🛡️ Enhanced error handling** - Robust Windows file locking support

## Package Discovery

The script automatically discovers and builds packages in the following locations:

**Default Behavior: Excludes `samples/` and `test/` directories automatically**

### Core Packages (Built by Default)
- **Main Package**: `./pyproject.toml` - Main Microsoft Kairo package
- **Observability**: `./microsoft_kairo/observability/` - Core observability package  
- **Notifications**: `./microsoft_kairo/notification/` - Notification extensions

### Tooling Packages (Built by Default)
- **Common Tooling**: `./microsoft_kairo/tooling/common/` - Shared tooling utilities
- **OpenAI Tooling**: `./microsoft_kairo/tooling/openai/` - OpenAI integration
- **Semantic Kernel Tooling**: `./microsoft_kairo/tooling/semantic_kernel/` - SK integration
- **Azure Foundry Tooling**: `./microsoft_kairo/tooling/azurefoundry/` - Azure AI Foundry integration

### Extension Packages (Built by Default)
- **OpenAI Observability**: `./microsoft_kairo/observability/wrappers/openai_agents/` - OpenAI tracing extensions
- **LangChain Observability**: `./microsoft_kairo/observability/wrappers/langchain/` - LangChain tracing extensions
- **Semantic Kernel Observability**: `./microsoft_kairo/observability/wrappers/semantic_kernel/` - SK tracing extensions

### Sample Packages (Excluded by Default)
- **Sample OpenAI Agent**: `./samples/sample_openai_agent/` - Example implementation

To build samples, use explicit include patterns:
```bash
python build-packages.py --include samples
```

## Package Names

The built packages use the following naming convention:

| Directory | Package Name |
|-----------|--------------|
| Root | `microsoft-kairo` |
| observability | `microsoft-agents-a365-observability` |
| notification | `microsoft-agents-a365-notifications` |
| tooling/common | `microsoft-agents-a365-tooling` |
| tooling/openai | `microsoft-agents-a365-tooling-extensions-openai` |
| tooling/semantic_kernel | `microsoft-agents-a365-tooling-extensions-semantickernel` |
| tooling/azurefoundry | `microsoft-agents-a365-tooling-extensions-azureaifoundry` |
| observability/wrappers/openai_agents | `microsoft-agents-a365-observability-extensions-openai` |
| observability/wrappers/langchain | `microsoft-agents-a365-observability-extensions-langchain` |
| observability/wrappers/semantic_kernel | `microsoft-agents-a365-observability-extensions-semantic-kernel` |
| samples/sample_openai_agent | `sample-openai-agent` |

## Default Exclusions

**Important:** The build script excludes the following directories by default:
- `samples/` - Example and demonstration code
- `test/` - Test packages and directories

This ensures that production builds focus on core packages. To include excluded packages, use explicit include patterns:

```bash
# Include samples
python build-packages.py --include samples

# Include everything (overrides default exclusions)
python build-packages.py --include "*"
```

## Output

All built wheel files (`.whl`) are placed in the `dist/` directory by default. The scripts provide:

- **🎯 Progress indicators** for each package being built
- **✅ Success/failure status** for each build with colored output
- **📊 Summary statistics** at the end
- **📦 List of built packages** with their filenames
- **⚡ Performance metrics** showing build speed improvements with `uv`

### Sample Output
```
=== Microsoft Agent 365 Package Builder ===

Checking prerequisites...
Output directory: D:\Agent365\python\dist

Discovering packages...
Found 10 packages to build:
  - .
  - microsoft_kairo\notification
  - microsoft_kairo\observability
  ...

[1/10] Building .
Building package in: D:\Agent365\python
  Running: uv build --wheel
  ✓ Built: microsoft_kairo-2025.10.15+preview.112152-py3-none-any.whl

=== Build Summary ===
Total packages: 10
Successful: 10
Failed: 0

Built packages are available in: D:\Agent365\python\dist
```

## Build Order Considerations

The scripts build packages independently, but when installing, you should consider dependencies:

1. Install core packages first: `microsoft-kairo`, `microsoft-agents-a365-observability`
2. Install tooling base: `microsoft-agents-a365-tooling`
3. Install extensions: tooling and observability extensions
4. Install notification package: `microsoft-agents-a365-notifications`

## Troubleshooting

### Common Issues

**uv not found (Python script):**
```bash
pip install uv
```

**Build module not found (PowerShell/Batch):**
```bash
pip install build
```

**Permission errors on Windows:**
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

**Python not in PATH:**
- Ensure Python is properly installed and added to system PATH
- Use full path to Python executable if needed

**Windows file locking issues:**
The Python script now includes robust handling for Windows file locking with automatic retry logic.

### Performance Comparison

**Before (python -m build):**
- ~60-90 seconds for all packages
- Sequential dependency resolution
- Limited error recovery

**After (uv build --wheel):**
- ~15-25 seconds for all packages ⚡
- Modern dependency resolution
- Enhanced error handling and recovery

### Verbose Output

Use the verbose flag (`-Verbose`, `--verbose`) to see detailed build output for debugging failed builds.

### Selective Building

Use include/exclude patterns to build only specific packages during development:

```powershell
# Build only observability packages
.\build-packages.ps1 -Include @("observability")

# Build only core packages (default behavior)
.\build-packages.ps1

# Include samples in build (overrides default exclusion)
.\build-packages.ps1 -Include @("samples")

# Build everything including samples and tests
.\build-packages.ps1 -Include @("*")

# Exclude wrapper packages but build everything else
.\build-packages.ps1 -Exclude @("wrappers")
```

## Development Workflow

For active development, you can use the clean flag to ensure fresh builds:

```bash
# Clean build of core packages only (default) - FAST with uv!
python build-packages.py --clean --verbose

# Clean build including samples for testing
python build-packages.py --clean --verbose --include samples

# Clean build of specific components
python build-packages.py --clean --include observability tooling
```

This removes all previous build artifacts before building, ensuring no stale files interfere with the build process.

### Typical Build Scenarios

```bash
# Daily development - core packages only (⚡ ~15 seconds)
python build-packages.py

# Testing with samples (⚡ ~20 seconds)
python build-packages.py --include samples

# Full CI/CD build including everything (⚡ ~25 seconds)
python build-packages.py --include "*" --clean

# Debug specific package with detailed output
python build-packages.py --include tooling --verbose --clean
```

### Script Architecture

The Python script has been refactored with a clean, modular architecture:

- **`BuildConfig`**: Centralized configuration management
- **`BuildLogger`**: Consistent colored logging and output
- **`SystemUtils`**: Command execution and prerequisite checks  
- **`FileUtils`**: File operations with Windows compatibility
- **`ProjectDiscovery`**: Automatic project discovery logic
- **`PackageBuilder`**: Core package building functionality
- **`BuildOrchestrator`**: Main workflow coordination

This architecture makes the script maintainable, testable, and easy to extend with new features.