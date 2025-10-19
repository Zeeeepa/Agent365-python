# Copyright (c) Microsoft. All rights reserved.

"""
Provides constant values used throughout the Tooling components.
"""


class Constants:
    """
    Provides constant values used throughout the Tooling components.
    """

    class Headers:
        """
        Provides constant header values used for authentication and environment identification.
        """

        #: The header name used for HTTP authorization tokens.
        AUTHORIZATION = "Authorization"

        #: The prefix used for Bearer authentication tokens in HTTP headers.
        BEARER_PREFIX = "Bearer"

        #: The header name used to specify the environment identifier in HTTP requests.
        ENVIRONMENT_ID = "x-ms-environment-id"
