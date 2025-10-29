# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

import os
from datetime import datetime
from zoneinfo import ZoneInfo

from setuptools import setup


def build_version():
    """
    Example: 2025.10.3+preview.65532  (PEP 440 compliant; avoids hyphens)
    Uses UTC.
    """

    if defined_version := os.getenv("A365_SDK_VERSION"):
        return defined_version  # For CI/CD to set a specific version.

    today = datetime.now(ZoneInfo("UTC"))

    return (
        f"{today.year}.{today.month}.{today.day}+preview.{today.hour}{today.minute}{today.second}"
    )


VERSION = build_version()

setup(
    version=VERSION,
)
