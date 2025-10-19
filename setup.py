# Copyright (c) Microsoft. All rights reserved.

# Kairo Python SDK for AI agents with observability, identity, and tooling capabilities.

from __future__ import annotations

import os
import tomllib
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

from setuptools import find_packages, setup


def read_pyproject():
    text = Path("pyproject.toml").read_text(encoding="utf-8")
    data = tomllib.loads(text)
    project = data["project"]
    name = project["name"]
    description = project["description"]
    required_py_version = project["requires-python"]
    return name, description, required_py_version


PROJECT_NAME, PROJECT_DESCRIPTION, REQUIRED_PY_VERSION = read_pyproject()

MODULE_NAME = (PROJECT_NAME or "microsoft-kairo").replace("-", "_")


def build_version():
    """
    Example: 2025.10.3+preview.65532  (PEP 440 compliant; avoids hyphens)
    Uses America/Los_Angeles so CI in other timezones stamps same 'day'.
    """

    if defined_version := os.getenv("A365_SDK_VERSION"):
        return defined_version  # For CI/CD to set a specific version.

    today = datetime.now(ZoneInfo("America/Los_Angeles"))

    return (
        f"{today.year}.{today.month}.{today.day}+preview.{today.hour}{today.minute}{today.second}"
    )


VERSION = build_version()


# Write the version attr used by [tool.setuptools.dynamic].version
pkg_dir = Path(__file__).parent / MODULE_NAME
pkg_dir.mkdir(parents=True, exist_ok=True)
(pkg_dir / "_version.py").write_text(f'__version__ = "{VERSION}"\n', encoding="utf-8")

# We pass name/description that we just read, so you don't duplicate them.
# Version is provided via the dynamic attr above.
long_desc = Path("README.md").read_text(encoding="utf-8") if Path("README.md").exists() else ""

setup(
    name=PROJECT_NAME,
    description=PROJECT_DESCRIPTION,
    long_description=long_desc,
    long_description_content_type="text/markdown",
    python_requires=REQUIRED_PY_VERSION,
    packages=find_packages(exclude=("tests", "docs")),
    include_package_data=True,
)
