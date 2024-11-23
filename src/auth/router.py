from typing import Annotated
import fastapi
from fastapi.security import OAuth2PasswordBearer

from src.auth.utils import Token

router = fastapi.APIRouter(prefix="/api/auth")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/api/auth/verify')

emails = {
    'driver':'Contact@henrikzabel.com',
    'costumer':'moritzluca.huber@tum.de'
}

@router.get("/verify")
def verify_token(
    role:str
):
    user_email = emails[role]
    token = Token.generate(user_email)

    return {"access_token": token.encoded, "token_type": "bearer"}
