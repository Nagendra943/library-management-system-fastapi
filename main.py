from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
import crud, schemas, models, auth, otp
from database import Base, engine, SessionLocal
from database import get_db
from fastapi.security import OAuth2PasswordRequestForm
from fastapi import Response
import bcrypt
from fastapi import Query
from fastapi.middleware.cors import CORSMiddleware

import secrets
import smtplib
from email.message import EmailMessage
from datetime import datetime, timedelta
import os


Base.metadata.create_all(bind=engine)

app=FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def send_otp_email(email: str, otp: str):

    smtp_email = os.getenv("SMTP_EMAIL")
    smtp_password = os.getenv("SMTP_PASSWORD")

    message = EmailMessage()

    message["Subject"] = "Library Management System - Password Reset OTP"
    message["From"] = smtp_email
    message["To"] = email

    message.set_content(
        f"""
Hello,

We received a request to reset your Library Management System password.

Your OTP is:

{otp}

This OTP will expire in 5 minutes.

If you did not request a password reset, please ignore this email.

Regards,
Library Management System
"""
    )

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login(smtp_email, smtp_password)
        smtp.send_message(message)

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
    current_user = Depends(auth.get_current_user_from_cookie)
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


# Global Search
@app.get(
    "/books/search",
    response_model=list[schemas.BookResponse]
)
def search_books(
    q: str,
    db: Session = Depends(get_db),
    current_user = Depends(auth.get_current_user_from_cookie)
):

    books = crud.search_books(db, q)

    if not books:
        raise HTTPException(
            status_code=404,
            detail="No books found"
        )

    return books


@app.get(
    "/books/categories",
    response_model=schemas.PaginatedCategoriesResponse
)
def get_categories(
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
    search: str | None = None,
    db: Session = Depends(get_db),
    current_user = Depends(
        auth.get_current_user_from_cookie
    )
):

    return crud.get_paginated_categories(
        db=db,
        page=page,
        limit=limit,
        search=search
    )

@app.get(
    "/books/browse",
    response_model=schemas.PaginatedBooksResponse
)
def browse_books(
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
    category: str | None = None,
    search: str | None = None,
    db: Session = Depends(get_db),
    current_user = Depends(
        auth.get_current_user_from_cookie
    )
):

    return crud.get_paginated_books(
        db=db,
        page=page,
        limit=limit,
        category=category,
        search=search
    )


#Get One Book by ID
@app.get(
    "/books/{book_id}",
    response_model=schemas.BookWithAvailability
)
def read_one(
    book_id: int,
    db: Session = Depends(get_db)
):

    book = crud.get_book(db, book_id)

    if not book:
        raise HTTPException(
            status_code=404,
            detail="Book Not Found"
        )

    return {
        "id": book.id,
        "title": book.title,
        "author": book.author,
        "category": book.category,
        "price": book.price,
        "quantity": book.quantity,
        "publisher": book.publisher,
        "available": book.quantity > 0,
        "status": (
            "Available"
            if book.quantity > 0
            else "Out of Stock"
        )
    }


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
        secure = True,
        samesite = "none"
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

# For Logout
@app.post("/logout")
def logout(response: Response):

    response.delete_cookie(
        key="access_token",
        httponly=True,
        secure=True,
        samesite="none"
    )

    return {
        "message": "Logout successful"
    }

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


# borrow Book
@app.post(
    "/books/{book_id}/borrow",
    response_model=schemas.BorrowBookResponse
)
def borrow_book(
    book_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(
        auth.get_current_user_from_cookie
    )
):

    result = crud.borrow_book(
        db,
        current_user.id,
        book_id
    )

    if result == "BOOK_NOT_FOUND":
        raise HTTPException(
            status_code=404,
            detail="Book Not Found"
        )

    if result == "OUT_OF_STOCK":
        raise HTTPException(
            status_code=400,
            detail="Book is out of stock"
        )

    if result == "ALREADY_BORROWED":
        raise HTTPException(
            status_code=400,
            detail="You already borrowed this book"
        )

    return result


# Return Book
@app.post(
    "/books/{book_id}/return",
    response_model=schemas.BorrowBookResponse
)
def return_book(
    book_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(
        auth.get_current_user_from_cookie
    )
):

    borrowing = crud.return_book(
        db,
        current_user.id,
        book_id
    )

    if not borrowing:
        raise HTTPException(
            status_code=404,
            detail="No active borrowing found"
        )

    return borrowing

# Borrowing History
@app.get(
    "/my-borrowings",
    response_model=list[schemas.BorrowingHistoryResponse]
)
def my_borrowings(
    db: Session = Depends(get_db),
    current_user = Depends(
        auth.get_current_user_from_cookie
    )
):

    return crud.get_my_borrowings(
        db,
        current_user.id
    )


# Admin borrowing Management
@app.get(
    "/admin/borrowings",
    response_model=list[schemas.AdminBorrowingResponse]
)
def admin_borrowings(
    db: Session = Depends(get_db),
    current_admin = Depends(
        auth.get_current_admin_from_cookie
    )
):

    return crud.get_all_borrowings(db)


