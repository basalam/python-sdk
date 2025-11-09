"""
Data models for the Core service API.

This module contains all the data models used by the core service client.
"""

from datetime import datetime
from enum import Enum, IntEnum
from typing import Dict, List, Optional, Any

from pydantic import BaseModel


# Enums
class ProductStatusInputEnum(IntEnum):
    """Product status input enum."""
    PUBLISHED = 2976
    UNPUBLISHED = 3790
    ILLEGAL = 4184
    PENDING_APPROVAL = 3568


class UnitTypeInputEnum(IntEnum):
    """Unit type input enum for product measurement units."""
    METER_SQUARE = 6375
    MILLIMETER = 6374
    VOLUME = 6373
    FOOT = 6332
    INCH = 6331
    SIR = 6330
    ASLEH = 6329
    KALAF = 6328
    GHALEB = 6327
    SHAKHEH = 6326
    BOUTEH = 6325
    DEST = 6324
    BOTTLE = 6323
    TAKHTEH = 6322
    CARTON = 6321
    BALL = 6320
    PACKAGE = 6319
    PAIR = 6318
    JEAN = 6317
    TAGEH = 6316
    GHAVAREH = 6315
    ONS = 6314
    CC = 6313
    MILLILITER = 6312
    LITER = 6311
    PIECE = 6310
    MESGHAL = 6309
    CENTIMETER = 6308
    METER = 6307
    GRAM = 6306
    KILOGRAM = 6305
    NUMERIC = 6304
    ROLL = 6392
    SUT = 6438
    QIRAT = 6466


class VendorStatusInputEnum(IntEnum):
    """Vendor status input enum."""
    ACTIVE = 2987
    DISABLE = 2988
    NEWBIE = 2989
    SEMI_ACTIVE = 2991
    CLOSED = 3199
    REQUEST_CREATE_VENDOR = 3748
    UNDER_MENTORSHIP = 2990


class ProductBulkActionTypeEnum(IntEnum):
    """Product bulk action type enum."""
    SET = 4101
    PERCENTAGE_INCREASE = 4102
    AMOUNT_INCREASE = 4103


class ProductBulkFieldInputEnum(str, Enum):
    """Product bulk field input enum."""
    PREPARATION_DAYS = "preparationDays"
    PRIMARY_PRICE = "primary_price"
    STOCK = "stock"
    STATUS = "status"


class VendorSettingResponse(BaseModel):
    """Vendor setting response model."""
    id: int
    vendor_id: int
    setting_key: str
    setting_value: str
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


class ResultResponse(BaseModel):
    """Result response model."""
    result: Optional[bool] = None


class UnitTypeResponse(BaseModel):
    """Unit type response model."""
    name: Optional[str] = None
    value: Optional[int] = None
    description: Optional[str] = None


class CategoryUnitTypeResponse(BaseModel):
    """Category unit type response model for categories API."""
    id: Optional[int] = None
    title: Optional[str] = None


class CategoryResponse(BaseModel):
    """Category response model with hierarchical structure."""
    id: Optional[int] = None
    title: Optional[str] = None
    children: Optional[List['CategoryResponse']] = None
    unit_type: Optional[CategoryUnitTypeResponse] = None


class CategoriesResponse(BaseModel):
    """Categories response model."""
    data: Optional[List[CategoryResponse]] = None


class AttributesResponse(BaseModel):
    """Attributes response model for category attributes."""
    data: List['AttributeGroupResponseSchema']


class ProductListResponse(BaseModel):
    """Product list response model."""
    data: Optional[List['ProductItemResponse']] = None
    total_count: Optional[int] = None
    result_count: Optional[int] = None
    total_page: Optional[int] = None
    page: Optional[int] = None
    per_page: Optional[int] = None


class VendorLegalDataSchema(BaseModel):
    """Vendor legal data schema."""
    is_legal: Optional[bool] = None
    economic_number: Optional[str] = None
    national_id: Optional[str] = None
    legal_name: Optional[str] = None
    registration_number: Optional[str] = None
    establishment_announcement_file: Optional[int] = None
    last_change_announcement_file: Optional[int] = None
    vendor_legal_type: Optional[int] = None
    board_phone_number: Optional[str] = None
    board_national_id: Optional[str] = None


class VendorLegalRequestSchema(BaseModel):
    """Vendor legal data schema."""
    is_legal: Optional[bool] = None


