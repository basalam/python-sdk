#!/usr/bin/env python
"""
Client Credentials Authentication Example

This example demonstrates how to use the Client Credentials authentication
method for server-to-server authentication with the Basalam SDK.
"""

import asyncio
import os

from basalam_sdk import BasalamClient
from basalam_sdk.auth import ClientCredentials
from basalam_sdk.errors import BasalamAuthError, BasalamApiError


def create_client():
    """Create an authenticated client using Client Credentials."""
    # Get credentials (from environment variables in real applications)
    client_id = os.environ.get("BASALAM_CLIENT_ID", "your-client-id")
    client_secret = os.environ.get("BASALAM_CLIENT_SECRET", "your-client-secret")

    # Create authentication object
    auth = ClientCredentials(
        client_id=client_id,
        client_secret=client_secret,
        scopes=["webhook:read", "wallet:read"]  # Request specific scopes
    )

    # Create and return the client
    return BasalamClient(auth=auth)


# Example of synchronous API usage
def sync_example(client):
    """Demonstrate synchronous API usage."""
    try:
        # Get webhooks
        print("Getting webhooks synchronously...")
        webhooks = client.webhook.get_webhooks_sync()
        print(f"Found {webhooks.result_count} webhooks")

        # Get wallet balance
        print("\nGetting wallet balance synchronously...")
        balance = client.wallet.get_balance_sync()
        print(f"Balance: {balance.amount} {balance.currency}")

        return True
    except BasalamAuthError as e:
        print(f"Authentication error: {e}")
        return False
    except BasalamApiError as e:
        print(f"API error: {e}")
        return False


# Example of asynchronous API usage
async def async_example(client):
    """Demonstrate asynchronous API usage."""
    try:
        # Execute multiple API calls concurrently
        print("Making concurrent API calls...")
        webhooks_task = asyncio.create_task(client.webhook.get_webhooks())
        balance_task = asyncio.create_task(client.wallet.get_balance())

        # Wait for both tasks to complete
        webhooks, balance = await asyncio.gather(webhooks_task, balance_task)

        # Print results
        print(f"Found {webhooks.result_count} webhooks")
        print(f"Balance: {balance.amount} {balance.currency}")

        return True
    except BasalamAuthError as e:
        print(f"Authentication error: {e}")
        return False
    except BasalamApiError as e:
        print(f"API error: {e}")
        return False


# Main function
def main():
    """Run the example."""
    print("=== Client Credentials Authentication Example ===")

    # Create authenticated client
    client = create_client()

    # Run synchronous example
    print("\n--- Synchronous API Calls ---")
    sync_example(client)

    # Run asynchronous example
    print("\n--- Asynchronous API Calls ---")
    asyncio.run(async_example(client))


if __name__ == "__main__":
    main()
