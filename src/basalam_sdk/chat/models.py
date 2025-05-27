"""
Models for the Chat service API.
"""
from typing import Dict, List, Optional, Any, Union

from pydantic import BaseModel


class ValidationError(BaseModel):
    """Validation error model."""
    loc: List[Union[str, int]]
    msg: str
    type: str


class HTTPValidationError(BaseModel):
    """HTTP validation error model."""
    detail: List[ValidationError]


class MessageInput(BaseModel):
    """Message input model."""
    text: Optional[str] = None
    entity_id: Optional[int] = None


class AttachmentFile(BaseModel):
    """Attachment file model."""
    id: int
    url: str
    height: Optional[int] = None
    width: Optional[int] = None
    name: Optional[str] = None
    type: Optional[str] = None
    size: Optional[int] = None
    blur_hash: Optional[str] = None


class Attachment(BaseModel):
    """Attachment model."""
    files: Optional[List[AttachmentFile]] = None


class MessageRequestModel(BaseModel):
    """Message request model."""
    chat_id: int
    message_type: str
    message_source: Optional[str] = None
    message: Optional[MessageInput] = None
    attachment: Optional[Attachment] = None
    replied_message_id: Optional[int] = None
    message_metadata: Optional[Dict[str, Any]] = None
    temp_id: Optional[int] = None


class CreateChatRequest(BaseModel):
    """Create chat request model."""
    user_id: int
    chat_type: str = "PRIVATE"
    chat_metadata: Optional[Dict[str, Any]] = None
