"""
Client for the Basalam OrderEnum Processing Service.

This module provides a client for interacting with Basalam's order processing service.
"""

import logging
from typing import Optional

from .models import (
    OrdersResponse,
    CustomerItemResponse,
    CustomerItemsResponse,
    ParcelResponse,
    OrderStatsResponse,
    ResourceStats,
    OrderFilter,
    ItemFilter,
    OrderParcelFilter,
    ParcelsResponse, Order,
    ParcelHintsResponse,
)
from ..base_client import BaseClient

logger = logging.getLogger(__name__)


class OrderProcessingService(BaseClient):
    """
    Client for the Basalam OrderEnum Processing Service API.

    This client provides methods for interacting with customer orders,
    vendor orders, and order statistics.
    """

    def __init__(self, **kwargs):
        """
        Initialize the order processing service client.
        """
        super().__init__(service="order-processing", **kwargs)

    # -------------------------------------------------------------------------
    # Customer OrderEnum endpoints
    # -------------------------------------------------------------------------

    async def get_customer_orders(
            self,
            filters: Optional[OrderFilter] = None
    ) -> OrdersResponse:
        """
        Get a list of customer orders.

        Args:
            filters: Optional filters to apply to the query.

        Returns:
            The response containing the list of orders.
        """
        endpoint = "/v3/customer-orders"
        filters = filters or OrderFilter()
        params = filters.model_dump(exclude_none=True)

        # Handle field mapping for API compatibility
        if "items_title" in params:
            params["items.title"] = params.pop("items_title")
        if "parcel_estimate_send_at" in params:
            params["parcel.estimate_send_at"] = params.pop("parcel_estimate_send_at")
        if "parcel_statuses" in params:
            params["parcel.statuses"] = params.pop("parcel_statuses")

        response = await self._get(endpoint, params=params)
        return OrdersResponse(**response)

    def get_customer_orders_sync(
            self,
            filters: Optional[OrderFilter] = None
    ) -> OrdersResponse:
        """
        Get a list of orders (synchronous version).

        Args:
            filters: Optional filters to apply to the query.

        Returns:
            The response containing the list of orders.
        """
        endpoint = "/v3/customer-orders"
        filters = filters or OrderFilter()
        params = filters.model_dump(exclude_none=True)

        # Handle field mapping for API compatibility
        if "items_title" in params:
            params["items.title"] = params.pop("items_title")
        if "parcel_estimate_send_at" in params:
            params["parcel.estimate_send_at"] = params.pop("parcel_estimate_send_at")
        if "parcel_statuses" in params:
            params["parcel.statuses"] = params.pop("parcel_statuses")

        response = self._get_sync(endpoint, params=params)
        return OrdersResponse(**response)

    async def get_customer_order(self, order_id: int) -> Order:
        """
        Get details of a specific order.

        Args:
            order_id: The ID of the order to retrieve.

        Returns:
            The response containing the order details.
        """
        endpoint = f"/v3/customer-orders/{order_id}"
        response = await self._get(endpoint)
        return Order(**response)

    def get_customer_order_sync(self, order_id: int) -> Order:
        """
        Get details of a specific order (synchronous version).

        Args:
            order_id: The ID of the order to retrieve.

        Returns:
            The response containing the order details.
        """
        endpoint = f"/v3/customer-orders/{order_id}"
        response = self._get_sync(endpoint)
        return Order(**response)

    async def get_customer_order_parcel_hints(self, order_id: int) -> ParcelHintsResponse:
        """
        Get parcel hints for a specific customer order.

        Args:
            order_id: The ID of the order to retrieve parcel hints for.

        Returns:
            The response containing the parcel hints.
        """
        endpoint = f"/v3/customer-orders/{order_id}/parcel-hints"
        response = await self._get(endpoint)
        return ParcelHintsResponse(**response)

    def get_customer_order_parcel_hints_sync(self, order_id: int) -> ParcelHintsResponse:
        """
        Get parcel hints for a specific customer order (synchronous version).

        Args:
            order_id: The ID of the order to retrieve parcel hints for.

        Returns:
            The response containing the parcel hints.
        """
        endpoint = f"/v3/customer-orders/{order_id}/parcel-hints"
        response = self._get_sync(endpoint)
        return ParcelHintsResponse(**response)

    async def get_customer_order_items(
            self,
            filters: Optional[ItemFilter] = None
    ) -> CustomerItemsResponse:
        """
        Get a list of order items.

        Args:
            filters: Optional filters to apply to the query.

        Returns:
            The response containing the list of items.
        """
        endpoint = "/v3/customer-items"
        filters = filters or ItemFilter()
        params = filters.model_dump(exclude_none=True)

        response = await self._get(endpoint, params=params)
        return CustomerItemsResponse(**response)

    def get_customer_order_items_sync(
            self,
            filters: Optional[ItemFilter] = None
    ) -> CustomerItemsResponse:
        """
        Get a list of order items (synchronous version).

        Args:
            filters: Optional filters to apply to the query.

        Returns:
            The response containing the list of items.
        """
        endpoint = "/v3/customer-items"
        filters = filters or ItemFilter()
        params = filters.model_dump(exclude_none=True)

        response = self._get_sync(endpoint, params=params)
        return CustomerItemsResponse(**response)

    async def get_customer_order_item(self, item_id: int) -> CustomerItemResponse:
        """
        Get details of a specific order item.

        Args:
            item_id: The ID of the item to retrieve.

        Returns:
            The response containing the item details.
        """
        endpoint = f"/v3/customer-items/{item_id}"
        response = await self._get(endpoint)
        return CustomerItemResponse(**response)

    def get_customer_order_item_sync(self, item_id: int) -> CustomerItemResponse:
        """
        Get details of a specific order item (synchronous version).

        Args:
            item_id: The ID of the item to retrieve.

        Returns:
            The response containing the item details.
        """
        endpoint = f"/v3/customer-items/{item_id}"
        response = self._get_sync(endpoint)
        return CustomerItemResponse(**response)

    # -------------------------------------------------------------------------
    # Vendor Parcel endpoints
    # -------------------------------------------------------------------------

    async def get_vendor_orders_parcels(
            self,
            filters: Optional[OrderParcelFilter] = None
    ) -> ParcelsResponse:
        """
        Get a list of orders parcels.

        Args:
            filters: Optional filters to apply to the query.

        Returns:
            The response containing the list of parcels.
        """
        endpoint = "/v3/vendor-parcels"
        filters = filters or OrderParcelFilter()

        params = {}
        if filters.created_at:
            params["created_at"] = filters.created_at
        if filters.cursor:
            params["cursor"] = filters.cursor
        if filters.estimate_send_at:
            params["estimate_send_at"] = filters.estimate_send_at
        if filters.ids:
            params["ids"] = filters.ids
        if filters.items_customer_ids:
            params["items.customer_ids"] = filters.items_customer_ids
        if filters.items_order_ids:
            params["items.order_ids"] = filters.items_order_ids
        if filters.items_product_ids:
            params["items.product_ids"] = filters.items_product_ids
        if filters.items_vendor_ids:
            params["items.vendor_ids"] = filters.items_vendor_ids
        if filters.per_page:
            params["per_page"] = filters.per_page
        if filters.sort:
            params["sort"] = filters.sort
        if filters.statuses:
            params["statuses"] = ",".join(str(status.value) for status in filters.statuses)

        response = await self._get(endpoint, params=params)
        return ParcelsResponse(**response)

    def get_vendor_orders_parcels_sync(
            self,
            filters: Optional[OrderParcelFilter] = None
    ) -> ParcelsResponse:
        """
        Get a list of orders parcels (synchronous version).

        Args:
            filters: Optional filters to apply to the query.

        Returns:
            The response containing the list of parcels.
        """
        endpoint = "/v3/vendor-parcels"
        filters = filters or OrderParcelFilter()

        params = {}
        if filters.created_at:
            params["created_at"] = filters.created_at
        if filters.cursor:
            params["cursor"] = filters.cursor
        if filters.estimate_send_at:
            params["estimate_send_at"] = filters.estimate_send_at
        if filters.ids:
            params["ids"] = filters.ids
        if filters.items_customer_ids:
            params["items.customer_ids"] = filters.items_customer_ids
        if filters.items_order_ids:
            params["items.order_ids"] = filters.items_order_ids
        if filters.items_product_ids:
            params["items.product_ids"] = filters.items_product_ids
        if filters.items_vendor_ids:
            params["items.vendor_ids"] = filters.items_vendor_ids
        if filters.per_page:
            params["per_page"] = filters.per_page
        if filters.sort:
            params["sort"] = filters.sort
        if filters.statuses:
            params["statuses"] = ",".join(str(status.value) for status in filters.statuses)

        response = self._get_sync(endpoint, params=params)
        return ParcelsResponse(**response)

    async def get_order_parcel(self, parcel_id: int) -> ParcelResponse:
        """
        Get details of a specific order parcel.

        Args:
            parcel_id: The ID of the parcel to retrieve.

        Returns:
            The response containing the parcel details.
        """
        endpoint = f"/v3/vendor-parcels/{parcel_id}"
        response = await self._get(endpoint)
        return ParcelResponse(**response)

    def get_order_parcel_sync(self, parcel_id: int) -> ParcelResponse:
        """
        Get details of a specific order parcel (synchronous version).

        Args:
            parcel_id: The ID of the parcel to retrieve.

        Returns:
            The response containing the parcel details.
        """
        endpoint = f"/v3/vendor-parcels/{parcel_id}"
        response = self._get_sync(endpoint)
        return ParcelResponse(**response)

    # -------------------------------------------------------------------------
    # OrderEnum Statistics endpoints
    # -------------------------------------------------------------------------

    async def get_orders_stats(
            self,
            resource_count: ResourceStats,
            vendor_id: Optional[int] = None,
            product_id: Optional[int] = None,
            customer_id: Optional[int] = None,
            coupon_code: Optional[str] = None,
            cache_control: Optional[str] = None
    ) -> OrderStatsResponse:
        """
        Get order statistics.

        Args:
            resource_count: The type of statistics to retrieve.
            vendor_id: Optional vendor ID to filter by.
            product_id: Optional product ID to filter by.
            customer_id: Optional customer ID to filter by.
            coupon_code: Optional coupon code to filter by.
            cache_control: Optional cache control header.

        Returns:
            The response containing the order statistics.
        """
        endpoint = "/v3/orders-calculate-stats"

        params = {"resource_count": resource_count.value}
        if vendor_id is not None:
            params["vendor_id"] = vendor_id
        if product_id is not None:
            params["product_id"] = product_id
        if customer_id is not None:
            params["customer_id"] = customer_id
        if coupon_code is not None:
            params["coupon_code"] = coupon_code

        headers = {}
        if cache_control is not None:
            headers["Cache-Control"] = cache_control

        response = await self._get(endpoint, params=params, headers=headers)
        return OrderStatsResponse(**response)

    def get_orders_stats_sync(
            self,
            resource_count: ResourceStats,
            vendor_id: Optional[int] = None,
            product_id: Optional[int] = None,
            customer_id: Optional[int] = None,
            coupon_code: Optional[str] = None,
            cache_control: Optional[str] = None
    ) -> OrderStatsResponse:
        """
        Get order statistics (synchronous version).

        Args:
            resource_count: The type of statistics to retrieve.
            vendor_id: Optional vendor ID to filter by.
            product_id: Optional product ID to filter by.
            customer_id: Optional customer ID to filter by.
            coupon_code: Optional coupon code to filter by.
            cache_control: Optional cache control header.

        Returns:
            The response containing the order statistics.
        """
        endpoint = "/v3/orders-calculate-stats"

        params = {"resource_count": resource_count.value}
        if vendor_id is not None:
            params["vendor_id"] = vendor_id
        if product_id is not None:
            params["product_id"] = product_id
        if customer_id is not None:
            params["customer_id"] = customer_id
        if coupon_code is not None:
            params["coupon_code"] = coupon_code

        headers = {}
        if cache_control is not None:
            headers["Cache-Control"] = cache_control

        response = self._get_sync(endpoint, params=params, headers=headers)
        return OrderStatsResponse(**response)
