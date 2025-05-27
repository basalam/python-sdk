"""
Chat service module for the Basalam SDK.

This module provides access to Basalam's chat service APIs.
"""

from .client import ChatService
from .models import MessageRequestModel, MessageInput, Attachment, AttachmentFile

__all__ = [
    "ChatService",
    "MessageRequestModel",
    "MessageInput",
    "Attachment",
    "AttachmentFile",
]
