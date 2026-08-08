from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
import crud, schemas, models
from database import Base, engine, SessionLocal

Base.metadata.create_all(bind=engine)

app=FastAPI()

def get_db():            #to start the db session fro every thing
    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()

# Welcome Route`
@app.get("/")
def welcome():
    return {"message" : "Welocome to Library Management System"}

# Create Book
@app.post("/books", response_model = schemas.BookResponse)
def create(book : schemas.BookCreate, db : Session = Depends(get_db)):
    return crud.create_book(db, book)

# Get All Books
@app.get("/books", response_model = list[schemas.BookResponse])
def all_books(db : Session = Depends(get_db)):
    return crud.get_all_books(db)


    return book

# Get Books by Category
@app.get("/books/category/{category_name}", response_model=list[schemas.BookResponse])
def books_by_category(category_name : str, db: Session = Depends(get_db)):
    books = crud.get_books_by_category(db, category_name)

    if not books:
        raise HTTPException(
            status_code = 404,
            detail = "No Books Found in this Category"
        )

    return books

#Get books by Author
@app.get("/books/author/{author_name}", response_model=list[schemas.BookResponse])
def books_by_author(author_name : str, db : Session = Depends(get_db)):
    books = crud.get_books_by_author(db, author_name)

    if not books:
        raise HTTPException(
            status_code = 404,
            detail = "No Books Found by This Author"
        )
    
    return books

#Get book by Publisher
@app.get("/books/publisher/{publisher_name}", response_model=list[schemas.BookResponse])
def book_by_publisher(publisher_name : str, db : Session = Depends(get_db)):
    books = crud.get_books_by_publisher(db, publisher_name)

    if not books :
        raise HTTPException(
            status_code = 404,
            detail = "No Books Found by this Publisher"
        )
    return books

@app.get("/books/price/{price_val}", response_model=list[schemas.BookResponse])
def get_by_price(price_val : float, db : Session = Depends(get_db)):
    books = crud.get_books_by_price(db, price_val)
    if not books :
        raise HTTPException(
            status_code = 404,
            detail = "No Books Found in this Price"
        )
    return books   

@app.get("/books/quantity/{quantity_val}", response_model=list[schemas.BookResponse])
def get_by_quantity(quantity_val : int, db : Session = Depends(get_db)):
    books = crud.get_books_by_quantity(db, quantity_val)
    if not books :
        raise HTTPException(
            status_code = 404,
            detail = "No Books Found in this Quantity"
        )
    return books

#by price range
@app.get("/books/price-range", response_model = list[schemas.BookResponse])
def get_by_price_range(min_price : float, max_price : float , db : Session = Depends(get_db)):
    books = crud.get_books_by_price_range(db, min_price, max_price)
    if not books :
            raise HTTPException(
                status_code = 404,
                detail = "No Books Found in this price range"
            )
    return books
    
#Get One Book by ID
@app.get("/books/{book_id}", response_model = schemas.BookResponse)
def read_one(book_id : int, db : Session = Depends(get_db)):

    book = crud.get_book(db, book_id)

    if not book:
        raise HTTPException(
            status_code = 404,
            detail = "Book Not Found"
        )
    return book

#update Book
@app.put("/books/{book_id}", response_model=schemas.BookResponse)
def update(book_id: int,
           book: schemas.BookCreate,
           db: Session = Depends(get_db)):

    updated_book = crud.update_book(db, book_id, book)

    if not updated_book:
        raise HTTPException(
            status_code=404,
            detail="Book Not Found"
        )

    return updated_book

# Delete Book
@app.delete("/books/{book_id}")
def delete(book_id: int, db: Session = Depends(get_db)):

    deleted_book = crud.delete_book(db, book_id)

    if not deleted_book:
        raise HTTPException(
            status_code=404,
            detail="Book Not Found"
        )

    return {
        "message": "Book Deleted Successfully"
    }

