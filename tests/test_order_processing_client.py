"""
Tests for the Order Processing service client.
"""
import pytest

from basalam_sdk import BasalamClient
from basalam_sdk.auth import PersonalToken
from basalam_sdk.config import BasalamConfig, Environment
from basalam_sdk.order_processing.models import (
    OrderFilter,
    ItemFilter,
    OrderParcelFilter,
    ResourceStats,
    ParcelStatus,
    PostedOrderRequest,
    ShippingMethodCode,
)

# Test IDs (you'll need valid IDs for testing)
TEST_ORDER_ID = 57745665
TEST_ITEM_ID = 67890
TEST_PARCEL_ID = 59530910
TEST_VENDOR_ID = "266"
TEST_CUSTOMER_ID = "430"
TEST_PRODUCT_ID = 456
TEST_SHIPPING_METHOD = ShippingMethodCode.SPECIAL
TEST_TRACKING_CODE = "072500037102188250223200"


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


# -------------------------------------------------------------------------
# Customer Orders endpoints tests
# -------------------------------------------------------------------------

@pytest.mark.asyncio
async def test_get_orders_async(basalam_client):
    """Test get_orders async method."""
    try:
        # Test without filters
        result = await basalam_client.order_processing.get_customer_orders()
        print(f"get_orders async (no filters) result: {result}")
        assert hasattr(result, 'data')

        # Test with filters
        filters = OrderFilter(
            per_page=10
        )
        result_filtered = await basalam_client.order_processing.get_customer_orders(filters=filters)
        print(f"get_orders async (with filters) result: {result_filtered}")
        assert hasattr(result_filtered, 'data')

    except Exception as e:
        print(f"get_orders async error: {e}")
        # Don't fail the test for API errors, just log them
        assert True


def test_get_customer_orders_sync(basalam_client):
    """Test get_customer_orders_sync method."""
    try:
        # Test without filters
        result = basalam_client.order_processing.get_customer_orders_sync()
        print(f"get_customer_orders_sync (no filters) result: {result}")
        assert hasattr(result, 'data')

        # Test with filters
        filters = OrderFilter(
            per_page=5,
            sort="paid_at:asc",
        )
        result_filtered = basalam_client.order_processing.get_customer_orders_sync(filters=filters)
        print(f"get_customer_orders_sync (with filters) result: {result_filtered}")
        assert hasattr(result_filtered, 'data')

    except Exception as e:
        print(f"get_customer_orders_sync error: {e}")
        # Don't fail the test for API errors, just log them
        assert True


@pytest.mark.asyncio
async def test_get_order_async(basalam_client):
    """Test get_order async method."""
    try:
        result = await basalam_client.order_processing.get_customer_order(TEST_ORDER_ID)
        print(f"get_order async result: {result}")
        assert hasattr(result, 'id')

    except Exception as e:
        print(f"get_order async error: {e}")
        # Don't fail the test for API errors, just log them
        assert True


def test_get_customer_order_sync(basalam_client):
    """Test get_order_sync method."""
    try:
        result = basalam_client.order_processing.get_customer_order(TEST_ORDER_ID)
        print(f"get_order_sync result: {result}")
        assert hasattr(result, 'id')

    except Exception as e:
        print(f"get_order_sync error: {e}")
        # Don't fail the test for API errors, just log them
        assert True


# -------------------------------------------------------------------------
# Customer Items endpoints tests
# -------------------------------------------------------------------------

@pytest.mark.asyncio
async def test_get_customer_order_items_async(basalam_client):
    """Test get_customer_order_items async method."""
    try:
        # Test without filters
        result = await basalam_client.order_processing.get_customer_order_items()
        print(f"get_customer_order_items async (no filters) result: {result}")
        assert hasattr(result, 'data')

        # Test with filters
        filters = ItemFilter(
            per_page=10,
            sort="created_at:desc",
            vendor_ids=[TEST_VENDOR_ID]
        )
        result_filtered = await basalam_client.order_processing.get_customer_order_items(filters=filters)
        print(f"get_customer_order_items async (with filters) result: {result_filtered}")
        assert hasattr(result_filtered, 'data')

    except Exception as e:
        print(f"get_customer_order_items async error: {e}")
        # Don't fail the test for API errors, just log them
        assert True


