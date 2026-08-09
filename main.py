from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
import crud, schemas, models, auth
from database import Base, engine, SessionLocal
from database import get_db
from fastapi.security import OAuth2PasswordRequestForm
from fastapi import Response
import bcrypt

Base.metadata.create_all(bind=engine)

app=FastAPI()

# Welcome Message
@app.get("/")
def welcome():
    return {"message" : "Welocome to Library Management System"}

# Create or post Books
@app.post("/books", response_model=schemas.BookResponse)
def create_book(
    book: schemas.BookCreate,
    db: Session = Depends(get_db),
    current_admin = Depends(auth.get_current_admin_from_cookie)
):
    return crud.create_book(db, book)

# Get All Books
@app.get("/books", response_model=list[schemas.BookResponse])
def all_books(
    db: Session = Depends(get_db),
    current_admin = Depends(auth.get_current_admin_from_cookie)
):
    return crud.get_all_books(db)

# Get books by title
@app.get("/books/title/{title_name}", response_model = list[schemas.BookResponse])
def books_by_title(
    title_name: str,
    db: Session = Depends(get_db),
    current_user = Depends(auth.get_current_user_from_cookie)
):

    books = crud.get_books_by_title(db, title_name)
    if not books:
        raise HTTPException(
            status_code = 404,
            detail = "No Books Found with this Title"
        )
    
    return books
    

# Get Books by Category
@app.get("/books/category/{category_name}", response_model=list[schemas.BookResponse])
def books_by_category(
    category_name: str,
    db: Session = Depends(get_db),
    current_user = Depends(auth.get_current_user_from_cookie)
):
    books = crud.get_books_by_category(db, category_name)

    if not books:
        raise HTTPException(
            status_code = 404,
            detail = "No Books Found with this Category"
        )

    return books

#Get books by Author
@app.get("/books/author/{author_name}", response_model=list[schemas.BookResponse])
def books_by_author(
    author_name: str,
    db: Session = Depends(get_db),
    current_user = Depends(auth.get_current_user_from_cookie)
):
    books = crud.get_books_by_author(db, author_name)

    if not books:
        raise HTTPException(
            status_code = 404,
            detail = "No Books Found by This Author"
        )
    
    return books

#Get book by Publisher
@app.get("/books/publisher/{publisher_name}", response_model=list[schemas.BookResponse])
def book_by_publisher(
    publisher_name: str,
    db: Session = Depends(get_db),
    current_user = Depends(auth.get_current_user_from_cookie)
):
    books = crud.get_books_by_publisher(db, publisher_name)

    if not books :
        raise HTTPException(
            status_code = 404,
            detail = "No Books Found by this Publisher"
        )
    return books

# Get books by price
@app.get("/books/price/{price_val}", response_model=list[schemas.BookResponse])
def get_by_price(
    price_val: float,
    db: Session = Depends(get_db),
    current_user = Depends(auth.get_current_user_from_cookie)
):
    books = crud.get_books_by_price(db, price_val)
    if not books :
        raise HTTPException(
            status_code = 404,
            detail = "No Books Found in this Price"
        )
    return books   

# Get books by Quantity
@app.get("/books/quantity/{quantity_val}", response_model=list[schemas.BookResponse])
def get_by_quantity(
    quantity_val: int,
    db: Session = Depends(get_db),
    current_user = Depends(auth.get_current_user_from_cookie)
):
    books = crud.get_books_by_quantity(db, quantity_val)
    if not books :
        raise HTTPException(
            status_code = 404,
            detail = "No Books Found in this Quantity"
        )
    return books

# Get books by price range
@app.get("/books/price-range", response_model=list[schemas.BookResponse])
def get_by_price_range(
    min_price: float,
    max_price: float,
    db: Session = Depends(get_db),
    current_user = Depends(auth.get_current_user_from_cookie)
):
    books = crud.get_books_by_price_range(db, min_price, max_price)
    if not books :
            raise HTTPException(
                status_code = 404,
                detail = "No Books Found in this price range"
            )
    return books
    
#Get One Book by ID
@app.get("/books/{book_id}", response_model=schemas.BookResponse)
def read_one(
    book_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(auth.get_current_user_from_cookie)
):

    book = crud.get_book(db, book_id)

    if not book:
        raise HTTPException(
            status_code = 404,
            detail = "Book Not Found"
        )
    return book