class CreateVendorSchema(BaseModel):
    """Create vendor schema."""
    title: str
    category_type: Optional[int] = None
    city: Optional[int] = None
    notice: Optional[str] = None
    summary: Optional[str] = None
    address: Optional[str] = None
    postal_code: Optional[str] = None
    secondary_tel: Optional[str] = None
    logo_id: Optional[int] = None
    covers_id: Optional[List[int]] = None
    licenses: Optional[List[int]] = None
    video_id: Optional[int] = None
    legal_data: Optional[VendorLegalRequestSchema] = None
    identifier: str
    referrer_user: Optional[str] = None
    referral_journey_enum: Optional[int] = None


class UpdateVendorSchema(BaseModel):
    """Update vendor schema."""
    title: Optional[str] = None
    category_type: Optional[int] = None
    city: Optional[int] = None
    notice: Optional[str] = None
    summary: Optional[str] = None
    address: Optional[str] = None
    postal_code: Optional[str] = None
    secondary_tel: Optional[str] = None
    logo_id: Optional[int] = None
    covers_id: Optional[List[int]] = None
    licenses: Optional[List[int]] = None
    video_id: Optional[int] = None
    legal_data: Optional[VendorLegalDataSchema] = None
    about_your_life: Optional[str] = None
    about_your_place: Optional[str] = None
    free_shipping_to_same_city: Optional[int] = None
    free_shipping_to_iran: Optional[int] = None
    national_code: Optional[str] = None
    birthday: Optional[str] = None
    telegram_id: Optional[str] = None
    telegram_channel: Optional[str] = None
    instagram: Optional[str] = None
    eitaa: Optional[str] = None
    email: Optional[str] = None
    credit_card_number: Optional[str] = None
    sheba_number: Optional[str] = None
    sheba_owner: Optional[str] = None
    sheba_bank: Optional[int] = None
    available_cities: Optional[List[int]] = None
    foreign_citizen_code: Optional[str] = None
    mobile: Optional[str] = None
    product_sort_type: Optional[int] = None
    identifier: Optional[str] = None
    info_verification_status: Optional[int] = None


class ShippingMethodUpdateItem(BaseModel):
    """Shipping method update item model."""
    method_id: Optional[int] = None
    is_customized: Optional[bool] = None
    base_cost: Optional[int] = None
    additional_cost: Optional[int] = None
    additional_dimensions_cost: Optional[int] = None


class GetVendorProductsSchema(BaseModel):
    """Get vendor products query parameters schema."""
    title: Optional[str] = None
    category: Optional[List[int]] = None
    statuses: Optional[List[ProductStatusInputEnum]] = None
    stock_gte: Optional[int] = None
    stock_lte: Optional[int] = None
    preparation_day_gte: Optional[int] = None
    preparation_day_lte: Optional[int] = None
    price_gte: Optional[int] = None
    price_lte: Optional[int] = None
    ids: Optional[List[int]] = None
    skus: Optional[List[str]] = None
    illegal_free_shipping_for_iran: Optional[int] = None
    illegal_free_shipping_for_same_city: Optional[int] = None
    page: int = 1
    per_page: int = 10
    variants_flatting: bool = True
    is_wholesale: Optional[bool] = None
    sort: Optional[str] = None


class GetProductsQuerySchema(BaseModel):
    """Get products query parameters schema."""
    category_id: Optional[int] = None
    created_at: Optional[str] = None
    ids: Optional[List[int]] = None
    page: Optional[int] = 1
    per_page: Optional[int] = 10
    price: Optional[str] = None
    product_title: Optional[str] = None
    sort: Optional[str] = "id:desc"
    status: Optional[int] = None
    vendor_ids: Optional[List[int]] = None
    vendor_mobile: Optional[str] = None
    vendor_title: Optional[str] = None


class UpdateShippingMethodSchema(BaseModel):
    """Update shipping method schema."""
    shipping_methods: Optional[List[ShippingMethodUpdateItem]] = None


class ShippingMethodInfo(BaseModel):
    """Shipping method info model."""
    name: Optional[str] = None
    value: Optional[int] = None
    description: Optional[str] = None


class ShippingMethodResponse(BaseModel):
    """Shipping method response model."""
    id: Optional[int] = None
    method: Optional[ShippingMethodInfo] = None
    base_cost: Optional[int] = None
    additional_cost: Optional[int] = None
    is_private: Optional[bool] = None
    additional_dimensions_cost: Optional[int] = None
    vendor_id: Optional[int] = None
    deleted_at: Optional[str] = None


