# Copyright (c) Microsoft. All rights reserved.

from __future__ import annotations

import os
from datetime import datetime
from zoneinfo import ZoneInfo


def build_version():
    """
    Build version string for Agent365 SDK packages.

    Example: 2025.10.3+preview.65532  (PEP 440 compliant; avoids hyphens)
    Uses UTC.

    Returns:
        str: Version string in format YYYY.M.D+preview.HHMMSS or environment override
    """
    if defined_version := os.getenv("A365_SDK_VERSION"):
        return defined_version  # For CI/CD to set a specific version.

    today = datetime.now(ZoneInfo("UTC"))

    return (
        f"{today.year}.{today.month}.{today.day}+preview.{today.hour}{today.minute}{today.second}"
    )