#update Book
@app.put("/books/{book_id}", response_model=schemas.BookResponse)
def update(
    book_id: int,
    book: schemas.BookCreate,
    db: Session = Depends(get_db),
    current_admin = Depends(auth.get_current_admin_from_cookie)
):

    updated_book = crud.update_book(db, book_id, book)

    if not updated_book:
        raise HTTPException(
            status_code=404,
            detail="Book Not Found"
        )

    return updated_book


# Delete Book
@app.delete("/books/{book_id}")
def delete(
    book_id: int,
    db: Session = Depends(get_db),
    current_admin = Depends(auth.get_current_admin_from_cookie)
):


    deleted_book = crud.delete_book(db, book_id)

    if not deleted_book:
        raise HTTPException(
            status_code=404,
            detail="Book Not Found"
        )

    return {
        "message": "Book Deleted Successfully"
    }

# Registering The user 
@app.post("/register", response_model = schemas.UserResponse)
def register_user(
    user: schemas.UserCreate,
    db: Session = Depends(get_db)
):

    existing_user = db.query(models.User).filter(
        models.User.email == user.email
    ).first()

    if existing_user:
        raise HTTPException(
            status_code=400,
            detail = "Email already registered"
        )

    return crud.create_user(user, db)

# Login User or Admin
@app.post("/login", response_model = schemas.Token)
def login_user(
    user: schemas.UserLogin,
    response : Response,
    db: Session = Depends(get_db)
):

    user_exist = crud.validate_user(user, db)

    if not user_exist:
        raise HTTPException(
            status_code = 401,
            detail = "Invalid email or password"
        )

    access_token = auth.create_access_token({
        "user_id" : user_exist.id
    })

    response.set_cookie(
        key = "access_token",
        value = access_token,
        httponly = True,
        max_age = 1800,
        secure = False,
        samesite = "lax"
    )

    return{
        "access_token" : access_token,
        "token_type" : "bearer"
    }


# Get Current Logged-in User
@app.get("/me", response_model=schemas.UserResponse)
def get_me(
    current_user = Depends(auth.get_current_user_from_cookie)
):
    return current_user


# Testing Authorization
@app.get("/test-auth")
def test_auth(
    current_user = Depends(auth.get_current_user)
):

    return {
        "message": "Authentication successful",
        "user_id": current_user.id,
        "username": current_user.username,
        "email": current_user.email
    }

# Testing Admin Authorization
@app.get("/test-admin")
def test_admin(
    current_admin = Depends(auth.get_current_admin)
):

    return {
        "message": "Admin authentication successful",
        "user_id": current_admin.id,
        "username": current_admin.username,
        "is_admin": current_admin.is_admin
    }

# Testing Cookie
@app.get("/test-cookie")
def test_cookie(
    current_user = Depends(auth.get_current_user_from_cookie)
):

    return {
        "message": "Cookie authentication successful",
        "user_id": current_user.id,
        "username": current_user.username,
        "email": current_user.email
    }

# Testing Admin Cookie
@app.get("/test-cookie-admin")
def test_cookie_admin(
    current_admin = Depends(auth.get_current_admin_from_cookie)
):

    return {
        "message": "Cookie admin authentication successful",
        "user_id": current_admin.id,
        "username": current_admin.username,
        "is_admin": current_admin.is_admin
    }

# For Logout
@app.post("/logout")
def logout(response: Response):

    response.delete_cookie(
        key="access_token"
    )

    return {
        "message": "Logout successful"
    }



# Change Password
@app.post("/change-password")
def change_password(
    password_data: schemas.ChangePassword,
    db: Session = Depends(get_db),
    current_user = Depends(auth.get_current_user_from_cookie)
):

    # Check current password
    password_correct = bcrypt.checkpw(
        password_data.current_password.encode(),
        current_user.hashed_password.encode()
    )

    if not password_correct:
        raise HTTPException(
            status_code=401,
            detail="Current password is incorrect"
        )

    # Check new password confirmation
    if password_data.new_password != password_data.confirm_password:
        raise HTTPException(
            status_code=400,
            detail="New passwords do not match"
        )

    # Don't allow same password
    if password_data.current_password == password_data.new_password:
        raise HTTPException(
            status_code=400,
            detail="New password must be different from current password"
        )

    # Change password
    crud.change_password(
        db,
        current_user,
        password_data.new_password
    )

    return {
        "message": "Password changed successfully"
    }