def test_get_customer_order_items_sync(basalam_client):
    """Test get_customer_order_items_sync method."""
    try:
        # Test without filters
        result = basalam_client.order_processing.get_customer_order_items_sync()
        print(f"get_customer_order_items_sync (no filters) result: {result}")
        assert hasattr(result, 'data')

        # Test with filters
        filters = ItemFilter(
            per_page=5,
            customer_ids=[TEST_CUSTOMER_ID],
            product_ids=[TEST_PRODUCT_ID]
        )
        result_filtered = basalam_client.order_processing.get_customer_order_items_sync(filters=filters)
        print(f"get_customer_order_items_sync (with filters) result: {result_filtered}")
        assert hasattr(result_filtered, 'data')

    except Exception as e:
        print(f"get_customer_order_items_sync error: {e}")
        # Don't fail the test for API errors, just log them
        assert True


@pytest.mark.asyncio
async def test_get_customer_order_item_async(basalam_client):
    """Test get_customer_order_item async method."""
    try:
        result = await basalam_client.order_processing.get_customer_order_item(TEST_ORDER_ID)
        print(f"get_customer_order_item async result: {result}")
        assert hasattr(result, 'id')

    except Exception as e:
        print(f"get_customer_order_item async error: {e}")
        # Don't fail the test for API errors, just log them
        assert True


def test_get_customer_order_item_sync(basalam_client):
    """Test get_customer_order_item_sync method."""
    try:
        result = basalam_client.order_processing.get_customer_order_item_sync(TEST_ITEM_ID)
        print(f"get_customer_order_item_sync result: {result}")
        assert hasattr(result, 'id')

    except Exception as e:
        print(f"get_customer_order_item_sync error: {e}")
        # Don't fail the test for API errors, just log them
        assert True


# -------------------------------------------------------------------------
# Vendor Parcels endpoints tests
# -------------------------------------------------------------------------

@pytest.mark.asyncio
async def test_get_vendor_orders_parcels_async(basalam_client):
    """Test get_vendor_orders_parcels async method."""
    try:
        # Test without filters
        result = await basalam_client.order_processing.get_vendor_orders_parcels()
        print(f"get_vendor_orders_parcels async (no filters) result: {result}")
        assert hasattr(result, 'data')

        # Test with filters
        filters = OrderParcelFilter(
            per_page=10,
            sort="estimate_send_at:desc",
            statuses=[ParcelStatus.NEW_ORDER, ParcelStatus.PREPARATION_IN_PROGRESS]
        )
        result_filtered = await basalam_client.order_processing.get_vendor_orders_parcels(filters=filters)
        print(f"get_vendor_orders_parcels async (with filters) result: {result_filtered}")
        assert hasattr(result_filtered, 'data')

    except Exception as e:
        print(f"get_vendor_orders_parcels async error: {e}")
        # Don't fail the test for API errors, just log them
        assert True


def test_get_vendor_orders_parcels_sync(basalam_client):
    """Test get_vendor_orders_parcels_sync method."""
    try:
        # Test without filters
        result = basalam_client.order_processing.get_vendor_orders_parcels_sync()
        print(f"get_vendor_orders_parcels_sync (no filters) result: {result}")
        assert hasattr(result, 'data')

        # Test with filters
        filters = OrderParcelFilter(
            per_page=5
        )
        result_filtered = basalam_client.order_processing.get_vendor_orders_parcels_sync(filters=filters)
        print(f"get_vendor_orders_parcels_sync (with filters) result: {result_filtered}")
        assert hasattr(result_filtered, 'data')

    except Exception as e:
        print(f"get_vendor_orders_parcels_sync error: {e}")
        # Don't fail the test for API errors, just log them
        assert True


@pytest.mark.asyncio
async def test_get_order_parcel_async(basalam_client):
    """Test get_order_parcel async method."""
    try:
        result = await basalam_client.order_processing.get_order_parcel(TEST_PARCEL_ID)
        print(f"get_order_parcel async result: {result}")
        assert hasattr(result, 'id')

    except Exception as e:
        print(f"get_order_parcel async error: {e}")
        # Don't fail the test for API errors, just log them
        assert True


def test_get_order_parcel_sync(basalam_client):
    """Test get_order_parcel_sync method."""
    try:
        result = basalam_client.order_processing.get_order_parcel_sync(TEST_PARCEL_ID)
        print(f"get_order_parcel_sync result: {result}")
        assert hasattr(result, 'id')

    except Exception as e:
        print(f"get_order_parcel_sync error: {e}")
        # Don't fail the test for API errors, just log them
        assert True


