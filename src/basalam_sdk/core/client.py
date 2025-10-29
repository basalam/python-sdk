"""
Core service client for the Basalam API.
"""
import asyncio
import copy
from typing import List, Dict, Optional, Any, Union, BinaryIO

from .models import (
    CreateVendorSchema, UpdateVendorSchema, PublicVendorResponse, PrivateVendorResponse,
    ShippingMethodResponse, ShippingMethodListResponse, UpdateShippingMethodSchema,
    ProductListResponse, GetVendorProductsSchema, GetProductsQuerySchema,
    UpdateVendorStatusSchema, UpdateVendorStatusResponse, ChangeVendorMobileRequestSchema,
    ChangeVendorMobileConfirmSchema, ResultResponse, UnsuccessfulBulkUpdateProducts,
    PrivateUserResponse, ConfirmCurrentUserMobileConfirmSchema,
    ChangeUserMobileRequestSchema, ChangeUserMobileConfirmSchema, UserCardsSchema, UserCardsOtpSchema,
    UserVerifyBankInformationSchema, UpdateUserBankInformationSchema, UserVerificationSchema,
    AttributesResponse, CategoryResponse, CategoriesResponse, UpdateProductVariationSchema, ProductRequestSchema,
    ProductResponseSchema, BatchUpdateProductsRequest, UpdateProductResponseItem,
    BulkProductsUpdateRequestSchema, BulkProductsUpdateResponseSchema, BulkProductsUpdatesListResponse,
    BulkProductsUpdatesCountResponse, ProductShelfResponse, CreateDiscountRequestSchema,
    DeleteDiscountRequestSchema, ShelveSchema, UpdateShelveProductsSchema
)
from ..auth import BaseAuth
from ..base_client import BaseClient
from ..config import BasalamConfig
from ..upload.client import UploadService
from ..upload.models import UserUploadFileTypeEnum


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
        endpoint = f"/v1/users/{user_id}/vendors"
        response = await self._post(endpoint, json_data=request.model_dump(exclude_none=True))
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
        endpoint = f"/v1/users/{user_id}/vendors"
        response = self._post_sync(endpoint, json_data=request.model_dump(exclude_none=True))
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
        endpoint = f"/v1/vendors/{vendor_id}"
        response = await self._patch(endpoint, json_data=request.model_dump(exclude_none=True))
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
        endpoint = f"/v1/vendors/{vendor_id}"
        response = self._patch_sync(endpoint, json_data=request.model_dump(exclude_none=True))
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
        endpoint = f"/v1/vendors/{vendor_id}"
        headers = {}
        if prefer is not None:
            headers["Prefer"] = prefer

        response = await self._get(endpoint, headers=headers)
        if prefer == "return=full":
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
        endpoint = f"/v1/vendors/{vendor_id}"
        headers = {}
        if prefer is not None:
            headers["Prefer"] = prefer

        response = self._get_sync(endpoint, headers=headers)
        if prefer == "return=full":
            return PrivateVendorResponse(**response)
        return PublicVendorResponse(**response)

    async def get_default_shipping_methods(self) -> List[ShippingMethodResponse]:
        """
        Get default shipping methods.

        Returns:
            List of default shipping methods.
        """
        endpoint = "/v1/shipping-methods/defaults"
        response = await self._get(endpoint)
        response = self._unwrap_response(response)
        return [ShippingMethodResponse(**item) for item in response]

    def get_default_shipping_methods_sync(self) -> List[ShippingMethodResponse]:
        """
        Get default shipping methods (synchronous version).

        Returns:
            List of default shipping methods.
        """
        endpoint = "/v1/shipping-methods/defaults"
        response = self._get_sync(endpoint)
        response = self._unwrap_response(response)
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
        endpoint = "/v1/shipping-methods"
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
        endpoint = "/v1/shipping-methods"
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

    async def get_working_shipping_methods(
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
        endpoint = f"/v1/vendors/{vendor_id}/shipping-methods"
        response = await self._get(endpoint)
        response = self._unwrap_response(response)
        return [ShippingMethodResponse(**item) for item in response]

    def get_working_shipping_methods_sync(
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
        endpoint = f"/v1/vendors/{vendor_id}/shipping-methods"
        response = self._get_sync(endpoint)
        response = self._unwrap_response(response)
        return [ShippingMethodResponse(**item) for item in response]

    async def update_shipping_methods(
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
        endpoint = f"/v1/vendors/{vendor_id}/shipping-methods"
        response = await self._put(endpoint, json_data=request.model_dump(exclude_none=True))
        response = self._unwrap_response(response)
        return [ShippingMethodResponse(**item) for item in response]

    def update_shipping_methods_sync(
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
        endpoint = f"/v1/vendors/{vendor_id}/shipping-methods"
        response = self._put_sync(endpoint, json_data=request.model_dump(exclude_none=True))
        response = self._unwrap_response(response)
        return [ShippingMethodResponse(**item) for item in response]

    async def get_vendor_products(
            self,
            vendor_id: int,
            query_params: Optional[GetVendorProductsSchema] = None
    ) -> ProductListResponse:
        """
        Get vendor products.

        Args:
            vendor_id: The ID of the vendor.
            query_params: Optional query parameters for filtering and pagination.

        Returns:
            The response containing the list of products.
        """
        endpoint = f"/v1/vendors/{vendor_id}/products"
        params = {}
        if query_params:
            params = query_params.model_dump(exclude_none=True)
            if "stock_gte" in params:
                params["stock[gte]"] = params.pop("stock_gte")

            if "stock_lte" in params:
                params["stock[lte]"] = params.pop("stock_lte")

            if "preparation_day_gte" in params:
                params["preparation_day[gte]"] = params.pop("preparation_day_gte")

            if "preparation_day_lte" in params:
                params["preparation_day[lte]"] = params.pop("preparation_day_lte")

            if "price_gte" in params:
                params["price[gte]"] = params.pop("price_gte")

            if "price_lte" in params:
                params["price[lte]"] = params.pop("price_lte")

        response = await self._get(endpoint, params=params)
        return ProductListResponse(**response)

    def get_vendor_products_sync(
            self,
            vendor_id: int,
            query_params: Optional[GetVendorProductsSchema] = None
    ) -> ProductListResponse:
        """
        Get vendor products (synchronous version).

        Args:
            vendor_id: The ID of the vendor.
            query_params: Optional query parameters for filtering and pagination.

        Returns:
            The response containing the list of products.
        """
        endpoint = f"/v1/vendors/{vendor_id}/products"
        params = {}
        if query_params:
            params = query_params.model_dump(exclude_none=True)
            if "stock_gte" in params:
                params["stock[gte]"] = params.pop("stock_gte")

            if "stock_lte" in params:
                params["stock[lte]"] = params.pop("stock_lte")

            if "preparation_day_gte" in params:
                params["preparation_day[gte]"] = params.pop("preparation_day_gte")

            if "preparation_day_lte" in params:
                params["preparation_day[lte]"] = params.pop("preparation_day_lte")

            if "price_gte" in params:
                params["price[gte]"] = params.pop("price_gte")

            if "price_lte" in params:
                params["price[lte]"] = params.pop("price_lte")

        response = self._get_sync(endpoint, params=params)
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
        endpoint = f"/v1/vendors/{vendor_id}/status"
        response = await self._patch(endpoint, json_data=request.model_dump(exclude_none=True))
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
        endpoint = f"/v1/vendors/{vendor_id}/status"
        response = self._patch_sync(endpoint, json_data=request.model_dump(exclude_none=True))
        return UpdateVendorStatusResponse(**response)

    async def create_vendor_mobile_change_request(
            self,
            vendor_id: int,
            request: ChangeVendorMobileRequestSchema
    ) -> ResultResponse:
        """
        Create a vendor mobile change request.

        Args:
            vendor_id: The ID of the vendor.
            request: The mobile change request.

        Returns:
            The result response.
        """
        endpoint = f"/v1/vendors/{vendor_id}/mobile-change-requests"
        response = await self._post(endpoint, json_data=request.model_dump(exclude_none=True))
        return ResultResponse(**response)

    def create_vendor_mobile_change_request_sync(
            self,
            vendor_id: int,
            request: ChangeVendorMobileRequestSchema
    ) -> ResultResponse:
        """
        Create a vendor mobile change request (synchronous version).

        Args:
            vendor_id: The ID of the vendor.
            request: The mobile change request.

        Returns:
            The result response.
        """
        endpoint = f"/v1/vendors/{vendor_id}/mobile-change-requests"
        response = self._post_sync(endpoint, json_data=request.model_dump(exclude_none=True))
        return ResultResponse(**response)

    async def create_vendor_mobile_change_confirmation(
            self,
            vendor_id: int,
            request: ChangeVendorMobileConfirmSchema
    ) -> ResultResponse:
        """
        Create a vendor mobile confirmation.

        Args:
            vendor_id: The ID of the vendor.
            request: The mobile change confirmation request.

        Returns:
            The result response.
        """
        endpoint = f"/v1/vendors/{vendor_id}/mobile-change-confirmations"
        response = await self._post(endpoint, json_data=request.model_dump(exclude_none=True))
        return ResultResponse(**response)

    def create_vendor_mobile_change_confirmation_sync(
            self,
            vendor_id: int,
            request: ChangeVendorMobileConfirmSchema
    ) -> ResultResponse:
        """
        Create a vendor mobile confirmation (synchronous version).

        Args:
            vendor_id: The ID of the vendor.
            request: The mobile change confirmation request.

        Returns:
            The result response.
        """
        endpoint = f"/v1/vendors/{vendor_id}/mobile-change-confirmations"
        response = self._post_sync(endpoint, json_data=request.model_dump(exclude_none=True))
        return ResultResponse(**response)

    async def create_product(
            self,
            vendor_id: int,
            request: ProductRequestSchema,
            photo_files: Optional[List[BinaryIO]] = None,
            video_file: Optional[BinaryIO] = None
    ) -> ProductResponseSchema:
        """
        Create a new product for a vendor with optional automatic file upload.

        This method can automatically upload photo and video files, then creates the product
        with the uploaded file IDs merged with any existing IDs in the request.

        Args:
            vendor_id: The ID of the vendor.
            request: The product creation request.
            photo_files: Optional list of photo files to upload.
            video_file: Optional video file to upload.

        Returns:
            The created product resource.
        """
        # Create a copy of the request to avoid modifying the original
        enhanced_request = copy.deepcopy(request)

        # If files are provided, upload them first
        if photo_files or video_file:
            # Create upload service instance
            upload_service = UploadService(auth=self.auth, config=self.config)

            # Initialize existing IDs
            existing_photo_ids = enhanced_request.photos or []
            if enhanced_request.photo is not None:
                existing_photo_ids.append(enhanced_request.photo)

            existing_video_id = enhanced_request.video

            # Upload photo files if provided
            uploaded_photo_ids = []
            if photo_files:
                photo_upload_tasks = []
                for photo_file in photo_files:
                    task = upload_service.upload_file(
                        file=photo_file,
                        file_type=UserUploadFileTypeEnum.PRODUCT_PHOTO,
                        custom_unique_name=None,
                        expire_minutes=None
                    )
                    photo_upload_tasks.append(task)

                # Execute all photo uploads concurrently
                photo_responses = await asyncio.gather(*photo_upload_tasks)
                uploaded_photo_ids = [response.id for response in photo_responses]

            # Upload video file if provided
            uploaded_video_id = None
            if video_file:
                video_response = await upload_service.upload_file(
                    file=video_file,
                    file_type=UserUploadFileTypeEnum.PRODUCT_VIDEO,
                    custom_unique_name=None,
                    expire_minutes=None
                )
                uploaded_video_id = video_response.id

            # Merge photo IDs
            all_photo_ids = existing_photo_ids + uploaded_photo_ids

            # Set photo/photos fields based on total count
            # The photo field is always required when there are photos
            # First photo goes to photo field, remaining photos go to photos field
            if len(all_photo_ids) == 0:
                enhanced_request.photo = None
                enhanced_request.photos = None
            elif len(all_photo_ids) == 1:
                enhanced_request.photo = all_photo_ids[0]
                enhanced_request.photos = None
            else:
                enhanced_request.photo = all_photo_ids[0]  # First photo in photo field
                enhanced_request.photos = all_photo_ids[1:]  # Remaining photos in photos field

            # Set video field
            if uploaded_video_id is not None:
                enhanced_request.video = uploaded_video_id
            elif existing_video_id is not None:
                enhanced_request.video = existing_video_id

        # Create the product with enhanced request
        endpoint = f"/v1/vendors/{vendor_id}/products"
        response = await self._post(endpoint, json_data=enhanced_request.model_dump(exclude_none=True))
        return ProductResponseSchema(**response)

    def create_product_sync(
            self,
            vendor_id: int,
            request: ProductRequestSchema,
            photo_files: Optional[List[BinaryIO]] = None,
            video_file: Optional[BinaryIO] = None
    ) -> ProductResponseSchema:
        """
        Create a new product for a vendor with optional automatic file upload (synchronous version).

        This method can automatically upload photo and video files, then creates the product
        with the uploaded file IDs merged with any existing IDs in the request.

        Args:
            vendor_id: The ID of the vendor.
            request: The product creation request.
            photo_files: Optional list of photo files to upload.
            video_file: Optional video file to upload.

        Returns:
            The created product resource.
        """
        # Create a copy of the request to avoid modifying the original
        enhanced_request = copy.deepcopy(request)

        # If files are provided, upload them first
        if photo_files or video_file:
            # Create upload service instance
            upload_service = UploadService(auth=self.auth, config=self.config)

            # Initialize existing IDs
            existing_photo_ids = enhanced_request.photos or []
            if enhanced_request.photo is not None:
                existing_photo_ids.append(enhanced_request.photo)

            existing_video_id = enhanced_request.video

            # Upload photo files if provided
            uploaded_photo_ids = []
            if photo_files:
                for photo_file in photo_files:
                    photo_response = upload_service.upload_file_sync(
                        file=photo_file,
                        file_type=UserUploadFileTypeEnum.PRODUCT_PHOTO,
                        custom_unique_name=None,
                        expire_minutes=None
                    )
                    uploaded_photo_ids.append(photo_response.id)

            # Upload video file if provided
            uploaded_video_id = None
            if video_file:
                video_response = upload_service.upload_file_sync(
                    file=video_file,
                    file_type=UserUploadFileTypeEnum.PRODUCT_VIDEO,
                    custom_unique_name=None,
                    expire_minutes=None
                )
                uploaded_video_id = video_response.id

            # Merge photo IDs
            all_photo_ids = existing_photo_ids + uploaded_photo_ids

            # Set photo/photos fields based on total count
            # The photo field is always required when there are photos
            # First photo goes to photo field, remaining photos go to photos field
            if len(all_photo_ids) == 0:
                enhanced_request.photo = None
                enhanced_request.photos = None
            elif len(all_photo_ids) == 1:
                enhanced_request.photo = all_photo_ids[0]
                enhanced_request.photos = None
            else:
                enhanced_request.photo = all_photo_ids[0]  # First photo in photo field
                enhanced_request.photos = all_photo_ids[1:]  # Remaining photos in photos field

            # Set video field
            if uploaded_video_id is not None:
                enhanced_request.video = uploaded_video_id
            elif existing_video_id is not None:
                enhanced_request.video = existing_video_id

        # Create the product with enhanced request
        endpoint = f"/v1/vendors/{vendor_id}/products"
        response = self._post_sync(endpoint, json_data=enhanced_request.model_dump(exclude_none=True))
        return ProductResponseSchema(**response)

    async def get_product(
            self,
            product_id: int,
            prefer: Optional[str] = "return=minimal"
    ) -> ProductResponseSchema:
        """
        Get a product (v4).

        Args:
            product_id: The ID of the product.
            prefer: Optional header to control response type.

        Returns:
            The product resource.
        """
        endpoint = f"/v1/products/{product_id}"
        headers = {}
        if prefer is not None:
            headers["Prefer"] = prefer

        response = await self._get(endpoint, headers=headers)
        return ProductResponseSchema(**response)

    def get_product_sync(
            self,
            product_id: int,
            prefer: Optional[str] = "return=minimal"
    ) -> ProductResponseSchema:
        """
        Get a product (v4) (synchronous version).

        Args:
            product_id: The ID of the product.
            prefer: Optional header to control response type.

        Returns:
            The product resource.
        """
        endpoint = f"/v1/products/{product_id}"
        headers = {}
        if prefer is not None:
            headers["Prefer"] = prefer

        response = self._get_sync(endpoint, headers=headers)
        return ProductResponseSchema(**response)

    async def get_products(
            self,
            query_params: Optional[GetProductsQuerySchema] = None,
            prefer: Optional[str] = "return=minimal"
    ) -> ProductListResponse:
        """
        Get products list.

        Args:
            query_params: Query parameters for filtering products.
            prefer: Optional header to control response type.

        Returns:
            The response containing the list of products.
        """
        endpoint = "/v1/products"
        params = {}
        headers = {}

        if query_params is not None:
            # Convert the model to dict and exclude None values
            params = query_params.model_dump(exclude_none=True)

        if prefer is not None:
            headers["Prefer"] = prefer

        response = await self._get(endpoint, params=params, headers=headers)
        return ProductListResponse(**response)

    def get_products_sync(
            self,
            query_params: Optional[GetProductsQuerySchema] = None,
            prefer: Optional[str] = "return=minimal"
    ) -> ProductListResponse:
        """
        Get products list (synchronous version).

        Args:
            query_params: Query parameters for filtering products.
            prefer: Optional header to control response type.

        Returns:
            The response containing the list of products.
        """
        endpoint = "/v1/products"
        params = {}
        headers = {}

        if query_params is not None:
            # Convert the model to dict and exclude None values
            params = query_params.model_dump(exclude_none=True)

        if prefer is not None:
            headers["Prefer"] = prefer

        response = self._get_sync(endpoint, params=params, headers=headers)
        return ProductListResponse(**response)

    async def create_products_bulk_action_request(
            self,
            vendor_id: int,
            request: BulkProductsUpdateRequestSchema,
    ) -> BulkProductsUpdateResponseSchema:
        """
        Create a vendor product update request.

        Args:
            vendor_id: The ID of the vendor
            request: The bulk update request

        Returns:
            BulkProductsUpdateResponseSchema: The bulk update response
        """
        endpoint = f"/v1/vendors/{vendor_id}/batch-jobs"
        response = await self._post(endpoint, json_data=request.model_dump(exclude_none=True))
        return BulkProductsUpdateResponseSchema(**response)

    def create_products_bulk_action_request_sync(
            self,
            vendor_id: int,
            request: BulkProductsUpdateRequestSchema,
    ) -> BulkProductsUpdateResponseSchema:
        """
        Create a vendor product update request (synchronous).

        Args:
            vendor_id: The ID of the vendor
            request: The bulk update request

        Returns:
            BulkProductsUpdateResponseSchema: The bulk update response
        """
        endpoint = f"/v1/vendors/{vendor_id}/batch-jobs"
        response = self._post_sync(endpoint, json_data=request.model_dump(exclude_none=True))
        return BulkProductsUpdateResponseSchema(**response)

    async def update_product_variation(
            self,
            product_id: int,
            variation_id: int,
            request: UpdateProductVariationSchema,
    ) -> ProductResponseSchema:
        """
        Update a product variation.

        Args:
            product_id: The ID of the product
            variation_id: The ID of the variation to update
            request: The variation update request

        Returns:
            ProductResponseSchema: The updated product with the modified variation
        """
        response = await self._patch(
            f"/v1/products/{product_id}/variations/{variation_id}",
            json_data=request.model_dump(exclude_none=True),
        )
        return ProductResponseSchema(**response)

    def update_product_variation_sync(
            self,
            product_id: int,
            variation_id: int,
            request: UpdateProductVariationSchema,
    ) -> ProductResponseSchema:
        """
        Update a product variation (synchronous).

        Args:
            product_id: The ID of the product
            variation_id: The ID of the variation to update
            request: The variation update request

        Returns:
            ProductResponseSchema: The updated product with the modified variation
        """
        response = self._patch_sync(
            f"/v1/products/{product_id}/variations/{variation_id}",
            json_data=request.model_dump(exclude_none=True),
        )
        return ProductResponseSchema(**response)

    async def get_products_bulk_action_requests(
            self,
            vendor_id: int,
            page: int = 1,
            per_page: int = 30
    ) -> BulkProductsUpdatesListResponse:
        """
        Get list of vendor product updates.

        Args:
            vendor_id: The ID of the vendor.
            page: Page number for pagination.
            per_page: Number of items per page.

        Returns:
            The list of bulk update requests.
        """
        endpoint = f"/v1/vendors/{vendor_id}/batch-jobs"
        params = {
            "page": page,
            "per_page": per_page
        }
        response = await self._get(endpoint, params=params)
        return BulkProductsUpdatesListResponse(**response)

    def get_products_bulk_action_requests_sync(
            self,
            vendor_id: int,
            page: int = 1,
            per_page: int = 30
    ) -> BulkProductsUpdatesListResponse:
        """
        Get list of vendor product updates (synchronous version).

        Args:
            vendor_id: The ID of the vendor.
            page: Page number for pagination.
            per_page: Number of items per page.

        Returns:
            The list of bulk update requests.
        """
        endpoint = f"/v1/vendors/{vendor_id}/batch-jobs"
        params = {
            "page": page,
            "per_page": per_page
        }
        response = self._get_sync(endpoint, params=params)
        return BulkProductsUpdatesListResponse(**response)

    async def get_products_bulk_action_requests_count(
            self,
            vendor_id: int
    ) -> BulkProductsUpdatesCountResponse:
        """
        Get count of vendor bulk products updates.

        Args:
            vendor_id: The ID of the vendor.

        Returns:
            The count of bulk update requests by type.
        """
        endpoint = f"/v1/vendors/{vendor_id}/batch-jobs/count"
        response = await self._get(endpoint)
        return BulkProductsUpdatesCountResponse(**response)

    def get_products_bulk_action_requests_count_sync(
            self,
            vendor_id: int
    ) -> BulkProductsUpdatesCountResponse:
        """
        Get count of vendor bulk products updates (synchronous version).

        Args:
            vendor_id: The ID of the vendor.

        Returns:
            The count of bulk update requests by type.
        """
        endpoint = f"/v1/vendors/{vendor_id}/batch-jobs/count"
        response = self._get_sync(endpoint)
        return BulkProductsUpdatesCountResponse(**response)

    async def get_products_unsuccessful_bulk_action_requests(
            self,
            request_id: int,
            page: int = 1,
            per_page: int = 20
    ) -> UnsuccessfulBulkUpdateProducts:
        """
        Get list of unsuccessful products from a product update request.

        Args:
            request_id: The ID of the bulk update request.
            page: Page number for pagination.
            per_page: Number of items per page.

        Returns:
            The list of unsuccessful products.
        """
        endpoint = f"/v1/batch-jobs/{request_id}/failed-items"
        params = {
            "page": page,
            "per_page": per_page
        }
        response = await self._get(endpoint, params=params)
        return UnsuccessfulBulkUpdateProducts(**response)

    def get_products_unsuccessful_bulk_action_requests_sync(
            self,
            request_id: int,
            page: int = 1,
            per_page: int = 20
    ) -> UnsuccessfulBulkUpdateProducts:
        """
        Get list of unsuccessful products from a product update request (synchronous version).

        Args:
            request_id: The ID of the bulk update request.
            page: Page number for pagination.
            per_page: Number of items per page.

        Returns:
            The list of unsuccessful products.
        """
        endpoint = f"/v1/batch-jobs/{request_id}/failed-items"
        params = {
            "page": page,
            "per_page": per_page
        }
        response = self._get_sync(endpoint, params=params)
        return UnsuccessfulBulkUpdateProducts(**response)

    async def get_product_shelves(
            self,
            product_id: int
    ) -> List[ProductShelfResponse]:
        """
        Get product shelves.

        Args:
            product_id: The ID of the product.

        Returns:
            List of product shelves.
        """
        endpoint = f"/v1/products/{product_id}/shelves"
        response = await self._get(endpoint)
        response = self._unwrap_response(response)
        return [ProductShelfResponse(**item) for item in response]

    def get_product_shelves_sync(
            self,
            product_id: int
    ) -> List[ProductShelfResponse]:
        """
        Get product shelves (synchronous version).

        Args:
            product_id: The ID of the product.

        Returns:
            List of product shelves.
        """
        endpoint = f"/v1/products/{product_id}/shelves"
        response = self._get_sync(endpoint)
        response = self._unwrap_response(response)
        return [ProductShelfResponse(**item) for item in response]

    async def create_discount(
            self,
            vendor_id: int,
            request: CreateDiscountRequestSchema
    ) -> Dict[str, Any]:
        """
        Create a discount for vendor products.

        Args:
            vendor_id: The ID of the vendor.
            request: The discount creation request.

        Returns:
            General response data.
        """
        endpoint = f"/v1/vendors/{vendor_id}/discounts"
        response = await self._post(endpoint, json_data=request.model_dump(exclude_none=True))
        return response

    def create_discount_sync(
            self,
            vendor_id: int,
            request: CreateDiscountRequestSchema
    ) -> Dict[str, Any]:
        """
        Create a discount for vendor products (synchronous version).

        Args:
            vendor_id: The ID of the vendor.
            request: The discount creation request.

        Returns:
            General response data.
        """
        endpoint = f"/v1/vendors/{vendor_id}/discounts"
        response = self._post_sync(endpoint, json_data=request.model_dump(exclude_none=True))
        return response

    async def delete_discount(
            self,
            vendor_id: int,
            request: DeleteDiscountRequestSchema
    ) -> Dict[str, Any]:
        """
        Delete a discount for vendor products.

        Args:
            vendor_id: The ID of the vendor.
            request: The discount deletion request.

        Returns:
            General response data.
        """
        endpoint = f"/v1/vendors/{vendor_id}/discounts"
        response = await self._delete(endpoint, json_data=request.model_dump(exclude_none=True))
        return response

    def delete_discount_sync(
            self,
            vendor_id: int,
            request: DeleteDiscountRequestSchema
    ) -> Dict[str, Any]:
        """
        Delete a discount for vendor products (synchronous version).

        Args:
            vendor_id: The ID of the vendor.
            request: The discount deletion request.

        Returns:
            General response data.
        """
        endpoint = f"/v1/vendors/{vendor_id}/discounts"
        response = self._delete_sync(endpoint, json_data=request.model_dump(exclude_none=True))
        return response

    async def get_current_user(self) -> PrivateUserResponse:
        """
        Get current user information.

        Returns:
            The current user information.
        """
        endpoint = "/v1/users/me"
        response = await self._get(endpoint)
        return PrivateUserResponse(**response)

    def get_current_user_sync(self) -> PrivateUserResponse:
        """
        Get current user information (synchronous version).

        Returns:
            The current user information.
        """
        endpoint = "/v1/users/me"
        response = self._get_sync(endpoint)
        return PrivateUserResponse(**response)

    async def create_user_mobile_confirmation_request(
            self,
            user_id: int
    ) -> ResultResponse:
        """
        Create a user mobile confirmation request.

        Args:
            user_id: The ID of the user.

        Returns:
            The result response.
        """
        endpoint = f"/v1/users/{user_id}/mobile-verification-requests"
        response = await self._post(endpoint)
        return ResultResponse(**response)

    def create_user_mobile_confirmation_request_sync(
            self,
            user_id: int
    ) -> ResultResponse:
        """
        Create a user mobile confirmation request (synchronous version).

        Args:
            user_id: The ID of the user.

        Returns:
            The result response.
        """
        endpoint = f"/v1/users/{user_id}/mobile-verification-requests"
        response = self._post_sync(endpoint)
        return ResultResponse(**response)

    async def verify_user_mobile_confirmation_request(
            self,
            user_id: int,
            request: ConfirmCurrentUserMobileConfirmSchema
    ) -> ResultResponse:
        """
        Create a user mobile confirmation.

        Args:
            user_id: The ID of the user.
            request: The mobile confirmation request.

        Returns:
            The result response.
        """
        endpoint = f"/v1/users/{user_id}/mobile-verification-confirmations"
        response = await self._post(endpoint, json_data=request.model_dump(exclude_none=True))
        return ResultResponse(**response)

    def verify_user_mobile_confirmation_request_sync(
            self,
            user_id: int,
            request: ConfirmCurrentUserMobileConfirmSchema
    ) -> ResultResponse:
        """
        Create a user mobile confirmation (synchronous version).

        Args:
            user_id: The ID of the user.
            request: The mobile confirmation request.

        Returns:
            The result response.
        """
        endpoint = f"/v1/users/{user_id}/mobile-verification-confirmations"
        response = self._post_sync(endpoint, json_data=request.model_dump(exclude_none=True))
        return ResultResponse(**response)

    async def create_user_mobile_change_request(
            self,
            user_id: int,
            request: ChangeUserMobileRequestSchema
    ) -> ResultResponse:
        """
        Create a user mobile change request.

        Args:
            user_id: The ID of the user.
            request: The mobile change request.

        Returns:
            The result response.
        """
        endpoint = f"/v1/users/{user_id}/mobile-change-requests"
        response = await self._post(endpoint, json_data=request.model_dump(exclude_none=True))
        return ResultResponse(**response)

    def create_user_mobile_change_request_sync(
            self,
            user_id: int,
            request: ChangeUserMobileRequestSchema
    ) -> ResultResponse:
        """
        Create a user mobile change request (synchronous version).

        Args:
            user_id: The ID of the user.
            request: The mobile change request.

        Returns:
            The result response.
        """
        endpoint = f"/v1/users/{user_id}/mobile-change-requests"
        response = self._post_sync(endpoint, json_data=request.model_dump(exclude_none=True))
        return ResultResponse(**response)

    async def verify_user_mobile_change_request(
            self,
            user_id: int,
            request: ChangeUserMobileConfirmSchema
    ) -> ResultResponse:
        """
        Create a user mobile change confirmation.

        Args:
            user_id: The ID of the user.
            request: The mobile change confirmation request.

        Returns:
            The result response.
        """
        endpoint = f"/v1/users/{user_id}/mobile-change-confirmations"
        response = await self._post(endpoint, json_data=request.model_dump(exclude_none=True))
        return ResultResponse(**response)

    def verify_user_mobile_change_request_sync(
            self,
            user_id: int,
            request: ChangeUserMobileConfirmSchema
    ) -> ResultResponse:
        """
        Create a user mobile change confirmation (synchronous version).

        Args:
            user_id: The ID of the user.
            request: The mobile change confirmation request.

        Returns:
            The result response.
        """
        endpoint = f"/v1/users/{user_id}/mobile-change-confirmations"
        response = self._post_sync(endpoint, json_data=request.model_dump(exclude_none=True))
        return ResultResponse(**response)

    async def get_user_bank_accounts(
            self,
            user_id: int,
            prefer: Optional[str] = "return=minimal"
    ) -> List[Dict[str, Any]]:
        """
        Get user bank accounts.

        Args:
            user_id: The ID of the user.
            prefer: Optional header to control response format.

        Returns:
            List of bank accounts data.
        """
        endpoint = f"/v1/users/{user_id}/bank-accounts"
        headers = {}
        if prefer is not None:
            headers["prefer"] = prefer
        response = await self._get(endpoint, headers=headers)
        response = self._unwrap_response(response)
        return response

    def get_user_bank_accounts_sync(
            self,
            user_id: int,
            prefer: Optional[str] = "return=minimal"
    ) -> List[Dict[str, Any]]:
        """
        Get user bank accounts (synchronous version).

        Args:
            user_id: The ID of the user.
            prefer: Optional header to control response format.

        Returns:
            List of bank accounts data.
        """
        endpoint = f"/v1/users/{user_id}/bank-accounts"
        headers = {}
        if prefer is not None:
            headers["prefer"] = prefer
        response = self._get_sync(endpoint, headers=headers)
        response = self._unwrap_response(response)
        return response

    async def create_user_bank_account(
            self,
            user_id: int,
            request: UserCardsSchema,
            prefer: Optional[str] = "return=minimal"
    ) -> Dict[str, Any]:
        """
        Create user bank accounts.

        Args:
            user_id: The ID of the user.
            request: The bank information request.
            prefer: Optional header to control response format.

        Returns:
            General JSON response containing the created bank information.
        """
        endpoint = f"/v1/users/{user_id}/bank-accounts"
        headers = {}
        if prefer is not None:
            headers["prefer"] = prefer
        response = await self._post(endpoint, json_data=request.model_dump(exclude_none=True), headers=headers)
        return response

    def create_user_bank_account_sync(
            self,
            user_id: int,
            request: UserCardsSchema,
            prefer: Optional[str] = "return=minimal"
    ) -> Dict[str, Any]:
        """
        Create user bank accounts (synchronous version).

        Args:
            user_id: The ID of the user.
            request: The bank information request.
            prefer: Optional header to control response format.

        Returns:
            General JSON response containing the created bank information.
        """
        endpoint = f"/v1/users/{user_id}/bank-accounts"
        headers = {}
        if prefer is not None:
            headers["prefer"] = prefer
        response = self._post_sync(endpoint, json_data=request.model_dump(exclude_none=True), headers=headers)
        return response

    async def verify_user_bank_account_otp(
            self,
            user_id: int,
            request: UserCardsOtpSchema
    ) -> Dict[str, Any]:
        """
        Verify user bank account OTP.

        Args:
            user_id: The ID of the user.
            request: The OTP verification request.

        Returns:
            General JSON response containing the verification result.
        """
        endpoint = f"/v1/users/{user_id}/bank-accounts/verify-otp"
        response = await self._post(endpoint, json_data=request.model_dump(exclude_none=True))
        return response

    def verify_user_bank_account_otp_sync(
            self,
            user_id: int,
            request: UserCardsOtpSchema
    ) -> Dict[str, Any]:
        """
        Verify user bank account OTP (synchronous version).

        Args:
            user_id: The ID of the user.
            request: The OTP verification request.

        Returns:
            General JSON response containing the verification result.
        """
        endpoint = f"/v1/users/{user_id}/bank-accounts/verify-otp"
        response = self._post_sync(endpoint, json_data=request.model_dump(exclude_none=True))
        return response

    async def verify_user_bank_account(
            self,
            user_id: int,
            request: UserVerifyBankInformationSchema
    ) -> Dict[str, Any]:
        """
        Verify user bank accounts.

        Args:
            user_id: The ID of the user.
            request: The bank information verification request.

        Returns:
            General JSON response containing the verification result.
        """
        endpoint = f"/v1/users/{user_id}/bank-accounts/verify"
        response = await self._post(endpoint, json_data=request.model_dump(exclude_none=True))
        return response

    def verify_user_bank_account_sync(
            self,
            user_id: int,
            request: UserVerifyBankInformationSchema
    ) -> Dict[str, Any]:
        """
        Verify user bank accounts (synchronous version).

        Args:
            user_id: The ID of the user.
            request: The bank information verification request.

        Returns:
            General JSON response containing the verification result.
        """
        endpoint = f"/v1/users/{user_id}/bank-accounts/verify"
        response = self._post_sync(endpoint, json_data=request.model_dump(exclude_none=True))
        return response

    async def delete_user_bank_account(
            self,
            user_id: int,
            bank_account_id: int
    ) -> Dict[str, Any]:
        """
        Delete user bank account.

        Args:
            user_id: The ID of the user.
            bank_account_id: The ID of the bank account.

        Returns:
            General JSON response containing the deletion result.
        """
        endpoint = f"/v1/users/{user_id}/bank-accounts/{bank_account_id}"
        response = await self._delete(endpoint)
        return response

    def delete_user_bank_account_sync(
            self,
            user_id: int,
            bank_account_id: int
    ) -> Dict[str, Any]:
        """
        Delete user bank account (synchronous version).

        Args:
            user_id: The ID of the user.
            bank_account_id: The ID of the bank account.

        Returns:
            General JSON response containing the deletion result.
        """
        endpoint = f"/v1/users/{user_id}/bank-accounts/{bank_account_id}"
        response = self._delete_sync(endpoint)
        return response

    async def update_user_bank_account(
            self,
            bank_account_id: int,
            request: UpdateUserBankInformationSchema,
    ) -> Dict[str, Any]:
        """
        Update bank account for a specific bank account.

        Args:
            bank_account_id: The ID of the bank account to update
            request: The bank information update request

        Returns:
            Dict[str, Any]: The updated bank information
        """
        response = await self._patch(
            f"/v1/users/{request.user_id}/bank-accounts/{bank_account_id}",
            json_data=request.model_dump(exclude_none=True),
        )
        return response

    def update_user_bank_account_sync(
            self,
            bank_account_id: int,
            request: UpdateUserBankInformationSchema,
    ) -> Dict[str, Any]:
        """
        Update bank account for a specific bank account (synchronous).

        Args:
            bank_account_id: The ID of the bank account to update
            request: The bank information update request

        Returns:
            Dict[str, Any]: The updated bank information
        """
        response = self._patch_sync(
            f"/v1/users/{request.user_id}/bank-accounts/{bank_account_id}",
            json_data=request.model_dump(exclude_none=True),
        )
        return response

    async def update_user_verification(
            self,
            user_id: int,
            request: UserVerificationSchema,
    ) -> PrivateUserResponse:
        """
        Update user verification.

        Args:
            user_id: The ID of the user to verify
            request: The verification request data

        Returns:
            PrivateUserResponse: The updated user information
        """
        endpoint = f"/v1/users/{user_id}/verification-requests"
        response = await self._patch(endpoint, json_data=request.model_dump(exclude_none=True))
        return PrivateUserResponse(**response)

    def update_user_verification_sync(
            self,
            user_id: int,
            request: UserVerificationSchema,
    ) -> PrivateUserResponse:
        """
        Update user verification (synchronous).

        Args:
            user_id: The ID of the user to verify
            request: The verification request data

        Returns:
            PrivateUserResponse: The updated user information
        """
        endpoint = f"/v1/users/{user_id}/verification-requests"
        response = self._patch_sync(endpoint, json_data=request.model_dump(exclude_none=True))
        return PrivateUserResponse(**response)

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

        endpoint = f"/v1/categories/{category_id}/attributes"
        response = self._get(endpoint, params=params)
        return AttributesResponse(**response)

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

        endpoint = f"/v1/categories/{category_id}/attributes"
        response = self._get_sync(endpoint, params=params)
        return AttributesResponse(**response)

    async def get_categories(self) -> CategoriesResponse:
        """
        Get all categories.

        Returns:
            CategoriesResponse: The list of categories
        """
        endpoint = "/v1/categories"
        response = await self._get(endpoint)
        return CategoriesResponse(**response)

    def get_categories_sync(self) -> CategoriesResponse:
        """
        Get all categories (synchronous).

        Returns:
            CategoriesResponse: The list of categories
        """
        endpoint ="/v1/categories"
        response = self._get_sync(endpoint)
        return CategoriesResponse(**response)

    async def get_category(self, category_id: int) -> CategoryResponse:
        """
        Get a specific category.

        Args:
            category_id: The ID of the category

        Returns:
            CategoryResponse: The category details with hierarchical structure
        """
        endpoint = f"/v1/categories/{category_id}"
        response = await self._get(endpoint)
        return CategoryResponse(**response)

    def get_category_sync(self, category_id: int) -> CategoryResponse:
        """
        Get a specific category (synchronous).

        Args:
            category_id: The ID of the category

        Returns:
            CategoryResponse: The category details with hierarchical structure
        """
        endpoint = f"/v1/categories/{category_id}"
        response = self._get_sync(endpoint)
        return CategoryResponse(**response)

    async def update_bulk_products(
            self,
            vendor_id: int,
            request: BatchUpdateProductsRequest
    ) -> List[UpdateProductResponseItem]:
        """
        Update products for a vendor (v4).

        Args:
            vendor_id: The ID of the vendor.
            request: The product update request.

        Returns:
            List of update results for each product.
        """
        endpoint = f"/v1/vendors/{vendor_id}/products/batch-updates"
        response = await self._patch(endpoint, json_data=request.model_dump(exclude_none=True))
        response = self._unwrap_response(response)
        return [UpdateProductResponseItem(**item) for item in response]

    def update_bulk_products_sync(
            self,
            vendor_id: int,
            request: BatchUpdateProductsRequest
    ) -> List[UpdateProductResponseItem]:
        """
        Update products for a vendor (v4) (synchronous version).

        Args:
            vendor_id: The ID of the vendor.
            request: The product update request.

        Returns:
            List of update results for each product.
        """
        endpoint = f"/v1/vendors/{vendor_id}/products/batch-updates"
        response = self._patch_sync(endpoint, json_data=request.model_dump(exclude_none=True))
        response = self._unwrap_response(response)
        return [UpdateProductResponseItem(**item) for item in response]

    async def update_product(
            self,
            product_id: int,
            request: ProductRequestSchema,
            photo_files: Optional[List[BinaryIO]] = None,
            video_file: Optional[BinaryIO] = None
    ) -> ProductResponseSchema:
        """
        Update a product with optional automatic file upload.

        This method can automatically upload photo and video files, then updates the product
        with the uploaded file IDs merged with any existing IDs in the request.

        Args:
            product_id: The ID of the product.
            request: The product update request.
            photo_files: Optional list of photo files to upload.
            video_file: Optional video file to upload.

        Returns:
            The updated product resource.
        """
        # Create a copy of the request to avoid modifying the original
        enhanced_request = copy.deepcopy(request)

        # If files are provided, upload them first
        if photo_files or video_file:
            # Create upload service instance
            upload_service = UploadService(auth=self.auth, config=self.config)

            # Initialize existing IDs
            existing_photo_ids = enhanced_request.photos or []
            if enhanced_request.photo is not None:
                existing_photo_ids.append(enhanced_request.photo)

            existing_video_id = enhanced_request.video

            # Upload photo files if provided
            uploaded_photo_ids = []
            if photo_files:
                photo_upload_tasks = []
                for photo_file in photo_files:
                    task = upload_service.upload_file(
                        file=photo_file,
                        file_type=UserUploadFileTypeEnum.PRODUCT_PHOTO,
                        custom_unique_name=None,
                        expire_minutes=None
                    )
                    photo_upload_tasks.append(task)

                # Execute all photo uploads concurrently
                photo_responses = await asyncio.gather(*photo_upload_tasks)
                uploaded_photo_ids = [response.id for response in photo_responses]

            # Upload video file if provided
            uploaded_video_id = None
            if video_file:
                video_response = await upload_service.upload_file(
                    file=video_file,
                    file_type=UserUploadFileTypeEnum.PRODUCT_VIDEO,
                    custom_unique_name=None,
                    expire_minutes=None
                )
                uploaded_video_id = video_response.id

            # Merge photo IDs
            all_photo_ids = existing_photo_ids + uploaded_photo_ids

            # Set photo/photos fields based on total count
            # The photo field is always required when there are photos
            # First photo goes to photo field, remaining photos go to photos field
            if len(all_photo_ids) == 0:
                enhanced_request.photo = None
                enhanced_request.photos = None
            elif len(all_photo_ids) == 1:
                enhanced_request.photo = all_photo_ids[0]
                enhanced_request.photos = None
            else:
                enhanced_request.photo = all_photo_ids[0]  # First photo in photo field
                enhanced_request.photos = all_photo_ids[1:]  # Remaining photos in photos field

            # Set video field
            if uploaded_video_id is not None:
                enhanced_request.video = uploaded_video_id
            elif existing_video_id is not None:
                enhanced_request.video = existing_video_id

        # Update the product with enhanced request
        endpoint = f"/v1/products/{product_id}"
        response = await self._patch(endpoint, json_data=enhanced_request.model_dump(exclude_none=True))
        return ProductResponseSchema(**response)

    def update_product_sync(
            self,
            product_id: int,
            request: ProductRequestSchema,
            photo_files: Optional[List[BinaryIO]] = None,
            video_file: Optional[BinaryIO] = None
    ) -> ProductResponseSchema:
        """
        Update a product with optional automatic file upload (synchronous version).

        This method can automatically upload photo and video files, then updates the product
        with the uploaded file IDs merged with any existing IDs in the request.

        Args:
            product_id: The ID of the product.
            request: The product update request.
            photo_files: Optional list of photo files to upload.
            video_file: Optional video file to upload.

        Returns:
            The updated product resource.
        """
        # Create a copy of the request to avoid modifying the original
        enhanced_request = copy.deepcopy(request)

        # If files are provided, upload them first
        if photo_files or video_file:
            # Create upload service instance
            upload_service = UploadService(auth=self.auth, config=self.config)

            # Initialize existing IDs
            existing_photo_ids = enhanced_request.photos or []
            if enhanced_request.photo is not None:
                existing_photo_ids.append(enhanced_request.photo)

            existing_video_id = enhanced_request.video

            # Upload photo files if provided
            uploaded_photo_ids = []
            if photo_files:
                for photo_file in photo_files:
                    photo_response = upload_service.upload_file_sync(
                        file=photo_file,
                        file_type=UserUploadFileTypeEnum.PRODUCT_PHOTO,
                        custom_unique_name=None,
                        expire_minutes=None
                    )
                    uploaded_photo_ids.append(photo_response.id)

            # Upload video file if provided
            uploaded_video_id = None
            if video_file:
                video_response = upload_service.upload_file_sync(
                    file=video_file,
                    file_type=UserUploadFileTypeEnum.PRODUCT_VIDEO,
                    custom_unique_name=None,
                    expire_minutes=None
                )
                uploaded_video_id = video_response.id

            # Merge photo IDs
            all_photo_ids = existing_photo_ids + uploaded_photo_ids

            # Set photo/photos fields based on total count
            # The photo field is always required when there are photos
            # First photo goes to photo field, remaining photos go to photos field
            if len(all_photo_ids) == 0:
                enhanced_request.photo = None
                enhanced_request.photos = None
            elif len(all_photo_ids) == 1:
                enhanced_request.photo = all_photo_ids[0]
                enhanced_request.photos = None
            else:
                enhanced_request.photo = all_photo_ids[0]  # First photo in photo field
                enhanced_request.photos = all_photo_ids[1:]  # Remaining photos in photos field

            # Set video field
            if uploaded_video_id is not None:
                enhanced_request.video = uploaded_video_id
            elif existing_video_id is not None:
                enhanced_request.video = existing_video_id

        # Update the product with enhanced request
        endpoint = f"/v1/products/{product_id}"
        response = self._patch_sync(endpoint, json_data=enhanced_request.model_dump(exclude_none=True))
        return ProductResponseSchema(**response)

    async def create_shelve(
            self,
            request: ShelveSchema
    ) -> Dict[str, Any]:
        """
        Create a new shelve.

        Args:
            request: The shelve creation request.

        Returns:
            General response data.
        """
        endpoint = "/v1/shelves"
        response = await self._post(endpoint, json_data=request.model_dump(exclude_none=True))
        return response

    def create_shelve_sync(
            self,
            request: ShelveSchema
    ) -> Dict[str, Any]:
        """
        Create a new shelve (synchronous version).

        Args:
            request: The shelve creation request.

        Returns:
            General response data.
        """
        endpoint = "/v1/shelves"
        response = self._post_sync(endpoint, json_data=request.model_dump(exclude_none=True))
        return response

    async def update_shelve(
            self,
            shelve_id: int,
            request: ShelveSchema
    ) -> Dict[str, Any]:
        """
        Update a shelve.

        Args:
            shelve_id: The ID of the shelve.
            request: The shelve update request.

        Returns:
            General response data.
        """
        endpoint = f"/v1/shelves/{shelve_id}"
        response = await self._put(endpoint, json_data=request.model_dump(exclude_none=True))
        return response

    def update_shelve_sync(
            self,
            shelve_id: int,
            request: ShelveSchema
    ) -> Dict[str, Any]:
        """
        Update a shelve (synchronous version).

        Args:
            shelve_id: The ID of the shelve.
            request: The shelve update request.

        Returns:
            General response data.
        """
        endpoint = f"/v1/shelves/{shelve_id}"
        response = self._put_sync(endpoint, json_data=request.model_dump(exclude_none=True))
        return response

    async def delete_shelve(
            self,
            shelve_id: int
    ) -> Dict[str, Any]:
        """
        Delete a shelve.

        Args:
            shelve_id: The ID of the shelve to delete.

        Returns:
            General response data.
        """
        endpoint = f"/v1/shelves/{shelve_id}"
        response = await self._delete(endpoint)
        return response

    def delete_shelve_sync(
            self,
            shelve_id: int
    ) -> Dict[str, Any]:
        """
        Delete a shelve (synchronous version).

        Args:
            shelve_id: The ID of the shelve to delete.

        Returns:
            General response data.
        """
        endpoint = f"/v1/shelves/{shelve_id}"
        response = self._delete_sync(endpoint)
        return response

    async def get_shelve_products(
            self,
            shelve_id: int,
            title: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Get products list for a shelve.

        Args:
            shelve_id: The ID of the shelve.
            title: Optional filter by product title.

        Returns:
            General response data containing the list of products.
        """
        endpoint = f"/v1/shelves/{shelve_id}/products"
        params = {}
        if title is not None:
            params["title"] = title

        response = await self._get(endpoint, params=params)
        return response

    def get_shelve_products_sync(
            self,
            shelve_id: int,
            title: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Get products list for a shelve (synchronous version).

        Args:
            shelve_id: The ID of the shelve.
            title: Optional filter by product title.

        Returns:
            General response data containing the list of products.
        """
        endpoint = f"/v1/shelves/{shelve_id}/products"
        params = {}
        if title is not None:
            params["title"] = title

        response = self._get_sync(endpoint, params=params)
        return response

    async def update_shelve_products(
            self,
            shelve_id: int,
            request: UpdateShelveProductsSchema
    ) -> Dict[str, Any]:
        """
        Update products in a shelve.

        Args:
            shelve_id: The ID of the shelve.
            request: The shelve products update request.

        Returns:
            General response data.
        """
        endpoint = f"/v1/shelves/{shelve_id}/products"
        response = await self._put(endpoint, json_data=request.model_dump(exclude_none=True))
        return response

    def update_shelve_products_sync(
            self,
            shelve_id: int,
            request: UpdateShelveProductsSchema
    ) -> Dict[str, Any]:
        """
        Update products in a shelve (synchronous version).

        Args:
            shelve_id: The ID of the shelve.
            request: The shelve products update request.

        Returns:
            General response data.
        """
        endpoint = f"/v1/shelves/{shelve_id}/products"
        response = self._put_sync(endpoint, json_data=request.model_dump(exclude_none=True))
        return response

    async def delete_shelve_product(
            self,
            shelve_id: int,
            product_id: int
    ) -> Dict[str, Any]:
        """
        Delete a product from a shelve.

        Args:
            shelve_id: The ID of the shelve.
            product_id: The ID of the product to delete.

        Returns:
            General response data.
        """
        endpoint = f"/v1/shelves/{shelve_id}/products/{product_id}"
        response = await self._delete(endpoint)
        return response

    def delete_shelve_product_sync(
            self,
            shelve_id: int,
            product_id: int
    ) -> Dict[str, Any]:
        """
        Delete a product from a shelve (synchronous version).

        Args:
            shelve_id: The ID of the shelve.
            product_id: The ID of the product to delete.

        Returns:
            General response data.
        """
        endpoint = f"/v1/shelves/{shelve_id}/products/{product_id}"
        response = self._delete_sync(endpoint)
        return response