class ShippingMethodListResponse(BaseModel):
    """Shipping method list response model."""
    data: Optional[List[ShippingMethodResponse]] = None
    total_count: Optional[int] = None
    result_count: Optional[int] = None
    total_page: Optional[int] = None
    page: Optional[int] = None
    per_page: Optional[int] = None


class ImageResponse(BaseModel):
    """Image response model with different sizes."""
    id: Optional[int] = None
    original: Optional[str] = None
    xs: Optional[str] = None
    sm: Optional[str] = None
    md: Optional[str] = None
    lg: Optional[str] = None


class LocationDeploymentResponseSchema(BaseModel):
    """Location deployment response schema."""
    name: Optional[str] = None
    value: Optional[int] = None
    description: Optional[str] = None


class VideoDetailResponse(BaseModel):
    """Video detail response model."""
    id: Optional[int] = None
    url: Optional[str] = None
    original: Optional[str] = None
    thumbnail: Optional[str] = None
    hls: Optional[str] = None
    width: Optional[int] = None
    height: Optional[int] = None
    duration: Optional[int] = None


class ProvinceResponse(BaseModel):
    """Province response model."""
    name: Optional[str] = None
    value: Optional[int] = None
    description: Optional[str] = None


class CityResponse(BaseModel):
    """City response model."""
    name: Optional[str] = None
    value: Optional[int] = None
    province: Optional[ProvinceResponse] = None


class StatusResponse(BaseModel):
    """Status response model."""
    name: Optional[str] = None
    value: Optional[int] = None
    description: Optional[str] = None


class GenderResponse(BaseModel):
    """Gender response model."""
    name: Optional[str] = None
    value: Optional[int] = None
    description: Optional[str] = None


class MarkedTypeResponse(BaseModel):
    """Marked type response model."""
    name: Optional[str] = None
    value: Optional[int] = None
    description: Optional[str] = None


class ReferralJourneyResponse(BaseModel):
    """Referral journey response model."""
    name: Optional[str] = None
    value: Optional[int] = None
    description: Optional[str] = None


class ProductSortTypeResponse(BaseModel):
    """Product sort type response model."""
    name: Optional[str] = None
    value: Optional[int] = None
    description: Optional[str] = None


class ShippingMethodItemResponse(BaseModel):
    """Shipping method item response model."""
    name: Optional[str] = None
    value: Optional[int] = None
    description: Optional[str] = None


class CategoryTypeResponse(BaseModel):
    """Category type response model."""
    name: Optional[str] = None
    value: Optional[int] = None
    description: Optional[str] = None


class PublicVendorSimpleResponse(BaseModel):
    """Simple vendor response for nested user data."""
    id: Optional[int] = None
    identifier: Optional[str] = None
    title: Optional[str] = None
    description: Optional[str] = None
    is_active: Optional[bool] = None
    free_shipping_to_iran: Optional[int] = None
    free_shipping_to_same_city: Optional[int] = None
    worth_buy: Optional[str] = None
    created_at: Optional[str] = None
    activated_at: Optional[str] = None
    order_count: Optional[int] = None
    status: Optional[int] = None


class PublicUserResponse(BaseModel):
    """Public user response model."""
    id: Optional[int] = None
    hash_id: Optional[str] = None
    username: Optional[str] = None
    name: Optional[str] = None
    avatar: Optional[ImageResponse] = None
    marked_type: Optional[MarkedTypeResponse] = None
    user_follower_count: Optional[int] = None
    user_following_count: Optional[int] = None
    gender: Optional[GenderResponse] = None
    bio: Optional[str] = None
    city: Optional[CityResponse] = None
    created_at: Optional[str] = None
    last_activity: Optional[str] = None
    referral_journey_enum: Optional[ReferralJourneyResponse] = None
    is_banned_in_social: Optional[bool] = None
    ban_user: Optional[Dict[str, Any]] = None
    vendor: Optional[PublicVendorSimpleResponse] = None


