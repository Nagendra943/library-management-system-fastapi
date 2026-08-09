from pydantic import BaseModel  #datavalidation , serialization, type check

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
