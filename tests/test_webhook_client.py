"""
Tests for the Webhook service client.
"""
import pytest

from basalam_sdk import BasalamClient
from basalam_sdk.auth import PersonalToken
from basalam_sdk.config import BasalamConfig, Environment
from basalam_sdk.webhook.models import (
    CreateServiceRequest,
    RegisterClientRequest,
    UnRegisterClientRequest,
)


@pytest.fixture
def basalam_client():
    """Create a BasalamClient instance with real auth and config."""
    config = BasalamConfig(
        environment=Environment.PRODUCTION,
        timeout=30.0,
        user_agent="SDK-Test"
    )
    auth = PersonalToken(
        token=""
    )
    return BasalamClient(auth=auth, config=config)


@pytest.mark.asyncio
async def test_get_webhook_services_async(basalam_client):
    """Test getting webhook services asynchronously."""
    webhook_service = basalam_client.webhook

    # Call the method
    result = await webhook_service.get_webhook_services()

    # Print the result
    print(f"Async webhook services result: {result}")

    # Check response structure
    assert hasattr(result, 'data')
    assert isinstance(result.data, list)


def test_get_webhook_services_sync(basalam_client):
    """Test getting webhook services synchronously."""
    webhook_service = basalam_client.webhook

    # Call the method
    result = webhook_service.get_webhook_services_sync()

    # Print the result
    print(f"Sync webhook services result: {result}")

    # Check response structure
    assert hasattr(result, 'data')
    assert isinstance(result.data, list)


@pytest.mark.asyncio
async def test_create_webhook_service_async(basalam_client):
    """Test creating a webhook service asynchronously."""
    webhook_service = basalam_client.webhook

    # Create a service request
    service_request = CreateServiceRequest(
        title="سلام سلام سلام",
        description="ستنیذسنت مینرتیسمت سیمرتسیمرتسیمرت"
    )

    # Call the method
    result = await webhook_service.create_webhook_service(service_request)

    # Print the result
    print(f"Async create webhook service result: {result}")

    # Check response structure
    assert hasattr(result, 'id')
    assert hasattr(result, 'title')
    assert result.title == "Test Service Async"
    assert result.description == "Test description for async service creation"


def test_create_webhook_service_sync(basalam_client):
    """Test creating a webhook service synchronously."""
    webhook_service = basalam_client.webhook

    # Create a service request
    service_request = CreateServiceRequest(
        title="Test Service Sync",
        description="Test description for sync service creation"
    )

    # Call the method
    result = webhook_service.create_webhook_service_sync(service_request)

    # Print the result
    print(f"Sync create webhook service result: {result}")

    # Check response structure
    assert hasattr(result, 'id')
    assert hasattr(result, 'title')
    assert result.title == "Test Service Sync"
    assert result.description == "Test description for sync service creation"


@pytest.mark.asyncio
async def test_get_webhook_events_async(basalam_client):
    """Test getting webhook events asynchronously."""
    webhook_service = basalam_client.webhook

    # Call the method
    result = await webhook_service.get_webhook_events()

    # Print the result
    print(f"Async webhook events result: {result}")

    # Check response structure
    assert hasattr(result, 'data')
    assert isinstance(result.data, list)


def test_get_webhook_events_sync(basalam_client):
    """Test getting webhook events synchronously."""
    webhook_service = basalam_client.webhook

    # Call the method
    result = webhook_service.get_webhook_events_sync()

    # Print the result
    print(f"Sync webhook events result: {result}")

    # Check response structure
    assert hasattr(result, 'data')
    assert isinstance(result.data, list)


@pytest.mark.asyncio
async def test_get_webhooks_async(basalam_client):
    """Test getting webhooks asynchronously."""
    webhook_service = basalam_client.webhook

    # Call the method
    result = await webhook_service.get_webhooks()

    # Print the result
    print(f"Async webhooks result: {result}")

    # Check response structure
    assert hasattr(result, 'data')
    assert isinstance(result.data, list)


def test_get_webhooks_sync(basalam_client):
    """Test getting webhooks synchronously."""
    webhook_service = basalam_client.webhook

    # Call the method
    result = webhook_service.get_webhooks_sync(event_ids="5,2")

    # Print the result
    print(f"Sync webhooks result: {result}")

    # Check response structure
    assert hasattr(result, 'data')
    assert isinstance(result.data, list)


@pytest.mark.asyncio
async def test_get_webhook_customers_async(basalam_client):
    """Test getting webhook customers asynchronously."""
    webhook_service = basalam_client.webhook

    # Call the method
    result = await webhook_service.get_webhook_customers(page=1, per_page=5)

    # Print the result
    print(f"Async webhook customers result: {result}")

    # Check response structure
    assert hasattr(result, 'data')
    assert result.data is not None


def test_get_webhook_customers_sync(basalam_client):
    """Test getting webhook customers synchronously."""
    webhook_service = basalam_client.webhook

    # Call the method
    result = webhook_service.get_webhook_customers_sync(page=1, per_page=5)

    # Print the result
    print(f"Sync webhook customers result: {result}")

    # Check response structure
    assert hasattr(result, 'data')
    assert result.data is not None


@pytest.mark.asyncio
async def test_get_registered_webhooks_async(basalam_client):
    """Test getting registered webhooks asynchronously."""
    webhook_service = basalam_client.webhook

    # Call the method
    result = await webhook_service.get_registered_webhooks(page=1, per_page=5)

    # Print the result
    print(f"Async registered webhooks result: {result}")

    # Check response structure
    assert hasattr(result, 'data')
    assert result.data is not None