class PrivateUserResponse(BaseModel):
    """Private user response model."""
    id: Optional[int] = None
    hash_id: Optional[str] = None
    username: Optional[str] = None
    name: Optional[str] = None
    avatar: Optional[ImageResponse] = None
    marked_type: Optional[MarkedTypeResponse] = None
    user_follower_count: Optional[int] = None
    user_following_count: Optional[int] = None
    gender: Optional[GenderResponse] = None
    bio: Optional[str] = None
    city: Optional[CityResponse] = None
    created_at: Optional[str] = None
    last_activity: Optional[str] = None
    referral_journey_enum: Optional[ReferralJourneyResponse] = None
    is_banned_in_social: Optional[bool] = None
    ban_user: Optional[Dict[str, Any]] = None
    vendor: Optional[PublicVendorSimpleResponse] = None
    email: Optional[str] = None
    birthday: Optional[str] = None
    national_code: Optional[str] = None
    mobile: Optional[str] = None
    credit_card_number: Optional[str] = None
    credit_card_owner: Optional[str] = None
    foreign_citizen_code: Optional[str] = None
    user_sheba_number: Optional[str] = None
    user_sheba_owner: Optional[str] = None
    bank_information: Optional[str] = None
    bank_information_owner: Optional[str] = None
    info_verification_status: Optional[MarkedTypeResponse] = None
    referrer_user_id: Optional[int] = None


class HomeTabSettingsResponse(BaseModel):
    """Home tab settings response model."""
    name: Optional[str] = None
    order: Optional[int] = None
    is_active: Optional[bool] = None
    extra_data: Optional[Dict[str, Any]] = None


class PublicVendorResponse(BaseModel):
    """Public vendor response model."""
    id: Optional[int] = None
    identifier: Optional[str] = None
    title: Optional[str] = None
    logo: Optional[ImageResponse] = None
    covers: Optional[List[ImageResponse]] = None
    available_cities: Optional[List[CityResponse]] = None
    summary: Optional[str] = None
    status: Optional[StatusResponse] = None
    city: Optional[CityResponse] = None
    category_type: Optional[List[Optional[CategoryTypeResponse]]] = None
    user: Optional[PublicUserResponse] = None
    is_active: Optional[bool] = None
    notice: Optional[str] = None
    gallery: Optional[List[ImageResponse]] = None
    product_count: Optional[int] = None
    free_shipping_to_iran: Optional[int] = None
    free_shipping_to_same_city: Optional[int] = None
    about_your_life: Optional[str] = None
    about_your_place: Optional[str] = None
    worth_buy: Optional[str] = None
    telegram_id: Optional[str] = None
    telegram_channel: Optional[str] = None
    instagram: Optional[str] = None
    eitaa: Optional[str] = None
    order_count: Optional[int] = None
    last_activity: Optional[str] = None
    created_at: Optional[str] = None
    elapsed_time_from_creation: Optional[str] = None
    score: Optional[float] = None
    video: Optional[VideoDetailResponse] = None
    shipping_methods: Optional[List[ShippingMethodItemResponse]] = None
    product_sort_type: Optional[ProductSortTypeResponse] = None
    home_tab_settings: Optional[List[HomeTabSettingsResponse]] = None
    shipping_version: Optional[int] = None


class PrivateVendorResponse(BaseModel):
    """Private vendor response model."""
    id: Optional[int] = None
    name: Optional[str] = None
    description: Optional[str] = None
    logo: Optional[dict] = None
    cover: Optional[str] = None
    mobile: Optional[str] = None
    email: Optional[str] = None
    address: Optional[str] = None
    city_id: Optional[int] = None
    settings: Optional[List[VendorSettingResponse]] = None
    legal_data: Optional[VendorLegalDataSchema] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


class UnsuccessfulProductItem(BaseModel):
    """Unsuccessful product item model."""
    id: Optional[int] = None
    title: Optional[str] = None
    price: Optional[int] = None
    photo: Optional[ImageResponse] = None
    inventory: Optional[int] = None
    primary_price: Optional[int] = None
    preparation_day: Optional[int] = None


class UnsuccessfulBulkUpdateProducts(BaseModel):
    """Unsuccessful bulk update products response model."""
    data: Optional[List[UnsuccessfulProductItem]] = None
    total_count: Optional[int] = None
    result_count: Optional[int] = None
    total_page: Optional[int] = None
    page: Optional[int] = None
    per_page: Optional[int] = None


class ConfirmCurrentUserMobileConfirmSchema(BaseModel):
    """Confirm current user mobile confirm schema."""
    verification_code: int


