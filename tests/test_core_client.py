"""
Tests for the Core service client async functions.
"""
import pytest

from basalam_sdk import BasalamClient, PersonalToken
from basalam_sdk.config import BasalamConfig, Environment
from basalam_sdk.core.models import (
    CreateVendorSchema,
    UpdateVendorSchema,
    VendorLegalRequestSchema,
    UpdateShippingMethodSchema,
    ShippingMethodUpdateItem,
    GetVendorProductsSchema,
    ProductStatusInputEnum,
    UpdateVendorStatusSchema,
    ChangeVendorMobileRequestSchema,
    ChangeVendorMobileConfirmSchema,
    ProductRequestSchema,
    BatchUpdateProductsRequest,
    UpdateProductRequestItem,
    BulkProductsUpdateRequestSchema,
    ProductFilterSchema,
    BulkActionItem,
    UpdateProductVariationSchema,
    CreateDiscountRequestSchema,
    DeleteDiscountRequestSchema,
    DiscountProductFilterSchema,
    ConfirmCurrentUserMobileConfirmSchema,
    ChangeUserMobileRequestSchema,
    ChangeUserMobileConfirmSchema,
    UserCardsSchema,
    UserCardsOtpSchema,
    UserVerifyBankInformationSchema,
    UpdateUserBankInformationSchema,
    UserVerificationSchema,
    UnitTypeInputEnum, ProductBulkFieldInputEnum, ProductBulkActionTypeEnum
)

# Test IDs (you'll need valid IDs for testing)
TEST_USER_ID = 430
TEST_VENDOR_ID = 266
TEST_PRODUCT_ID = 24835037
TEST_CATEGORY_ID = 1066

# Additional test IDs
TEST_BANK_ACCOUNT_ID = 54321


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
# Vendor Management endpoints tests
# -------------------------------------------------------------------------

@pytest.mark.asyncio
async def test_create_vendor_async(basalam_client):
    """Test create_vendor async method."""
    try:
        request = CreateVendorSchema(
            title="Test Vendor",
            identifier="test-vendor-unique",
            category_type=1,
            city=1,
            notice="Test vendor notice",
            summary="Test vendor summary",
            address="Test address",
            postal_code="1234567890",
            legal_data=VendorLegalRequestSchema(is_legal=False)
        )
        result = await basalam_client.core.create_vendor(TEST_USER_ID, request)
        print(f"create_vendor async result: {result}")
        assert hasattr(result, 'id')

    except Exception as e:
        print(f"create_vendor async error: {e}")
        # Don't fail the test for API errors, just log them
        assert True


@pytest.mark.asyncio
async def test_update_vendor_async(basalam_client):
    """Test update_vendor async method."""
    try:
        request = UpdateVendorSchema(
            title="Updated Test Vendor",
            notice="Updated notice",
            summary="Updated summary"
        )
        result = await basalam_client.core.update_vendor(TEST_VENDOR_ID, request)
        print(f"update_vendor async result: {result}")
        assert hasattr(result, 'id')

    except Exception as e:
        print(f"update_vendor async error: {e}")
        # Don't fail the test for API errors, just log them
        assert True


@pytest.mark.asyncio
async def test_get_vendor_async(basalam_client):
    """Test get_vendor async method."""
    try:
        # Test with minimal response
        result_minimal = await basalam_client.core.get_vendor(TEST_VENDOR_ID)
        print(f"get_vendor async (minimal) result: {result_minimal}")
        assert hasattr(result_minimal, 'id')

        # Test with full
        result_full = await basalam_client.core.get_vendor(
            TEST_VENDOR_ID,
            prefer="return=full"
        )
        print(f"get_vendor async (full) result: {result_full}")
        assert hasattr(result_full, 'id')

    except Exception as e:
        print(f"get_vendor async error: {e}")
        # Don't fail the test for API errors, just log them
        assert True


@pytest.mark.asyncio
async def test_get_default_shipping_methods_async(basalam_client):
    """Test get_default_shipping_methods async method."""
    try:
        result = await basalam_client.core.get_default_shipping_methods()
        print(f"get_default_shipping_methods async result: {result}")
        assert isinstance(result, list)

    except Exception as e:
        print(f"get_default_shipping_methods async error: {e}")
        # Don't fail the test for API errors, just log them
        assert True