def test_get_registered_webhooks_sync(basalam_client):
    """Test getting registered webhooks synchronously."""
    webhook_service = basalam_client.webhook

    # Call the method
    result = webhook_service.get_registered_webhooks_sync(page=1, per_page=5)

    # Print the result
    print(f"Sync registered webhooks result: {result}")

    # Check response structure
    assert hasattr(result, 'data')
    assert result.data is not None


@pytest.mark.asyncio
async def test_register_webhook_async(basalam_client):
    """Test registering a webhook asynchronously."""
    webhook_service = basalam_client.webhook

    # Create a register client request
    register_request = RegisterClientRequest(webhook_id=123)  # Use a test webhook_id

    # Call the method
    result = await webhook_service.register_webhook(register_request)

    # Print the result
    print(f"Async register webhook result: {result}")

    # Check response structure
    assert hasattr(result, 'id')
    assert hasattr(result, 'customer_id')
    assert hasattr(result, 'webhook_id')


def test_register_webhook_sync(basalam_client):
    """Test registering a webhook synchronously."""
    webhook_service = basalam_client.webhook

    # Create a register client request
    register_request = RegisterClientRequest(webhook_id=1647)  # Use a test webhook_id

    # Call the method
    result = webhook_service.register_webhook_sync(register_request)

    # Print the result
    print(f"Sync register webhook result: {result}")

    # Check response structure
    assert hasattr(result, 'id')
    assert hasattr(result, 'customer_id')
    assert hasattr(result, 'webhook_id')


@pytest.mark.asyncio
async def test_get_webhook_logs_async(basalam_client):
    """Test getting webhook logs asynchronously."""
    webhook_service = basalam_client.webhook

    # Use a test webhook ID (you may need to adjust this based on your test data)
    webhook_id = 196

    # Call the method
    result = await webhook_service.get_webhook_logs(webhook_id)

    # Print the result
    print(f"Async webhook logs result: {result}")

    # Check response structure
    assert hasattr(result, 'data')
    assert result.data is not None
    assert hasattr(result, 'result_count')
    assert hasattr(result, 'total_count')
    assert hasattr(result, 'page')
    assert hasattr(result, 'per_page')


def test_get_webhook_logs_sync(basalam_client):
    """Test getting webhook logs synchronously."""
    webhook_service = basalam_client.webhook

    # Use a test webhook ID (you may need to adjust this based on your test data)
    webhook_id = 196

    # Call the method
    result = webhook_service.get_webhook_logs_sync(webhook_id)

    # Print the result
    print(f"Sync webhook logs result: {result}")

    # Check response structure
    assert hasattr(result, 'data')
    assert result.data is not None
    assert hasattr(result, 'result_count')
    assert hasattr(result, 'total_count')
    assert hasattr(result, 'page')
    assert hasattr(result, 'per_page')


@pytest.mark.asyncio
async def test_delete_webhook_async(basalam_client):
    """Test deleting a webhook asynchronously."""
    webhook_service = basalam_client.webhook

    # Use a test webhook ID (you may need to adjust this based on your test data)
    webhook_id = 196

    # Call the method
    result = await webhook_service.delete_webhook(webhook_id)

    # Print the result
    print(f"Async delete webhook result: {result}")

    # Check response structure
    assert hasattr(result, 'id')
    assert result.id == webhook_id
    assert hasattr(result, 'deleted_at')


def test_delete_webhook_sync(basalam_client):
    """Test deleting a webhook synchronously."""
    webhook_service = basalam_client.webhook

    # Use a test webhook ID (you may need to adjust this based on your test data)
    webhook_id = 196

    # Call the method
    result = webhook_service.delete_webhook_sync(webhook_id)

    # Print the result
    print(f"Sync delete webhook result: {result}")

    # Check response structure
    assert hasattr(result, 'id')
    assert result.id == webhook_id
    assert hasattr(result, 'deleted_at')


@pytest.mark.asyncio
async def test_unregister_webhook_async(basalam_client):
    """Test unregistering a webhook client asynchronously."""
    webhook_service = basalam_client.webhook

    # Create an unregister client request
    unregister_request = UnRegisterClientRequest(
        webhook_id=153,
        customer_id=430  # Optional parameter
    )

    # Call the method
    result = await webhook_service.unregister_webhook(unregister_request)

    # Print the result
    print(f"Async unregister webhook result: {result}")

    # Check response structure
    assert hasattr(result, 'webhook_id')
    assert hasattr(result, 'customer_id')
    assert hasattr(result, 'deleted_at')


def test_unregister_webhook_sync(basalam_client):
    """Test unregistering a webhook client synchronously."""
    webhook_service = basalam_client.webhook

    # Create an unregister client request
    unregister_request = UnRegisterClientRequest(
        webhook_id=196,
        customer_id=123  # Optional parameter
    )

    # Call the method
    result = webhook_service.unregister_webhook_sync(unregister_request)

    # Print the result
    print(f"Sync unregister webhook result: {result}")

    # Check response structure
    assert hasattr(result, 'webhook_id')
    assert result.webhook_id == 196
    assert hasattr(result, 'customer_id')
    assert hasattr(result, 'deleted_at')
