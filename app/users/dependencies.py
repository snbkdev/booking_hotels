from fastapi import Request, Depends
from jose import jwt, JWTError
from ..config import settings
from datetime import datetime
from app.users.repository import UsersDAO
from ..exceptions import ExpiredTokenException, TokenAbsentException, IncorrectTokenFormatException, UserNotFoundException


def get_token(request: Request):
    token = request.cookies.get("booking_access_token")
    if not token:
        raise TokenAbsentException
    return token


async def get_current_user(token:str = Depends(get_token)):
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, settings.ALGORITHM)
    except JWTError:
        raise IncorrectTokenFormatException
    
    expire: str = payload.get("exp")
    if (not expire) or (int(expire) < datetime.utcnow().timestamp()):
        raise ExpiredTokenException
    
    user_id: str = payload.get("sub")
    if not user_id:
        raise UserNotFoundException
    
    user = await UsersDAO.find_by_id(int(user_id))
    if not user:
        raise UserNotFoundException
    
    return user