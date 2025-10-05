"""
OrderEnum service client for the Basalam SDK.

This module provides a client for interacting with Basalam's order service.
"""

import logging
from typing import Optional, Dict, Any

from .models import (
    CreatePaymentRequestModel,
    PaymentCallbackRequestModel,
    PaymentVerifyRequestModel,
    UnpaidInvoiceStatusEnum,
    OrderEnum,
    BasketResponse,
)
from ..base_client import BaseClient

logger = logging.getLogger(__name__)


class OrderService(BaseClient):
    """
    Client for the Basalam OrderEnum Service API.

    This client provides methods for managing payments and invoices.
    """

    def __init__(self, **kwargs):
        """
        Initialize the order service client.
        """
        super().__init__(service="order", **kwargs)

    async def get_baskets(self, refresh: bool = False) -> BasketResponse:
        """
        Get active baskets.

        Args:
            refresh: Whether to refresh the basket data from the server.

        Returns:
            BasketResponse: The active basket data.
        """
        endpoint = "/v1/baskets"
        params = {"refresh": refresh}
        response = await self._get(endpoint, params=params)
        return BasketResponse(**response)

    def get_baskets_sync(self, refresh: bool = False) -> BasketResponse:
        """
        Get active baskets (synchronous version).

        Args:
            refresh: Whether to refresh the basket data from the server.

        Returns:
            BasketResponse: The active basket data.
        """
        endpoint = "/v1/baskets"
        params = {"refresh": refresh}
        response = self._get_sync(endpoint, params=params)
        return BasketResponse(**response)

    async def get_product_variation_status(self, product_id: int) -> Dict[str, Any]:
        """
        Get product variation status.
        """
        endpoint = f"/v1/baskets/products/{product_id}/status"
        response = await self._get(endpoint)
        return response

    def get_product_variation_status_sync(self, product_id: int) -> Dict[str, Any]:
        """
        Get product variation status (synchronous version).
        """
        endpoint = f"/v1/baskets/products/{product_id}/status"
        response = self._get_sync(endpoint)
        return response

    async def create_invoice_payment(
            self,
            invoice_id: int,
            request: CreatePaymentRequestModel
    ) -> Dict[str, Any]:
        """
        Create payment for an invoice.
        """
        endpoint = f"/v1/invoices/{invoice_id}/payments"
        response = await self._post(endpoint, json_data=request.model_dump(exclude_none=True))
        return response

    def create_invoice_payment_sync(
            self,
            invoice_id: int,
            request: CreatePaymentRequestModel
    ) -> Dict[str, Any]:
        """
        Create payment for an invoice (synchronous version).
        """
        endpoint = f"/v1/invoices/{invoice_id}/payments"
        response = self._post_sync(endpoint, json_data=request.model_dump(exclude_none=True))
        return response

    async def get_payable_invoices(
            self,
            page: int,
            per_page: int
    ) -> Dict[str, Any]:
        """
        Get payable invoices.
        """
        endpoint = "/v1/invoices/payable"
        params = {
            "page": page,
            "per_page": per_page
        }
        response = await self._get(endpoint, params=params)
        return response

    def get_payable_invoices_sync(
            self,
            page: int,
            per_page: int
    ) -> Dict[str, Any]:
        """
        Get payable invoices (synchronous version).
        """
        endpoint = "/v1/invoices/payable"
        params = {
            "page": page,
            "per_page": per_page
        }
        response = self._get_sync(endpoint, params=params)
        return response

    async def get_unpaid_invoices(
            self,
            invoice_id: Optional[int] = None,
            status: Optional[UnpaidInvoiceStatusEnum] = None,
            page: int = 1,
            per_page: int = 20,
            sort: OrderEnum = OrderEnum.DESC
    ) -> Dict[str, Any]:
        """
        Get unpaid invoices.
        """
        endpoint = "/v1/invoices/unpaid"
        params = {
            "page": page,
            "per_page": per_page,
            "sort": sort.value
        }
        if invoice_id:
            params["invoice_id"] = invoice_id
        if status:
            params["status"] = status.value

        response = await self._get(endpoint, params=params)
        return response

    def get_unpaid_invoices_sync(
            self,
            invoice_id: Optional[int] = None,
            status: Optional[UnpaidInvoiceStatusEnum] = None,
            page: int = 1,
            per_page: int = 20,
            sort: OrderEnum = OrderEnum.DESC
    ) -> Dict[str, Any]:
        """
        Get unpaid invoices (synchronous version).
        """
        endpoint = "/v1/invoices/unpaid"
        params = {
            "page": page,
            "per_page": per_page,
            "sort": sort.value
        }
        if invoice_id:
            params["invoice_id"] = invoice_id
        if status:
            params["status"] = status.value

        response = self._get_sync(endpoint, params=params)
        return response

    async def get_payment_callback(
            self,
            payment_id: int,
            request: PaymentCallbackRequestModel
    ) -> Dict[str, Any]:
        """
        Get payment callback.
        """
        endpoint = f"/v1/payments/{payment_id}/callbacks"
        response = await self._get(endpoint, params=request.model_dump(exclude_none=True))
        return response

    def get_payment_callback_sync(
            self,
            payment_id: int,
            request: PaymentCallbackRequestModel
    ) -> Dict[str, Any]:
        """
        Get payment callback (synchronous version).
        """
        endpoint = f"/v1/payments/{payment_id}/callbacks"
        response = self._get_sync(endpoint, params=request.model_dump(exclude_none=True))
        return response

    async def create_payment_callback(
            self,
            payment_id: int,
            request: PaymentVerifyRequestModel
    ) -> Dict[str, Any]:
        """
        Create payment callback.
        """
        endpoint = f"/v1/payments/{payment_id}/callbacks"
        response = await self._post(endpoint, json_data=request.model_dump(exclude_none=True))
        return response

    def create_payment_callback_sync(
            self,
            payment_id: int,
            request: PaymentVerifyRequestModel
    ) -> Dict[str, Any]:
        """
        Create payment callback (synchronous version).
        """
        endpoint = f"/v1/payments/{payment_id}/callbacks"
        response = self._post_sync(endpoint, json_data=request.model_dump(exclude_none=True))
        return response
