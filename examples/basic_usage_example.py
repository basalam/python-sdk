#!/usr/bin/env python
"""
Basic Authentication and Usage Example

This minimal example demonstrates:
1. Basic authentication using different methods
2. Simple client usage patterns
3. Both synchronous and asynchronous API calls
"""

import asyncio

from basalam_sdk import BasalamClient
from basalam_sdk.auth import ClientCredentials, AuthorizationCode
from basalam_sdk.config import BasalamConfig


# 1. Client Credentials Authentication (Server-to-Server)
def client_credentials_example():
    """Example of using client credentials authentication."""
    print("\n=== Client Credentials Authentication ===")

    # Create authentication object
    auth = ClientCredentials(
        client_id="your-client-id",
        client_secret="your-client-secret",
        scopes=["webhook:read", "wallet:read"]  # Request specific scopes
    )

    # Get the token synchronously (authentication happens here)
    token_info = auth.get_token_sync()
    print(f"Access Token: {token_info.access_token[:10]}... (truncated)")
    print(f"Token Type: {token_info.token_type}")
    print(f"Expires In: {token_info.expires_in} seconds")

    # Create client with the authentication object
    client = BasalamClient(auth=auth)

    # Check granted scopes
    scopes = client.get_granted_scopes()
    print(f"Granted Scopes: {', '.join(scopes)}")

    return client


# 2. Authorization Code Flow (User Authentication)
def authorization_code_example():
    """Example of using authorization code authentication."""
    print("\n=== Authorization Code Authentication ===")

    # Create authentication object
    auth = AuthorizationCode(
        client_id="your-client-id",
        client_secret="your-client-secret",
        redirect_uri="https://your-app.com/callback",
        scopes=["webhook:read", "webhook:write", "wallet:read"]
    )

    # Generate authorization URL
    auth_url = auth.get_authorization_url(state="random-state-value")
    print(f"Authorization URL: {auth_url}")
    print("In a real application, redirect the user to this URL")

    # After user authorization, exchange the code for a token
    # In a real application, this would happen in your callback endpoint
    # code = "authorization-code-from-callback"
    # token_info = auth.exchange_code_sync(code)

    # For demonstration purposes, we'll mock a token
    print("Mocking token exchange (in a real app, you'd use the code from callback)")

    # Create client with the auth object
    # The token will be retrieved when making the first API call
    client = BasalamClient(auth=auth)

    return client


# 3. Using a custom configuration
def custom_config_example():
    """Example of using a custom configuration."""
    print("\n=== Custom Configuration ===")

    # Create a custom configuration
    config = BasalamConfig(
        api_base_url="https://api.custom-basalam.com",
        api_version="v2",
        timeout=60  # Longer timeout
    )

    # Create authentication with custom config
    auth = ClientCredentials(
        client_id="your-client-id",
        client_secret="your-client-secret",
        config=config
    )

    # Create client with custom auth and config
    client = BasalamClient(auth=auth, config=config)

    print(f"Using API Base URL: {config.api_base_url}")
    print(f"Using API Version: {config.api_version}")
    print(f"Using Timeout: {config.timeout} seconds")

    return client


# 4. Synchronous API calls
def synchronous_api_example(client):
    """Example of making synchronous API calls."""
    print("\n=== Synchronous API Calls ===")

    try:
        # Use the webhook service
        print("Using webhook service:")
        webhooks = client.webhook.get_webhooks_sync()
        print(f"Found {webhooks.result_count if hasattr(webhooks, 'result_count') else 0} webhooks")

        # Use the wallet service
        print("\nUsing wallet service:")
        balance = client.wallet.get_balance_sync()
        print(f"Balance: {balance.amount if hasattr(balance, 'amount') else 'N/A'}")

        # Use the order service
        print("\nUsing order service:")
        orders = client.order.get_orders_sync(limit=5)
        print(f"Found {len(orders) if orders else 0} recent orders")
    except Exception as e:
        print(f"API call failed: {e}")


# 5. Asynchronous API calls
async def asynchronous_api_example(client):
    """Example of making asynchronous API calls."""
    print("\n=== Asynchronous API Calls ===")

    try:
        # Use multiple services concurrently
        print("Making concurrent API calls...")

        # Create tasks for concurrent execution
        webhook_task = asyncio.create_task(client.webhook.get_webhooks())
        wallet_task = asyncio.create_task(client.wallet.get_balance())
        orders_task = asyncio.create_task(client.order.get_orders(limit=5))

        # Wait for all tasks to complete
        webhooks, balance, orders = await asyncio.gather(
            webhook_task, wallet_task, orders_task
        )

        # Show results
        print(f"Webhooks: Found {webhooks.result_count if hasattr(webhooks, 'result_count') else 0}")
        print(f"Wallet: Balance {balance.amount if hasattr(balance, 'amount') else 'N/A'}")
        print(f"Orders: Found {len(orders) if orders else 0} recent orders")
    except Exception as e:
        print(f"Async API call failed: {e}")


# 6. Error handling example
def error_handling_example(client):
    """Example of handling API errors."""
    print("\n=== Error Handling ===")

    from basalam_sdk.errors import (
        BasalamAuthError, BasalamApiError,
        ResourceNotFoundError, ValidationError
    )

    try:
        # Try to get a non-existent webhook
        print("Attempting to access a non-existent resource...")
        webhook = client.webhook.get_webhook_sync(webhook_id=99999)
    except ResourceNotFoundError as e:
        print(f"Resource not found: {e}")
    except ValidationError as e:
        print(f"Validation error: {e}")
    except BasalamAuthError as e:
        print(f"Authentication error: {e}")
    except BasalamApiError as e:
        print(f"API error: {e}")
    except Exception as e:
        print(f"Other error: {e}")


# 7. Token refresh example
def token_refresh_example(client):
    """Example of manually refreshing an authentication token."""
    print("\n=== Token Refresh ===")

    # Check if we need to refresh
    token_info = client.auth.token_info
    if token_info and token_info.should_refresh:
        print(f"Token will expire soon (expires in {token_info.expires_at - time.time():.1f} seconds)")

        # Refresh the token synchronously
        print("Refreshing token synchronously...")
        client.refresh_auth_token_sync()

        # Show new expiration time
        print(f"Token refreshed, new expiration: {client.auth.token_info.expires_in} seconds")
    else:
        print("Token refresh not needed")


# Main function
def main():
    """Run all examples."""
    print("=== Basalam SDK Basic Usage Example ===")

    # Client credentials example
    client = client_credentials_example()

    # Authorization code example would typically be in a web application flow
    # auth_client = authorization_code_example()

    # Custom configuration example
    # config_client = custom_config_example()

    # Synchronous API example
    synchronous_api_example(client)

    # Asynchronous API example
    asyncio.run(asynchronous_api_example(client))

    # Error handling example
    error_handling_example(client)

    # Token refresh example (would typically be needed for long-running applications)
    # token_refresh_example(client)


if __name__ == "__main__":
    main()
