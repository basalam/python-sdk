"""
Data models for the Core service API.

This module contains all the data models used by the core service client.
"""

from datetime import datetime
from enum import Enum
from typing import Dict, List, Optional, Any, Union

from pydantic import BaseModel


# Enums
class ProductStatusInputEnum(str, Enum):
    """Product status input enum."""
    DRAFT = "draft"
    PUBLISHED = "published"
    ARCHIVED = "archived"
    REJECTED = "rejected"
    PENDING = "pending"


class ProductBulkFieldInputEnum(str, Enum):
    """Product bulk field input enum."""
    PRICE = "price"
    STOCK = "stock"
    STATUS = "status"
    CATEGORY = "category"
    SHIPPING_METHOD = "shipping_method"
    SHIPPING_CITY = "shipping_city"
    PREPARATION_DAYS = "preparation_days"
    PACKAGE_WEIGHT = "package_weight"
    WEIGHT = "weight"
    KEYWORDS = "keywords"
    BRIEF = "brief"
    DESCRIPTION = "description"
    PHOTO = "photo"
    PHOTOS = "photos"
    VIDEO = "video"
    ORDER = "order"


class ProductBulkActionTypeEnum(str, Enum):
    """Product bulk action type enum."""
    SET = "set"
    INCREASE = "increase"
    DECREASE = "decrease"
    MULTIPLY = "multiply"
    DIVIDE = "divide"
    APPEND = "append"
    PREPEND = "prepend"
    REPLACE = "replace"
    REMOVE = "remove"


class ProductBulkFieldInputV4Enum(str, Enum):
    """Product bulk field input v4 enum."""
    PRICE = "price"
    STOCK = "stock"
    STATUS = "status"
    CATEGORY = "category"
    SHIPPING_METHOD = "shipping_method"
    SHIPPING_CITY = "shipping_city"
    PREPARATION_DAYS = "preparation_days"
    PACKAGE_WEIGHT = "package_weight"
    WEIGHT = "weight"
    KEYWORDS = "keywords"
    BRIEF = "brief"
    DESCRIPTION = "description"
    PHOTO = "photo"
    PHOTOS = "photos"
    VIDEO = "video"
    ORDER = "order"


class ProductRevisionInputEnums(str, Enum):
    """Product revision input enums."""
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"
    DRAFT = "draft"


# Base Models
class RangeInput(BaseModel):
    """Range input model."""
    min: Optional[int] = None
    max: Optional[int] = None


class WholePrice(BaseModel):
    """Whole price model."""
    price: int
    min_count: int
    max_count: Optional[int] = None


class VendorSettingResponse(BaseModel):
    """Vendor setting response model."""
    id: int
    vendor_id: int
    setting_key: str
    setting_value: str
    created_at: datetime
    updated_at: datetime


# Response Models
class OkResponse(BaseModel):
    """OK response model."""
    message: str


class EnumResponse(BaseModel):
    """Enum response model."""
    value: str
    label: str


class PhotoResponse(BaseModel):
    """Photo response model."""
    id: int
    url: str
    width: int
    height: int
    size: int
    created_at: datetime


class VideoResponse(BaseModel):
    """Video response model."""
    id: int
    url: str
    width: int
    height: int
    size: int
    duration: int
    created_at: datetime


class CityResponse(BaseModel):
    """City response model."""
    id: int
    name: str
    province_id: int
    created_at: datetime
    updated_at: datetime


class NavigationResponse(BaseModel):
    """Navigation response model."""
    id: int
    title: str
    url: str
    order: int
    created_at: datetime
    updated_at: datetime


class PublicUserResponse(BaseModel):
    """Public user response model."""
    id: int
    name: str
    avatar: Optional[str] = None
    created_at: datetime
    updated_at: datetime


class PrivateUserResponse(BaseModel):
    """Private user response model."""
    id: int
    name: str
    email: str
    mobile: str
    avatar: Optional[str] = None
    created_at: datetime
    updated_at: datetime


class BankInformationResponse(BaseModel):
    """Bank information response model."""
    id: int
    user_id: int
    bank_name: str
    account_number: str
    card_number: str
    sheba_number: str
    created_at: datetime
    updated_at: datetime