class ChangeUserMobileRequestSchema(BaseModel):
    """Change user mobile request schema."""
    mobile: str


class ChangeUserMobileConfirmSchema(BaseModel):
    """Change user mobile confirm schema."""
    mobile: str
    verification_code: int


class UserCardsSchema(BaseModel):
    """User cards schema."""
    card_number: Optional[str] = None
    sheba_number: Optional[str] = None
    sheba_owner: Optional[str] = None
    birthday: Optional[str] = None
    national_code: Optional[str] = None
    bank_account_status: Optional[int] = None
    verify_type: Optional[int] = None
    operator_id: Optional[int] = None


class UserCardsOtpSchema(BaseModel):
    """User cards OTP schema."""
    card_number: str
    otp_code: str


class UserVerifyBankInformationSchema(BaseModel):
    """User verify bank information schema."""
    bank_information_id: int
    national_code: str
    birthday: str


class UserVerificationSchema(BaseModel):
    """User verification schema."""
    national_code: str
    birthday: str


class UpdateUserBankInformationSchema(BaseModel):
    """Update user bank information schema."""
    user_id: Optional[int] = None
    card_number: Optional[str] = None
    sheba_number: Optional[str] = None
    account_owner: Optional[str] = None
    status: Optional[int] = None
    bank_name: Optional[str] = None
    sheba_status: Optional[str] = None
    bank_account_number: Optional[str] = None


class UpdateVendorStatusSchema(BaseModel):
    """Update vendor status schema."""
    status: Optional[int] = None
    description: Optional[str] = None
    reason: Optional[int] = None


class UpdateVendorStatusResponse(BaseModel):
    """Update vendor status response."""
    status: Optional[int] = None
    updated_at: Optional[str] = None
    reason: Optional[int] = None
    is_status_changed: Optional[bool] = None
    activated_at: Optional[str] = None


class ChangeVendorMobileRequestSchema(BaseModel):
    """Change vendor mobile request schema."""
    mobile: str


class ChangeVendorMobileConfirmSchema(BaseModel):
    """Change vendor mobile confirm schema."""
    mobile: Optional[str] = None
    verification_code: Optional[int] = None


class UpdateProductVariationSchema(BaseModel):
    """Update product variation schema."""
    primary_price: Optional[int] = None
    stock: Optional[int] = None
    sku: Optional[str] = None


class ShippingDataResponse(BaseModel):
    """Shipping data response model."""
    illegal_for_iran: Optional[bool] = None
    illegal_for_same_city: Optional[bool] = None


class PropertyResponse(BaseModel):
    """Property response model."""
    id: Optional[int] = None
    title: Optional[str] = None
    type: Optional[str] = None


class PropertyValueResponse(BaseModel):
    """Property value response model."""
    id: Optional[int] = None
    title: Optional[str] = None
    value: Optional[str] = None
    order: Optional[int] = None


class VariantPropertyResponse(BaseModel):
    """Variant property response model."""
    property: Optional[PropertyResponse] = None
    value: Optional[PropertyValueResponse] = None


class ProductVariantResponse(BaseModel):
    """Product variant response model."""
    id: Optional[int] = None
    price: Optional[int] = None
    primary_price: Optional[int] = None
    stock: Optional[int] = None
    order: Optional[int] = None
    properties: Optional[List[VariantPropertyResponse]] = None
    sku: Optional[str] = None
    discount: Optional[Dict[str, Any]] = None


class ProductAttributeValueResponse(BaseModel):
    """Product attribute value response model."""
    id: Optional[int] = None
    title: Optional[str] = None
    value: Optional[str] = None
    attribute_id: Optional[int] = None
    order: Optional[int] = None
    vendor_id: Optional[int] = None


class ProductAttributeResponse(BaseModel):
    """Product attribute response model."""
    id: Optional[int] = None
    unit: Optional[str] = None
    type: Optional[StatusResponse] = None
    title: Optional[str] = None
    value: Optional[str] = None
    selected_values: Optional[List[ProductAttributeValueResponse]] = None
    required: Optional[bool] = None


class CategoryProductResponse(BaseModel):
    """Category product response model."""
    id: Optional[int] = None
    title: Optional[str] = None
    placeholder: Optional[str] = None
    parent: Optional[Dict[str, Any]] = None
    unit_type_id: Optional[StatusResponse] = None