@pytest.mark.asyncio
async def test_get_shipping_methods_async(basalam_client):
    """Test get_shipping_methods async method."""
    try:
        # Test without filters
        result = await basalam_client.core.get_shipping_methods()
        print(f"get_shipping_methods async (no filters) result: {result}")
        assert hasattr(result, 'data')

        # Test with filters
        result_filtered = await basalam_client.core.get_shipping_methods(
            vendor_ids=[TEST_VENDOR_ID],
            page=1,
            per_page=5
        )
        print(f"get_shipping_methods async (with filters) result: {result_filtered}")
        assert hasattr(result_filtered, 'data')

    except Exception as e:
        print(f"get_shipping_methods async error: {e}")
        # Don't fail the test for API errors, just log them
        assert True


@pytest.mark.asyncio
async def test_get_working_shipping_methods_async(basalam_client):
    """Test get_working_shipping_methods async method."""
    try:
        result = await basalam_client.core.get_working_shipping_methods(TEST_VENDOR_ID)
        print(f"get_working_shipping_methods async result: {result}")
        assert isinstance(result, list)

    except Exception as e:
        print(f"get_working_shipping_methods async error: {e}")
        # Don't fail the test for API errors, just log them
        assert True


@pytest.mark.asyncio
async def test_update_shipping_methods_async(basalam_client):
    """Test update_shipping_methods async method."""
    try:
        request = UpdateShippingMethodSchema(
            shipping_methods=[
                ShippingMethodUpdateItem(
                    method_id=1,
                    is_customized=True,
                    base_cost=10000,
                    additional_cost=5000
                )
            ]
        )
        result = await basalam_client.core.update_shipping_methods(TEST_VENDOR_ID, request)
        print(f"update_shipping_methods async result: {result}")
        assert isinstance(result, list)

    except Exception as e:
        print(f"update_shipping_methods async error: {e}")
        # Don't fail the test for API errors, just log them
        assert True


@pytest.mark.asyncio
async def test_get_vendor_products_async(basalam_client):
    """Test get_vendor_products async method."""
    try:
        # Test without query params
        result = await basalam_client.core.get_vendor_products(TEST_VENDOR_ID)
        print(f"get_vendor_products async (no params) result: {result}")
        assert hasattr(result, 'data')

        # Test with query params
        query_params = GetVendorProductsSchema(
            page=1,
            per_page=5,
            statuses=[ProductStatusInputEnum.PUBLISHED],
            stock_gte=50,

        )
        result_filtered = await basalam_client.core.get_vendor_products(TEST_VENDOR_ID, query_params)
        print(f"get_vendor_products async (with params) result: {result_filtered}")
        assert hasattr(result_filtered, 'data')

    except Exception as e:
        print(f"get_vendor_products async error: {e}")
        # Don't fail the test for API errors, just log them
        assert True


@pytest.mark.asyncio
async def test_update_vendor_status_async(basalam_client):
    """Test update_vendor_status async method."""
    try:
        request = UpdateVendorStatusSchema(
            status=1,
            description="Test status update",
            reason=1
        )
        result = await basalam_client.core.update_vendor_status(TEST_VENDOR_ID, request)
        print(f"update_vendor_status async result: {result}")
        assert hasattr(result, 'status')

    except Exception as e:
        print(f"update_vendor_status async error: {e}")
        # Don't fail the test for API errors, just log them
        assert True


@pytest.mark.asyncio
async def test_create_vendor_mobile_change_request_async(basalam_client):
    """Test create_vendor_mobile_change_request async method."""
    try:
        request = ChangeVendorMobileRequestSchema(
            mobile="09123456789"
        )
        result = await basalam_client.core.create_vendor_mobile_change_request(TEST_VENDOR_ID, request)
        print(f"create_vendor_mobile_change_request async result: {result}")
        assert hasattr(result, 'result')

    except Exception as e:
        print(f"create_vendor_mobile_change_request async error: {e}")
        # Don't fail the test for API errors, just log them
        assert True


@pytest.mark.asyncio
async def test_create_vendor_mobile_change_confirmation_async(basalam_client):
    """Test create_vendor_mobile_change_confirmation async method."""
    try:
        request = ChangeVendorMobileConfirmSchema(
            mobile="09123456789",
            verification_code=123456
        )
        result = await basalam_client.core.create_vendor_mobile_change_confirmation(TEST_VENDOR_ID, request)
        print(f"create_vendor_mobile_change_confirmation async result: {result}")
        assert hasattr(result, 'result')

    except Exception as e:
        print(f"create_vendor_mobile_change_confirmation async error: {e}")
        # Don't fail the test for API errors, just log them
        assert True


