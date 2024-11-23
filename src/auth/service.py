from fastapi import HTTPException, status

from magic_admin import Magic
from magic_admin.error import MagicError

from src.config import MAGIC_SECRET_KEY


magic = Magic(api_secret_key=MAGIC_SECRET_KEY)

def verify_magic_token(token: str):
    try:
        magic.Token.validate(token)

        user_metadata = magic.user.get_metadata_by_token(token)

        return user_metadata
    except MagicError as e:
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