class ProductRevisionDataResponse(BaseModel):
    """Product revision data response model."""
    title: Optional[str] = None
    brief: Optional[str] = None
    description: Optional[str] = None
    status: Optional[StatusResponse] = None
    category: Optional[CategoryProductResponse] = None
    keywords: Optional[List[str]] = None
    photo: Optional[ImageResponse] = None
    photos: Optional[List[ImageResponse]] = None
    video: Optional[VideoDetailResponse] = None
    product_attribute: Optional[List[ProductAttributeResponse]] = None
    packaged_weight: Optional[int] = None
    net_weight: Optional[int] = None
    net_weight_decimal: Optional[float] = None
    preparation_day: Optional[int] = None
    price: Optional[int] = None
    primary_price: Optional[int] = None
    inventory: Optional[int] = None
    variants: Optional[List[ProductVariantResponse]] = None
    is_wholesale: Optional[bool] = None


class RejectionReasonResponse(BaseModel):
    """Rejection reason response model."""
    name: Optional[str] = None
    value: Optional[int] = None
    description: Optional[str] = None


class IllegalPhotoResponse(BaseModel):
    """Illegal photo response model."""
    file_id: Optional[int] = None
    rejection_reasons: Optional[List[RejectionReasonResponse]] = None


class RevisionMetadataResponse(BaseModel):
    """Revision metadata response model."""
    illegal_photos: Optional[List[IllegalPhotoResponse]] = None
    description: Optional[str] = None
    is_conditional_approval: Optional[bool] = None


class ProductRevisionResponse(BaseModel):
    """Product revision response model."""
    rejection_reasons: Optional[List[RejectionReasonResponse]] = None
    data: Optional[ProductRevisionDataResponse] = None
    rejected_at: Optional[str] = None
    metadata: Optional[RevisionMetadataResponse] = None


class ProductAttributeRequestItem(BaseModel):
    """Product attribute request item model."""
    attribute_id: int
    value: Optional[str] = None
    selected_values: Optional[List[int]] = None


class VariantPropertyRequestItem(BaseModel):
    """Variant property request item model."""
    value: str
    property: str


class VariantRequestItem(BaseModel):
    """Variant request item model."""
    primary_price: int
    stock: int
    sku: Optional[str] = None
    properties: List[VariantPropertyRequestItem]


class ShippingDataRequestItem(BaseModel):
    """Shipping data request item model."""
    illegal_for_iran: bool
    illegal_for_same_city: bool


class PackagingDimensionsRequestItem(BaseModel):
    """Packaging dimensions request item model."""
    height: int
    length: int
    width: int


class ProductRequestSchema(BaseModel):
    """Product request schema for create and update operations."""
    name: Optional[str] = None
    photo: Optional[int] = None
    photos: Optional[List[int]] = None
    video: Optional[int] = None
    brief: Optional[str] = None
    description: Optional[str] = None
    order: Optional[int] = None
    category_id: Optional[int] = None
    status: ProductStatusInputEnum = ProductStatusInputEnum.PUBLISHED
    preparation_days: int = 1
    keywords: Optional[List[str]] = None
    weight: Optional[float] = None
    package_weight: Optional[int] = None
    primary_price: Optional[int] = None
    stock: Optional[int] = None
    shipping_city_ids: Optional[List[int]] = None
    shipping_method_ids: Optional[List[int]] = None
    product_attribute: Optional[List[ProductAttributeRequestItem]] = None
    virtual: Optional[bool] = None
    variants: Optional[List[VariantRequestItem]] = None
    shipping_data: Optional[ShippingDataRequestItem] = None
    unit_quantity: Optional[float] = None
    unit_type: Optional[UnitTypeInputEnum] = None
    sku: Optional[str] = None
    packaging_dimensions: Optional[PackagingDimensionsRequestItem] = None
    is_wholesale: bool = False


