from fastapi.security.api_key import APIKeyQuery
from fastapi import HTTPException, Security

from src.settings.config import api_key, DEBUG

api_key_header = APIKeyQuery(name='access_token', auto_error=False)


async def get_api_key(api_key_header_value: str = Security(api_key_header)):
    if not DEBUG:
        if api_key_header_value == api_key:
            return api_key_header_value
        raise HTTPException(
            status_code=401,
            detail="Invalid or missing API Key",
        )
    return api_key_header_value
