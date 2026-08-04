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