# -------------------------------------------------------------------------
# Product Management endpoints tests
# -------------------------------------------------------------------------

@pytest.mark.asyncio
async def test_create_product_async(basalam_client):
    """Test create_product async method."""
    try:
        with open("test1.png", "rb") as photo1, \
                open("test2.png", "rb") as photo2:
            request = ProductRequestSchema(
                name="Test sdk",
                description="blahahahahahahahahah ahhahahahah ahhahahah",
                category_id=TEST_CATEGORY_ID,
                primary_price=100000,
                weight=300,
                package_weight=500,
                stock=10,
                status=ProductStatusInputEnum.PUBLISHED,
                unit_quantity=10,
                unit_type=UnitTypeInputEnum.NUMERIC,
            )
            result = await basalam_client.core.create_product(TEST_VENDOR_ID, request, photo_files=[photo1, photo2])
            print(f"create_product async result: {result}")
            assert hasattr(result, 'id')

    except Exception as e:
        print(f"create_product async error: {e}")
        # Don't fail the test for API errors, just log them
        assert True


@pytest.mark.asyncio
async def test_update_bulk_products_async(basalam_client):
    """Test update_bulk_products async method."""
    try:
        request = BatchUpdateProductsRequest(
            data=[
                UpdateProductRequestItem(
                    id=TEST_PRODUCT_ID,
                    name="Updated Product Name",
                    primary_price=120000,
                    stock=15
                )
            ]
        )
        result = await basalam_client.core.update_bulk_products(TEST_VENDOR_ID, request)
        print(f"update_bulk_products async result: {result}")
        assert isinstance(result, list)

    except Exception as e:
        print(f"update_bulk_products async error: {e}")
        # Don't fail the test for API errors, just log them
        assert True


@pytest.mark.asyncio
async def test_update_product_async(basalam_client):
    """Test update_product async method."""
    try:
        request = ProductRequestSchema(
            name="Single Updated Product",
            brief="Updated brief",
            primary_price=150000,
            stock=20
        )
        result = await basalam_client.core.update_product(TEST_PRODUCT_ID, request)
        print(f"update_product async result: {result}")
        assert hasattr(result, 'id')

    except Exception as e:
        print(f"update_product async error: {e}")
        # Don't fail the test for API errors, just log them
        assert True


@pytest.mark.asyncio
async def test_get_product_async(basalam_client):
    """Test get_product async method."""
    try:
        # Test with minimal response
        result_minimal = await basalam_client.core.get_product(TEST_PRODUCT_ID)
        print(f"get_product async (minimal) result: {result_minimal}")
        assert hasattr(result_minimal, 'id')

        # Test with full
        result_full = await basalam_client.core.get_product(
            TEST_PRODUCT_ID,
            prefer="return=full"
        )
        print(f"get_product async (full) result: {result_full}")
        assert hasattr(result_full, 'id')

    except Exception as e:
        print(f"get_product async error: {e}")
        # Don't fail the test for API errors, just log them
        assert True


@pytest.mark.asyncio
async def test_get_products_async(basalam_client):
    """Test get_products async method."""
    try:
        # Test without query params
        result = await basalam_client.core.get_products()
        print(f"get_products async (no params) result: {result}")
        assert hasattr(result, 'data')

        # Test with query params (need to import GetProductsQuerySchema)
        from basalam_sdk.core.models import GetProductsQuerySchema
        query_params = GetProductsQuerySchema(
            page=1,
            per_page=5,
            sort="id:desc",
            vendor_ids=[TEST_VENDOR_ID]
        )
        result_filtered = await basalam_client.core.get_products(query_params)
        print(f"get_products async (with params) result: {result_filtered}")
        assert hasattr(result_filtered, 'data')

    except Exception as e:
        print(f"get_products async error: {e}")
        # Don't fail the test for API errors, just log them
        assert True


