"""
Error classes for the Basalam SDK.
"""
from typing import Any, Dict, Optional


class BasalamError(Exception):
    """Base exception for all Basalam SDK errors."""

    def __init__(self, message: str):
        """Initialize the exception with a message."""
        self.message = message
        super().__init__(self.message)


class BasalamAPIError(BasalamError):
    """Exception raised when an API request fails."""

    def __init__(
            self,
            message: str,
            status_code: int,
            code: Optional[str] = None,
            response: Optional[Any] = None,
    ):
        """
        Initialize the API error.
        """
        self.status_code = status_code
        self.code = code
        self.response = response
        super().__init__(f"API error {status_code}: {message}")


class BasalamAuthError(BasalamAPIError):
    """Exception raised for authentication errors."""

    def __init__(
            self,
            message: str,
            response: Optional[Any] = None,
    ):
        """
        Initialize the authentication error.
        """
        super().__init__(message=message, status_code=401, response=response)


class BasalamValidationError(BasalamError):
    """Exception raised for data validation errors."""

    def __init__(
            self,
            message: str,
            errors: Optional[Dict[str, Any]] = None,
    ):
        """
        Initialize the validation error.
        """
        self.errors = errors or {}
        super().__init__(message)
