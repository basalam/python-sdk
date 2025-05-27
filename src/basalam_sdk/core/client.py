"""
Core service client for the Basalam API.
"""
from typing import List, Optional, Dict, Any, Union

from .models import Product, Category, User, UserInfo, CreateVendorSchema, UpdateVendorSchema, PublicVendorResponse, \
    PrivateVendorResponse, ShippingMethodResponse, ShippingMethodListResponse, UpdateShippingMethodSchema, \
    ProductResponse, ProductListResponse, ProductStatusInputEnum, \
    UpdateVendorStatusSchema, UpdateVendorStatusResponse, ChangeVendorMobileRequestSchema, \
    ChangeVendorMobileConfirmSchema, OkResponse, VendorBulkActionRequestSchema, CreateBulkUpdateResponse, \
    BulkUpdateListResponse, UnsuccessfulBulkUpdateProducts, PrivateUserResponse, ConfirmCurrentUserMobileConfirmSchema, \
    ChangeUserMobileRequestSchema, ChangeUserMobileConfirmSchema, UserCardsSchema, UserCardsOtpSchema, \
    UserVerifyBankInformationSchema, BankInformationResponse, UpdateUserBankInformationSchema, UserVerificationSchema, \
    BulkUpdateProductSchema, \
    AttributesResponse, CategoryResponse, CategoriesResponse, UpdateProductVariantsSchema, \
    BatchResponse, CategoryLV12Response, CategoryListResponse, \
    CityResponse, NavigationResponse, PrivateProductListResponse
from ..auth import BaseAuth
from ..base_client import BaseClient
from ..config import BasalamConfig


