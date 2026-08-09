from pydantic import BaseModel, field_serializer #datavalidation , serialization, type check
from datetime import datetime
from typing import Optional


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

