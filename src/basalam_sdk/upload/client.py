"""
Client for the Upload service API.
"""
from typing import Optional, BinaryIO

from .models import FileResponse, UserUploadFileTypeEnum
from ..base_client import BaseClient


class UploadService(BaseClient):
    """Client for the Upload service API."""

    def __init__(self, **kwargs):
        """Initialize the upload service client."""
        super().__init__(service_name="upload", **kwargs)

    async def upload_file(
            self,
            file: BinaryIO,
            file_type: UserUploadFileTypeEnum,
            custom_unique_name: Optional[str] = None,
            expire_minutes: Optional[int] = None
    ) -> FileResponse:
        """
        Upload a file.

        Args:
            file: The file to upload.
            file_type: The type of file being uploaded.
            custom_unique_name: Optional custom unique name for the file.
            expire_minutes: Optional expiration time in minutes.

        Returns:
            The response containing the uploaded file details.
        """
        endpoint = "/v3/files"
        files = {"file": file}
        data = {
            "file_type": file_type
        }
        if custom_unique_name is not None:
            data["custom_unique_name"] = custom_unique_name
        if expire_minutes is not None:
            data["expire_minutes"] = expire_minutes

        response = await self._post(endpoint, files=files, data=data)
        return FileResponse(**response)

    def upload_file_sync(
            self,
            file: BinaryIO,
            file_type: UserUploadFileTypeEnum,
            custom_unique_name: Optional[str] = None,
            expire_minutes: Optional[int] = None
    ) -> FileResponse:
        """
        Upload a file (synchronous version).

        Args:
            file: The file to upload.
            file_type: The type of file being uploaded.
            custom_unique_name: Optional custom unique name for the file.
            expire_minutes: Optional expiration time in minutes.

        Returns:
            The response containing the uploaded file details.
        """
        endpoint = "/v3/files"
        files = {"file": file}
        data = {
            "file_type": file_type
        }
        if custom_unique_name is not None:
            data["custom_unique_name"] = custom_unique_name
        if expire_minutes is not None:
            data["expire_minutes"] = expire_minutes

        response = self._post_sync(endpoint, files=files, data=data)
        return FileResponse(**response)
