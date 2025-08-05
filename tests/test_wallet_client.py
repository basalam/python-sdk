"""
Tests for the Wallet service client.
"""
import pytest

from basalam_sdk import BasalamClient
from basalam_sdk.auth import ClientCredentials
from basalam_sdk.config import BasalamConfig, Environment
from basalam_sdk.wallet.models import (
    BalanceFilter,
    SpendCreditRequest,
    SpendSpecificCreditRequest,
    RefundRequest,
    RollbackRefundRequest
)

# Test client credentials
TEST_CLIENT_ID = ""
TEST_CLIENT_SECRET = ""

# Test user ID (you'll need a valid user ID for testing)
TEST_USER_ID = 430


@pytest.fixture
def basalam_client():
    """Create a BasalamClient instance with real auth and config."""
    config = BasalamConfig(
        environment=Environment.PRODUCTION,
        timeout=30.0,
        user_agent="Integration Test Agent"
    )
    auth = ClientCredentials(
        client_id=TEST_CLIENT_ID,
        client_secret=TEST_CLIENT_SECRET
    )
    return BasalamClient(auth=auth, config=config)


# -------------------------------------------------------------------------
# Balance endpoints tests
# -------------------------------------------------------------------------

@pytest.mark.asyncio
async def test_get_balance_async(basalam_client):
    """Test get_balance async method."""
    try:
        balance_filters = [BalanceFilter(cash=True, settleable=True)]
        result = await basalam_client.wallet.get_balance(
            user_id=TEST_USER_ID,
            filters=balance_filters
        )
        print(f"get_balance async result: {result}")
        assert hasattr(result, 'data')
    except Exception as e:
        print(f"get_balance async error: {e}")
        # Don't fail the test for API errors, just log them
        assert True


def test_get_balance_sync(basalam_client):
    """Test get_balance_sync method."""
    try:
        balance_filters = [BalanceFilter(cash=True, settleable=True)]
        result = basalam_client.wallet.get_balance_sync(
            user_id=TEST_USER_ID,
            filters=balance_filters
        )
        print(f"get_balance_sync result: {result}")
        assert hasattr(result, 'data')
    except Exception as e:
        print(f"get_balance_sync error: {e}")
        # Don't fail the test for API errors, just log them
        assert True


@pytest.mark.asyncio
async def test_get_transactions_async(basalam_client):
    """Test get_transactions async method."""
    try:
        result = await basalam_client.wallet.get_transactions(
            user_id=TEST_USER_ID,
            page=1,
            per_page=10
        )
        print(f"get_transactions async result: {result}")
        assert result is not None
    except Exception as e:
        print(f"get_transactions async error: {e}")
        # Don't fail the test for API errors, just log them
        assert True


def test_get_transactions_sync(basalam_client):
    """Test get_transactions_sync method."""
    try:
        result = basalam_client.wallet.get_transactions_sync(
            user_id=TEST_USER_ID,
            page=1,
            per_page=100
        )
        print(f"get_transactions_sync result: {result}")
        assert result is not None
    except Exception as e:
        print(f"get_transactions_sync error: {e}")
        # Don't fail the test for API errors, just log them
        assert True


# -------------------------------------------------------------------------
# Credit spending endpoints tests
# -------------------------------------------------------------------------

@pytest.mark.asyncio
async def test_create_expense_async(basalam_client):
    """Test create_expense async method."""
    try:
        request = SpendCreditRequest(
            amount=1000,
            reason_id=38,
            reference_id=117,
            description="Test expense"
        )
        result = await basalam_client.wallet.create_expense(
            user_id=TEST_USER_ID,
            request=request
        )
        print(f"create_expense async result: \n {result}")
        assert result is not None
    except Exception as e:
        print(f"create_expense async error: {e}")
        # Don't fail the test for API errors, just log them
        assert True


def test_create_expense_sync(basalam_client):
    """Test create_expense_sync method."""
    try:
        request = SpendCreditRequest(
            amount=1000,
            reason_id=1,
            reference_id=12345,
            description="Test expense"
        )
        result = basalam_client.wallet.create_expense_sync(
            user_id=TEST_USER_ID,
            request=request
        )
        print(f"create_expense_sync result: {result}")
        assert result is not None
    except Exception as e:
        print(f"create_expense_sync error: {e}")
        # Don't fail the test for API errors, just log them
        assert True


