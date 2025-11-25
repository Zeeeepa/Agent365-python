# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

"""Unit tests for version_utils module."""

import os
import unittest
import warnings

from microsoft_agents_a365.runtime.version_utils import build_version


class TestVersionUtils(unittest.TestCase):
    """Test cases for version utility functions.

    Tests: Default version behavior, environment variable usage, and deprecation warning.
    """

    def tearDown(self):
        """Clean up environment variables after each test."""
        if "AGENT365_PYTHON_SDK_PACKAGE_VERSION" in os.environ:
            del os.environ["AGENT365_PYTHON_SDK_PACKAGE_VERSION"]

    def test_build_version_default_value(self):
        """Test build_version returns default version when no env var is set."""
        if "AGENT365_PYTHON_SDK_PACKAGE_VERSION" in os.environ:
            del os.environ["AGENT365_PYTHON_SDK_PACKAGE_VERSION"]

        with warnings.catch_warnings():
            warnings.simplefilter("ignore", DeprecationWarning)
            result = build_version()

        self.assertEqual(result, "0.0.0")

    def test_build_version_with_env_var(self):
        """Test build_version returns version from environment variable."""
        test_version = "1.2.3"
        os.environ["AGENT365_PYTHON_SDK_PACKAGE_VERSION"] = test_version

        with warnings.catch_warnings():
            warnings.simplefilter("ignore", DeprecationWarning)
            result = build_version()

        self.assertEqual(result, test_version)

    def test_build_version_deprecation_warning(self):
        """Test that build_version raises DeprecationWarning."""
        with self.assertWarns(DeprecationWarning) as cm:
            build_version()

        warning_message = str(cm.warning)
        self.assertIn("deprecated", warning_message.lower())
        self.assertIn("setuptools-git-versioning", warning_message)


if __name__ == "__main__":
    unittest.main()
