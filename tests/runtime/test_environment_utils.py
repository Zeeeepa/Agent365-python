# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

"""Unit tests for environment_utils module."""

import os
import unittest

from microsoft_agents_a365.runtime.environment_utils import (
    DEVELOPMENT_ENVIRONMENT_NAME,
    PROD_OBSERVABILITY_CLUSTER_CATEGORY,
    PROD_OBSERVABILITY_SCOPE,
    PRODUCTION_ENVIRONMENT_NAME,
    get_observability_authentication_scope,
    is_development_environment,
)


class TestEnvironmentUtils(unittest.TestCase):
    """Test cases for environment utility functions.
    
    Tests: Constants validation, observability scope retrieval, and environment detection logic.
    """

    def tearDown(self):
        """Clean up environment variables after each test."""
        if "PYTHON_ENVIRONMENT" in os.environ:
            del os.environ["PYTHON_ENVIRONMENT"]

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
        if "PYTHON_ENVIRONMENT" in os.environ:
            del os.environ["PYTHON_ENVIRONMENT"]

        result = is_development_environment()

        self.assertFalse(result)

    def test_is_development_environment_with_development_env_var(self):
        """Test is_development_environment returns True when PYTHON_ENVIRONMENT is 'Development'."""
        os.environ["PYTHON_ENVIRONMENT"] = "Development"

        result = is_development_environment()

        self.assertTrue(result)

    def test_is_development_environment_with_production_env_var(self):
        """Test is_development_environment returns False when PYTHON_ENVIRONMENT is 'production'."""
        os.environ["PYTHON_ENVIRONMENT"] = "production"

        result = is_development_environment()

        self.assertFalse(result)


if __name__ == "__main__":
    unittest.main()
