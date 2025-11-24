# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

"""Unit tests for version_utils module."""

import os
import unittest
import warnings

from microsoft_agents_a365.runtime.version_utils import build_version


class TestVersionUtils(unittest.TestCase):
    """Test cases for version utility functions."""

    def tearDown(self):
        """Clean up environment variables after each test."""
        if "AGENT365_PYTHON_SDK_PACKAGE_VERSION" in os.environ:
            del os.environ["AGENT365_PYTHON_SDK_PACKAGE_VERSION"]

    def test_build_version_returns_string(self):
        """Test that build_version returns a string."""
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", DeprecationWarning)
            result = build_version()
        
        self.assertIsInstance(result, str)

    def test_build_version_default_value(self):
        """Test build_version returns default version when no env var is set."""
        # Ensure environment variable is not set
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

    def test_build_version_with_complex_version(self):
        """Test build_version with complex version strings."""
        test_cases = [
            "1.0.0-alpha",
            "2.3.4-beta.1",
            "3.0.0-rc.2",
            "1.2.3+build.456",
            "2.0.0-alpha.1+build.789",
        ]
        
        for version in test_cases:
            with self.subTest(version=version):
                os.environ["AGENT365_PYTHON_SDK_PACKAGE_VERSION"] = version
                
                with warnings.catch_warnings():
                    warnings.simplefilter("ignore", DeprecationWarning)
                    result = build_version()
                
                self.assertEqual(result, version)

    def test_build_version_with_empty_env_var(self):
        """Test build_version with empty environment variable."""
        os.environ["AGENT365_PYTHON_SDK_PACKAGE_VERSION"] = ""
        
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", DeprecationWarning)
            result = build_version()
        
        self.assertEqual(result, "")

    def test_build_version_deprecation_warning(self):
        """Test that build_version raises DeprecationWarning."""
        with self.assertWarns(DeprecationWarning) as cm:
            build_version()
        
        warning_message = str(cm.warning)
        self.assertIn("deprecated", warning_message.lower())
        self.assertIn("setuptools-git-versioning", warning_message)

    def test_build_version_deprecation_warning_message(self):
        """Test that deprecation warning contains the correct message."""
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            build_version()
            
            # Check that exactly one warning was raised
            self.assertEqual(len(w), 1)
            
            # Check that it's a DeprecationWarning
            self.assertTrue(issubclass(w[0].category, DeprecationWarning))
            
            # Check the message content
            message = str(w[0].message)
            self.assertIn("build_version() is deprecated", message)
            self.assertIn("setuptools-git-versioning", message)

    def test_build_version_stacklevel(self):
        """Test that deprecation warning has correct stack level."""
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            build_version()
            
            # The warning should point to the caller of build_version
            # not to the function itself (stacklevel=2)
            self.assertEqual(len(w), 1)
            warning = w[0]
            
            # Verify the warning was captured
            self.assertIsNotNone(warning.filename)
            self.assertGreater(warning.lineno, 0)


class TestVersionUtilsDocstring(unittest.TestCase):
    """Test cases for version_utils module documentation."""

    def test_module_has_docstring(self):
        """Test that the module has a docstring."""
        import microsoft_agents_a365.runtime.version_utils as version_utils
        
        self.assertIsNotNone(version_utils.__doc__)
        self.assertGreater(len(version_utils.__doc__), 0)

    def test_module_docstring_mentions_deprecation(self):
        """Test that module docstring mentions deprecation."""
        import microsoft_agents_a365.runtime.version_utils as version_utils
        
        self.assertIn("deprecated", version_utils.__doc__.lower())

    def test_function_has_docstring(self):
        """Test that build_version function has a docstring."""
        self.assertIsNotNone(build_version.__doc__)
        self.assertGreater(len(build_version.__doc__), 0)

    def test_function_docstring_mentions_deprecation(self):
        """Test that function docstring mentions deprecation."""
        self.assertIn("DEPRECATED", build_version.__doc__)


if __name__ == "__main__":
    unittest.main()