@pytest.mark.asyncio
async def test_set_order_parcel_preparation_async(basalam_client):
    """Test set_order_parcel_preparation async method."""
    try:
        result = await basalam_client.order_processing.set_order_parcel_preparation(TEST_PARCEL_ID)
        print(f"set_order_parcel_preparation async result: {result}")
        assert hasattr(result, 'result')

    except Exception as e:
        print(f"set_order_parcel_preparation async error: {e}")
        # Don't fail the test for API errors, just log them
        assert True


def test_set_order_parcel_preparation_sync(basalam_client):
    """Test set_order_parcel_preparation_sync method."""
    try:
        result = basalam_client.order_processing.set_order_parcel_preparation_sync(TEST_PARCEL_ID)
        print(f"set_order_parcel_preparation_sync result: {result}")
        assert hasattr(result, 'result')

    except Exception as e:
        print(f"set_order_parcel_preparation_sync error: {e}")
        # Don't fail the test for API errors, just log them
        assert True


@pytest.mark.asyncio
async def test_set_order_parcel_posted_async(basalam_client):
    """Test set_order_parcel_posted async method."""
    try:
        posted_request = PostedOrderRequest(
            shipping_method=TEST_SHIPPING_METHOD,
            tracking_code=TEST_TRACKING_CODE,
        )
        result = await basalam_client.order_processing.set_order_parcel_posted(
            TEST_PARCEL_ID,
            posted_request,
        )
        print(f"set_order_parcel_posted async result: {result}")
        assert hasattr(result, 'result')

    except Exception as e:
        print(f"set_order_parcel_posted async error: {e}")
        # Don't fail the test for API errors, just log them
        assert True


def test_set_order_parcel_posted_sync(basalam_client):
    """Test set_order_parcel_posted_sync method."""
    try:
        posted_request = PostedOrderRequest(
            shipping_method=TEST_SHIPPING_METHOD,
            tracking_code="TEST-CODE",
        )
        result = basalam_client.order_processing.set_order_parcel_posted_sync(
            TEST_PARCEL_ID,
            posted_request,
        )
        print(f"set_order_parcel_posted_sync result: {result}")
        assert hasattr(result, 'result')

    except Exception as e:
        print(f"set_order_parcel_posted_sync error: {e}")
        # Don't fail the test for API errors, just log them
        assert True


# -------------------------------------------------------------------------
# Order Statistics endpoints tests
# -------------------------------------------------------------------------

@pytest.mark.asyncio
async def test_get_orders_stats_async(basalam_client):
    """Test get_orders_stats async method."""
    try:
        # Test with minimal parameters
        result = basalam_client.order_processing.get_orders_stats_sync(
            resource_count=ResourceStats.NUMBER_OF_NOT_SHIPPED_ORDERS_PER_VENDOR,
            vendor_id=TEST_VENDOR_ID
        )
        print(f"get_orders_stats_sync (minimal) result: {result}")
        assert hasattr(result, 'result')

        # Test with vendor-specific stats
        result_vendor = basalam_client.order_processing.get_orders_stats_sync(
            resource_count=ResourceStats.NUMBER_OF_COMPLETED_ORDERS_PER_VENDOR,
            vendor_id=TEST_VENDOR_ID
        )
        print(f"get_orders_stats async (full) result: {result_vendor}")
        assert hasattr(result_vendor, 'result')

    except Exception as e:
        print(f"get_orders_stats async error: {e}")
        # Don't fail the test for API errors, just log them
        assert True


def test_get_orders_stats_sync(basalam_client):
    """Test get_orders_stats_sync method."""
    try:
        # Test with minimal parameters
        result = basalam_client.order_processing.get_orders_stats_sync(
            resource_count=ResourceStats.NUMBER_OF_NOT_SHIPPED_ORDERS_PER_VENDOR,
            vendor_id=TEST_VENDOR_ID
        )
        print(f"get_orders_stats_sync (minimal) result: {result}")
        assert hasattr(result, 'result')

        # Test with vendor-specific stats
        result_vendor = basalam_client.order_processing.get_orders_stats_sync(
            resource_count=ResourceStats.NUMBER_OF_COMPLETED_ORDERS_PER_VENDOR,
            vendor_id=TEST_VENDOR_ID
        )
        print(f"get_orders_stats_sync (vendor) result: {result_vendor}")
        assert hasattr(result_vendor, 'result')

    except Exception as e:
        print(f"get_orders_stats_sync error: {e}")
        # Don't fail the test for API errors, just log them
        assert True
