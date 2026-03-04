from fastapi import FastAPI, HTTPException, Request, Query, Depends, Response
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

from typing import Optional
from bson import ObjectId
from pymongo.errors import PyMongoError

from jose import JWTError, jwt
from passlib.context import CryptContext
from datetime import datetime, timedelta

from database import connect_to_mongo, close_mongo_connection, get_database
from models import Author, Book, BookUpdate

import copy

from pydantic import BaseModel

class UserCreate(BaseModel):
    username: str
    password: str
    role: str = "user"

app = FastAPI()

@app.on_event("startup")
async def startup():
    await connect_to_mongo()

    db = get_database()

    await db["users"].create_index("username", unique=True)

    await db["books"].create_index("author_id")

    await db["books"].create_index([("published_year", -1)])

    await db["books"].create_index(
        [("author_id", 1), ("published_year", -1)]
    )

@app.on_event("shutdown")
async def shutdown():
    await close_mongo_connection()


# ================= JWT CONFIG =================

SECRET_KEY = "super_secret_key_change_this_in_production"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")
# ================= PASSWORD & TOKEN HELPERS =================

def hash_password(password: str):
    return pwd_context.hash(password)


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()

    expire = datetime.utcnow() + (
        expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )

    to_encode.update({"exp": expire})

    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

@app.post("/register")
async def register(user: UserCreate):
    db = get_database()

    existing_user = await db["users"].find_one({"username": user.username})
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already exists")

    hashed_password = hash_password(user.password)

    await db["users"].insert_one({
        "username": user.username,
        "hashed_password": hashed_password,
        "role": user.role
    })

    return {"message": "User registered successfully"}


from fastapi import Form

@app.post("/login")
async def login(
    username: str = Form(...),
    password: str = Form(...),
    grant_type: str = Form(None)
):
    db = get_database()

    user = await db["users"].find_one({"username": username})

    if not user or not verify_password(password, user["hashed_password"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    access_token = create_access_token(
        data={"sub": user["username"]}
    )

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }


from fastapi import FastAPI
from database import connect_to_mongo, close_mongo_connection

from routers import authors, books, users, loans

app = FastAPI(title="Library Management System")

# Include routers
app.include_router(authors.router)
app.include_router(books.router)
app.include_router(users.router)
app.include_router(loans.router)


@app.on_event("startup")
async def startup():
    await connect_to_mongo()


@app.on_event("shutdown")
async def shutdown():
    await close_mongo_connection()


@app.get("/", tags=["System"])
async def root(token: str = Depends(oauth2_scheme)):
    return {"message": "Library Management System API"}
