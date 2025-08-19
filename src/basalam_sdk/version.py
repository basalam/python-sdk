"""
Version information for the Basalam SDK.

This module centralizes version management and User-Agent generation.
"""

__version__ = "1.0.2"
__sdk_name__ = "basalam-python-sdk"


def get_user_agent(custom_agent: str = None) -> str:
    """
    Get the User-Agent string for the SDK.

    Args:
        custom_agent: Optional custom User-Agent to append to SDK User-Agent.

    Returns:
        Complete User-Agent string.
    """
    sdk_agent = f"{__sdk_name__}/{__version__}"

    if custom_agent:
        return f"{sdk_agent} {custom_agent}".strip()

    return sdk_agent
