from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException
from datetime import datetime, timedelta
from jose import JWTError, jwt

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="users/login")

SECRET_KEY = "your_secret_key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60


def create_access_token(data: dict):
    to_encode = data.copy()

    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt


def verify_token(token: str):

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        username: str = payload.get("sub")

        if username is None:
            return None

        return username

    except JWTError:
        return None


async def get_current_user(token: str = Depends(oauth2_scheme)):

    username = verify_token(token)

    if username is None:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

    return {"username": username}
