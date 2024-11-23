"""
    Contains logic for injecting into route handles
    Here: Contains authentication checks for restricted access
"""
from typing import Annotated
from fastapi import Depends, HTTPException, status

from fastapi.security import OAuth2PasswordBearer

from src.auth import utils

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='verify')


def requires_auth(encoded_token: Annotated[str, Depends(oauth2_scheme)]):
    if encoded_token is None:
        # no cookie was set
        raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="No Token was set"
            )

    # validate token
    token = utils.Token.from_encoded(encoded_token)

    if not token.is_valid():
        raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid Token"
            )
    return token


TokenDependency = Annotated[utils.Token, Depends(requires_auth)]