# Basalam SDK for Python

A comprehensive Python client library for interacting with Basalam API services.

![Python Versions](https://img.shields.io/badge/python-3.8%20%7C%203.9%20%7C%203.10%20%7C%203.11-blue)
![License](https://img.shields.io/badge/license-MIT-green)

## 📑 Overview

The Basalam SDK provides a clean, consistent interface to Basalam's API services, enabling developers to easily
integrate with the Basalam platform. The SDK follows a service-oriented architecture, with support for both synchronous
and asynchronous operations.

### Key Features

- **Modular Service Architecture** - Separate clients for each Basalam service
- **Authentication Support** - OAuth2 flows including Client Credentials and Authorization Code
- **Synchronous & Asynchronous APIs** - Choose your preferred programming style
- **Comprehensive Type Hinting** - Excellent editor support and code completion
- **Error Handling** - Consistent error handling across all services
- **Backward Compatibility** - Designed with API versioning and compatibility in mind

## 🚀 Installation

```bash
pip install basalam-sdk
```

## 🏁 Quick Start

### Basic Usage

```python
from basalam_sdk import BasalamClient

# Create client with Client Credentials
client = BasalamClient(
    client_id="your-client-id",
    client_secret="your-client-secret"
)

# Get a service client
webhook_service = client.webhook()

# Make synchronous API calls
webhooks = webhook_service.get_webhooks_sync()
print(f"Found {webhooks.result_count} webhooks")

# Or use async/await
async def get_webhooks():
    webhooks = await webhook_service.get_webhooks()
    return webhooks

```

### Authentication Options

#### Client Credentials (Server-to-Server)

```python
from basalam_sdk import BasalamClient

# Client will automatically authenticate using client credentials
client = BasalamClient(
    client_id="your-client-id",
    client_secret="your-client-secret"
)
```

#### Authorization Code (User Authentication)

```python
from basalam_sdk import BasalamClient, AuthorizationCodeFlow

# Create an auth flow object
auth_flow = AuthorizationCodeFlow(
    client_id="your-client-id",
    client_secret="your-client-secret",
    redirect_uri="https://your-app.com/callback"
)

# Get the authorization URL
auth_url = auth_flow.get_authorization_url(
    scope=["webhook:read", "webhook:write"]
)

# After user authorization, exchange code for tokens
tokens = auth_flow.get_tokens_from_code("authorization_code_from_callback")

# Create client with user tokens
client = BasalamClient(auth_tokens=tokens)
```

## 📚 Documentation

The SDK includes comprehensive documentation:

- [**Usage Guide**](docs/usage_guide.md) - Detailed usage instructions for all SDK features
- [**Authentication Guide**](docs/authentication.md) - In-depth information on authentication flows
- [**Architecture**](docs/architecture.md) - SDK structure, design patterns, and principles
- [**Versioning & Compatibility**](docs/versioning_and_compatibility.md) - How we maintain backward compatibility

## 💡 Examples

Complete examples are available in the [examples/](examples/) directory:

- [**Client Credentials Example**](examples/client_credentials_example.py) - Server-to-server authentication demo
- [**Authorization Code Example**](examples/authorization_code_example.py) - User authorization flow with a Flask web
  app
- [**Webhook Service Example**](examples/webhook_service_example.py) - Comprehensive webhook management
- [**Order Processing Example**](examples/order_processing_example.py) - Working with orders

## 🔧 Services

The SDK provides clients for the following Basalam services:

| Service              | Description                                          |
|----------------------|------------------------------------------------------|
| **Webhook**          | Manage webhook subscriptions for event notifications |
| **Wallet**           | Handle financial transactions and wallet operations  |
| **Order Processing** | Manage orders and fulfillment                        |
| **Upload**           | Upload and manage files                              |
| **Search**           | Search for products and other entities               |
| **Chat**             | Messaging and chat functionalities                   |

## 🧩 Project Structure

```
basalam-sdk/
├── docs/                   # Documentation
│   ├── authentication.md   # Authentication guide
│   ├── usage_guide.md      # Detailed usage guide
│   ├── architecture.md     # SDK architecture and design
│   └── versioning_and_compatibility.md  # Compatibility policies
├── examples/               # Example implementations
├── src/                    # Source code
│   └── basalam_sdk/        # SDK package
│       ├── webhook/        # Webhook service
│       ├── wallet/         # Wallet service
│       ├── order/          # Order service
│       ├── upload/         # Upload service
│       ├── search/         # Search service
│       ├── chat/           # Chat service
│       ├── auth.py         # Authentication functionality
│       ├── base_client.py  # Base client implementation
│       ├── config.py       # Configuration
│       ├── errors.py       # Error definitions
│       └── __init__.py     # Package initialization
└── tests/                  # Test suite
```

## 📋 Requirements

- Python 3.8 or higher
- Dependencies:
    - requests
    - aiohttp
    - pydantic
    - python-dateutil

## 🔄 Versioning

This SDK follows [Semantic Versioning](https://semver.org/). See
the [versioning guide](docs/versioning_and_compatibility.md) for details on our compatibility policies.

## 🔒 Security

For details on security practices and recommendations, see
the [authentication guide](docs/authentication.md#security-best-practices).

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📮 Support

If you encounter any issues or require assistance, please open an issue in the GitHub repository or contact
support@basalam.com. 
