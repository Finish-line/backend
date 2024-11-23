from fastapi import HTTPException, status
import jwt

from magic_admin import Magic
from magic_admin.error import MagicException

from sqlmodel import Session, select

from src import models
from src.auth.config import MAGIC_SECRET_KEY


magic = Magic(api_secret_key=MAGIC_SECRET_KEY)

def verify_magic_token(token: str):
    try:
        magic.user.validate_token(token)

        user_metadata = magic.user.get_metadata_by_token(token)

        return user_metadata
    except MagicException as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Authentication failed: {str(e)}"
        )
    except Exception as e:
        # Handle other errors
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"An error occurred: {str(e)}"
        )