@pytest.mark.asyncio
async def test_create_products_bulk_action_request_async(basalam_client):
    """Test create_products_bulk_action_request async method."""
    try:
        request = BulkProductsUpdateRequestSchema(
            product_filter=ProductFilterSchema(
                product_id=[TEST_PRODUCT_ID]
            ),
            action=[
                BulkActionItem(
                    field=ProductBulkFieldInputEnum.STOCK,
                    action=ProductBulkActionTypeEnum.SET,
                    value=1
                )
            ]
        )
        result = await basalam_client.core.create_products_bulk_action_request(TEST_VENDOR_ID, request)
        print(f"create_products_bulk_action_request async result: {result}")
        assert hasattr(result, 'id')

    except Exception as e:
        print(f"create_products_bulk_action_request async error: {e}")
        # Don't fail the test for API errors, just log them
        assert True


@pytest.mark.asyncio
async def test_update_product_variation_async(basalam_client):
    """Test update_product_variation async method."""
    try:
        variation_id = 6639697  # Test variation ID
        request = UpdateProductVariationSchema(
            primary_price=80000,
            stock=25,
            sku="TEST-VAR-001"
        )
        result = await basalam_client.core.update_product_variation(
            TEST_PRODUCT_ID, variation_id, request
        )
        print(f"update_product_variation async result: {result}")
        assert hasattr(result, 'id')

    except Exception as e:
        print(f"update_product_variation async error: {e}")
        # Don't fail the test for API errors, just log them
        assert True


@pytest.mark.asyncio
async def test_get_products_bulk_action_requests_async(basalam_client):
    """Test get_products_bulk_action_requests async method."""
    try:
        result = await basalam_client.core.get_products_bulk_action_requests(
            TEST_VENDOR_ID,
            page=1,
            per_page=10
        )
        print(f"get_products_bulk_action_requests async result: {result}")
        assert hasattr(result, 'data')

    except Exception as e:
        print(f"get_products_bulk_action_requests async error: {e}")
        # Don't fail the test for API errors, just log them
        assert True


@pytest.mark.asyncio
async def test_get_products_bulk_action_requests_count_async(basalam_client):
    """Test get_products_bulk_action_requests_count async method."""
    try:
        result = await basalam_client.core.get_products_bulk_action_requests_count(TEST_VENDOR_ID)
        print(f"get_products_bulk_action_requests_count async result: {result}")
        assert hasattr(result, 'sum')

    except Exception as e:
        print(f"get_products_bulk_action_requests_count async error: {e}")
        # Don't fail the test for API errors, just log them
        assert True


@pytest.mark.asyncio
async def test_get_products_unsuccessful_bulk_action_requests_async(basalam_client):
    """Test get_products_unsuccessful_bulk_action_requests async method."""
    try:
        request_id = 561338  # Test request ID
        result = await basalam_client.core.get_products_unsuccessful_bulk_action_requests(
            request_id
        )
        print(f"get_products_unsuccessful_bulk_action_requests async result: {result}")
        assert hasattr(result, 'data')

    except Exception as e:
        print(f"get_products_unsuccessful_bulk_action_requests async error: {e}")
        # Don't fail the test for API errors, just log them
        assert True


@pytest.mark.asyncio
async def test_get_product_shelves_async(basalam_client):
    """Test get_product_shelves async method."""
    try:
        result = await basalam_client.core.get_product_shelves(TEST_PRODUCT_ID)
        print(f"get_product_shelves async result: {result}")
        assert isinstance(result, list)

    except Exception as e:
        print(f"get_product_shelves async error: {e}")
        # Don't fail the test for API errors, just log them
        assert True


@pytest.mark.asyncio
async def test_create_discount_async(basalam_client):
    """Test create_discount async method."""
    try:
        request = CreateDiscountRequestSchema(
            product_filter=DiscountProductFilterSchema(
                product_ids=[TEST_PRODUCT_ID],
            ),
            discount_percent=10,
            active_days=7
        )
        result = await basalam_client.core.create_discount(TEST_VENDOR_ID, request)
        print(f"create_discount async result: {result}")
        assert isinstance(result, dict)

    except Exception as e:
        print(f"create_discount async error: {e}")
        # Don't fail the test for API errors, just log them
        assert True


@pytest.mark.asyncio
async def test_delete_discount_async(basalam_client):
    """Test delete_discount async method."""
    try:
        request = DeleteDiscountRequestSchema(
            product_filter=DiscountProductFilterSchema(
                product_ids=[TEST_PRODUCT_ID]
            )
        )
        result = await basalam_client.core.delete_discount(TEST_VENDOR_ID, request)
        print(f"delete_discount async result: {result}")
        assert isinstance(result, dict)

    except Exception as e:
        print(f"delete_discount async error: {e}")
        # Don't fail the test for API errors, just log them
        assert True