class ProductItemResponse(BaseModel):
    """Product item response model."""
    id: Optional[int] = None
    title: Optional[str] = None
    price: Optional[int] = None
    photo: Optional[ImageResponse] = None
    photos: Optional[List[ImageResponse]] = None
    video: Optional[VideoDetailResponse] = None
    status: Optional[StatusResponse] = None
    vendor: Optional[PublicVendorResponse] = None
    summary: Optional[str] = None
    category: Optional[CategoryProductResponse] = None
    inventory: Optional[int] = None
    net_weight: Optional[int] = None
    created_at: Optional[str] = None
    updated_at: Optional[str] = None
    description: Optional[str] = None
    primary_price: Optional[int] = None
    packaged_weight: Optional[int] = None
    preparation_day: Optional[int] = None
    net_weight_decimal: Optional[float] = None
    location_deployment: Optional[LocationDeploymentResponseSchema] = None
    url: Optional[str] = None
    published: Optional[bool] = None
    sales_count: Optional[int] = None
    view_count: Optional[int] = None
    can_add_to_cart: Optional[bool] = None
    has_variation: Optional[bool] = None
    unit_quantity: Optional[float] = None
    unit_type: Optional[UnitTypeResponse] = None
    discount: Optional[Dict[str, Any]] = None
    is_product_for_revision: Optional[bool] = None
    revision: Optional[ProductRevisionResponse] = None
    shipping_data: Optional[ShippingDataResponse] = None
    variant: Optional[List[ProductVariantResponse]] = None
    sku: Optional[str] = None
    is_wholesale: Optional[bool] = None


class CategoryListItemResponseSchema(BaseModel):
    """Category list item response schema."""
    id: Optional[int] = None
    title: Optional[str] = None
    slug: Optional[str] = None


class AttributeGroupResponseSchema(BaseModel):
    """Attribute group response schema."""
    title: Optional[str] = None
    attributes: Optional[List[ProductAttributeResponse]] = None


class FreeShippingResponseSchema(BaseModel):
    """Free shipping response schema."""
    result: Optional[bool] = None
    meta_data: Optional[Dict[str, Any]] = None


class NavigationResponseSchema(BaseModel):
    """Navigation response schema."""
    slug: Optional[str] = None
    title: Optional[str] = None
    categoryIds: Optional[List[int]] = None
    parent: Optional[Dict[str, Any]] = None


class PackagingDimensionsResponseSchema(BaseModel):
    """Packaging dimensions response schema."""
    height: Optional[int] = None
    width: Optional[int] = None
    length: Optional[int] = None


class ProductResponseSchema(BaseModel):
    """Product response schema for create and update operations."""
    id: Optional[int] = None
    title: Optional[str] = None
    price: Optional[int] = None
    photo: Optional[ImageResponse] = None
    photos: Optional[List[ImageResponse]] = None
    video: Optional[VideoDetailResponse] = None
    status: Optional[StatusResponse] = None
    vendor: Optional[PublicVendorResponse] = None
    summary: Optional[str] = None
    category: Optional[CategoryProductResponse] = None
    category_list: Optional[List[CategoryListItemResponseSchema]] = None
    inventory: Optional[int] = None
    net_weight: Optional[int] = None
    net_weight_decimal: Optional[float] = None
    created_at: Optional[str] = None
    updated_at: Optional[str] = None
    description: Optional[str] = None
    is_saleable: Optional[bool] = None
    is_showable: Optional[bool] = None
    is_available: Optional[bool] = None
    primary_price: Optional[int] = None
    shipping_area: Optional[List[CityResponse]] = None
    packaged_weight: Optional[int] = None
    preparation_day: Optional[int] = None
    attribute_groups: Optional[List[AttributeGroupResponseSchema]] = None
    is_free_shipping: Optional[bool] = None
    location_deployment: Optional[LocationDeploymentResponseSchema] = None
    is_product_for_revision: Optional[bool] = None
    has_selectable_variation: Optional[bool] = None
    revision: Optional[ProductRevisionResponse] = None
    view_count: Optional[int] = None
    can_add_to_cart: Optional[bool] = None
    review_count: Optional[int] = None
    rating: Optional[float] = None
    navigation: Optional[NavigationResponseSchema] = None
    variants: Optional[List[ProductVariantResponse]] = None
    variants_selected_index: Optional[int] = None
    shipping_data: Optional[ShippingDataResponse] = None
    free_shipping: Optional[FreeShippingResponseSchema] = None
    allow_category_change: Optional[bool] = None
    unit_quantity: Optional[float] = None
    unit_type: Optional[UnitTypeResponse] = None
    sku: Optional[str] = None
    discount: Optional[Dict[str, Any]] = None
    packaging_dimensions: Optional[PackagingDimensionsResponseSchema] = None
    is_wholesale: Optional[bool] = None


class UpdateVariantRequestItem(BaseModel):
    """Update variant request item model."""
    id: Optional[int] = None
    primary_price: Optional[int] = None
    stock: Optional[int] = None


