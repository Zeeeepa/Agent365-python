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


def get_dynamic_dependencies(pyproject_path: str = "pyproject.toml") -> List[str]:
    """
    Read dependencies from pyproject.toml and update internal package versions.
    
    All internal packages (microsoft-agents-a365-*) will use EXACT version matching (==)
    since they are built together in the same monorepo with the same version.
    
    External packages keep their original version constraints.
    
    Args:
        pyproject_path: Path to the pyproject.toml file (default: "pyproject.toml")
    
    Returns:
        List of dependency strings with updated internal package versions
    """
    package_version = get_package_version()
    
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
            # Handle formats like: "package >= 0.0.0", "package==0.0.0", "package"
            pkg_name = dep.split(">=")[0].split("==")[0].split("<")[0].strip()
            
            # Use EXACT version match for internal packages
            # All packages in this monorepo are built together, so they share the same version
            updated_dependencies.append(f"{pkg_name} == {package_version}")
        else:
            # Keep external dependencies as-is
            updated_dependencies.append(dep)
    
    return updated_dependencies