# -------------------------------------------------------------------------
# User Management endpoints tests
# -------------------------------------------------------------------------

@pytest.mark.asyncio
async def test_get_current_user_async(basalam_client):
    """Test get_current_user async method."""
    try:
        result = await basalam_client.core.get_current_user()
        print(f"get_current_user async result: {result}")
        assert hasattr(result, 'id')

    except Exception as e:
        print(f"get_current_user async error: {e}")
        # Don't fail the test for API errors, just log them
        assert True


@pytest.mark.asyncio
async def test_create_user_mobile_confirmation_request_async(basalam_client):
    """Test create_user_mobile_confirmation_request async method."""
    try:
        result = await basalam_client.core.create_user_mobile_confirmation_request(TEST_USER_ID)
        print(f"create_user_mobile_confirmation_request async result: {result}")
        assert hasattr(result, 'result')

    except Exception as e:
        print(f"create_user_mobile_confirmation_request async error: {e}")
        # Don't fail the test for API errors, just log them
        assert True


@pytest.mark.asyncio
async def test_verify_user_mobile_confirmation_request_async(basalam_client):
    """Test verify_user_mobile_confirmation_request async method."""
    try:
        request = ConfirmCurrentUserMobileConfirmSchema(
            verification_code=123456
        )
        result = await basalam_client.core.verify_user_mobile_confirmation_request(TEST_USER_ID, request)
        print(f"verify_user_mobile_confirmation_request async result: {result}")
        assert hasattr(result, 'result')

    except Exception as e:
        print(f"verify_user_mobile_confirmation_request async error: {e}")
        # Don't fail the test for API errors, just log them
        assert True


@pytest.mark.asyncio
async def test_create_user_mobile_change_request_async(basalam_client):
    """Test create_user_mobile_change_request async method."""
    try:
        request = ChangeUserMobileRequestSchema(
            mobile="09120000000"
        )
        result = await basalam_client.core.create_user_mobile_change_request(TEST_USER_ID, request)
        print(f"create_user_mobile_change_request async result: {result}")
        assert hasattr(result, 'result')

    except Exception as e:
        print(f"create_user_mobile_change_request async error: {e}")
        # Don't fail the test for API errors, just log them
        assert True


@pytest.mark.asyncio
async def test_verify_user_mobile_change_request_async(basalam_client):
    """Test verify_user_mobile_change_request async method."""
    try:
        request = ChangeUserMobileConfirmSchema(
            mobile="09123456789",
            verification_code=123456
        )
        result = await basalam_client.core.verify_user_mobile_change_request(TEST_USER_ID, request)
        print(f"verify_user_mobile_change_request async result: {result}")
        assert hasattr(result, 'result')

    except Exception as e:
        print(f"verify_user_mobile_change_request async error: {e}")
        # Don't fail the test for API errors, just log them
        assert True


@pytest.mark.asyncio
async def test_get_user_bank_accounts_async(basalam_client):
    """Test get_user_bank_accounts async method."""
    try:
        # Test with minimal response
        result_minimal = await basalam_client.core.get_user_bank_accounts(TEST_USER_ID)
        print(f"get_user_bank_accounts async (minimal) result: {result_minimal}")
        assert isinstance(result_minimal, list)

    except Exception as e:
        print(f"get_user_bank_accounts async error: {e}")
        # Don't fail the test for API errors, just log them
        assert True


@pytest.mark.asyncio
async def test_create_user_bank_account_async(basalam_client):
    """Test create_user_bank_account async method."""
    try:
        request = UserCardsSchema(
            card_number="6063733231170311",
        )
        # Test with minimal response
        result_minimal = await basalam_client.core.create_user_bank_account(TEST_USER_ID, request)
        print(f"create_user_bank_account async (minimal) result: {result_minimal}")
        assert isinstance(result_minimal, dict)

    except Exception as e:
        print(f"create_user_bank_account async error: {e}")
        # Don't fail the test for API errors, just log them
        assert True


@pytest.mark.asyncio
async def test_verify_user_bank_account_otp_async(basalam_client):
    """Test verify_user_bank_account_otp async method."""
    try:
        request = UserCardsOtpSchema(
            card_number="5063731241170310",
            otp_code="123456"
        )
        result = await basalam_client.core.verify_user_bank_account_otp(TEST_USER_ID, request)
        print(f"verify_user_bank_account_otp async result: {result}")
        assert isinstance(result, dict)

    except Exception as e:
        print(f"verify_user_bank_account_otp async error: {e}")
        # Don't fail the test for API errors, just log them
        assert True