class UpdateProductRequestItem(BaseModel):
    """Update product request item model."""
    id: Optional[int] = None
    name: Optional[str] = None
    primary_price: Optional[int] = None
    order: Optional[int] = None
    stock: Optional[int] = None
    status: Optional[int] = None
    preparation_days: Optional[int] = None
    variants: Optional[List[UpdateVariantRequestItem]] = None
    product_attribute: Optional[List[ProductAttributeRequestItem]] = None
    shipping_data: Optional[ShippingDataRequestItem] = None


class BatchUpdateProductsRequest(BaseModel):
    """Update products request schema."""
    data: Optional[List[UpdateProductRequestItem]] = None


class UpdateProductResponseItem(BaseModel):
    """Update product response item model."""
    id: Optional[int] = None
    is_product_for_revision: Optional[bool] = None
    has_error: Optional[bool] = None
    error_message: Optional[str] = None


class RangeFilterItem(BaseModel):
    """Range filter item model for start/end values."""
    start: Optional[int] = None
    end: Optional[int] = None


class ProductFilterSchema(BaseModel):
    """Product filter schema for bulk operations."""
    title: Optional[str] = None
    product_id: Optional[List[int]] = None
    category: Optional[List[int]] = None
    status: Optional[List[str]] = None
    stock: Optional[RangeFilterItem] = None
    preparation_day: Optional[RangeFilterItem] = None
    price: Optional[RangeFilterItem] = None
    exclude: Optional[List[int]] = None


class BulkActionItem(BaseModel):
    """Bulk action item model."""
    field: ProductBulkFieldInputEnum
    action: ProductBulkActionTypeEnum
    value: Optional[int] = None


class BulkProductsUpdateRequestSchema(BaseModel):
    """Bulk products update request schema."""
    product_filter: Optional[ProductFilterSchema] = None
    action: List[BulkActionItem]


class BulkProductsUpdateResponseSchema(BaseModel):
    """Bulk products update response schema."""
    id: Optional[int] = None


class BulkProductUpdateItemResponse(BaseModel):
    """Bulk product update item response model."""
    id: Optional[int] = None
    successful_count: Optional[int] = None
    unsuccessful_count: Optional[int] = None
    ended_at: Optional[str] = None
    unsuccessful_products: Optional[List[int]] = None
    status: Optional[Dict[str, Any]] = None


class BulkProductsUpdatesListResponse(BaseModel):
    """Bulk products updates list response model."""
    data: Optional[List[BulkProductUpdateItemResponse]] = None
    total_count: Optional[int] = None
    result_count: Optional[int] = None
    total_page: Optional[int] = None
    page: Optional[int] = None
    per_page: Optional[int] = None


class BulkProductsUpdatesCountResponse(BaseModel):
    """Bulk products updates count response model."""
    remove_discounts_requests_count: Optional[int] = None
    apply_discount_requests_count: Optional[int] = None
    bulk_action_requests_count: Optional[int] = None
    sum: Optional[int] = None


class ProductShelfResponse(BaseModel):
    """Product shelf response model."""
    id: Optional[int] = None
    title: Optional[str] = None
    description: Optional[str] = None
    vendor_id: Optional[int] = None


class DiscountProductFilterSchema(BaseModel):
    """Product filter schema for discount operations."""
    variation_ids: Optional[List[int]] = None
    product_ids: Optional[List[int]] = None
    status: Optional[List[str]] = None
    stock: Optional[RangeFilterItem] = None
    price: Optional[RangeFilterItem] = None
    exclude: Optional[List[int]] = None
    category_id: Optional[List[int]] = None
    title: Optional[str] = None


class CreateDiscountRequestSchema(BaseModel):
    """Create discount request schema."""
    product_filter: Optional[DiscountProductFilterSchema] = None
    discount_percent: int
    active_days: int


class DeleteDiscountRequestSchema(BaseModel):
    """Delete discount request schema."""
    product_filter: Optional[DiscountProductFilterSchema] = None


class ShelveSchema(BaseModel):
    """Shelve request schema for create and update operations."""
    title: str
    description: Optional[str] = None
    file_id: Optional[int] = None


class UpdateShelveProductsSchema(BaseModel):
    """Update shelve products request schema."""
    include_products: Optional[List[int]] = None
    exclude_products: Optional[List[int]] = None
