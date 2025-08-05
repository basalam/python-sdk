"""
Client for the Upload service API.
"""
from typing import Optional, BinaryIO

from .models import FileResponse, UserUploadFileTypeEnum, UploadFileRequest
from ..base_client import BaseClient


class UploadService(BaseClient):
    """Client for the Upload service API."""

    def __init__(self, **kwargs):
        """Initialize the upload service client."""
        super().__init__(service="upload", **kwargs)

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

        # Prepare files for multipart/form-data
        files = {"file": file}

        # Prepare form data according to OpenAPI specification
        # Create request model to validate parameters, then extract data
        request = UploadFileRequest(
            file_type=file_type,
            custom_unique_name=custom_unique_name,
            expire_minutes=expire_minutes
        )

        # Convert to form data, excluding None values
        data = request.model_dump(exclude_none=True, mode='json')

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

        # Prepare files for multipart/form-data
        files = {"file": file}

        # Prepare form data according to OpenAPI specification
        # Create request model to validate parameters, then extract data
        request = UploadFileRequest(
            file_type=file_type,
            custom_unique_name=custom_unique_name,
            expire_minutes=expire_minutes
        )

        # Convert to form data, excluding None values
        data = request.model_dump(exclude_none=True, mode='json')

        response = self._post_sync(endpoint, files=files, data=data)
        return FileResponse(**response)
