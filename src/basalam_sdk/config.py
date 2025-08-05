"""
Configuration settings for the Basalam SDK.

This module provides configuration management for the Basalam API client,
including environment-specific URLs, service endpoints, and client settings.
"""
from dataclasses import dataclass
from enum import Enum
from typing import Dict, Optional

from .version import get_user_agent


class Environment(str, Enum):
    """Available environments for the Basalam API."""
    PRODUCTION = "production"
    DEVELOPMENT = "development"


@dataclass
class ServiceConfig:
    """Configuration for a specific service."""
    base_url: str
    api_version: str = "v1"
    path: str = ""

    @property
    def url(self) -> str:
        """
        Get the full service URL.
        """
        parts = [self.base_url.rstrip("/")]
        if self.path.strip("/"):
            parts.append(self.path.strip("/"))
        if self.api_version.strip("/"):
            parts.append(self.api_version.strip("/"))
        return "/".join(parts)


class BasalamConfig:
    """Configuration for Basalam API client."""

    BASE_URLS = {
        Environment.PRODUCTION: "https://basalam.com",
        Environment.DEVELOPMENT: "https://basalam.dev",
    }

    AUTH_URLS = {
        Environment.PRODUCTION: {
            "authorize": "https://basalam.com/accounts/sso",
            "token": "https://auth.basalam.com/oauth/token",
        },
        Environment.DEVELOPMENT: {
            "authorize": "https://basalam.dev/accounts/sso",
            "token": "https://auth.basalam.dev/oauth/token",
        },
    }

    SERVICE_CONFIGS = {
        "core": ServiceConfig(
            base_url="https://core.basalam.com",
            path="",
            api_version="v3"
        ),
        "wallet": ServiceConfig(
            base_url="https://wallet.basalam.com",
            path="",
            api_version="v2"
        ),
        "chat": ServiceConfig(
            base_url="https://conversation.basalam.com",
            path="",
            api_version="v2"
        ),
        "order": ServiceConfig(
            base_url="https://order.basalam.com",
            path="",
            api_version="v2"
        ),
        "order-processing": ServiceConfig(
            base_url="https://order-processing.basalam.com",
            path="",
            api_version="v3"
        ),
        "search": ServiceConfig(
            base_url="https://search.basalam.com",
            path="ai-engine/api",
            api_version="v2.0"
        ),
        "upload": ServiceConfig(
            base_url="https://uploadio.basalam.com",
            path="",
            api_version="v3"
        ),
        "webhook": ServiceConfig(
            base_url="https://webhook.basalam.com",
            path="",
            api_version="v1"
        ),
    }

    def __init__(
            self,
            environment: str = Environment.PRODUCTION,
            api_version: str = "v1",
            timeout: float = 30.0,
            user_agent: Optional[str] = None,
            custom_base_url: Optional[str] = None,
            custom_auth_urls: Optional[Dict[str, str]] = None,
    ):
        """
        Initialize the configuration.

        Args:
            environment: The environment to use (production or development).
            api_version: The API version to use.
            timeout: Request timeout in seconds.
            user_agent: Custom User-Agent string to append to SDK User-Agent.
            custom_base_url: Custom base URL to override environment default.
            custom_auth_urls: Custom authentication URLs.
        """
        self.environment = Environment(environment)
        self.api_version = api_version
        self.timeout = timeout
        self.base_url = custom_base_url or self.BASE_URLS[self.environment]

        # Set auth URLs
        auth_env = self.AUTH_URLS[self.environment]
        self.authorize_url = auth_env["authorize"] if not custom_auth_urls else custom_auth_urls.get("authorize",
                                                                                                     auth_env[
                                                                                                         "authorize"])
        self.token_url = auth_env["token"] if not custom_auth_urls else custom_auth_urls.get("token", auth_env["token"])

        # Initialize service URLs
        self.service_urls = self._initialize_service_urls()

        # Generate User-Agent with SDK information
        self.user_agent = get_user_agent(user_agent)

    def _initialize_service_urls(self) -> Dict[str, str]:
        """
        Initialize service URLs based on environment.
        """
        base_url = self.BASE_URLS[self.environment]
        domain = base_url.replace("https://", "")
        return {
            service: config.url.replace("basalam.com", domain)
            for service, config in self.SERVICE_CONFIGS.items()
        }

    def get_service_url(self, service: str) -> str:
        """
        Get the base URL for a service.

        Args:
            service: The service name.

        Returns:
            The base URL for the service.
        """
        return self.service_urls.get(service, self.base_url)

    def get_headers(self) -> Dict[str, str]:
        """
        Get default headers for API requests.

        Returns:
            Dictionary of default headers including User-Agent.
        """
        return {
            "User-Agent": self.user_agent,
        }
