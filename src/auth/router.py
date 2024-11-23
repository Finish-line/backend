from typing import Annotated
import fastapi
from fastapi import HTTPException, Depends, status
from fastapi.security import OAuth2PasswordBearer

from src.auth.service import verify_magic_token
from src.auth.utils import Token

router = fastapi.APIRouter(prefix="/api/auth")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/api/auth/verify')


@router.get("/verify")
def verify_token(token: Annotated[str, Depends(oauth2_scheme)]):
    """ Verify Token issued by magic """
    if token is None:
        raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="No Token was set"
            )

    user_info = verify_magic_token(token)
    user_email = user_info.get('email')

    token = Token.generate(user_email)

    return {"access_token": token.encoded, "token_type": "bearer"}
