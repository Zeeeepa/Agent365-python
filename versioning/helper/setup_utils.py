# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

"""
Shared utilities for setup.py files across all Agent365 Python SDK packages.

This module provides helper functions to dynamically set internal package versions
at build time, ensuring all packages in the monorepo use the exact same version.
"""

from os import environ
from typing import List


def get_package_version() -> str:
    """
    Get the package version from environment variable.
    
    Returns:
        The version string from AGENT365_PYTHON_SDK_PACKAGE_VERSION environment variable,
        or "0.0.0" if not set.
    """
    return environ.get("AGENT365_PYTHON_SDK_PACKAGE_VERSION", "0.0.0")


def get_dynamic_dependencies(
    pyproject_path: str = "pyproject.toml",
    use_exact_match: bool = False,
    use_compatible_release: bool = False,
) -> List[str]:
    """
    Read dependencies from pyproject.toml and update internal package versions.
    
    Internal packages (microsoft-agents-a365-*) can use different versioning strategies:
    
    1. Minimum version (default, recommended):
       >= base_version
       Example: >= 0.1.0
       - Maximum flexibility for consumers
    
    2. Compatible release:
       >= base_version, < next_major_version
       Example: >= 0.1.0, < 0.2.0
       - Allows updates within major version
    
    3. Exact match:
       == current_version
       Example: == 0.1.0.dev5
       - Forces exact version match
    
    External packages keep their original version constraints.
    
    Args:
        pyproject_path: Path to the pyproject.toml file (default: "pyproject.toml")
        use_exact_match: If True, use == for internal packages
        use_compatible_release: If True, use >= with < upper bound
    
    Returns:
        List of dependency strings with updated internal package versions
    """
    package_version = get_package_version()
    
    # Extract base version (remove dev/pre-release suffixes)
    base_version = package_version.split(".dev")[0].split("a")[0].split("b")[0].split("rc")[0]
    
    try:
        import tomllib  # Python 3.11+
    except ImportError:
        import tomli as tomllib  # Fallback for older Python
    
    with open(pyproject_path, "rb") as f:
        pyproject = tomllib.load(f)
    
    dependencies = pyproject.get("project", {}).get("dependencies", [])
    
    # Update internal package versions dynamically
    updated_dependencies = []
    for dep in dependencies:
        if dep.startswith("microsoft-agents-a365-"):
            # Extract package name (everything before >=, ==, or other operators)
            pkg_name = dep.split(">=")[0].split("==")[0].split("<")[0].strip()
            
            if use_exact_match:
                # Exact match: == current_version
                updated_dependencies.append(f"{pkg_name} == {package_version}")
            elif use_compatible_release:
                # Compatible release: >= base_version, < next_major
                parts = base_version.split(".")
                if len(parts) >= 3:
                    major = int(parts[0])
                    if major == 0:
                        # For 0.x.y, increment minor (0.1.0 -> 0.2.0)
                        minor = int(parts[1])
                        next_major = f"{major}.{minor + 1}.0"
                    else:
                        # For x.y.z where x > 0, increment major (1.2.3 -> 2.0.0)
                        next_major = f"{major + 1}.0.0"
                else:
                    next_major = base_version
                updated_dependencies.append(f"{pkg_name} >= {base_version}, < {next_major}")
            else:
                # Minimum version (default): >= base_version
                updated_dependencies.append(f"{pkg_name} >= {base_version}")
        else:
            # Keep external dependencies as-is
            updated_dependencies.append(dep)
    
    return updated_dependencies
