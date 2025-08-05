"""
Models for the Upload service API.
"""
from enum import Enum
from typing import Optional, Dict

from pydantic import BaseModel


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


class UploadFileRequest(BaseModel):
    """Upload file request model matching OpenAPI Body_create_file_v3_files_post schema."""
    file_type: str
    custom_unique_name: Optional[str] = None
    expire_minutes: Optional[int] = None


class FileResponse(BaseModel):
    """File response model matching OpenAPI FileResponse schema."""
    # Required fields according to OpenAPI
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

    # Optional fields (not in required list in OpenAPI)
    mime_type: Optional[str] = None
    url: Optional[str] = None
