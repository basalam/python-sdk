"""
Models for the Upload service API.
"""
from enum import Enum
from typing import List, Optional, Union, Dict

from pydantic import BaseModel


class ValidationError(BaseModel):
    """Validation error model."""
    loc: List[Union[str, int]]
    msg: str
    type: str


class HTTPValidationError(BaseModel):
    """HTTP validation error model."""
    detail: List[ValidationError]


class UserUploadFileTypeEnum(str, Enum):
    """User upload file type enum."""
    PRODUCT_PHOTO = "product.photo"
    PRODUCT_VIDEO = "product.video"
    USER_AVATAR = "user.avatar"
    USER_COVER = "user.cover"
    VENDOR_COVER = "vendor.cover"
    VENDOR_LOGO = "vendor.logo"
    CHAT_PHOTO = "chat.photo"
    CHAT_VIDEO = "chat.video"
    CHAT_VOICE = "chat.voice"
    CHAT_FILE = "chat.file"


class FileResponse(BaseModel):
    """File response model."""
    id: int
    file_name: str
    file_name_alone: str
    path: str
    format: str
    type: str
    file_type: int
    width: int
    height: int
    size: int
    duration: int
    urls: Dict[str, str]
    created_at: str
    creator_user_id: int
    mime_type: Optional[str] = None
    url: Optional[str] = None
