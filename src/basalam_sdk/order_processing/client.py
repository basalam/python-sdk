"""
Client for the Basalam Order Processing Service.

This module provides a client for interacting with Basalam's order processing service.
"""

import logging
from typing import Dict, Optional, Any

from .models import (
    OrderResponse,
    OrdersResponse,
    ItemResponse,
    ItemsResponse,
    ParcelResponse,
    OrderStatsResponse,
    ResourceStats,
    OrderFilter,
    ItemFilter,
    OrderParcelFilter,
)
from ..base_client import BaseClient

logger = logging.getLogger(__name__)


class OrderProcessingService(BaseClient):
    """
    Client for the Basalam Order Processing Service API.

    This client provides methods for interacting with customer orders,
    vendor orders, and order statistics.
    """

    def __init__(self, **kwargs):
        """
        Initialize the order processing service client.
        """
        super().__init__(service_name="order-processing", **kwargs)

    # -------------------------------------------------------------------------
    # Customer Order endpoints
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
        params = filters.dict(exclude_none=True)
        response = await self._get(endpoint, params=params)
        return OrdersResponse(**response)

    def get_customer_orders_sync(
            self,
            filters: Optional[OrderFilter] = None
    ) -> OrdersResponse:
        """
        Get a list of customer orders (synchronous version).

        Args:
            filters: Optional filters to apply to the query.

        Returns:
            The response containing the list of orders.
        """
        endpoint = "/v3/customer-orders"
        filters = filters or OrderFilter()
        params = filters.dict(exclude_none=True)
        response = self._get_sync(endpoint, params=params)
        return OrdersResponse(**response)

    async def get_customer_order(self, order_id: int) -> OrderResponse:
        """
        Get details of a specific customer order.

        Args:
            order_id: The ID of the order to retrieve.

        Returns:
            The response containing the order details.
        """
        endpoint = f"/v3/customer-orders/{order_id}"
        response = await self._get(endpoint)
        return OrderResponse(**response)

    def get_customer_order_sync(self, order_id: int) -> OrderResponse:
        """
        Get details of a specific customer order (synchronous version).

        Args:
            order_id: The ID of the order to retrieve.

        Returns:
            The response containing the order details.
        """
        endpoint = f"/v3/customer-orders/{order_id}"
        response = self._get_sync(endpoint)
        return OrderResponse(**response)

    async def get_customer_items(
            self,
            filters: Optional[ItemFilter] = None
    ) -> ItemsResponse:
        """
        Get a list of customer order items.
        """
        endpoint = "/customer-items"
        filters = filters or ItemFilter()

        params = {}
        if filters.ids:
            params["ids"] = ",".join(str(id) for id in filters.ids)
        if filters.order_ids:
            params["order_ids"] = ",".join(str(id) for id in filters.order_ids)
        if filters.customer_ids:
            params["customer_ids"] = ",".join(str(id) for id in filters.customer_ids)
        if filters.product_ids:
            params["product_ids"] = ",".join(str(id) for id in filters.product_ids)
        if filters.vendor_ids:
            params["vendor_ids"] = ",".join(str(id) for id in filters.vendor_ids)
        if filters.created_at_gte:
            params["created_at[gte]"] = filters.created_at_gte
        if filters.created_at_lte:
            params["created_at[lte]"] = filters.created_at_lte
        if filters.sort:
            params["sort"] = filters.sort
        if filters.per_page:
            params["per_page"] = filters.per_page
        if filters.cursor:
            params["cursor"] = filters.cursor

        response = await self._get(endpoint, params=params)
        return self._parse_response(response, ItemsResponse)

    def get_customer_items_sync(
            self,
            filters: Optional[ItemFilter] = None
    ) -> ItemsResponse:
        """
        Get a list of customer order items (synchronous version).
        """
        endpoint = "/customer-items"
        filters = filters or ItemFilter()

        params = {}
        if filters.ids:
            params["ids"] = ",".join(str(id) for id in filters.ids)
        if filters.order_ids:
            params["order_ids"] = ",".join(str(id) for id in filters.order_ids)
        if filters.customer_ids:
            params["customer_ids"] = ",".join(str(id) for id in filters.customer_ids)
        if filters.product_ids:
            params["product_ids"] = ",".join(str(id) for id in filters.product_ids)
        if filters.vendor_ids:
            params["vendor_ids"] = ",".join(str(id) for id in filters.vendor_ids)
        if filters.created_at_gte:
            params["created_at[gte]"] = filters.created_at_gte
        if filters.created_at_lte:
            params["created_at[lte]"] = filters.created_at_lte
        if filters.sort:
            params["sort"] = filters.sort
        if filters.per_page:
            params["per_page"] = filters.per_page
        if filters.cursor:
            params["cursor"] = filters.cursor

        response = self._get_sync(endpoint, params=params)
        return self._parse_response(response, ItemsResponse)

    async def get_customer_item(self, item_id: int) -> ItemResponse:
        """
        Get details of a specific customer order item.
        """
        endpoint = f"/customer-items/{item_id}"
        response = await self._get(endpoint)
        return self._parse_response(response, ItemResponse)

    def get_customer_item_sync(self, item_id: int) -> ItemResponse:
        """
        Get details of a specific customer order item (synchronous version).
        """
        endpoint = f"/customer-items/{item_id}"
        response = self._get_sync(endpoint)
        return self._parse_response(response, ItemResponse)

    # -------------------------------------------------------------------------
    # Vendor Parcel endpoints
    # -------------------------------------------------------------------------

    async def get_vendor_parcels(
            self,
            filters: Optional[OrderParcelFilter] = None
    ) -> Dict[str, Any]:  # Return type is complex and varies
        """
        Get a list of vendor parcels/orders.
        """
        endpoint = "/vendor-parcels"
        filters = filters or OrderParcelFilter()

        params = {}
        if filters.ids:
            params["ids"] = ",".join(str(id) for id in filters.ids)
        if filters.customer_ids:
            params["items.customer_ids"] = ",".join(str(id) for id in filters.customer_ids)
        if filters.vendor_ids:
            params["items.vendor_ids"] = ",".join(str(id) for id in filters.vendor_ids)
        if filters.product_ids:
            params["items.product_ids"] = ",".join(str(id) for id in filters.product_ids)
        if filters.order_ids:
            params["items.order_ids"] = ",".join(str(id) for id in filters.order_ids)
        if filters.statuses:
            params["statuses"] = ",".join(str(status.value) for status in filters.statuses)
        if filters.estimate_send_at_gte:
            params["estimate_send_at[gte]"] = filters.estimate_send_at_gte
        if filters.estimate_send_at_lte:
            params["estimate_send_at[lte]"] = filters.estimate_send_at_lte
        if filters.created_at_gte:
            params["created_at[gte]"] = filters.created_at_gte
        if filters.created_at_lte:
            params["created_at[lte]"] = filters.created_at_lte
        if filters.sort:
            params["sort"] = filters.sort
        if filters.per_page:
            params["per_page"] = filters.per_page
        if filters.cursor:
            params["cursor"] = filters.cursor

        response = await self._get(endpoint, params=params)
        return response

    def get_vendor_parcels_sync(
            self,
            filters: Optional[OrderParcelFilter] = None
    ) -> Dict[str, Any]:  # Return type is complex and varies
        """
        Get a list of vendor parcels/orders (synchronous version).
        """
        endpoint = "/vendor-parcels"
        filters = filters or OrderParcelFilter()

        params = {}
        if filters.ids:
            params["ids"] = ",".join(str(id) for id in filters.ids)
        if filters.customer_ids:
            params["items.customer_ids"] = ",".join(str(id) for id in filters.customer_ids)
        if filters.vendor_ids:
            params["items.vendor_ids"] = ",".join(str(id) for id in filters.vendor_ids)
        if filters.product_ids:
            params["items.product_ids"] = ",".join(str(id) for id in filters.product_ids)
        if filters.order_ids:
            params["items.order_ids"] = ",".join(str(id) for id in filters.order_ids)
        if filters.statuses:
            params["statuses"] = ",".join(str(status.value) for status in filters.statuses)
        if filters.estimate_send_at_gte:
            params["estimate_send_at[gte]"] = filters.estimate_send_at_gte
        if filters.estimate_send_at_lte:
            params["estimate_send_at[lte]"] = filters.estimate_send_at_lte
        if filters.created_at_gte:
            params["created_at[gte]"] = filters.created_at_gte
        if filters.created_at_lte:
            params["created_at[lte]"] = filters.created_at_lte
        if filters.sort:
            params["sort"] = filters.sort
        if filters.per_page:
            params["per_page"] = filters.per_page
        if filters.cursor:
            params["cursor"] = filters.cursor

        response = self._get_sync(endpoint, params=params)
        return response

    async def get_vendor_parcel(self, parcel_id: int) -> ParcelResponse:
        """
        Get details of a specific vendor parcel/order.
        """
        endpoint = f"/vendor-parcels/{parcel_id}"
        response = await self._get(endpoint)
        return self._parse_response(response, ParcelResponse)

    def get_vendor_parcel_sync(self, parcel_id: int) -> ParcelResponse:
        """
        Get details of a specific vendor parcel/order (synchronous version).
        """
        endpoint = f"/vendor-parcels/{parcel_id}"
        response = self._get_sync(endpoint)
        return self._parse_response(response, ParcelResponse)

    # -------------------------------------------------------------------------
    # Order Statistics endpoints
    # -------------------------------------------------------------------------

    async def get_order_stats(
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
        """
        endpoint = "/orders-calculate-stats"

        params = {"resource_count": resource_count.value}
        if vendor_id:
            params["vendor_id"] = vendor_id
        if product_id:
            params["product_id"] = product_id
        if customer_id:
            params["customer_id"] = customer_id
        if coupon_code:
            params["coupon_code"] = coupon_code

        headers = {}
        if cache_control:
            headers["Cache-Control"] = cache_control

        response = await self._get(endpoint, params=params, headers=headers)
        return self._parse_response(response, OrderStatsResponse)

    def get_order_stats_sync(
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
        """
        endpoint = "/orders-calculate-stats"

        params = {"resource_count": resource_count.value}
        if vendor_id:
            params["vendor_id"] = vendor_id
        if product_id:
            params["product_id"] = product_id
        if customer_id:
            params["customer_id"] = customer_id
        if coupon_code:
            params["coupon_code"] = coupon_code

        headers = {}
        if cache_control:
            headers["Cache-Control"] = cache_control

        response = self._get_sync(endpoint, params=params, headers=headers)
        return self._parse_response(response, OrderStatsResponse)
