"""
Models for the Webhook service API.
"""
from datetime import datetime
from enum import Enum
from typing import List, Optional, Dict, Any

from pydantic import BaseModel


class RequestMethodType(str, Enum):
    POST = "POST"
    PUT = "PUT"
    PATCH = "PATCH"


class ServiceResource(BaseModel):
    """Service resource model."""
    id: Optional[int] = None
    title: Optional[str] = None
    description: Optional[str] = None
    is_verified: Optional[bool] = None
    is_active: Optional[bool] = None
    created_at: Optional[str] = None


class ServiceListResource(BaseModel):
    """Service list resource model."""
    data: Optional[List[ServiceResource]] = None
    result_count: Optional[int] = None
    total_count: Optional[int] = None
    total_page: Optional[int] = None
    page: Optional[int] = None
    per_page: Optional[int] = None


class CreateServiceRequest(BaseModel):
    """Create service request model."""
    title: str
    description: str


class WebhookResource(BaseModel):
    """Webhook resource model."""
    id: int
    service_id: int
    events: Optional[List[Dict[str, Any]]] = None
    request_headers: Optional[Dict[str, Any]] = None
    request_method: Optional[RequestMethodType] = None
    url: Optional[str] = None
    is_active: Optional[bool] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


class WebhookListResource(BaseModel):
    """Webhook list resource model."""
    data: Optional[List[WebhookResource]] = None
    result_count: Optional[int] = None
    total_count: Optional[int] = None
    total_page: Optional[int] = None
    page: Optional[int] = None
    per_page: Optional[int] = None


class CreateWebhookRequest(BaseModel):
    """Create webhook request model."""
    service_id: Optional[int] = None
    event_ids: List[int]
    request_headers: Optional[str] = None
    request_method: RequestMethodType
    url: str
    is_active: Optional[bool] = None
    register_me: Optional[bool] = None


class EventResource(BaseModel):
    """Event resource model."""
    id: int
    name: str
    description: Optional[str] = None
    sample_data: Optional[Dict[str, Any]] = None
    scopes: Optional[str] = None


class EventListResource(BaseModel):
    """Event list resource model."""
    data: Optional[List[EventResource]] = None
    result_count: Optional[int] = None
    total_count: Optional[int] = None
    total_page: Optional[int] = None
    page: Optional[int] = None
    per_page: Optional[int] = None


class UpdateWebhookRequest(BaseModel):
    """Request model for updating a webhook."""
    event_ids: Optional[List[int]] = None
    request_headers: Optional[str] = None
    request_method: Optional[RequestMethodType] = None
    url: Optional[str] = None
    is_active: Optional[bool] = None


class DeleteWebhookResponse(BaseModel):
    """Response model for webhook deletion."""
    id: int
    deleted_at: Optional[datetime] = None


class WebhookLogResource(BaseModel):
    """Response model for webhook log resources."""
    id: int
    user_id: int
    status_code: int
    request: Dict[str, Any]
    response: str
    created_at: Optional[datetime] = None


class WebhookLogListResource(BaseModel):
    """Response model for list of webhook logs."""
    data: Optional[List[WebhookLogResource]] = None
    result_count: Optional[int] = None
    total_count: Optional[int] = None
    total_page: Optional[int] = None
    page: Optional[int] = None
    per_page: Optional[int] = None


class RegisterClientRequest(BaseModel):
    """Request model for registering a client to a webhook."""
    webhook_id: int


class UnRegisterClientRequest(BaseModel):
    """Request model for unregistering a client from a webhook."""
    webhook_id: int
    customer_id: Optional[int] = None


class UnRegisterClientResponse(BaseModel):
    """Response model for client unregistration."""
    webhook_id: int
    customer_id: int
    deleted_at: Optional[datetime] = None


class ClientResource(BaseModel):
    """Response model for client resources."""
    id: int
    customer_id: int
    webhook_id: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


class ClientListResource(BaseModel):
    """Response model for list of clients."""
    data: Optional[List[ClientResource]] = None
    result_count: Optional[int] = None
    total_count: Optional[int] = None
    total_page: Optional[int] = None
    page: Optional[int] = None
    per_page: Optional[int] = None


class WebhookRegisteredOnResource(BaseModel):
    """Response model for webhook registration resources."""
    id: int
    service_id: int
    customer_id: int
    events: List[Dict[str, Any]]
    is_active: Optional[bool] = None
    registered_at: Optional[datetime] = None


class WebhookRegisteredOnListResource(BaseModel):
    """Response model for list of webhook registrations."""
    data: Optional[List[WebhookRegisteredOnResource]] = None
    result_count: Optional[int] = None
    total_count: Optional[int] = None
    total_page: Optional[int] = None
    page: Optional[int] = None
    per_page: Optional[int] = None