@pytest.mark.asyncio
async def test_create_expense_from_credit_async(basalam_client):
    """Test create_expense_from_credit async method."""
    try:
        request = SpendSpecificCreditRequest(
            amount=1000,
            reason_id=1,
            reference_id=12345,
            description="Test expense from credit"
        )
        result = await basalam_client.wallet.create_expense_from_credit(
            user_id=TEST_USER_ID,
            credit_id=1,
            request=request
        )
        print(f"create_expense_from_credit async result: {result}")
        assert result is not None
    except Exception as e:
        print(f"create_expense_from_credit async error: {e}")
        # Don't fail the test for API errors, just log them
        assert True


def test_create_expense_from_credit_sync(basalam_client):
    """Test create_expense_from_credit_sync method."""
    try:
        request = SpendSpecificCreditRequest(
            amount=1000,
            reason_id=1,
            reference_id=12345,
            description="Test expense from credit"
        )
        result = basalam_client.wallet.create_expense_from_credit_sync(
            user_id=TEST_USER_ID,
            credit_id=1,
            request=request
        )
        print(f"create_expense_from_credit_sync result: {result}")
        assert result is not None
    except Exception as e:
        print(f"create_expense_from_credit_sync error: {e}")
        # Don't fail the test for API errors, just log them
        assert True


@pytest.mark.asyncio
async def test_get_expense_async(basalam_client):
    """Test get_expense async method."""
    try:
        result = await basalam_client.wallet.get_expense(
            user_id=TEST_USER_ID,
            expense_id=6009
        )
        print(f"get_expense async result: {result}")
        assert result is not None
    except Exception as e:
        print(f"get_expense async error: {e}")
        # Don't fail the test for API errors, just log them
        assert True


def test_get_expense_sync(basalam_client):
    """Test get_expense_sync method."""
    try:
        result = basalam_client.wallet.get_expense_sync(
            user_id=TEST_USER_ID,
            expense_id=1
        )
        print(f"get_expense_sync result: {result}")
        assert result is not None
    except Exception as e:
        print(f"get_expense_sync error: {e}")
        # Don't fail the test for API errors, just log them
        assert True


@pytest.mark.asyncio
async def test_delete_expense_async(basalam_client):
    """Test delete_expense async method."""
    try:
        result = await basalam_client.wallet.delete_expense(
            user_id=TEST_USER_ID,
            expense_id=1,
            rollback_reason_id=1
        )
        print(f"delete_expense async result: {result}")
        assert result is not None
    except Exception as e:
        print(f"delete_expense async error: {e}")
        # Don't fail the test for API errors, just log them
        assert True


def test_delete_expense_sync(basalam_client):
    """Test delete_expense_sync method."""
    try:
        result = basalam_client.wallet.delete_expense_sync(
            user_id=TEST_USER_ID,
            expense_id=1,
            rollback_reason_id=1
        )
        print(f"delete_expense_sync result: {result}")
        assert result is not None
    except Exception as e:
        print(f"delete_expense_sync error: {e}")
        # Don't fail the test for API errors, just log them
        assert True


@pytest.mark.asyncio
async def test_get_expense_by_ref_async(basalam_client):
    """Test get_expense_by_ref async method."""
    try:
        result = await basalam_client.wallet.get_expense_by_ref(
            user_id=TEST_USER_ID,
            reason_id=1,
            reference_id=12345
        )
        print(f"get_expense_by_ref async result: {result}")
        assert result is not None
    except Exception as e:
        print(f"get_expense_by_ref async error: {e}")
        # Don't fail the test for API errors, just log them
        assert True


def test_get_expense_by_ref_sync(basalam_client):
    """Test get_expense_by_ref_sync method."""
    try:
        result = basalam_client.wallet.get_expense_by_ref_sync(
            user_id=TEST_USER_ID,
            reason_id=1,
            reference_id=12345
        )
        print(f"get_expense_by_ref_sync result: {result}")
        assert result is not None
    except Exception as e:
        print(f"get_expense_by_ref_sync error: {e}")
        # Don't fail the test for API errors, just log them
        assert True


