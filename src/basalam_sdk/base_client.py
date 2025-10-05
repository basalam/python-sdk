"""
Base client for making requests to the Basalam API.
"""
import json
from typing import Any, Dict, List, Optional, Union, TypeVar, Type
from urllib.parse import urljoin

import httpx
from pydantic import BaseModel

from .auth import BaseAuth
from .config import BasalamConfig
from .errors import BasalamError, BasalamAPIError, BasalamAuthError

# Type variable for response models
T = TypeVar('T', bound=BaseModel)


class BaseClient:
    """
    Base client for making requests to the Basalam API.

    This class handles HTTP requests, authentication, and error handling.
    It serves as the foundation for all service-specific clients.
    """

    def __init__(
            self,
            auth: BaseAuth,
            config: Optional[BasalamConfig] = None,
            service: Optional[str] = None,
    ):
        """
        Initialize the base client.
        """
        self.auth = auth
        self.config = config or BasalamConfig()
        self.service = service

        # Set the base URL for this service
        if service:
            self.base_url = self.config.get_service_url(service)
        else:
            self.base_url = self.config.base_url

    @staticmethod
    def _handle_http_error(e: httpx.HTTPStatusError) -> None:
        """Handle HTTP errors and convert them to Basalam exceptions."""
        # Print the response data for debugging
        try:
            response_data = e.response.json()
            print(
                f"API Error Response ({e.response.status_code}): {json.dumps(response_data, ensure_ascii=False, indent=2)}")
        except (json.JSONDecodeError, ValueError):
            print(f"API Error Response ({e.response.status_code}): {e.response.text}")

        if e.response.status_code == 401:
            raise BasalamAuthError(f"Authentication failed: {e}", response=e.response)

        try:
            error_data = e.response.json()
            error_message = error_data.get("message", str(e))
            error_code = error_data.get("code", e.response.status_code)
        except (json.JSONDecodeError, ValueError):
            error_message = str(e)
            error_code = e.response.status_code

        raise BasalamAPIError(
            message=error_message,
            status_code=e.response.status_code,
            code=error_code,
            response=e.response,
        )

    @staticmethod
    def _unwrap_response(data: Union[Dict, List]) -> Union[Dict, List]:
        """
        Unwrap response data if it's wrapped in a single-key dictionary.

        This handles cases where the API returns data wrapped in a single key,
        like {"openapi_raw_data": [...]} or any future wrapper format.

        Args:
            data: The response data to unwrap

        Returns:
            The unwrapped data if it was wrapped, otherwise the original data
        """
        # If it's a dict with exactإإly one key and the value is a list,
        # return the list value (unwrap it)
        if isinstance(data, dict) and len(data) == 1:
            key = next(iter(data))
            value = data[key]
            # Only unwrap if the single value is a list (common for wrapped list responses)
            # This preserves single-key dict responses that are meant to be dicts
            if isinstance(value, list):
                return value

        return data

    @staticmethod
    def _parse_response_data(
            response: httpx.Response,
            response_model: Optional[Type[T]] = None
    ) -> Union[Dict[str, Any], List[Dict[str, Any]], T]:
        """Parse response data and validate with model if provided."""
        # Handle empty responses
        if not response.content:
            return {}

        try:
            data = response.json()
        except json.JSONDecodeError:
            raise BasalamError(f"Invalid JSON response: {response.text}")

        # Parse the response using the provided model
        if response_model:
            if isinstance(data, list):
                return [response_model.model_validate(item) for item in data]
            return response_model.model_validate(data)

        return data

    async def request(
            self,
            method: str,
            path: str,
            params: Optional[Dict[str, Any]] = None,
            data: Optional[Dict[str, Any]] = None,
            json_data: Optional[Dict[str, Any]] = None,
            files: Optional[Dict[str, Any]] = None,
            headers: Optional[Dict[str, str]] = None,
            response_model: Optional[Type[T]] = None,
            require_auth: bool = True,
    ) -> Union[Dict[str, Any], List[Dict[str, Any]], T]:
        """
        Make an async request to the API.
        """
        url = urljoin(self.base_url, path)

        # Build headers: start with config headers, add auth headers if needed, then custom headers
        request_headers = self.config.get_headers().copy()

        if require_auth:
            auth_headers = await self.auth.get_auth_headers()
            request_headers.update(auth_headers)

        if headers:
            request_headers.update(headers)

        async with httpx.AsyncClient(
                timeout=self.config.timeout,
                follow_redirects=True,
        ) as client:
            try:
                response = await client.request(
                    method=method,
                    url=url,
                    headers=request_headers,
                    params=params,
                    data=data,
                    json=json_data,
                    files=files,
                )
                response.raise_for_status()

            except httpx.HTTPStatusError as e:
                self._handle_http_error(e)

            except httpx.RequestError as e:
                raise BasalamError(f"Request failed: {e}")

            return self._parse_response_data(response, response_model)

    def request_sync(
            self,
            method: str,
            path: str,
            params: Optional[Dict[str, Any]] = None,
            data: Optional[Dict[str, Any]] = None,
            json_data: Optional[Dict[str, Any]] = None,
            files: Optional[Dict[str, Any]] = None,
            headers: Optional[Dict[str, str]] = None,
            response_model: Optional[Type[T]] = None,
            require_auth: bool = True,
    ) -> Union[Dict[str, Any], List[Dict[str, Any]], T]:
        """
        Make a synchronous request to the API.
        """
        url = urljoin(self.base_url, path)

        # Build headers: start with config headers, add auth headers if needed, then custom headers
        request_headers = self.config.get_headers().copy()

        if require_auth:
            auth_headers = self.auth.get_auth_headers_sync()
            request_headers.update(auth_headers)

        if headers:
            request_headers.update(headers)

        with httpx.Client(
                timeout=self.config.timeout,
                follow_redirects=True,
        ) as client:
            try:
                response = client.request(
                    method=method,
                    url=url,
                    headers=request_headers,
                    params=params,
                    data=data,
                    json=json_data,
                    files=files,
                )
                response.raise_for_status()

            except httpx.HTTPStatusError as e:
                self._handle_http_error(e)

            except httpx.RequestError as e:
                raise BasalamError(f"Request failed: {e}")

            return self._parse_response_data(response, response_model)

    # HTTP method helpers
    async def _get(
            self,
            path: str,
            params: Optional[Dict[str, Any]] = None,
            headers: Optional[Dict[str, str]] = None,
            response_model: Optional[Type[T]] = None,
            require_auth: bool = True,
    ) -> Union[Dict[str, Any], List[Dict[str, Any]], T]:
        """Make a GET request."""
        return await self.request("GET", path, params=params, headers=headers, response_model=response_model,
                                  require_auth=require_auth)

    def _get_sync(
            self,
            path: str,
            params: Optional[Dict[str, Any]] = None,
            headers: Optional[Dict[str, str]] = None,
            response_model: Optional[Type[T]] = None,
            require_auth: bool = True,
    ) -> Union[Dict[str, Any], List[Dict[str, Any]], T]:
        """Make a synchronous GET request."""
        return self.request_sync("GET", path, params=params, headers=headers, response_model=response_model,
                                 require_auth=require_auth)

    async def _post(
            self,
            path: str,
            data: Optional[Dict[str, Any]] = None,
            json_data: Optional[Dict[str, Any]] = None,
            files: Optional[Dict[str, Any]] = None,
            headers: Optional[Dict[str, str]] = None,
            response_model: Optional[Type[T]] = None,
            require_auth: bool = True,
    ) -> Union[Dict[str, Any], List[Dict[str, Any]], T]:
        """Make a POST request."""
        return await self.request("POST", path, data=data, json_data=json_data, files=files, headers=headers,
                                  response_model=response_model, require_auth=require_auth)

    def _post_sync(
            self,
            path: str,
            data: Optional[Dict[str, Any]] = None,
            json_data: Optional[Dict[str, Any]] = None,
            files: Optional[Dict[str, Any]] = None,
            headers: Optional[Dict[str, str]] = None,
            response_model: Optional[Type[T]] = None,
            require_auth: bool = True,
    ) -> Union[Dict[str, Any], List[Dict[str, Any]], T]:
        """Make a synchronous POST request."""
        return self.request_sync("POST", path, data=data, json_data=json_data, files=files, headers=headers,
                                 response_model=response_model, require_auth=require_auth)

    async def _put(
            self,
            path: str,
            data: Optional[Dict[str, Any]] = None,
            json_data: Optional[Dict[str, Any]] = None,
            headers: Optional[Dict[str, str]] = None,
            response_model: Optional[Type[T]] = None,
            require_auth: bool = True,
    ) -> Union[Dict[str, Any], List[Dict[str, Any]], T]:
        """Make a PUT request."""
        return await self.request("PUT", path, data=data, json_data=json_data, headers=headers,
                                  response_model=response_model, require_auth=require_auth)

    def _put_sync(
            self,
            path: str,
            data: Optional[Dict[str, Any]] = None,
            json_data: Optional[Dict[str, Any]] = None,
            headers: Optional[Dict[str, str]] = None,
            response_model: Optional[Type[T]] = None,
            require_auth: bool = True,
    ) -> Union[Dict[str, Any], List[Dict[str, Any]], T]:
        """Make a synchronous PUT request."""
        return self.request_sync("PUT", path, data=data, json_data=json_data, headers=headers,
                                 response_model=response_model, require_auth=require_auth)

    async def _patch(
            self,
            path: str,
            data: Optional[Dict[str, Any]] = None,
            json_data: Optional[Dict[str, Any]] = None,
            headers: Optional[Dict[str, str]] = None,
            response_model: Optional[Type[T]] = None,
            require_auth: bool = True,
    ) -> Union[Dict[str, Any], List[Dict[str, Any]], T]:
        """Make a PATCH request."""
        return await self.request("PATCH", path, data=data, json_data=json_data, headers=headers,
                                  response_model=response_model, require_auth=require_auth)

    def _patch_sync(
            self,
            path: str,
            data: Optional[Dict[str, Any]] = None,
            json_data: Optional[Dict[str, Any]] = None,
            headers: Optional[Dict[str, str]] = None,
            response_model: Optional[Type[T]] = None,
            require_auth: bool = True,
    ) -> Union[Dict[str, Any], List[Dict[str, Any]], T]:
        """Make a synchronous PATCH request."""
        return self.request_sync("PATCH", path, data=data, json_data=json_data, headers=headers,
                                 response_model=response_model, require_auth=require_auth)

    async def _delete(
            self,
            path: str,
            params: Optional[Dict[str, Any]] = None,
            data: Optional[Dict[str, Any]] = None,
            json_data: Optional[Dict[str, Any]] = None,
            headers: Optional[Dict[str, str]] = None,
            response_model: Optional[Type[T]] = None,
            require_auth: bool = True,
    ) -> Union[Dict[str, Any], List[Dict[str, Any]], T]:
        """Make a DELETE request."""
        return await self.request("DELETE", path, params=params, data=data, json_data=json_data, headers=headers,
                                  response_model=response_model, require_auth=require_auth)

    def _delete_sync(
            self,
            path: str,
            params: Optional[Dict[str, Any]] = None,
            data: Optional[Dict[str, Any]] = None,
            json_data: Optional[Dict[str, Any]] = None,
            headers: Optional[Dict[str, str]] = None,
            response_model: Optional[Type[T]] = None,
            require_auth: bool = True,
    ) -> Union[Dict[str, Any], List[Dict[str, Any]], T]:
        """Make a synchronous DELETE request."""
        return self.request_sync("DELETE", path, params=params, data=data, json_data=json_data, headers=headers,
                                 response_model=response_model, require_auth=require_auth)
