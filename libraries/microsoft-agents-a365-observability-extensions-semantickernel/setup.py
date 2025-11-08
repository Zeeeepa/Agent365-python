# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

import sys
from pathlib import Path
from setuptools import setup

# Add versioning helper to path
helper_path = Path(__file__).parent.parent.parent / "versioning" / "helper"
sys.path.insert(0, str(helper_path))

from setup_utils import get_package_version, get_dynamic_dependencies

setup(
    version=get_package_version(),
    install_requires=get_dynamic_dependencies(),
)
