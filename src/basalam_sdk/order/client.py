"""
Order service client for the Basalam SDK.

This module provides a client for interacting with Basalam's order service.
"""

import logging
from typing import Optional, Dict, Any

from .models import (
    CreatePaymentRequestModel,
    PaymentCallbackRequestModel,
    PaymentVerifyRequestModel,
    UnpaidInvoiceStatusEnum,
    Order,
)
from ..base_client import BaseClient

logger = logging.getLogger(__name__)


class OrderService(BaseClient):
    """
    Client for the Basalam Order Service API.

    This client provides methods for managing payments and invoices.
    """

    def __init__(self, **kwargs):
        """
        Initialize the order service client.
        """
        super().__init__(service_name="order", **kwargs)

    async def get_product_variation_status(self, product_id: int) -> Dict[str, Any]:
        """
        Get product variation status.
        """
        endpoint = f"/v2/basket/product/{product_id}/status"
        response = await self._get(endpoint)
        return response

    def get_product_variation_status_sync(self, product_id: int) -> Dict[str, Any]:
        """
        Get product variation status (synchronous version).
        """
        endpoint = f"/v2/basket/product/{product_id}/status"
        response = self._get_sync(endpoint)
        return response

    async def create_payment(
            self,
            invoice_id: int,
            request: CreatePaymentRequestModel
    ) -> Dict[str, Any]:
        """
        Create payment for an invoice.
        """
        endpoint = f"/v2/invoice/{invoice_id}/payment"
        response = await self._post(endpoint, json=request.dict())
        return response

    def create_payment_sync(
            self,
            invoice_id: int,
            request: CreatePaymentRequestModel
    ) -> Dict[str, Any]:
        """
        Create payment for an invoice (synchronous version).
        """
        endpoint = f"/v2/invoice/{invoice_id}/payment"
        response = self._post_sync(endpoint, json=request.dict())
        return response

    async def get_payable_invoices(
            self,
            page: int,
            per_page: int
    ) -> Dict[str, Any]:
        """
        Get payable invoices.
        """
        endpoint = "/v2/invoice/payable"
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
        endpoint = "/v2/invoice/payable"
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
            sort: Order = Order.DESC
    ) -> Dict[str, Any]:
        """
        Get unpaid invoices.
        """
        endpoint = "/v2/invoice/unpaid"
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
            sort: Order = Order.DESC
    ) -> Dict[str, Any]:
        """
        Get unpaid invoices (synchronous version).
        """
        endpoint = "/v2/invoice/unpaid"
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

    async def payment_callback(
            self,
            pay_id: int,
            request: PaymentCallbackRequestModel
    ) -> Dict[str, Any]:
        """
        Handle payment callback.
        """
        endpoint = f"/v2/payment/{pay_id}/callback"
        response = await self._get(endpoint, params=request.dict())
        return response

    def payment_callback_sync(
            self,
            pay_id: int,
            request: PaymentCallbackRequestModel
    ) -> Dict[str, Any]:
        """
        Handle payment callback (synchronous version).
        """
        endpoint = f"/v2/payment/{pay_id}/callback"
        response = self._get_sync(endpoint, params=request.dict())
        return response

    async def verify_payment(
            self,
            pay_id: int,
            request: PaymentVerifyRequestModel
    ) -> Dict[str, Any]:
        """
        Verify payment.
        """
        endpoint = f"/v2/payment/{pay_id}/verify"
        response = await self._post(endpoint, json=request.dict())
        return response

    def verify_payment_sync(
            self,
            pay_id: int,
            request: PaymentVerifyRequestModel
    ) -> Dict[str, Any]:
        """
        Verify payment (synchronous version).
        """
        endpoint = f"/v2/payment/{pay_id}/verify"
        response = self._post_sync(endpoint, json=request.dict())
        return response

    async def get_payment_status(self, pay_id: int) -> Dict[str, Any]:
        """
        Get payment status.
        """
        endpoint = f"/v2/payment/{pay_id}/status"
        response = await self._get(endpoint)
        return response

    def get_payment_status_sync(self, pay_id: int) -> Dict[str, Any]:
        """
        Get payment status (synchronous version).
        """
        endpoint = f"/v2/payment/{pay_id}/status"
        response = self._get_sync(endpoint)
        return response