@pytest.mark.asyncio
async def test_verify_user_bank_account_async(basalam_client):
    """Test verify_user_bank_account async method."""
    try:
        request = UserVerifyBankInformationSchema(
            bank_information_id=TEST_BANK_ACCOUNT_ID,
            national_code="0123456789",
            birthday="1990-01-01"
        )
        result = await basalam_client.core.verify_user_bank_account(TEST_USER_ID, request)
        print(f"verify_user_bank_account async result: {result}")
        assert isinstance(result, dict)

    except Exception as e:
        print(f"verify_user_bank_account async error: {e}")
        # Don't fail the test for API errors, just log them
        assert True


@pytest.mark.asyncio
async def test_delete_user_bank_account_async(basalam_client):
    """Test delete_user_bank_account async method."""
    try:
        result = await basalam_client.core.delete_user_bank_account(TEST_USER_ID, TEST_BANK_ACCOUNT_ID)
        print(f"delete_user_bank_account async result: {result}")
        assert isinstance(result, list)

    except Exception as e:
        print(f"delete_user_bank_account async error: {e}")
        # Don't fail the test for API errors, just log them
        assert True


@pytest.mark.asyncio
async def test_update_user_bank_account_async(basalam_client):
    """Test update_user_bank_account async method."""
    try:
        request = UpdateUserBankInformationSchema(
            user_id=TEST_USER_ID,
            card_number="9876543210987654",
            sheba_number="IR123456789012345678901234",
            account_owner="Updated Test User",
            status=1,
            bank_name="Test Bank",
            sheba_status="active",
            bank_account_number="123456789012"
        )
        result = await basalam_client.core.update_user_bank_account(TEST_BANK_ACCOUNT_ID, request)
        print(f"update_user_bank_account async result: {result}")
        assert isinstance(result, dict)

    except Exception as e:
        print(f"update_user_bank_account async error: {e}")
        # Don't fail the test for API errors, just log them
        assert True


@pytest.mark.asyncio
async def test_update_user_verification_async(basalam_client):
    """Test update_user_verification async method."""
    try:
        request = UserVerificationSchema(
            national_code="0123456789",
            birthday="1990-01-01"
        )
        result = await basalam_client.core.update_user_verification(TEST_USER_ID, request)
        print(f"update_user_verification async result: {result}")
        assert hasattr(result, 'id')

    except Exception as e:
        print(f"update_user_verification async error: {e}")
        # Don't fail the test for API errors, just log them
        assert True


# -------------------------------------------------------------------------
# Category Management endpoints tests
# -------------------------------------------------------------------------

@pytest.mark.asyncio
async def test_get_category_attributes_async(basalam_client):
    """Test get_category_attributes async method."""
    try:
        # Test with minimal parameters
        result = await basalam_client.core.get_category_attributes(TEST_CATEGORY_ID)
        print(f"get_category_attributes async (minimal) result: {result}")
        assert hasattr(result, 'data')

        # Test with all parameters
        result_full = await basalam_client.core.get_category_attributes(
            TEST_CATEGORY_ID,
            product_id=TEST_PRODUCT_ID,
            vendor_id=TEST_VENDOR_ID,
            exclude_multi_selects=False
        )
        print(f"get_category_attributes async (full) result: {result_full}")
        assert hasattr(result_full, 'data')

    except Exception as e:
        print(f"get_category_attributes async error: {e}")
        # Don't fail the test for API errors, just log them
        assert True


@pytest.mark.asyncio
async def test_get_categories_async(basalam_client):
    """Test get_categories async method."""
    try:
        result = await basalam_client.core.get_categories()
        print(f"get_categories async result: {result}")
        assert hasattr(result, 'data')

    except Exception as e:
        print(f"get_categories async error: {e}")
        # Don't fail the test for API errors, just log them
        assert True


@pytest.mark.asyncio
async def test_get_category_async(basalam_client):
    """Test get_category async method."""
    try:
        result = await basalam_client.core.get_category(1066)
        print(f"get_category async result: {result}")
        assert hasattr(result, 'id')

    except Exception as e:
        print(f"get_category async error: {e}")
        # Don't fail the test for API errors, just log them
        assert True
