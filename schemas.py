from pydantic import BaseModel, field_serializer, field_validator #datavalidation , serialization, type check
from datetime import datetime
from typing import Optional
import re

def format_datetime(value):
    if value is None:
        return None

    return value.strftime("%d %b %Y, %I:%M %p")


class BookCreate(BaseModel):
    title : str
    author : str
    category : str
    price : float
    quantity : int
    publisher : str

class BookResponse(BookCreate):
    id : int

    model_config = {
        "from_attributes" : True
    }


class UserCreate(BaseModel):
    username: str
    email: str
    password: str

    @field_validator("password")
    @classmethod
    def validate_password(cls, value):
        if len(value) < 8:
            raise ValueError("Password must be at least 8 characters long")

        if not re.search(r"[A-Za-z]", value):
            raise ValueError("Password must contain at least one letter")

        if not re.search(r"[0-9]", value):
            raise ValueError("Password must contain at least one number")

        if not re.search(r"[^A-Za-z0-9]", value):
            raise ValueError("Password must contain at least one special character")

        return value


class UserLogin(BaseModel):
    email: str
    password: str


class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    is_admin: bool

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token : str
    token_type : str

class ChangePassword(BaseModel):
    current_password: str
    new_password: str
    confirm_password: str

class BookWithAvailability(BookResponse):

    available: bool
    status: str


class BorrowBookResponse(BaseModel):

    id: int
    user_id: int
    book_id: int
    borrowed_at: datetime
    returned_at: datetime | None
    status: str

    @field_serializer("borrowed_at", "returned_at")
    def format_datetime(self, value):
        if value is None:
            return None

        return value.strftime("%d %b %Y, %I:%M %p")

    model_config = {
        "from_attributes": True
    }


class BorrowingHistoryResponse(BaseModel):

    id: int
    book_id: int
    borrowed_at: datetime
    returned_at: datetime | None
    status: str

    model_config = {
        "from_attributes": True
    }


class AdminBorrowingResponse(BaseModel):

    id: int
    user_id: int
    book_id: int
    borrowed_at: datetime
    returned_at: datetime | None
    status: str

    model_config = {
        "from_attributes": True
    }


class DashboardResponse(BaseModel):

    total_books: int
    total_users: int
    total_borrowed: int
    available_books: int

class ForgotPasswordRequest(BaseModel):
    email: str


class VerifyOTPRequest(BaseModel):
    email: str
    otp: str


class ResetPasswordRequest(BaseModel):
    email: str
    otp: str
    new_password: str
    confirm_password: str

    @field_validator("new_password")
    @classmethod
    def validate_password(cls, value):
        if len(value) < 8:
            raise ValueError(
                "Password must be at least 8 characters long"
            )

        if not re.search(r"[A-Za-z]", value):
            raise ValueError(
                "Password must contain at least one letter"
            )

        if not re.search(r"[0-9]", value):
            raise ValueError(
                "Password must contain at least one number"
            )

        if not re.search(r"[^A-Za-z0-9]", value):
            raise ValueError(
                "Password must contain at least one special character"
            )

        return value

class PaginatedBooksResponse(BaseModel):
    books: list[BookResponse]
    page: int
    limit: int
    total_books: int
    total_pages: int
    has_next: bool
    has_previous: bool


class CategoryResponse(BaseModel):
    category: str
    book_count: int