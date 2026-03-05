from pydantic import BaseModel
from typing import Optional


# ---------------- AUTHORS ----------------

class AuthorCreate(BaseModel):
    name: str
    bio: Optional[str] = None


class AuthorResponse(BaseModel):
    id: str
    name: str
    bio: Optional[str] = None


# ---------------- BOOKS ----------------

class BookCreate(BaseModel):
    title: str
    author_id: str
    published_year: Optional[int] = None
    pages: Optional[int] = None


class BookUpdate(BaseModel):
    title: Optional[str] = None
    author_id: Optional[str] = None
    published_year: Optional[int] = None
    pages: Optional[int] = None

class BookUpdate(BaseModel):
    title: Optional[str]
    author_id: Optional[str]
    available: Optional[bool]


# ---------------- USERS ----------------

class UserRegister(BaseModel):
    username: str
    password: str
    role: Optional[str] = "user"


class UserLogin(BaseModel):
    username: str
    password: str


# ---------------- LOANS ----------------

class LoanCreate(BaseModel):
    book_id: str
    user_id: str


