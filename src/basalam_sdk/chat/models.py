"""
Models for the Chat service API.
"""
from enum import Enum
from typing import Dict, List, Optional, Any

from pydantic import BaseModel


class MessageTypeEnum(str, Enum):
    """Message type enumeration."""
    FILE = "file"
    OLD_FILE = "old_file"
    PRODUCT = "product"
    VENDOR = "vendor"
    SOCIAL_POST = "social_post"
    USER = "user"
    COUPON = "coupon"
    NOTIFICATION = "notification"
    ORDER_PROCESS = "order_process"
    STORY = "story"
    PRODUCT_VOICE = "product_voice"
    REVIEW = "review"
    ORDER = "order"
    TEXT = "text"
    PICTURE = "picture"
    GALLERY = "gallery"
    LABEL = "label"
    STICKER = "sticker"
    VOICE = "voice"
    VIDEO = "video"
    LOCATION = "location"


class MessageOrderByEnum(str, Enum):
    """Order by enumeration for get_chats endpoint."""
    UPDATED_AT = "updated_at"
    MODIFIED_AT = "modified_at"


class MessageFiltersEnum(str, Enum):
    """Filters enumeration for get_chats endpoint."""
    UNSEEN = "unseen"
    ORDER = "order"


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


class MessageRequest(BaseModel):
    """Message request model."""
    chat_id: int
    content: Optional[MessageInput] = None
    message_type: MessageTypeEnum
    attachment: Optional[Attachment] = None
    replied_message_id: Optional[int] = None
    message_metadata: Optional[Dict[str, Any]] = None
    temp_id: Optional[int] = None


class GetChatsRequest(BaseModel):
    """Get chats request model."""
    limit: Optional[int] = 30
    order_by: Optional[MessageOrderByEnum] = MessageOrderByEnum.UPDATED_AT
    updated_from: Optional[str] = None
    updated_before: Optional[str] = None
    modified_from: Optional[str] = None
    modified_before: Optional[str] = None
    filters: Optional[MessageFiltersEnum] = None


class LocationResource(BaseModel):
    """Location request model."""
    geo_width: int
    geo_height: int


class MessageLink(BaseModel):
    """Message link model."""
    url: str
    start_index: int
    end_index: int
    is_basalam_link: bool


class MessageFile(BaseModel):
    """Message file model."""
    id: int
    url: str
    name: Optional[str] = None
    size: Optional[int] = None
    type: Optional[str] = None
    width: Optional[int] = None
    height: Optional[int] = None
    blur_hash: Optional[str] = None


class MessageContent(BaseModel):
    """Message content model."""
    links: List[MessageLink] = []
    files: List[MessageFile] = []
    text: Optional[str] = None
    entity_id: Optional[int] = None
    location: Optional[LocationResource] = None


class MessageSender(BaseModel):
    """Message sender model."""
    id: str


class BaseMessageResource(BaseModel):
    """Base message resource model."""
    id: int
    chat_id: int
    seen_at: str
    created_at: str
    updated_at: str
    message_type: str
    sender: MessageSender
    content: MessageContent


class MessageResource(BaseModel):
    """Message resource model."""
    id: int
    chat_id: int
    seen_at: Optional[str] = None
    created_at: str
    updated_at: str
    message_type: str
    sender: MessageSender  # also could be GroupSender
    content: MessageContent
    replied_message: Optional[BaseMessageResource] = None


class MessageResponse(BaseModel):
    """Message response model for create_message endpoint."""
    data: MessageResource
    temp_id: Optional[int] = None


class CreateChatRequest(BaseModel):
    """Create chat request model."""
    user_id: Optional[int] = None
    hash_id: Optional[str] = None


class GroupMetadata(BaseModel):
    """Group model."""
    title: str
    description: Optional[str] = None
    avatar: Optional[str] = None
    link: str
    creator_id: int
    id: int
    chat_id: int


class ChannelMetadata(BaseModel):
    """Channel metadata model."""
    title: str
    description: Optional[str] = None
    avatar: Optional[str] = None
    link: Optional[str] = None
    owner: int
    is_admin: bool = False
    members_count: Optional[int] = None
    can_leave: bool = True
    verified: bool = True


class ChatResource(BaseModel):
    """Chat resource model for create_chat response."""
    id: int
    marked_as_unread: bool
    unseen_message_count: int
    updated_at: str
    deleted_at: Optional[str] = None
    created_at: Optional[str] = None
    modified_at: Optional[str] = None
    chat_type: str
    last_seen_id: Optional[int] = None
    last_message: Optional[MessageResource] = None
    contact: Optional[Dict[str, Any]] = None
    contact_id: Optional[int] = None
    contact_is_blocked: bool
    show_approvals: bool
    reply_markup: Optional[Dict[str, Any]] = None
    archive_state: Optional[str] = None
    group: Optional[GroupMetadata] = None
    channel: Optional[ChannelMetadata] = None


class CreateChatResponse(BaseModel):
    """Chat response model for create_chat endpoint."""
    data: ChatResource


class GetMessagesRequest(BaseModel):
    """Get messages request model."""
    chat_id: int
    message_id: Optional[int] = None
    limit: Optional[int] = 20
    order: Optional[str] = "desc"  # "desc" or "asc"
    cmp: Optional[str] = "lt"  # "lte", "lt", "gte", "gt", "bt"


class GetMessagesListData(BaseModel):
    """Get messages list data model."""
    messages: List[MessageResource]


class GetMessagesResponse(BaseModel):
    """Get messages response model."""
    data: GetMessagesListData


class Contact(BaseModel):
    """Contact model."""
    id: int
    hash_id: str
    name: str
    avatar: Optional[str] = None
    badge: Optional[str] = None
    verified: bool
    vendor: Optional[Dict[str, Any]] = None
    description: Optional[str] = None


class ChatResponse(BaseModel):
    """Response model for a single chat."""
    id: int
    marked_as_unread: bool
    unseen_message_count: int
    updated_at: str
    deleted_at: Optional[str] = None
    created_at: Optional[str] = None
    modified_at: Optional[str] = None
    chat_type: str
    last_seen_id: Optional[int] = None
    last_message: Optional[MessageResource] = None
    contact: Optional[Contact] = None
    contact_id: Optional[int] = None
    contact_is_blocked: bool
    show_approvals: bool
    reply_markup: Optional[Dict[str, Any]] = None
    archive_state: Optional[str] = None
    group: Optional[GroupMetadata] = None
    channel: Optional[ChannelMetadata] = None


class ChatListData(BaseModel):
    """Chat list data model."""
    chats: List[ChatResponse]


class ChatListResponse(BaseModel):
    """Response model for chat list endpoint."""
    data: ChatListData


class EditMessageRequest(BaseModel):
    """Edit message request model."""
    message_id: int
    content: Optional[MessageInput] = None


class DeleteMessageRequest(BaseModel):
    """Delete message request model."""
    message_ids: List[int]


class DeleteChatsRequest(BaseModel):
    """Delete chats request model."""
    chat_ids: List[int]


class ForwardMessageRequest(BaseModel):
    """Forward message request model."""
    message_ids: List[int]
    chat_ids: List[int]


class BooleanResponse(BaseModel):
    """Boolean response model."""
    data: bool


class UnseenChatCountResponse(BaseModel):
    """Unseen chat count response model."""
    count: int
    more_than_count: bool


class EditMessageResponse(BaseModel):
    """Edit message response model."""
    data: MessageResource
