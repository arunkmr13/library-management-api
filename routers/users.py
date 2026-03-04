from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm
from fastapi import APIRouter, HTTPException
from database import get_database
from schemas import UserRegister, UserLogin
from auth import create_access_token
from passlib.context import CryptContext

router = APIRouter(tags=["Users"])

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str):
    return pwd_context.hash(password)


def verify_password(plain, hashed):
    return pwd_context.verify(plain, hashed)


@router.post("/register")
async def register(user: UserRegister):

    db = get_database()

    existing_user = await db["users"].find_one({"username": user.username})

    if existing_user:
        raise HTTPException(status_code=400, detail="Username already exists")

    hashed_password = hash_password(user.password)

    new_user = {
        "username": user.username,
        "password": hashed_password,
        "role": user.role
    }

    result = await db["users"].insert_one(new_user)

    return {"message": "User registered", "id": str(result.inserted_id)}


@router.post("/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):

    db = get_database()

    db_user = await db["users"].find_one({"username": form_data.username})

    if not db_user:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    if not verify_password(form_data.password, db_user["password"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token({"sub": form_data.username})

    return {
        "access_token": token,
        "token_type": "bearer"
    }