class CategoryResponse(BaseModel):
    """Category response model."""
    id: int
    name: str
    parent_id: Optional[int] = None
    level: int
    created_at: datetime
    updated_at: datetime


class CategoriesResponse(BaseModel):
    """Categories response model."""
    data: List[CategoryResponse]
    total: int
    per_page: int
    current_page: int
    last_page: int
    from_value: int
    to: int


class CategoryLV12Response(BaseModel):
    """Category level 1&2 response model."""
    id: int
    name: str
    parent_id: Optional[int] = None
    level: int
    children: List[CategoryResponse]
    created_at: datetime
    updated_at: datetime


class AttributesResponse(BaseModel):
    """Attributes response model."""
    id: int
    name: str
    type: str
    values: List[str]
    created_at: datetime
    updated_at: datetime


class ProductResponse(BaseModel):
    """Product response model."""
    id: int
    name: str
    brief: str
    description: str
    price: int
    stock: int
    status: ProductStatusInputEnum
    category_id: int
    vendor_id: int
    photos: List[PhotoResponse]
    video: Optional[VideoResponse] = None
    created_at: datetime
    updated_at: datetime


class ProductListResponse(BaseModel):
    """Product list response model."""
    data: List[ProductResponse]
    total: int
    per_page: int
    current_page: int
    last_page: int
    from_value: int
    to: int


class BulkUpdateProductsResponse(BaseModel):
    """Bulk update products response model."""
    data: List[ProductResponse]
    total: int
    per_page: int
    current_page: int
    last_page: int
    from_value: int
    to: int


# Request Models
class CreateVendorSchema(BaseModel):
    """Create vendor schema."""
    name: str
    description: str
    logo: Optional[str] = None
    cover: Optional[str] = None
    mobile: str
    email: str
    address: str
    city_id: int


class UpdateVendorSchema(BaseModel):
    """Update vendor schema."""
    name: Optional[str] = None
    description: Optional[str] = None
    logo: Optional[str] = None
    cover: Optional[str] = None
    mobile: Optional[str] = None
    email: Optional[str] = None
    address: Optional[str] = None
    city_id: Optional[int] = None


class CreateProductSchema(BaseModel):
    """Create product schema."""
    name: str
    brief: str
    description: str
    price: int
    stock: int
    status: ProductStatusInputEnum
    category_id: int
    photos: List[str]
    video: Optional[str] = None


class UpdateProductSchema(BaseModel):
    """Update product schema."""
    name: Optional[str] = None
    brief: Optional[str] = None
    description: Optional[str] = None
    price: Optional[int] = None
    stock: Optional[int] = None
    status: Optional[ProductStatusInputEnum] = None
    category_id: Optional[int] = None
    photos: Optional[List[str]] = None
    video: Optional[str] = None


class ProductFilterSchema(BaseModel):
    """Product filter schema."""
    name: Optional[str] = None
    category_id: Optional[int] = None
    vendor_id: Optional[int] = None
    status: Optional[ProductStatusInputEnum] = None
    min_price: Optional[int] = None
    max_price: Optional[int] = None
    min_stock: Optional[int] = None
    max_stock: Optional[int] = None
    created_at_start: Optional[datetime] = None
    created_at_end: Optional[datetime] = None
    updated_at_start: Optional[datetime] = None
    updated_at_end: Optional[datetime] = None
    sort_by: Optional[str] = None
    sort_order: Optional[str] = None
    page: Optional[int] = None
    per_page: Optional[int] = None


class ProductBulkActionSchema(BaseModel):
    """Product bulk action schema."""
    field: ProductBulkFieldInputEnum
    action: ProductBulkActionTypeEnum
    value: Any
    product_ids: List[int]


class ShippingMethodSchema(BaseModel):
    """Shipping method schema."""
    name: str
    description: str
    price: int
    min_order_amount: int
    max_order_amount: Optional[int] = None
    preparation_days: int
    is_default: bool = False


class UpdateShippingMethodSchema(BaseModel):
    """Update shipping method schema."""
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[int] = None
    min_order_amount: Optional[int] = None
    max_order_amount: Optional[int] = None
    preparation_days: Optional[int] = None
    is_default: Optional[bool] = None