class CoreService(BaseClient):
    """Client for the Core service API."""

    def __init__(
            self,
            auth: BaseAuth,
            config: Optional[BasalamConfig] = None,
    ):
        """
        Initialize the Core service client.
        """
        super().__init__(auth=auth, config=config, service="core")

    async def create_vendor(
            self,
            user_id: int,
            request: CreateVendorSchema
    ) -> PublicVendorResponse:
        """
        Create a new vendor.

        Args:
            user_id: The ID of the user.
            request: The vendor creation request.

        Returns:
            The created vendor resource.
        """
        endpoint = f"/v3/users/{user_id}/vendors"
        response = await self._post(endpoint, json=request.dict())
        return PublicVendorResponse(**response)

    def create_vendor_sync(
            self,
            user_id: int,
            request: CreateVendorSchema
    ) -> PublicVendorResponse:
        """
        Create a new vendor (synchronous version).

        Args:
            user_id: The ID of the user.
            request: The vendor creation request.

        Returns:
            The created vendor resource.
        """
        endpoint = f"/v3/users/{user_id}/vendors"
        response = self._post_sync(endpoint, json=request.dict())
        return PublicVendorResponse(**response)

    async def update_vendor(
            self,
            vendor_id: int,
            request: UpdateVendorSchema
    ) -> PublicVendorResponse:
        """
        Update a vendor.

        Args:
            vendor_id: The ID of the vendor.
            request: The vendor update request.

        Returns:
            The updated vendor resource.
        """
        endpoint = f"/v3/vendors/{vendor_id}"
        response = await self._patch(endpoint, json=request.dict())
        return PublicVendorResponse(**response)

    def update_vendor_sync(
            self,
            vendor_id: int,
            request: UpdateVendorSchema
    ) -> PublicVendorResponse:
        """
        Update a vendor (synchronous version).

        Args:
            vendor_id: The ID of the vendor.
            request: The vendor update request.

        Returns:
            The updated vendor resource.
        """
        endpoint = f"/v3/vendors/{vendor_id}"
        response = self._patch_sync(endpoint, json=request.dict())
        return PublicVendorResponse(**response)

    async def get_vendor(
            self,
            vendor_id: int,
            prefer: Optional[str] = "return=minimal"
    ) -> Union[PublicVendorResponse, PrivateVendorResponse]:
        """
        Get vendor details.

        Args:
            vendor_id: The ID of the vendor.
            prefer: Optional header to control response type.

        Returns:
            The vendor resource.
        """
        endpoint = f"/v3/vendors/{vendor_id}"
        headers = {}
        if prefer is not None:
            headers["Prefer"] = prefer

        response = await self._get(endpoint, headers=headers)
        if prefer == "return=representation":
            return PrivateVendorResponse(**response)
        return PublicVendorResponse(**response)

    def get_vendor_sync(
            self,
            vendor_id: int,
            prefer: Optional[str] = "return=minimal"
    ) -> Union[PublicVendorResponse, PrivateVendorResponse]:
        """
        Get vendor details (synchronous version).

        Args:
            vendor_id: The ID of the vendor.
            prefer: Optional header to control response type.

        Returns:
            The vendor resource.
        """
        endpoint = f"/v3/vendors/{vendor_id}"
        headers = {}
        if prefer is not None:
            headers["Prefer"] = prefer

        response = self._get_sync(endpoint, headers=headers)
        if prefer == "return=representation":
            return PrivateVendorResponse(**response)
        return PublicVendorResponse(**response)

    async def get_default_shipping_methods(self) -> List[ShippingMethodResponse]:
        """
        Get default shipping methods.

        Returns:
            List of default shipping methods.
        """
        endpoint = "/v3/shipping-methods/defaults"
        response = await self._get(endpoint)
        return [ShippingMethodResponse(**item) for item in response]

    def get_default_shipping_methods_sync(self) -> List[ShippingMethodResponse]:
        """
        Get default shipping methods (synchronous version).

        Returns:
            List of default shipping methods.
        """
        endpoint = "/v3/shipping-methods/defaults"
        response = self._get_sync(endpoint)
        return [ShippingMethodResponse(**item) for item in response]

    async def get_shipping_methods(
            self,
            ids: Optional[List[int]] = None,
            vendor_ids: Optional[List[int]] = None,
            include_deleted: Optional[bool] = None,
            page: int = 1,
            per_page: int = 10
    ) -> ShippingMethodListResponse:
        """
        Get shipping methods list.

        Args:
            ids: Optional list of shipping method IDs to filter by.
            vendor_ids: Optional list of vendor IDs to filter by.
            include_deleted: Optional flag to include deleted methods.
            page: Page number for pagination.
            per_page: Number of items per page.

        Returns:
            The response containing the list of shipping methods.
        """
        endpoint = "/v3/shipping-methods"
        params = {
            "page": page,
            "per_page": per_page
        }
        if ids is not None:
            params["ids"] = ids
        if vendor_ids is not None:
            params["vendor_ids"] = vendor_ids
        if include_deleted is not None:
            params["include_deleted"] = include_deleted

        response = await self._get(endpoint, params=params)
        return ShippingMethodListResponse(**response)

    def get_shipping_methods_sync(
            self,
            ids: Optional[List[int]] = None,
            vendor_ids: Optional[List[int]] = None,
            include_deleted: Optional[bool] = None,
            page: int = 1,
            per_page: int = 10
    ) -> ShippingMethodListResponse:
        """
        Get shipping methods list (synchronous version).

        Args:
            ids: Optional list of shipping method IDs to filter by.
            vendor_ids: Optional list of vendor IDs to filter by.
            include_deleted: Optional flag to include deleted methods.
            page: Page number for pagination.
            per_page: Number of items per page.

        Returns:
            The response containing the list of shipping methods.
        """
        endpoint = "/v3/shipping-methods"
        params = {
            "page": page,
            "per_page": per_page
        }
        if ids is not None:
            params["ids"] = ids
        if vendor_ids is not None:
            params["vendor_ids"] = vendor_ids
        if include_deleted is not None:
            params["include_deleted"] = include_deleted

        response = self._get_sync(endpoint, params=params)
        return ShippingMethodListResponse(**response)

    async def get_vendor_shipping_methods(
            self,
            vendor_id: int
    ) -> List[ShippingMethodResponse]:
        """
        Get working shipping methods for a vendor.

        Args:
            vendor_id: The ID of the vendor.

        Returns:
            List of working shipping methods.
        """
        endpoint = f"/v3/vendors/{vendor_id}/shipping-methods"
        response = await self._get(endpoint)
        return [ShippingMethodResponse(**item) for item in response]

    def get_vendor_shipping_methods_sync(
            self,
            vendor_id: int
    ) -> List[ShippingMethodResponse]:
        """
        Get working shipping methods for a vendor (synchronous version).

        Args:
            vendor_id: The ID of the vendor.

        Returns:
            List of working shipping methods.
        """
        endpoint = f"/v3/vendors/{vendor_id}/shipping-methods"
        response = self._get_sync(endpoint)
        return [ShippingMethodResponse(**item) for item in response]

    async def update_vendor_shipping_methods(
            self,
            vendor_id: int,
            request: UpdateShippingMethodSchema
    ) -> List[ShippingMethodResponse]:
        """
        Update shipping methods for a vendor.

        Args:
            vendor_id: The ID of the vendor.
            request: The shipping method update request.

        Returns:
            List of updated shipping methods.
        """
        endpoint = f"/v3/vendors/{vendor_id}/shipping-methods"
        response = await self._put(endpoint, json=request.dict())
        return [ShippingMethodResponse(**item) for item in response]

    def update_vendor_shipping_methods_sync(
            self,
            vendor_id: int,
            request: UpdateShippingMethodSchema
    ) -> List[ShippingMethodResponse]:
        """
        Update shipping methods for a vendor (synchronous version).

        Args:
            vendor_id: The ID of the vendor.
            request: The shipping method update request.

        Returns:
            List of updated shipping methods.
        """
        endpoint = f"/v3/vendors/{vendor_id}/shipping-methods"
        response = self._put_sync(endpoint, json=request.dict())
        return [ShippingMethodResponse(**item) for item in response]

    async def get_vendor_products(
            self,
            vendor_id: int,
            title: Optional[str] = None,
            category: Optional[List[int]] = None,
            statuses: Optional[List[ProductStatusInputEnum]] = None,
            stock_gte: Optional[int] = None,
            stock_lte: Optional[int] = None,
            preparation_day_gte: Optional[int] = None,
            preparation_day_lte: Optional[int] = None,
            price_gte: Optional[int] = None,
            price_lte: Optional[int] = None,
            ids: Optional[List[int]] = None,
            skus: Optional[List[str]] = None,
            illegal_free_shipping_for_iran: Optional[int] = None,
            illegal_free_shipping_for_same_city: Optional[int] = None,
            page: int = 1,
            per_page: int = 10,
            variants_flatting: bool = True,
            is_wholesale: Optional[bool] = None,
            sort: Optional[str] = None
    ) -> ProductListResponse:
        """
        Get vendor products.

        Args:
            vendor_id: The ID of the vendor.
            title: Optional title to filter by.
            category: Optional list of category IDs to filter by.
            statuses: Optional list of statuses to filter by.
            stock_gte: Optional minimum stock to filter by.
            stock_lte: Optional maximum stock to filter by.
            preparation_day_gte: Optional minimum preparation days to filter by.
            preparation_day_lte: Optional maximum preparation days to filter by.
            price_gte: Optional minimum price to filter by.
            price_lte: Optional maximum price to filter by.
            ids: Optional list of product IDs to filter by.
            skus: Optional list of SKUs to filter by.
            illegal_free_shipping_for_iran: Optional flag for Iran shipping.
            illegal_free_shipping_for_same_city: Optional flag for same city shipping.
            page: Page number for pagination.
            per_page: Number of items per page.
            variants_flatting: Whether to flatten variants.
            is_wholesale: Optional flag for wholesale products.
            sort: Optional sort parameter.

        Returns:
            The response containing the list of products.
        """
        endpoint = f"/v3/vendors/{vendor_id}/products"
        params = {
            "page": page,
            "per_page": per_page,
            "variants_flatting": variants_flatting
        }
        if title is not None:
            params["title"] = title
        if category is not None:
            params["category"] = category
        if statuses is not None:
            params["statuses"] = statuses
        if stock_gte is not None:
            params["stock[gte]"] = stock_gte
        if stock_lte is not None:
            params["stock[lte]"] = stock_lte
        if preparation_day_gte is not None:
            params["preparation_day[gte]"] = preparation_day_gte
        if preparation_day_lte is not None:
            params["preparation_day[lte]"] = preparation_day_lte
        if price_gte is not None:
            params["price[gte]"] = price_gte
        if price_lte is not None:
            params["price[lte]"] = price_lte
        if ids is not None:
            params["ids"] = ids
        if skus is not None:
            params["skus"] = skus
        if illegal_free_shipping_for_iran is not None:
            params["illegal_free_shipping_for_iran"] = illegal_free_shipping_for_iran
        if illegal_free_shipping_for_same_city is not None:
            params["illegal_free_shipping_for_same_city"] = illegal_free_shipping_for_same_city
        if is_wholesale is not None:
            params["is_wholesale"] = is_wholesale
        if sort is not None:
            params["sort"] = sort

        response = await self._get(endpoint, params=params)
        return ProductListResponse(**response)

    async def update_vendor_status(
            self,
            vendor_id: int,
            request: UpdateVendorStatusSchema
    ) -> UpdateVendorStatusResponse:
        """
        Update vendor status.

        Args:
            vendor_id: The ID of the vendor.
            request: The vendor status update request.

        Returns:
            The updated vendor status response.
        """
        endpoint = f"/v3/vendors/{vendor_id}/status"
        response = await self._patch(endpoint, json=request.dict())
        return UpdateVendorStatusResponse(**response)

    def update_vendor_status_sync(
            self,
            vendor_id: int,
            request: UpdateVendorStatusSchema
    ) -> UpdateVendorStatusResponse:
        """
        Update vendor status (synchronous version).

        Args:
            vendor_id: The ID of the vendor.
            request: The vendor status update request.

        Returns:
            The updated vendor status response.
        """
        endpoint = f"/v3/vendors/{vendor_id}/status"
        response = self._patch_sync(endpoint, json=request.dict())
        return UpdateVendorStatusResponse(**response)

    async def change_vendor_mobile_request(
            self,
            vendor_id: int,
            request: ChangeVendorMobileRequestSchema
    ) -> OkResponse:
        """
        Request a change of vendor mobile number.

        Args:
            vendor_id: The ID of the vendor.
            request: The mobile change request.

        Returns:
            The success response.
        """
        endpoint = f"/v3/vendors/{vendor_id}/change-mobile-request"
        response = await self._post(endpoint, json=request.dict())
        return OkResponse(**response)

    def change_vendor_mobile_request_sync(
            self,
            vendor_id: int,
            request: ChangeVendorMobileRequestSchema
    ) -> OkResponse:
        """
        Request a change of vendor mobile number (synchronous version).

        Args:
            vendor_id: The ID of the vendor.
            request: The mobile change request.

        Returns:
            The success response.
        """
        endpoint = f"/v3/vendors/{vendor_id}/change-mobile-request"
        response = self._post_sync(endpoint, json=request.dict())
        return OkResponse(**response)

    async def change_vendor_mobile_confirm(
            self,
            vendor_id: int,
            request: ChangeVendorMobileConfirmSchema
    ) -> OkResponse:
        """
        Confirm a change of vendor mobile number.

        Args:
            vendor_id: The ID of the vendor.
            request: The mobile change confirmation request.

        Returns:
            The success response.
        """
        endpoint = f"/v3/vendors/{vendor_id}/change-mobile-confirm"
        response = await self._post(endpoint, json=request.dict())
        return OkResponse(**response)

    def change_vendor_mobile_confirm_sync(
            self,
            vendor_id: int,
            request: ChangeVendorMobileConfirmSchema
    ) -> OkResponse:
        """
        Confirm a change of vendor mobile number (synchronous version).

        Args:
            vendor_id: The ID of the vendor.
            request: The mobile change confirmation request.

        Returns:
            The success response.
        """
        endpoint = f"/v3/vendors/{vendor_id}/change-mobile-confirm"
        response = self._post_sync(endpoint, json=request.dict())
        return OkResponse(**response)

    async def create_bulk_update_product_request(
            self,
            vendor_id: int,
            request: VendorBulkActionRequestSchema
    ) -> CreateBulkUpdateResponse:
        """
        Create a bulk update product request.

        Args:
            vendor_id: The ID of the vendor.
            request: The bulk update request.

        Returns:
            The created bulk update request response.
        """
        endpoint = f"/v3/vendors/{vendor_id}/bulk-update-product-request"
        response = await self._post(endpoint, json=request.dict())
        return CreateBulkUpdateResponse(**response)

    def create_bulk_update_product_request_sync(
            self,
            vendor_id: int,
            request: VendorBulkActionRequestSchema
    ) -> CreateBulkUpdateResponse:
        """
        Create a bulk update product request (synchronous version).

        Args:
            vendor_id: The ID of the vendor.
            request: The bulk update request.

        Returns:
            The created bulk update request response.
        """
        endpoint = f"/v3/vendors/{vendor_id}/bulk-update-product-request"
        response = self._post_sync(endpoint, json=request.dict())
        return CreateBulkUpdateResponse(**response)

    async def get_bulk_update_requests(
            self,
            vendor_id: int,
            page: int = 1,
            per_page: int = 30
    ) -> BulkUpdateListResponse:
        """
        Get list of bulk update requests for a vendor.

        Args:
            vendor_id: The ID of the vendor.
            page: Page number for pagination.
            per_page: Number of items per page.

        Returns:
            The list of bulk update requests.
        """
        endpoint = f"/v3/vendors/{vendor_id}/bulk-update-product-request"
        params = {
            "page": page,
            "per_page": per_page
        }
        response = await self._get(endpoint, params=params)
        return BulkUpdateListResponse(**response)

    def get_bulk_update_requests_sync(
            self,
            vendor_id: int,
            page: int = 1,
            per_page: int = 30
    ) -> BulkUpdateListResponse:
        """
        Get list of bulk update requests for a vendor (synchronous version).

        Args:
            vendor_id: The ID of the vendor.
            page: Page number for pagination.
            per_page: Number of items per page.

        Returns:
            The list of bulk update requests.
        """
        endpoint = f"/v3/vendors/{vendor_id}/bulk-update-product-request"
        params = {
            "page": page,
            "per_page": per_page
        }
        response = self._get_sync(endpoint, params=params)
        return BulkUpdateListResponse(**response)

    async def get_unsuccessful_bulk_update_products(
            self,
            request_id: int,
            page: int = 1,
            per_page: int = 20
    ) -> UnsuccessfulBulkUpdateProducts:
        """
        Get list of unsuccessful products from a bulk update request.

        Args:
            request_id: The ID of the bulk update request.
            page: Page number for pagination.
            per_page: Number of items per page.

        Returns:
            The list of unsuccessful products.
        """
        endpoint = f"/v3/bulk-update-product-request/{request_id}/unsuccessful_products"
        params = {
            "page": page,
            "per_page": per_page
        }
        response = await self._get(endpoint, params=params)
        return UnsuccessfulBulkUpdateProducts(**response)

    def get_unsuccessful_bulk_update_products_sync(
            self,
            request_id: int,
            page: int = 1,
            per_page: int = 20
    ) -> UnsuccessfulBulkUpdateProducts:
        """
        Get list of unsuccessful products from a bulk update request (synchronous version).

        Args:
            request_id: The ID of the bulk update request.
            page: Page number for pagination.
            per_page: Number of items per page.

        Returns:
            The list of unsuccessful products.
        """
        endpoint = f"/v3/bulk-update-product-request/{request_id}/unsuccessful_products"
        params = {
            "page": page,
            "per_page": per_page
        }
        response = self._get_sync(endpoint, params=params)
        return UnsuccessfulBulkUpdateProducts(**response)

    async def get_current_user(self) -> PrivateUserResponse:
        """
        Get current user information.

        Returns:
            The current user information.
        """
        endpoint = "/v3/users/me"
        response = await self._get(endpoint)
        return PrivateUserResponse(**response)

    def get_current_user_sync(self) -> PrivateUserResponse:
        """
        Get current user information (synchronous version).

        Returns:
            The current user information.
        """
        endpoint = "/v3/users/me"
        response = self._get_sync(endpoint)
        return PrivateUserResponse(**response)

    async def confirm_current_user_mobile_request(
            self,
            user_id: int
    ) -> OkResponse:
        """
        Request confirmation of current user mobile number.

        Args:
            user_id: The ID of the user.

        Returns:
            The success response.
        """
        endpoint = f"/v3/users/{user_id}/confirm-mobile-request"
        response = await self._post(endpoint)
        return OkResponse(**response)

    def confirm_current_user_mobile_request_sync(
            self,
            user_id: int
    ) -> OkResponse:
        """
        Request confirmation of current user mobile number (synchronous version).

        Args:
            user_id: The ID of the user.

        Returns:
            The success response.
        """
        endpoint = f"/v3/users/{user_id}/confirm-mobile-request"
        response = self._post_sync(endpoint)
        return OkResponse(**response)

    async def confirm_current_user_mobile(
            self,
            user_id: int,
            request: ConfirmCurrentUserMobileConfirmSchema
    ) -> OkResponse:
        """
        Confirm current user mobile number.

        Args:
            user_id: The ID of the user.
            request: The mobile confirmation request.

        Returns:
            The success response.
        """
        endpoint = f"/v3/users/{user_id}/confirm-mobile"
        response = await self._post(endpoint, json=request.dict())
        return OkResponse(**response)

    def confirm_current_user_mobile_sync(
            self,
            user_id: int,
            request: ConfirmCurrentUserMobileConfirmSchema
    ) -> OkResponse:
        """
        Confirm current user mobile number (synchronous version).

        Args:
            user_id: The ID of the user.
            request: The mobile confirmation request.

        Returns:
            The success response.
        """
        endpoint = f"/v3/users/{user_id}/confirm-mobile"
        response = self._post_sync(endpoint, json=request.dict())
        return OkResponse(**response)

    async def change_user_mobile_request(
            self,
            user_id: int,
            request: ChangeUserMobileRequestSchema
    ) -> OkResponse:
        """
        Request a change of user mobile number.

        Args:
            user_id: The ID of the user.
            request: The mobile change request.

        Returns:
            The success response.
        """
        endpoint = f"/v3/users/{user_id}/change-mobile-request"
        response = await self._post(endpoint, json=request.dict())
        return OkResponse(**response)

    def change_user_mobile_request_sync(
            self,
            user_id: int,
            request: ChangeUserMobileRequestSchema
    ) -> OkResponse:
        """
        Request a change of user mobile number (synchronous version).

        Args:
            user_id: The ID of the user.
            request: The mobile change request.

        Returns:
            The success response.
        """
        endpoint = f"/v3/users/{user_id}/change-mobile-request"
        response = self._post_sync(endpoint, json=request.dict())
        return OkResponse(**response)

    async def change_user_mobile_confirm(
            self,
            user_id: int,
            request: ChangeUserMobileConfirmSchema
    ) -> OkResponse:
        """
        Confirm a change of user mobile number.

        Args:
            user_id: The ID of the user.
            request: The mobile change confirmation request.

        Returns:
            The success response.
        """
        endpoint = f"/v3/users/{user_id}/change-mobile-confirm"
        response = await self._post(endpoint, json=request.dict())
        return OkResponse(**response)

    def change_user_mobile_confirm_sync(
            self,
            user_id: int,
            request: ChangeUserMobileConfirmSchema
    ) -> OkResponse:
        """
        Confirm a change of user mobile number (synchronous version).

        Args:
            user_id: The ID of the user.
            request: The mobile change confirmation request.

        Returns:
            The success response.
        """
        endpoint = f"/v3/users/{user_id}/change-mobile-confirm"
        response = self._post_sync(endpoint, json=request.dict())
        return OkResponse(**response)

    async def get_user_bank_information(
            self,
            user_id: int,
            prefer: Optional[str] = "return=minimal"
    ) -> List[BankInformationResponse]:
        """
        Get user bank information.

        Args:
            user_id: The ID of the user.
            prefer: Optional header to control response format.

        Returns:
            The list of bank information.
        """
        endpoint = f"/v3/users/{user_id}/bank-information"
        headers = {}
        if prefer is not None:
            headers["prefer"] = prefer
        response = await self._get(endpoint, headers=headers)
        return [BankInformationResponse(**item) for item in response]

    def get_user_bank_information_sync(
            self,
            user_id: int,
            prefer: Optional[str] = "return=minimal"
    ) -> List[BankInformationResponse]:
        """
        Get user bank information (synchronous version).

        Args:
            user_id: The ID of the user.
            prefer: Optional header to control response format.

        Returns:
            The list of bank information.
        """
        endpoint = f"/v3/users/{user_id}/bank-information"
        headers = {}
        if prefer is not None:
            headers["prefer"] = prefer
        response = self._get_sync(endpoint, headers=headers)
        return [BankInformationResponse(**item) for item in response]

    async def create_user_bank_information(
            self,
            user_id: int,
            request: UserCardsSchema,
            prefer: Optional[str] = "return=minimal"
    ) -> BankInformationResponse:
        """
        Create user bank information.

        Args:
            user_id: The ID of the user.
            request: The bank information request.
            prefer: Optional header to control response format.

        Returns:
            The created bank information.
        """
        endpoint = f"/v3/users/{user_id}/bank-information"
        headers = {}
        if prefer is not None:
            headers["prefer"] = prefer
        response = await self._post(endpoint, json=request.dict(), headers=headers)
        return BankInformationResponse(**response)

    def create_user_bank_information_sync(
            self,
            user_id: int,
            request: UserCardsSchema,
            prefer: Optional[str] = "return=minimal"
    ) -> BankInformationResponse:
        """
        Create user bank information (synchronous version).

        Args:
            user_id: The ID of the user.
            request: The bank information request.
            prefer: Optional header to control response format.

        Returns:
            The created bank information.
        """
        endpoint = f"/v3/users/{user_id}/bank-information"
        headers = {}
        if prefer is not None:
            headers["prefer"] = prefer
        response = self._post_sync(endpoint, json=request.dict(), headers=headers)
        return BankInformationResponse(**response)

    async def verify_bank_information_otp(
            self,
            user_id: int,
            request: UserCardsOtpSchema
    ) -> OkResponse:
        """
        Verify bank information OTP.

        Args:
            user_id: The ID of the user.
            request: The OTP verification request.

        Returns:
            The success response.
        """
        endpoint = f"/v3/users/{user_id}/bank-information/verify-otp"
        response = await self._post(endpoint, json=request.dict())
        return OkResponse(**response)

    def verify_bank_information_otp_sync(
            self,
            user_id: int,
            request: UserCardsOtpSchema
    ) -> OkResponse:
        """
        Verify bank information OTP (synchronous version).

        Args:
            user_id: The ID of the user.
            request: The OTP verification request.

        Returns:
            The success response.
        """
        endpoint = f"/v3/users/{user_id}/bank-information/verify-otp"
        response = self._post_sync(endpoint, json=request.dict())
        return OkResponse(**response)

    async def verify_bank_information(
            self,
            user_id: int,
            request: UserVerifyBankInformationSchema
    ) -> OkResponse:
        """
        Verify bank information.

        Args:
            user_id: The ID of the user.
            request: The bank information verification request.

        Returns:
            The success response.
        """
        endpoint = f"/v3/users/{user_id}/bank-information/verify"
        response = await self._post(endpoint, json=request.dict())
        return OkResponse(**response)

    def verify_bank_information_sync(
            self,
            user_id: int,
            request: UserVerifyBankInformationSchema
    ) -> OkResponse:
        """
        Verify bank information (synchronous version).

        Args:
            user_id: The ID of the user.
            request: The bank information verification request.

        Returns:
            The success response.
        """
        endpoint = f"/v3/users/{user_id}/bank-information/verify"
        response = self._post_sync(endpoint, json=request.dict())
        return OkResponse(**response)

    async def delete_bank_information(
            self,
            user_id: int,
            bank_account_id: int
    ) -> OkResponse:
        """
        Delete bank information.

        Args:
            user_id: The ID of the user.
            bank_account_id: The ID of the bank account.

        Returns:
            The success response.
        """
        endpoint = f"/v3/users/{user_id}/bank-information/{bank_account_id}"
        response = await self._delete(endpoint)
        return OkResponse(**response)

    def delete_bank_information_sync(
            self,
            user_id: int,
            bank_account_id: int
    ) -> OkResponse:
        """
        Delete bank information (synchronous version).

        Args:
            user_id: The ID of the user.
            bank_account_id: The ID of the bank account.

        Returns:
            The success response.
        """
        endpoint = f"/v3/users/{user_id}/bank-information/{bank_account_id}"
        response = self._delete_sync(endpoint)
        return OkResponse(**response)

    async def update_bank_information(
            self,
            bank_account_id: int,
            request: UpdateUserBankInformationSchema,
    ) -> Dict[str, Any]:
        """
        Update bank information for a specific bank account.

        Args:
            bank_account_id: The ID of the bank account to update
            request: The bank information update request

        Returns:
            Dict[str, Any]: The updated bank information
        """
        response = await self._client.patch(
            f"/v3/bank-information/{bank_account_id}",
            json=request.dict(exclude_none=True),
        )
        return response.json()

    def update_bank_information_sync(
            self,
            bank_account_id: int,
            request: UpdateUserBankInformationSchema,
    ) -> Dict[str, Any]:
        """
        Update bank information for a specific bank account (synchronous).

        Args:
            bank_account_id: The ID of the bank account to update
            request: The bank information update request

        Returns:
            Dict[str, Any]: The updated bank information
        """
        response = self._client_sync.patch(
            f"/v3/bank-information/{bank_account_id}",
            json=request.dict(exclude_none=True),
        )
        return response.json()

    async def user_verification_request(
            self,
            user_id: int,
            request: UserVerificationSchema,
    ) -> PrivateUserResponse:
        """
        Submit a user verification request.

        Args:
            user_id: The ID of the user to verify
            request: The verification request data

        Returns:
            PrivateUserResponse: The updated user information
        """
        response = await self._client.patch(
            f"/v3/users/{user_id}/verification-request",
            json=request.dict(exclude_none=True),
        )
        return PrivateUserResponse(**response.json())

    def user_verification_request_sync(
            self,
            user_id: int,
            request: UserVerificationSchema,
    ) -> PrivateUserResponse:
        """
        Submit a user verification request (synchronous).

        Args:
            user_id: The ID of the user to verify
            request: The verification request data

        Returns:
            PrivateUserResponse: The updated user information
        """
        response = self._client_sync.patch(
            f"/v3/users/{user_id}/verification-request",
            json=request.dict(exclude_none=True),
        )
        return PrivateUserResponse(**response.json())

    async def get_category_attributes(
            self,
            category_id: int,
            product_id: Optional[int] = None,
            vendor_id: Optional[int] = None,
            exclude_multi_selects: bool = True,
    ) -> AttributesResponse:
        """
        Get attributes for a specific category.

        Args:
            category_id: The ID of the category
            product_id: Optional ID of a product to get its attribute values
            vendor_id: Optional ID of a vendor to get its attribute values
            exclude_multi_selects: Whether to exclude multi-select attributes

        Returns:
            AttributesResponse: The list of category attributes
        """
        params = {
            "exclude_multi_selects": exclude_multi_selects,
        }
        if product_id is not None:
            params["product_id"] = product_id
        if vendor_id is not None:
            params["vendor_id"] = vendor_id

        response = await self._client.get(
            f"/v3/categories/{category_id}/attributes",
            params=params,
        )
        return AttributesResponse(**response.json())

    def get_category_attributes_sync(
            self,
            category_id: int,
            product_id: Optional[int] = None,
            vendor_id: Optional[int] = None,
            exclude_multi_selects: bool = True,
    ) -> AttributesResponse:
        """
        Get attributes for a specific category (synchronous).

        Args:
            category_id: The ID of the category
            product_id: Optional ID of a product to get its attribute values
            vendor_id: Optional ID of a vendor to get its attribute values
            exclude_multi_selects: Whether to exclude multi-select attributes

        Returns:
            AttributesResponse: The list of category attributes
        """
        params = {
            "exclude_multi_selects": exclude_multi_selects,
        }
        if product_id is not None:
            params["product_id"] = product_id
        if vendor_id is not None:
            params["vendor_id"] = vendor_id

        response = self._client_sync.get(
            f"/v3/categories/{category_id}/attributes",
            params=params,
        )
        return AttributesResponse(**response.json())

    async def get_categories(self) -> CategoriesResponse:
        """
        Get all categories.

        Returns:
            CategoriesResponse: The list of categories
        """
        response = await self._client.get("/v3/categories")
        return CategoriesResponse(**response.json())

    def get_categories_sync(self) -> CategoriesResponse:
        """
        Get all categories (synchronous).

        Returns:
            CategoriesResponse: The list of categories
        """
        response = self._client_sync.get("/v3/categories")
        return CategoriesResponse(**response.json())

    async def get_category(self, category_id: int) -> CategoryResponse:
        """
        Get a specific category.

        Args:
            category_id: The ID of the category

        Returns:
            CategoryResponse: The category details
        """
        response = await self._client.get(f"/v3/categories/{category_id}")
        return CategoryResponse(**response.json())

    def get_category_sync(self, category_id: int) -> CategoryResponse:
        """
        Get a specific category (synchronous).

        Args:
            category_id: The ID of the category

        Returns:
            CategoryResponse: The category details
        """
        response = self._client_sync.get(f"/v3/categories/{category_id}")
        return CategoryResponse(**response.json())

    async def update_product_variation(
            self,
            product_id: int,
            variation_id: int,
            request: UpdateProductVariantsSchema,
    ) -> ProductResponse:
        """
        Update a product variation.

        Args:
            product_id: The ID of the product
            variation_id: The ID of the variation to update
            request: The variation update request

        Returns:
            ProductResponse: The updated product with the modified variation
        """
        response = await self._client.patch(
            f"/v4/products/{product_id}/variations/{variation_id}",
            json=request.dict(exclude_none=True),
        )
        return ProductResponse(**response.json())

    def update_product_variation_sync(
            self,
            product_id: int,
            variation_id: int,
            request: UpdateProductVariantsSchema,
    ) -> ProductResponse:
        """
        Update a product variation (synchronous).

        Args:
            product_id: The ID of the product
            variation_id: The ID of the variation to update
            request: The variation update request

        Returns:
            ProductResponse: The updated product with the modified variation
        """
        response = self._client_sync.patch(
            f"/v4/products/{product_id}/variations/{variation_id}",
            json=request.dict(exclude_none=True),
        )
        return ProductResponse(**response.json())

    async def create_vendor_bulk_action_request(
            self,
            vendor_id: int,
            request: BulkUpdateProductSchema,
    ) -> List[BatchResponse]:
        """
        Create a bulk action request for a vendor's products.

        Args:
            vendor_id: The ID of the vendor
            request: The bulk update request

        Returns:
            List[BatchResponse]: The list of batch responses
        """
        response = await self._client.post(
            f"/v4/vendors/{vendor_id}/bulk-update-product-request",
            json=request.dict(exclude_none=True),
        )
        return [BatchResponse(**item) for item in response.json()]

    def create_vendor_bulk_action_request_sync(
            self,
            vendor_id: int,
            request: BulkUpdateProductSchema,
    ) -> List[BatchResponse]:
        """
        Create a bulk action request for a vendor's products (synchronous).

        Args:
            vendor_id: The ID of the vendor
            request: The bulk update request

        Returns:
            List[BatchResponse]: The list of batch responses
        """
        response = self._client_sync.post(
            f"/v4/vendors/{vendor_id}/bulk-update-product-request",
            json=request.dict(exclude_none=True),
        )
        return [BatchResponse(**item) for item in response.json()]

    async def get_category_list(self) -> List[CategoryListResponse]:
        """
        Get a list of categories.

        Returns:
            List[CategoryListResponse]: The list of categories
        """
        response = await self._client.get("/v3/categories/list")
        return [CategoryListResponse(**item) for item in response.json()]

    def get_category_list_sync(self) -> List[CategoryListResponse]:
        """
        Get a list of categories (synchronous).

        Returns:
            List[CategoryListResponse]: The list of categories
        """
        response = self._client_sync.get("/v3/categories/list")
        return [CategoryListResponse(**item) for item in response.json()]

    async def get_category_lv12(self) -> List[CategoryLV12Response]:
        """
        Get a list of categories with level 1 and 2.

        Returns:
            List[CategoryLV12Response]: The list of categories with their children
        """
        response = await self._client.get("/v3/categories/lv12")
        return [CategoryLV12Response(**item) for item in response.json()]

    def get_category_lv12_sync(self) -> List[CategoryLV12Response]:
        """
        Get a list of categories with level 1 and 2 (synchronous).

        Returns:
            List[CategoryLV12Response]: The list of categories with their children
        """
        response = self._client_sync.get("/v3/categories/lv12")
        return [CategoryLV12Response(**item) for item in response.json()]

    async def get_cities(self) -> List[CityResponse]:
        """
        Get a list of cities.

        Returns:
            List[CityResponse]: The list of cities
        """
        response = await self._client.get("/v3/cities")
        return [CityResponse(**item) for item in response.json()]

    def get_cities_sync(self) -> List[CityResponse]:
        """
        Get a list of cities (synchronous).

        Returns:
            List[CityResponse]: The list of cities
        """
        response = self._client_sync.get("/v3/cities")
        return [CityResponse(**item) for item in response.json()]

    async def get_navigation(self) -> List[NavigationResponse]:
        """
        Get the navigation structure.

        Returns:
            List[NavigationResponse]: The navigation structure
        """
        response = await self._client.get("/v3/navigation")
        return [NavigationResponse(**item) for item in response.json()]

    def get_navigation_sync(self) -> List[NavigationResponse]:
        """
        Get the navigation structure (synchronous).

        Returns:
            List[NavigationResponse]: The navigation structure
        """
        response = self._client_sync.get("/v3/navigation")
        return [NavigationResponse(**item) for item in response.json()]

    async def get_private_product_list(
            self,
            user_id: int,
            page: Optional[int] = None,
            per_page: Optional[int] = None,
            status: Optional[str] = None,
            category_id: Optional[int] = None,
            search: Optional[str] = None,
            sort: Optional[str] = None,
            order: Optional[str] = None,
    ) -> PrivateProductListResponse:
        """Get private product list.

        Args:
            user_id: The ID of the user
            page: The page number
            per_page: The number of items per page
            status: The status of the products
            category_id: The ID of the category
            search: The search query
            sort: The sort field
            order: The sort order

        Returns:
            PrivateProductListResponse: The private product list
        """
        params = {
            "page": page,
            "per_page": per_page,
            "status": status,
            "category_id": category_id,
            "search": search,
            "sort": sort,
            "order": order,
        }
        return await self._get(f"/v3/users/{user_id}/products", PrivateProductListResponse, params=params)

    def get_private_product_list_sync(
            self,
            user_id: int,
            page: Optional[int] = None,
            per_page: Optional[int] = None,
            status: Optional[str] = None,
            category_id: Optional[int] = None,
            search: Optional[str] = None,
            sort: Optional[str] = None,
            order: Optional[str] = None,
    ) -> PrivateProductListResponse:
        """Get private product list synchronously.

        Args:
            user_id: The ID of the user
            page: The page number
            per_page: The number of items per page
            status: The status of the products
            category_id: The ID of the category
            search: The search query
            sort: The sort field
            order: The sort order

        Returns:
            PrivateProductListResponse: The private product list
        """
        params = {
            "page": page,
            "per_page": per_page,
            "status": status,
            "category_id": category_id,
            "search": search,
            "sort": sort,
            "order": order,
        }
        return self._get_sync(f"/v3/users/{user_id}/products", PrivateProductListResponse, params=params)