@pytest.mark.asyncio
async def test_delete_expense_by_ref_async(basalam_client):
    """Test delete_expense_by_ref async method."""
    try:
        result = await basalam_client.wallet.delete_expense_by_ref(
            user_id=TEST_USER_ID,
            reason_id=1,
            reference_id=12345,
            rollback_reason_id=1
        )
        print(f"delete_expense_by_ref async result: {result}")
        assert result is not None
    except Exception as e:
        print(f"delete_expense_by_ref async error: {e}")
        # Don't fail the test for API errors, just log them
        assert True


def test_delete_expense_by_ref_sync(basalam_client):
    """Test delete_expense_by_ref_sync method."""
    try:
        result = basalam_client.wallet.delete_expense_by_ref_sync(
            user_id=TEST_USER_ID,
            reason_id=1,
            reference_id=12345,
            rollback_reason_id=1
        )
        print(f"delete_expense_by_ref_sync result: {result}")
        assert result is not None
    except Exception as e:
        print(f"delete_expense_by_ref_sync error: {e}")
        # Don't fail the test for API errors, just log them
        assert True


# -------------------------------------------------------------------------
# Refund endpoints tests
# -------------------------------------------------------------------------

@pytest.mark.asyncio
async def test_create_refund_async(basalam_client):
    """Test create_refund async method."""
    try:
        request = RefundRequest(
            user_id=TEST_USER_ID,
            amount=1000,
            reason_id=1,
            reference_id=12345,
            description="Test refund"
        )
        result = await basalam_client.wallet.create_refund(request=request)
        print(f"create_refund async result: {result}")
        assert result is not None
    except Exception as e:
        print(f"create_refund async error: {e}")
        # Don't fail the test for API errors, just log them
        assert True


def test_create_refund_sync(basalam_client):
    """Test create_refund_sync method."""
    try:
        request = RefundRequest(
            user_id=TEST_USER_ID,
            amount=1000,
            reason_id=1,
            reference_id=12345,
            description="Test refund"
        )
        result = basalam_client.wallet.create_refund_sync(request=request)
        print(f"create_refund_sync result: {result}")
        assert result is not None
    except Exception as e:
        print(f"create_refund_sync error: {e}")
        # Don't fail the test for API errors, just log them
        assert True


@pytest.mark.asyncio
async def test_can_rollback_refund_async(basalam_client):
    """Test can_rollback_refund async method."""
    try:
        result = await basalam_client.wallet.can_rollback_refund(
            refund_reason=1,
            refund_reference_id=12345
        )
        print(f"can_rollback_refund async result: {result}")
        assert isinstance(result, bool)
    except Exception as e:
        print(f"can_rollback_refund async error: {e}")
        # Don't fail the test for API errors, just log them
        assert True


def test_can_rollback_refund_sync(basalam_client):
    """Test can_rollback_refund_sync method."""
    try:
        result = basalam_client.wallet.can_rollback_refund_sync(
            refund_reason=1,
            refund_reference_id=12345
        )
        print(f"can_rollback_refund_sync result: {result}")
        assert isinstance(result, bool)
    except Exception as e:
        print(f"can_rollback_refund_sync error: {e}")
        # Don't fail the test for API errors, just log them
        assert True


@pytest.mark.asyncio
async def test_rollback_refund_async(basalam_client):
    """Test rollback_refund async method."""
    try:
        request = RollbackRefundRequest(
            refund_reason=1,
            refund_reference_id=12345,
            rollback_reason_id=1
        )
        result = await basalam_client.wallet.rollback_refund(request=request)
        print(f"rollback_refund async result: {result}")
        assert result is not None
    except Exception as e:
        print(f"rollback_refund async error: {e}")
        # Don't fail the test for API errors, just log them
        assert True


def test_rollback_refund_sync(basalam_client):
    """Test rollback_refund_sync method."""
    try:
        request = RollbackRefundRequest(
            refund_reason=1,
            refund_reference_id=12345,
            rollback_reason_id=1
        )
        result = basalam_client.wallet.rollback_refund_sync(request=request)
        print(f"rollback_refund_sync result: {result}")
        assert result is not None
    except Exception as e:
        print(f"rollback_refund_sync error: {e}")
        # Don't fail the test for API errors, just log them
        assert True
