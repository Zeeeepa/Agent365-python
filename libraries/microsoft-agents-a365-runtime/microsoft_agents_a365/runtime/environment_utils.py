# Copyright (c) Microsoft. All rights reserved.

"""
Utility logic for environment-related operations.
"""

import os

# Authentication scopes for different environments
TEST_OBSERVABILITY_SCOPE = "https://api.test.powerplatform.com/.default"
PREPROD_OBSERVABILITY_SCOPE = "https://api.preprod.powerplatform.com/.default"
PROD_OBSERVABILITY_SCOPE = "https://api.powerplatform.com/.default"

# Cluster categories for different environments
TEST_OBSERVABILITY_CLUSTER_CATEGORY = "test"
PREPROD_OBSERVABILITY_CLUSTER_CATEGORY = "preprod"
PROD_OBSERVABILITY_CLUSTER_CATEGORY = "prod"

# Default environment names
PRODUCTION_ENVIRONMENT_NAME = "production"
DEVELOPMENT_ENVIRONMENT_NAME = "Development"


def get_observability_authentication_scope() -> list[str]:
    """
    Returns the scope for authenticating to the observability service based on the current environment.

    Returns:
        list[str]: The authentication scope for the current environment.
    """
    environment = _get_current_environment()

    environment_lower = environment.lower()

    if environment_lower == "development":
        # For now, map "development" to preprod scope for local testing
        return [PREPROD_OBSERVABILITY_SCOPE]
    elif environment_lower == "test":
        return [TEST_OBSERVABILITY_SCOPE]
    elif environment_lower == "production":
        return [PROD_OBSERVABILITY_SCOPE]
    else:
        # Default to production scope
        return [PROD_OBSERVABILITY_SCOPE]


def get_observability_cluster_category() -> str:
    """
    Returns the cluster category for the observability service based on the current environment.

    Returns:
        str: The cluster category for the current environment.
    """
    environment = _get_current_environment()

    environment_lower = environment.lower()

    if environment_lower == "development":
        # For now, map "development" to preprod scope for local testing
        return PREPROD_OBSERVABILITY_CLUSTER_CATEGORY
    elif environment_lower == "test":
        return TEST_OBSERVABILITY_CLUSTER_CATEGORY
    elif environment_lower == "production":
        return PROD_OBSERVABILITY_CLUSTER_CATEGORY
    else:
        # Default to production cluster category
        return PROD_OBSERVABILITY_CLUSTER_CATEGORY


def is_development_environment() -> bool:
    """
    Returns True if the current environment is a development environment.

    Returns:
        bool: True if the current environment is development, False otherwise.
    """
    environment = _get_current_environment()
    return environment.lower() == DEVELOPMENT_ENVIRONMENT_NAME.lower()


def _get_current_environment() -> str:
    """
    Gets the current environment name.

    Returns:
        str: The current environment name.
    """
    # Check environment variables in order of precedence

    # Check Python-specific environment variables
    environment = os.getenv("PYTHON_ENVIRONMENT")
    if environment:
        return environment

    # Default to Production
    return PRODUCTION_ENVIRONMENT_NAME
