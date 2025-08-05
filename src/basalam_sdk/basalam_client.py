"""
Basalam Python SDK for accessing the Basalam API.
"""
from typing import Optional, Union, List

from .auth import BaseAuth, Scope
from .chat.client import ChatService
from .config import BasalamConfig
# Import service clients
from .core.client import CoreService
from .order.client import OrderService
from .order_processing.client import OrderProcessingService
from .search.client import SearchService
from .upload.client import UploadService
from .wallet.client import WalletService
from .webhook.client import WebhookService


class BasalamClient:
    """
    Main client for interacting with the Basalam API.

    This client provides access to all Basalam services through a unified interface.
    It automatically configures and instantiates service-specific clients.

    You can access service methods in two ways:
    1. Through service attributes: client.webhook.get_webhooks_sync()
    2. Directly from client: client.get_webhooks_sync()
    """

    def __init__(
            self,
            auth: BaseAuth,
            config: Optional[BasalamConfig] = None,
    ):
        """
        Initialize the client.
        """
        self.auth = auth
        self.config = config or BasalamConfig()

        # Initialize service clients
        self.core = CoreService(auth=auth, config=self.config)
        self.wallet = WalletService(auth=auth, config=self.config)
        self.order = OrderService(auth=auth, config=self.config)
        self.order_processing = OrderProcessingService(auth=auth, config=self.config)
        self.search = SearchService(auth=auth, config=self.config)
        self.upload = UploadService(auth=auth, config=self.config)
        self.chat = ChatService(auth=auth, config=self.config)
        self.webhook = WebhookService(auth=auth, config=self.config)

        # Store services for dynamic method lookup
        self._services = [
            self.core,
            self.wallet,
            self.order,
            self.order_processing,
            self.search,
            self.upload,
            self.chat,
            self.webhook,
        ]

    def __getattr__(self, name: str):
        """
        Dynamically delegate method calls to the appropriate service.

        This allows calling service methods directly from the client:
        client.get_webhooks_sync() instead of client.webhook.get_webhooks_sync()

        Args:
            name: The method name being called

        Returns:
            The method from the appropriate service

        Raises:
            AttributeError: If the method is not found in any service
        """
        # Search through all services for the method
        for service in self._services:
            if hasattr(service, name):
                return getattr(service, name)

        # If method not found in any service, raise AttributeError
        raise AttributeError(f"'{self.__class__.__name__}' object has no attribute '{name}'")

    async def __aenter__(self):
        """Async context manager enter."""
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit."""
        # Close any open client connections if needed
        pass

    def has_scope(self, scope: Union[str, Scope]) -> bool:
        """
        Check if the client has a specific scope.
        """
        return self.auth.has_scope(scope)

    def get_granted_scopes(self) -> List[str]:
        """
        Get the list of granted scopes.
        """
        return list(self.auth.get_granted_scopes())

    async def refresh_auth_token(self) -> None:
        """
        Refresh the authentication token asynchronously.

        This is useful when you need to explicitly refresh the token
        before making a series of requests.
        """
        await self.auth.refresh_token()

    def refresh_auth_token_sync(self) -> None:
        """
        Refresh the authentication token synchronously.

        This is useful when you need to explicitly refresh the token
        before making a series of requests.
        """
        self.auth.refresh_token_sync()
