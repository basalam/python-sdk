# Introduction

Welcome to the Basalam Python SDK – a comprehensive library for interacting with Basalam service APIs. This SDK provides
a simple, clean, and developer-friendly interface to all Basalam services with full Sync/Async support. It is designed
to make integration with Basalam services as straightforward and efficient as possible. Whether you're building
server-to-server communication or developing a user-facing application, this SDK offers the tools you need.

**Supported Python Versions:**  
`Python 3.8+, Python 3.9+, Python 3.10+, Python 3.11+`

**Key Features:**

- **Comprehensive Service Coverage**: Access to all Basalam services, including Wallet, Orders, Chat, and more.
- **Multiple Authentication Methods**: Supports Client Credentials, Authorization Code Flow, and Personal Access
  Tokens (PAT).
- **Data Type Safety**: Uses Pydantic for strict data validation and type checking.
- **Full Async/Sync Support**: All methods support both Sync and Async usage patterns.
- **Error Management**: Detailed error classes for different error types.
- **Developer Friendly**: Clean and standard API design with full and clear documentation.

## Table of Contents

- [Installation](#installation)
- [Quick Start](#quick-start)
- [Authentication Methods](#authentication-methods)
- [Service Overview](#service-overview)

## Installation

Install the SDK using pip:

```bash
pip install basalam-sdk
```

## Quick Start

### 1. Configure Authentication

```python
from basalam_sdk import BasalamClient, PersonalToken

# Personal Access Token (PAT)
auth = PersonalToken(
    token="your-access-token",
    refresh_token="your-refresh-token"
)

# Create client
client = BasalamClient(auth=auth)
```

### 2. Your First API Calls

#### Get Products

```python
# Get products
async def get_products_example():

    products = await client.get_products()
    return products
```

#### Send a Message and Fetch Chats

```python
# Send a message
from basalam_sdk.chat.models import MessageRequest
async def chat_example():
    message = await client.create_message(
        request=MessageRequest(
            chat_id=123,
            content="Hello, how can I help you?",
            message_type=MessageTypeEnum.TEXT
        )
    )
    
    # Get messages from a chat
    messages = await client.get_messages(
        chat_id=123
    )
    return message, messages
```

## Service Overview

The Basalam Python SDK supports all resource endpoints for the following services:

- **Core Service (User, Booth, Product)** – Vendors, products, shipping methods, and user information
- **Order Service** – Manage baskets, payments, and invoices
- **Order Tracking Service** – Customer and vendor orders
- **Wallet Service** – Handle balances, expenses, and refunds
- **Chat Service** – Messaging and conversation functionality
- **Upload Service** – File uploads
- **Search Service** – Product and entity search
- **Webhook Service** – Manage events and webhooks
