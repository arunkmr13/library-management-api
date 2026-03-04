from pydantic import BaseModel, field_validator
from typing import Optional


class BookUpdate(BaseModel):
    title: Optional[str] = None
    author: Optional[str] = None
    published_year: Optional[int] = None
    isbn: Optional[str] = None
    pages: Optional[int] = None

    @field_validator("published_year")
    @classmethod
    def validate_year(cls, value):
        if value is None:
            return value
        current_year = datetime.now().year
        if value < 1450 or value > current_year:
            raise ValueError(
                f"published_year must be between 1450 and {current_year}"
            )
        return value

    @field_validator("pages")
    @classmethod
    def validate_pages(cls, value):
        if value is not None and value <= 0:
            raise ValueError("pages must be a positive integer")
        return value

    @field_validator("isbn")
    @classmethod
    def validate_isbn(cls, value):
        if value is None:
            return value
        isbn_pattern = r"^(?:\d{9}[\dXx]|\d{13})$"
        if not re.match(isbn_pattern, value):
            raise ValueError("isbn must be valid ISBN-10 or ISBN-13 format")
        return value



from typing import Optional
from pydantic import BaseModel, field_validator
from datetime import datetime
import re


class Book(BaseModel):
    title: str
    published_year: int
    author_id: str   # receive as string
    isbn: Optional[str] = None
    pages: Optional[int] = None


    # Validate published year
    @field_validator("published_year")
    @classmethod
    def validate_year(cls, value):
        current_year = datetime.now().year
        if value < 1450 or value > current_year:
            raise ValueError(
                f"published_year must be between 1450 and {current_year}"
            )
        return value

    # Validate pages
    @field_validator("pages")
    @classmethod
    def validate_pages(cls, value):
        if value is not None and value <= 0:
            raise ValueError("pages must be a positive integer")
        return value

    # Validate ISBN
    @field_validator("isbn")
    @classmethod
    def validate_isbn(cls, value):
        if value is None:
            return value

        isbn_pattern = r"^(?:\d{9}[\dXx]|\d{13})$"

        if not re.match(isbn_pattern, value):
            raise ValueError("isbn must be valid ISBN-10 or ISBN-13 format")

        return value


from typing import Optional
from pydantic import BaseModel, field_validator
from datetime import datetime
import re


class Author(BaseModel):
    name: str
    birth_year: Optional[int] = None

    @field_validator("birth_year")
    @classmethod
    def validate_birth_year(cls, value):
        if value is None:
            return value
        current_year = datetime.now().year
        if value > current_year:
            raise ValueError("birth_year cannot be in the future")
        return value