#Admin Dashboard
@app.get(
    "/admin/dashboard",
    response_model=schemas.DashboardResponse
)
def admin_dashboard(
    db: Session = Depends(get_db),
    current_admin = Depends(
        auth.get_current_admin_from_cookie
    )
):

    return crud.get_dashboard_stats(db)


# Admin view all users
@app.get(
    "/admin/users",
    response_model=list[schemas.UserResponse]
)
def admin_users(
    db: Session = Depends(get_db),
    current_admin = Depends(
        auth.get_current_admin_from_cookie
    )
):

    return crud.get_all_users(db)


#Admin make user admin
@app.put(
    "/admin/users/{user_id}/make-admin",
    response_model=schemas.UserResponse
)
def make_admin(
    user_id: int,
    db: Session = Depends(get_db),
    current_admin = Depends(
        auth.get_current_admin_from_cookie
    )
):

    user = crud.make_user_admin(
        db,
        user_id
    )

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User Not Found"
        )

    return user


# Admin Remove Admin
@app.put(
    "/admin/users/{user_id}/remove-admin",
    response_model=schemas.UserResponse
)
def remove_admin(
    user_id: int,
    db: Session = Depends(get_db),
    current_admin = Depends(
        auth.get_current_admin_from_cookie
    )
):

    if user_id == current_admin.id:
        raise HTTPException(
            status_code=400,
            detail="You cannot remove your own admin access"
        )

    user = crud.remove_user_admin(
        db,
        user_id
    )

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User Not Found"
        )

    return user



# Forgot Password - Send OTP

@app.post("/forgot-password")
def forgot_password(
    data: schemas.ForgotPasswordRequest,
    db: Session = Depends(get_db)
):

    # Check whether user exists
    user = db.query(models.User).filter(
        models.User.email == data.email
    ).first()

    if not user:
        raise HTTPException(
            status_code=404,
            detail="No account found with this email"
        )

    # Generate 6-digit OTP
    generated_otp = otp.generate_otp()

    # Hash OTP before storing it
    otp_hash = bcrypt.hashpw(
        generated_otp.encode(),
        bcrypt.gensalt()
    ).decode()

    # OTP expires after 5 minutes
    expires_at = datetime.utcnow() + timedelta(minutes=5)

    # Save OTP in database
    reset_otp = models.PasswordResetOTP(
        email=data.email,
        otp_hash=otp_hash,
        expires_at=expires_at,
        used=False
    )

    db.add(reset_otp)
    db.commit()

    # Send OTP to email
    otp.send_otp_email(
        data.email,
        generated_otp
    )

    return {
        "message": "OTP sent successfully"
    }


@app.post("/verify-otp")
def verify_otp(
    data: schemas.VerifyOTPRequest,
    db: Session = Depends(get_db)
):

    reset_otp = db.query(
        models.PasswordResetOTP
    ).filter(
        models.PasswordResetOTP.email == data.email,
        models.PasswordResetOTP.used == False
    ).order_by(
        models.PasswordResetOTP.created_at.desc()
    ).first()

    if not reset_otp:
        raise HTTPException(
            status_code=400,
            detail="OTP not found or expired"
        )

    if datetime.utcnow() > reset_otp.expires_at:
        raise HTTPException(
            status_code=400,
            detail="OTP has expired"
        )

    otp_correct = bcrypt.checkpw(
        data.otp.encode(),
        reset_otp.otp_hash.encode()
    )

    if not otp_correct:
        raise HTTPException(
            status_code=400,
            detail="Invalid OTP"
        )

    return {
        "message": "OTP verified successfully"
    }

# Reset Password
@app.post("/reset-password")
def reset_password(
    request: schemas.ResetPasswordRequest,
    db: Session = Depends(get_db)
):

    # Check password confirmation
    if request.new_password != request.confirm_password:
        raise HTTPException(
            status_code=400,
            detail="New passwords do not match"
        )

    # Find user
    user = db.query(models.User).filter(
        models.User.email == request.email
    ).first()

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    # Find latest unused OTP
    reset_otp = db.query(
        models.PasswordResetOTP
    ).filter(
        models.PasswordResetOTP.email == request.email,
        models.PasswordResetOTP.used == False
    ).order_by(
        models.PasswordResetOTP.created_at.desc()
    ).first()

    if not reset_otp:
        raise HTTPException(
            status_code=400,
            detail="OTP not found or already used"
        )

    # Check OTP expiration
    if datetime.utcnow() > reset_otp.expires_at:
        raise HTTPException(
            status_code=400,
            detail="OTP has expired"
        )

    # Verify OTP
    otp_correct = bcrypt.checkpw(
        request.otp.encode(),
        reset_otp.otp_hash.encode()
    )

    if not otp_correct:
        raise HTTPException(
            status_code=400,
            detail="Invalid OTP"
        )

    # Hash new password
    new_password_hash = bcrypt.hashpw(
        request.new_password.encode(),
        bcrypt.gensalt()
    ).decode()

    # Update password
    user.hashed_password = new_password_hash

    # Mark OTP as used
    reset_otp.used = True

    db.commit()

    return {
        "message": "Password reset successfully"
    }