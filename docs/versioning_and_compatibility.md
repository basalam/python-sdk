# Versioning and Backward Compatibility Guide

This document provides guidelines and best practices for maintaining backward compatibility and properly versioning the
Basalam SDK. It covers strategies for evolving the SDK while ensuring existing client code continues to work.

## Table of Contents

1. [Backward Compatibility Strategy](#backward-compatibility-strategy)
2. [Versioning Best Practices](#versioning-best-practices)
3. [Maintaining Architecture](#maintaining-architecture)
4. [Implementation Examples](#implementation-examples)
5. [Release Process](#release-process)

## Backward Compatibility Strategy

Maintaining backward compatibility is critical to ensure that clients can upgrade to newer versions of the SDK without
breaking their existing code.

### API Versioning

The current structure where services handle their own API versions works well:

```python
# In config.py
SERVICE_CONFIGS = {
    "wallet": ServiceConfig(
        name="wallet",
        api_version="v2",
        base_url=f"{BASE_URL}/wallet-service",
    ),
    "order-processing": ServiceConfig(
        name="order-processing",
        api_version="v3",
        base_url=f"{BASE_URL}/order-processing-service",
    )
    # Other services...
}
```

This approach allows:

- Each service to evolve independently
- API version management at the service level
- Centralized configuration

**Best Practice**: Keep the version prefixes in the configuration rather than hardcoding them in endpoint paths in
client code.

### Breaking Changes Policy

To maintain compatibility:

1. **Never remove or rename public methods in client classes**
    - Doing so would break client code that uses these methods

2. **Never change parameter order in existing methods**
    - Clients relying on positional arguments would break

3. **Never change return types of existing methods**
    - Client code expecting specific types would break

4. **For new mandatory parameters, always provide defaults**
    - This allows existing client code to continue working

### Deprecation Process

When functionality needs to be phased out:

1. **Add deprecation warnings**
   ```python
   import warnings
   
   class WebhookService(BaseClient):
       def get_webhook_logs(self, webhook_id: int) -> WebhookLogListResource:
           """
           Get logs for a webhook.
           
           Args:
               webhook_id: ID of the webhook
               
           Returns:
               List of webhook logs
               
           .. deprecated:: 2.1.0
              Use `get_webhook_detailed_logs` instead.
           """
           warnings.warn(
               "get_webhook_logs is deprecated since v2.1.0. Use get_webhook_detailed_logs instead.",
               DeprecationWarning,
               stacklevel=2
           )
           endpoint = f"/webhooks/{webhook_id}/logs"
           response = self._get_sync(endpoint)
           return WebhookLogListResource(**response)
   ```

2. **Document alternatives**
    - Always provide guidance on what to use instead
    - Include examples in docstrings

3. **Maintain deprecated methods for at least one major version**
    - Only remove in the next major version after deprecation
    - Document in the changelog when they will be removed

### Compatibility Layers

For significant API changes, consider providing compatibility layers:

```python
# Compatibility wrapper
def legacy_create_webhook(self, *args, **kwargs):
    """Legacy method for creating webhooks (deprecated)"""
    warnings.warn("This method is deprecated", DeprecationWarning)
    
    # Convert old format to new format
    converted_args = _convert_legacy_args(*args, **kwargs)
    return self.create_webhook(**converted_args)
```

## Versioning Best Practices

### Semantic Versioning

Follow [Semantic Versioning](https://semver.org/) strictly:

- **MAJOR** version for incompatible API changes
- **MINOR** version for backward-compatible functionality
- **PATCH** version for backward-compatible bug fixes

Example version progression:

```
1.0.0: Initial stable release
1.1.0: Added new endpoints, all backward compatible
1.1.1: Fixed bugs in existing functionality
2.0.0: Breaking changes (removed deprecated methods, changed parameter behavior)
```

### Type Hints

Type hints improve IDE support and serve as documentation:

```python
from typing import Dict, List, Optional, Union, Any

async def get_webhooks(
    self,
    service_id: Optional[int] = None,
    event_ids: Optional[str] = None
) -> WebhookListResource:
    """
    Get list of webhooks.
    
    Args:
        service_id: Optional service ID to filter by
        event_ids: Optional event IDs to filter by
        
    Returns:
        List of webhooks
    """
    # Implementation...
```

**Best Practice**: Always use proper typing for better IDE support, documentation, and static type checking.

### Method Overloading

For evolving APIs, consider method overloading patterns:

```python
# Original method
def create_webhook(self, request: CreateWebhookRequest) -> WebhookResource:
    # Original implementation
    
# Enhanced method that maintains backward compatibility
def create_webhook(
    self, 
    request: Union[CreateWebhookRequest, Dict[str, Any]] = None,
    *,
    event_ids: Optional[List[int]] = None,
    request_method: Optional[str] = None,
    url: Optional[str] = None,
    **kwargs
) -> WebhookResource:
    """
    Create a new webhook.
    
    This method can be called with either:
    1. A CreateWebhookRequest object
    2. Individual parameters
    
    Args:
        request: Webhook creation parameters as an object
        event_ids: List of event IDs to subscribe to
        request_method: HTTP method to use
        url: Webhook URL
        **kwargs: Additional parameters
    
    Returns:
        Created webhook
    """
    if request is None and (event_ids and request_method and url):
        # Build request from individual parameters
        request = CreateWebhookRequest(
            event_ids=event_ids,
            request_method=request_method,
            url=url,
            **kwargs
        )
    elif isinstance(request, dict):
        # Convert dict to request object
        request = CreateWebhookRequest(**request)
        
    # Normal implementation with request object
    endpoint = "/webhooks"
    response = self._post_sync(endpoint, json=request.__dict__)
    return WebhookResource(**response)
```

### Changelog

Maintain a detailed `CHANGELOG.md` file that documents all changes:

```markdown
# Changelog

## [2.1.0] - 2023-04-15

### Added
- New `get_webhook_detailed_logs` method in WebhookService
- Support for custom headers in all API calls

### Changed
- Improved error handling in BaseClient
- Enhanced documentation

### Deprecated
- `get_webhook_logs` method in WebhookService (will be removed in 3.0.0)

## [2.0.0] - 2023-01-10

### Breaking Changes
- Removed previously deprecated methods
- Changed authentication flow
```

### Interface Stability

Mark internal components to distinguish from the public API:

```python
# Mark internal utilities
def _internal_helper_function():
    """
    Internal helper function - not part of the public API.
    May change without notice.
    """
    # Implementation...

# Public API
def get_services():
    """
    Public API method - stable across minor versions.
    """
    # Implementation...
```

Consider using abstract base classes to define stable interfaces:

```python
from abc import ABC, abstractmethod

class BaseWebhookService(ABC):
    """
    Abstract base class defining the stable webhook service interface.
    Implementations may change, but this interface remains stable.
    """
    
    @abstractmethod
    def get_webhooks(self) -> WebhookListResource:
        """Get list of webhooks."""
        pass
        
    @abstractmethod
    def create_webhook(self, request: CreateWebhookRequest) -> WebhookResource:
        """Create a new webhook."""
        pass

class WebhookService(BaseWebhookService, BaseClient):
    """Concrete implementation of the webhook service."""
    # Implementation...
```

### Configuration Management

Allow overriding configuration at multiple levels:

```python
# Global default
DEFAULT_TIMEOUT = 30

# Client instance override
client = WebhookService(timeout=60)

# Individual request override
response = client.get_webhooks(timeout=10)
```

## Maintaining Architecture

The current architecture follows good practices and should be maintained:

### Service-Based Approach

Each service has its own module with:

- Client implementation
- Model definitions
- Service-specific utilities

```
src/basalam_sdk/
├── webhook/
│   ├── __init__.py
│   ├── client.py
│   └── models.py
├── wallet/
│   ├── __init__.py
│   ├── client.py
│   └── models.py
└── base_client.py
```

This allows:

- Independent evolution of services
- Clear separation of concerns
- Easy discovery of functionality

### Base Client Pattern

The `BaseClient` provides shared functionality:

```python
class BaseClient:
    """Base client for all API services."""
    
    def __init__(self, service_name, **kwargs):
        self.service_name = service_name
        self.config = self._get_service_config(service_name)
        # Other initialization...
    
    async def _get(self, endpoint, **kwargs):
        """Make a GET request."""
        # Implementation...
    
    async def _post(self, endpoint, **kwargs):
        """Make a POST request."""
        # Implementation...
    
    # Other shared methods...
```

Benefits:

- Code reuse across services
- Consistent handling of:
    - Authentication
    - Error handling
    - Request/response processing
    - Logging

### Model Separation

Keeping models separate from client logic:

```python
# models.py
@dataclass
class WebhookResource:
    """Response model for webhook resources."""
    id: int
    service_id: int
    events: Optional[List[Dict[str, Any]]] = None
    # Other fields...

# client.py
class WebhookService(BaseClient):
    def get_webhook(self, webhook_id: int) -> WebhookResource:
        """Get a webhook by ID."""
        endpoint = f"/webhooks/{webhook_id}"
        response = self._get_sync(endpoint)
        return WebhookResource(**response)
```

Benefits:

- Clear data structure definitions
- Separation of data and behavior
- Easy serialization/deserialization
- Type safety

### Sync/Async Support

Supporting both patterns gives flexibility:

```python
# Async
webhook = await service.get_webhook(123)

# Sync
webhook = service.get_webhook_sync(123)
```

## Implementation Examples

### Adding New Features Without Breaking Changes

```python
# Before: Original method
def create_webhook(self, request: CreateWebhookRequest) -> WebhookResource:
    endpoint = "/webhooks"
    response = self._post_sync(endpoint, json=request.__dict__)
    return WebhookResource(**response)

# After: Enhanced method with new optional functionality
def create_webhook(
    self, 
    request: CreateWebhookRequest,
    *,
    track_analytics: bool = False
) -> WebhookResource:
    """
    Create a new webhook.
    
    Args:
        request: Webhook creation parameters
        track_analytics: Whether to track webhook creation in analytics
        
    Returns:
        Created webhook
    """
    endpoint = "/webhooks"
    
    # New functionality is optional
    headers = {}
    if track_analytics:
        headers["X-Track-Analytics"] = "true"
        
    response = self._post_sync(
        endpoint, 
        json=request.__dict__,
        headers=headers
    )
    return WebhookResource(**response)
```

### Versioning Models

When models need to evolve:

```python
# Original model
@dataclass
class WebhookResource:
    id: int
    service_id: int
    url: str
    
# V2 model with backward compatibility
@dataclass
class WebhookResourceV2:
    id: int
    service_id: int
    url: str
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    
    @classmethod
    def from_v1(cls, v1: WebhookResource) -> 'WebhookResourceV2':
        """Convert from v1 model."""
        return cls(
            id=v1.id,
            service_id=v1.service_id,
            url=v1.url
        )
    
    def to_v1(self) -> WebhookResource:
        """Convert to v1 model for backward compatibility."""
        return WebhookResource(
            id=self.id,
            service_id=self.service_id,
            url=self.url
        )
```

### Unit Testing for Compatibility

Test cases should verify backward compatibility:

```python
import unittest

class BackwardCompatibilityTest(unittest.TestCase):
    def test_webhook_creation_backward_compatibility(self):
        """Test that old client code still works with new versions."""
        # Simulate old client code
        old_request = {"event_ids": [1, 2], "request_method": "POST", "url": "https://example.com/hook"}
        
        # Should still work with new service
        service = WebhookService()
        webhook = service.create_webhook_sync(CreateWebhookRequest(**old_request))
        
        self.assertIsNotNone(webhook.id)
        self.assertEqual(webhook.url, "https://example.com/hook")
```

## Release Process

To ensure smooth transitions between versions:

1. **Versioning**
    - Follow semantic versioning strictly
    - Document all changes in the changelog

2. **Testing**
    - Run compatibility tests for all changes
    - Include tests for deprecated functionality

3. **Documentation**
    - Update documentation with each release
    - Highlight breaking changes clearly
    - Provide migration guides for major versions

4. **Gradual Rollout**
    - Consider beta releases for major changes
    - Collect feedback before finalizing

5. **Support Policy**
    - Define support timeframes for each major version
    - Provide security fixes for older versions

---

By following these guidelines, the Basalam SDK can evolve while maintaining backward compatibility and providing a
clean, consistent API for consumers. 
