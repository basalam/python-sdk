"""
Basalam Python SDK for accessing the Basalam API.

This package provides a clean and simple interface to interact with Basalam's microservices.
"""

from .auth import BaseAuth, ClientCredentials, AuthorizationCode, Scope
from .basalam_client import BasalamClient
from .base_client import BaseClient
from .chat.client import ChatService
from .config import BasalamConfig
# Import service clients
from .core.client import CoreService
from .errors import BasalamError, BasalamAPIError, BasalamAuthError, BasalamValidationError
from .order.client import OrderService
from .order_processing.client import OrderProcessingService
from .search.client import SearchService
from .upload.client import UploadService
from .wallet.client import WalletService
from .webhook.client import WebhookService

__version__ = "0.1.0"

__all__ = [
    # Main client
    "BasalamClient",
    "BaseClient",

    # Authentication
    "BaseAuth",
    "ClientCredentials",
    "AuthorizationCode",
    "Scope",

    # Configuration
    "BasalamConfig",

    # Errors
    "BasalamError",
    "BasalamAPIError",
    "BasalamAuthError",
    "BasalamValidationError",

    # Service clients
    "CoreService",
    "WalletService",
    "OrderService",
    "OrderProcessingService",
    "SearchService",
    "UploadService",
    "ChatService",
    "WebhookService",
]