class ShippingMethodResponse(BaseModel):
    """Shipping method response model."""
    id: int
    vendor_id: int
    name: str
    description: str
    price: int
    min_order_amount: int
    max_order_amount: Optional[int] = None
    preparation_days: int
    is_default: bool
    created_at: datetime
    updated_at: datetime


class ShippingMethodListResponse(BaseModel):
    """Shipping method list response model."""
    data: List[ShippingMethodResponse]
    total: int
    per_page: int
    current_page: int
    last_page: int
    from_value: int
    to: int


class PublicVendorResponse(BaseModel):
    """Public vendor response model."""
    id: int
    name: str
    description: str
    logo: Optional[str] = None
    cover: Optional[str] = None
    mobile: str
    email: str
    address: str
    city_id: int
    created_at: datetime
    updated_at: datetime


class PrivateVendorResponse(BaseModel):
    """Private vendor response model."""
    id: int
    name: str
    description: str
    logo: Optional[str] = None
    cover: Optional[str] = None
    mobile: str
    email: str
    address: str
    city_id: int
    settings: List[VendorSettingResponse]
    created_at: datetime
    updated_at: datetime


class VendorBulkActionRequestSchema(BaseModel):
    """Vendor bulk action request schema."""
    action: str
    vendor_ids: List[int]


class CreateBulkUpdateResponse(BaseModel):
    """Create bulk update response model."""
    id: int
    status: str
    created_at: datetime
    updated_at: datetime


class BulkUpdateListResponse(BaseModel):
    """Bulk update list response model."""
    data: List[CreateBulkUpdateResponse]
    total: int
    per_page: int
    current_page: int
    last_page: int
    from_value: int
    to: int


class UnsuccessfulBulkUpdateProducts(BaseModel):
    """Unsuccessful bulk update products model."""
    product_id: int
    error: str


class ConfirmCurrentUserMobileConfirmSchema(BaseModel):
    """Confirm current user mobile confirm schema."""
    code: str


class ChangeUserMobileRequestSchema(BaseModel):
    """Change user mobile request schema."""
    mobile: str


class ChangeUserMobileConfirmSchema(BaseModel):
    """Change user mobile confirm schema."""
    code: str


class UserCardsSchema(BaseModel):
    """User cards schema."""
    bank_name: str
    account_number: str
    card_number: str
    sheba_number: str


class UserCardsOtpSchema(BaseModel):
    """User cards OTP schema."""
    code: str


class UserVerifyBankInformationSchema(BaseModel):
    """User verify bank information schema."""
    code: str


class UserVerificationSchema(BaseModel):
    """User verification schema."""
    national_code: str
    birth_date: str


class ValidationError(BaseModel):
    """Validation error model."""
    loc: List[Union[str, int]]
    msg: str
    type: str


class HTTPValidationError(BaseModel):
    """HTTP validation error model."""
    detail: List[ValidationError]


class ProductVariationResponse(BaseModel):
    """Product variation response model."""
    id: int
    product_id: int
    name: str
    price: int
    stock: int
    created_at: datetime
    updated_at: datetime


class ChangeMobileNumberSchema(BaseModel):
    """Change mobile number schema."""
    mobile: str


class BulkUpdateProductSchema(BaseModel):
    """Bulk update product schema."""
    field: ProductBulkFieldInputEnum
    action: ProductBulkActionTypeEnum
    value: Any
    product_ids: List[int]


class CategoryAttributeResponse(BaseModel):
    """Category attribute response model."""
    id: int
    name: str
    type: str
    values: List[str]
    created_at: datetime
    updated_at: datetime


class UpdateProductVariantsSchema(BaseModel):
    """Update product variants schema."""
    variants: List[Dict[str, Any]]


class BatchResponse(BaseModel):
    """Batch response model."""
    message: str


class BulkUpdateListItemResponse(BaseModel):
    """Bulk update list item response model."""
    id: int
    status: str
    created_at: datetime
    updated_at: datetime


class UnitTypeResponse(BaseModel):
    """Unit type response model."""
    id: int
    name: str
    created_at: datetime
    updated_at: datetime


class CategoryListResponse(BaseModel):
    """Category list response model."""
    id: int
    title: str
    slug: str


class PrivateProductListResponse(BaseModel):
    """Private product list response model."""
    data: List[ProductResponse]
    total: int
    per_page: int
    current_page: int
    last_page: int
    from_value: int
    to: int
