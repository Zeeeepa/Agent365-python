# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

"""Unit tests for environment_utils module."""

import os
import unittest
from unittest.mock import patch

from microsoft_agents_a365.runtime.environment_utils import (
    DEVELOPMENT_ENVIRONMENT_NAME,
    PROD_OBSERVABILITY_CLUSTER_CATEGORY,
    PROD_OBSERVABILITY_SCOPE,
    PRODUCTION_ENVIRONMENT_NAME,
    get_observability_authentication_scope,
    is_development_environment,
)


class TestEnvironmentUtils(unittest.TestCase):
    """Test cases for environment utility functions."""

    def tearDown(self):
        """Clean up environment variables after each test."""
        env_vars = ["PYTHON_ENVIRONMENT"]
        for var in env_vars:
            if var in os.environ:
                del os.environ[var]

    def test_constants(self):
        """Test that environment constants have expected values."""
        self.assertEqual(PROD_OBSERVABILITY_SCOPE, "https://api.powerplatform.com/.default")
        self.assertEqual(PROD_OBSERVABILITY_CLUSTER_CATEGORY, "prod")
        self.assertEqual(PRODUCTION_ENVIRONMENT_NAME, "production")
        self.assertEqual(DEVELOPMENT_ENVIRONMENT_NAME, "Development")

    def test_get_observability_authentication_scope_returns_prod_scope(self):
        """Test that get_observability_authentication_scope returns production scope."""
        result = get_observability_authentication_scope()
        
        self.assertIsInstance(result, list)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0], PROD_OBSERVABILITY_SCOPE)

    def test_is_development_environment_with_no_env_var(self):
        """Test is_development_environment returns False when no environment variable is set."""
        # Ensure environment variables are not set
        if "PYTHON_ENVIRONMENT" in os.environ:
            del os.environ["PYTHON_ENVIRONMENT"]
        
        result = is_development_environment()
        
        self.assertFalse(result)

    def test_is_development_environment_with_development_env_var(self):
        """Test is_development_environment returns True when PYTHON_ENVIRONMENT is 'Development'."""
        os.environ["PYTHON_ENVIRONMENT"] = "Development"
        
        result = is_development_environment()
        
        self.assertTrue(result)

    def test_is_development_environment_case_insensitive(self):
        """Test is_development_environment is case-insensitive."""
        test_cases = ["development", "DEVELOPMENT", "DeveLoPMenT", "Development"]
        
        for env_value in test_cases:
            with self.subTest(env_value=env_value):
                os.environ["PYTHON_ENVIRONMENT"] = env_value
                result = is_development_environment()
                self.assertTrue(result)

    def test_is_development_environment_with_production_env_var(self):
        """Test is_development_environment returns False when PYTHON_ENVIRONMENT is 'production'."""
        os.environ["PYTHON_ENVIRONMENT"] = "production"
        
        result = is_development_environment()
        
        self.assertFalse(result)

    def test_is_development_environment_with_other_env_var(self):
        """Test is_development_environment returns False for other environment values."""
        test_cases = ["staging", "test", "preprod", "custom"]
        
        for env_value in test_cases:
            with self.subTest(env_value=env_value):
                os.environ["PYTHON_ENVIRONMENT"] = env_value
                result = is_development_environment()
                self.assertFalse(result)

    def test_is_development_environment_with_empty_env_var(self):
        """Test is_development_environment returns False when PYTHON_ENVIRONMENT is empty."""
        os.environ["PYTHON_ENVIRONMENT"] = ""
        
        result = is_development_environment()
        
        self.assertFalse(result)

    def test_is_development_environment_with_whitespace_env_var(self):
        """Test is_development_environment returns False when PYTHON_ENVIRONMENT is whitespace."""
        os.environ["PYTHON_ENVIRONMENT"] = "   "
        
        result = is_development_environment()
        
        self.assertFalse(result)

    @patch.dict(os.environ, {"PYTHON_ENVIRONMENT": "Development"}, clear=False)
    def test_python_environment_precedence(self):
        """Test that PYTHON_ENVIRONMENT takes precedence."""
        result = is_development_environment()
        
        self.assertTrue(result)

    def test_default_environment_is_production(self):
        """Test that the default environment is production when no env vars are set."""
        # Ensure no environment variables are set
        if "PYTHON_ENVIRONMENT" in os.environ:
            del os.environ["PYTHON_ENVIRONMENT"]
        
        # The _get_current_environment function should default to PRODUCTION_ENVIRONMENT_NAME
        result = is_development_environment()
        
        self.assertFalse(result)


class TestObservabilityAuthenticationScope(unittest.TestCase):
    """Test cases for observability authentication scope."""

    def test_scope_is_list(self):
        """Test that the scope is returned as a list."""
        result = get_observability_authentication_scope()
        
        self.assertIsInstance(result, list)

    def test_scope_contains_single_value(self):
        """Test that the scope list contains exactly one value."""
        result = get_observability_authentication_scope()
        
        self.assertEqual(len(result), 1)

    def test_scope_value_is_string(self):
        """Test that the scope value is a string."""
        result = get_observability_authentication_scope()
        
        self.assertIsInstance(result[0], str)

    def test_scope_value_format(self):
        """Test that the scope value has the correct format."""
        result = get_observability_authentication_scope()
        
        self.assertTrue(result[0].startswith("https://"))
        self.assertTrue(result[0].endswith(".default"))

    def test_scope_consistency(self):
        """Test that multiple calls return the same scope."""
        result1 = get_observability_authentication_scope()
        result2 = get_observability_authentication_scope()
        
        self.assertEqual(result1, result2)


if __name__ == "__main__":
    unittest.main()
