# Basalam SDK Architecture

This document provides a comprehensive overview of the Basalam SDK architecture, design patterns, and project structure.

## Overview

The Basalam SDK is designed as a modular, service-oriented client library that provides access to various Basalam API
services. The architecture follows a clean, consistent pattern across different services, making it easy to maintain and
extend.

## Project Structure

```
src/basalam_sdk/
├── service_modules/            # Individual service implementations
│   ├── webhook/                # Webhook service
│   │   ├── __init__.py         # Exports and module initialization
│   │   ├── client.py           # Service client implementation
│   │   └── models.py           # Data models for the service
│   ├── wallet/                 # Wallet service
│   ├── order_processing/       # Order processing service
│   ├── upload/                 # Upload service
│   ├── search/                 # Search service
│   └── ...                     # Other service modules
├── auth.py                     # Authentication handling
├── base_client.py              # Base client class for all services
├── basalam_client.py           # Main client entry point
├── config.py                   # Configuration and service definitions
├── errors.py                   # Error definitions
└── __init__.py                 # SDK entry point and version info
```

## Core Components

### BaseClient

The `BaseClient` is the foundation of all service clients. It handles:

1. **HTTP Communication**: Manages API requests/responses
2. **Authentication**: Integrates with the auth module
3. **Error Handling**: Translates HTTP errors to SDK exceptions
4. **Serialization/Deserialization**: Converts between JSON and Python objects

Key features of `BaseClient`:

- Support for both synchronous and asynchronous operations
- Built-in logging
- Request tracing and debugging
- Consistent request/response handling

### Service Modules

Each service module follows a consistent pattern:

#### Client Implementation (`client.py`)

Service clients extend `BaseClient` to provide service-specific functionality:

```python
class WebhookService(BaseClient):
    def __init__(self, **kwargs):
        super().__init__(service_name="webhook", **kwargs)
        
    async def get_webhooks(self, **params):
        # Service-specific implementation
        endpoint = "/webhooks"
        response = await self._get(endpoint, params=params)
        return WebhookListResource(**response)
        
    def get_webhooks_sync(self, **params):
        # Synchronous version
        endpoint = "/webhooks"
        response = self._get_sync(endpoint, params=params)
        return WebhookListResource(**response)
```

Key characteristics:

- Each endpoint has both synchronous and asynchronous methods
- Strong typing with appropriate return types
- Comprehensive docstrings
- Consistent error handling

#### Data Models (`models.py`)

Data models use Python's `dataclass` to define request and response structures:

```python
@dataclass
class WebhookResource:
    """Response model for webhook resources."""
    id: int
    service_id: int
    events: Optional[List[Dict[str, Any]]] = None
    # Other fields...
```

Key characteristics:

- Type annotations for all fields
- Default values for optional fields
- Descriptive docstrings
- Immutable where appropriate

#### Module Initialization (`__init__.py`)

Each module's `__init__.py` exports the classes and functions that should be part of the public API:

```python
from .client import WebhookService
from .models import (
    WebhookResource, 
    CreateWebhookRequest,
    # Other models...
)

__all__ = [
    "WebhookService",
    "WebhookResource",
    "CreateWebhookRequest",
    # Other exports...
]
```

### Configuration Management

The SDK uses a centralized configuration system in `config.py`:

```python
class ServiceConfig:
    """Configuration for a service."""
    def __init__(
        self,
        name: str,
        api_version: str = "",
        base_url: str = "",
        timeout: int = 30,
    ):
        self.name = name
        self.api_version = api_version
        self.base_url = base_url
        self.timeout = timeout

SERVICE_CONFIGS = {
    "webhook": ServiceConfig(
        name="webhook",
        api_version="v1",
        base_url=f"{BASE_URL}/webhook-service",
    ),
    # Other services...
}
```

This approach allows:

- Centralized configuration for all services
- Per-service API version control
- Consistent timeouts and other settings

### Authentication

Authentication is handled by the `auth.py` module, which provides:

1. **OAuth2 Authentication**: Support for various OAuth2 flows
2. **Token Management**: Handling token acquisition, refreshing, and caching
3. **Credential Management**: Secure handling of API credentials

## Design Patterns

### Service Client Pattern

All service clients follow the same pattern:

1. Extend `BaseClient`
2. Implement service-specific API endpoints
3. Provide both async and sync methods for each endpoint
4. Return strongly-typed data models

### Data Transfer Object (DTO) Pattern

Data models are implemented as DTOs using Python's `dataclass`:

1. Defined in dedicated `models.py` files
2. Used for both request and response data
3. Include proper type annotations
4. Default values for optional fields

### Adapter Pattern

The BaseClient acts as an adapter between:

1. The high-level service API (what developers use)
2. The low-level HTTP communication layer
3. Authentication mechanisms

### Factory Pattern

The main client can act as a factory for service clients:

```python
class BasalamClient:
    def __init__(self, **kwargs):
        self.kwargs = kwargs
        
    def webhook(self) -> WebhookService:
        """Get webhook service client."""
        return WebhookService(**self.kwargs)
        
    def wallet(self) -> WalletService:
        """Get wallet service client."""
        return WalletService(**self.kwargs)
```

## API Versioning

The SDK handles API versioning at the service level:

1. Each service has its own API version in the configuration
2. Clients automatically use the correct API version
3. Version prefixes are added to endpoints internally
4. Developers don't need to manage versions manually

For more details on versioning and backward compatibility,
see [Versioning and Backward Compatibility Guide](versioning_and_compatibility.md).

## Error Handling

The SDK provides a consistent error handling mechanism:

1. HTTP errors are translated to SDK-specific exceptions
2. Exceptions contain detailed error information
3. Specific exception types for common error cases
4. Proper propagation in both sync and async contexts

## Best Practices for Using the SDK

1. **Prefer async methods** for high-performance applications
2. **Reuse client instances** rather than creating new ones for each request
3. **Use specific exception handling** for better error management
4. **Leverage the type system** for improved code completion and validation

## Extending the SDK

When adding new services to the SDK:

1. Follow the established module structure
2. Extend `BaseClient` for all new service clients
3. Use dataclasses for all data models
4. Provide both sync and async methods
5. Implement comprehensive docstrings
6. Add appropriate tests
7. Update the main client to expose the new service

By following these patterns, the SDK maintains consistency and predictability while allowing for extensibility and
evolution. 
