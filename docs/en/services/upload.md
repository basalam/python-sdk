# Upload Service

This service provides secure file upload capabilities: securely upload files, support for various file types (images,
documents, videos), assign custom file names and expiration times, and receive file URLs for access.

## Table of Contents

- [Upload Methods](#upload-methods)
- [Examples](#examples)

## Upload Methods

| Method                          | Description   | Parameters                                                  |
|---------------------------------|---------------|-------------------------------------------------------------|
| [`upload_file()`](#upload-file) | Upload a file | `file`, `file_type`, `custom_unique_name`, `expire_minutes` |

### Parameters

- `file` - File object (`file handle`, `BytesIO`, etc.)
- `file_type` - Type of file (from `UserUploadFileTypeEnum`). Supported file types:
    - Product: `product.photo`, `product.video`
    - User: `user.avatar`, `user.cover`
    - Vendor: `vendor.logo`, `vendor.cover`
    - Chat: `chat.photo`, `chat.video`, `chat.voice`, `chat.file`
- `custom_unique_name` – Optional custom name for the file
- `expire_minutes` – Optional expiration time in minutes

## Examples

### Initial Configuration

```python
from basalam_sdk import BasalamClient, PersonalToken

auth = PersonalToken(
    token="your_access_token",
    refresh_token="your_refresh_token"
)
client = BasalamClient(auth=auth)
```

### Upload File

```python
from basalam_sdk.upload.models import UserUploadFileTypeEnum

async def upload_file_example():
  with open("image.png", "rb") as file:
      response = await client.upload_file(
          file=file,
          file_type=UserUploadFileTypeEnum.PRODUCT_PHOTO
      )
      return response
```

#### Sample Response

The upload response is handled by the `FileResponse` model:

```python
FileResponse(
  id=238300331,
  file_name='image.png',
  file_name_alone='image',
  path='users/b28/07-13',
  format='png',
  type='image',
  file_type=5901,
  width=228,
  height=154,
  size=58007,
  duration=0,
  urls={'primary': '...'},
  created_at='2025-07-13 14:07:47',
  creator_user_id=430,
  mime_type=None,
  url=None
)
```

To see the list of valid upload formats, refer to [this document](http://localhost:8080/services/upload#فرمتهای-مجاز).
