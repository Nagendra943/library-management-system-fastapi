from sqlalchemy.orm import Session   # NEed session fro everey operarion
from datetime import datetime
import models
import schemas
import bcrypt
from sqlalchemy import func


def create_book(db : Session, book : schemas.BookCreate):

    db_book = models.Book(**book.model_dump())

    db.add(db_book)

    db.commit()

    db.refresh(db_book)

    return db_book

def get_all_books(db : Session):
    return db.query(models.Book).all() #all records 

def get_book(db : Session, book_id : int):
    return db.query(models.Book).filter(   # where 
        models.Book.id == book_id
    ).first()

def get_books_by_title(db : Session, title_name : str):
    return db.query(models.Book).filter(
        models.Book.title.ilike(f"%{title_name}%")
    ).all()

def get_books_by_category(db : Session, category_name : str):
    return db.query(models.Book).filter(
        models.Book.category.ilike(f"%{category_name}%")
    ).all()

def get_books_by_author(db : Session, author_name : str):
    return db.query(models.Book).filter(
        models.Book.author.ilike(f"%{author_name}%")
    ).all()

def get_books_by_publisher(db : Session, publisher_name : str):
    return db.query(models.Book).filter(
        models.Book.publisher.ilike(f"%{publisher_name}%")
    ).all()

def get_books_by_price(db : Session, price_val : float):
    return db.query(models.Book).filter(
        models.Book.price == price_val
    ).all()

def get_books_by_quantity(db : Session, quantity_val : int):
    return db.query(models.Book).filter(
        models.Book.quantity == quantity_val
    ).all()

def get_books_by_price_range(db : Session, min_price : int, max_price : int):
    return db.query(models.Book).filter(
        models.Book.price >= min_price,
        models.Book.price <= max_price
    ).all()

def get_book_categories(db: Session):

    categories = db.query(
        models.Book.category,
        func.count(models.Book.id)
    ).group_by(
        models.Book.category
    ).order_by(
        models.Book.category
    ).all()

    return [
        {
            "category": category,
            "book_count": count
        }
        for category, count in categories
    ]

def get_paginated_books(
    db: Session,
    page: int = 1,
    limit: int = 20,
    category: str | None = None,
    search: str | None = None
):

    query = db.query(models.Book)

    # =========================
    # CATEGORY FILTER
    # =========================

    if category:
        query = query.filter(
            models.Book.category.ilike(category)
        )

    # =========================
    # SEARCH
    # =========================

    if search:

        search_term = f"%{search}%"

        query = query.filter(
            (models.Book.title.ilike(search_term)) |
            (models.Book.author.ilike(search_term)) |
            (models.Book.category.ilike(search_term)) |
            (models.Book.publisher.ilike(search_term))
        )

    # =========================
    # TOTAL COUNT
    # =========================

    total_books = query.count()

    # =========================
    # PAGINATION
    # =========================

    offset = (page - 1) * limit

    books = query.order_by(
        models.Book.id
    ).offset(
        offset
    ).limit(
        limit
    ).all()

    # =========================
    # TOTAL PAGES
    # =========================

    total_pages = (
        (total_books + limit - 1) // limit
        if total_books > 0
        else 1
    )

    return {
        "books": books,
        "page": page,
        "limit": limit,
        "total_books": total_books,
        "total_pages": total_pages,
        "has_next": page < total_pages,
        "has_previous": page > 1
    }

def update_book(db : Session, book_id : int, book : schemas.BookCreate):
    db_book = get_book(db, book_id)
    if not db_book:
        return None
    db_book.title = book.title
    db_book.author = book.author 
    db_book.category = book.category
    db_book.price = book.price
    db_book.quantity = book.quantity
    db_book.publisher = book.publisher

    db.commit()
    db.refresh(db_book)   
    return db_book

def delete_book(db : Session, book_id : int):
    db_book = get_book(db, book_id)
    if not db_book:
        return None
    db.delete(db_book)

    db.commit()
    return db_book


def create_user(user: schemas.UserCreate, db: Session):

    hashed = bcrypt.hashpw(
        user.password.encode(),
        bcrypt.gensalt()
    ).decode("utf-8")

    new_user = models.User(
        username = user.username,
        email = user.email,
        hashed_password = hashed
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user

def validate_user(user: schemas.UserLogin, db: Session):

    user_exist = db.query(models.User).filter(
        models.User.email == user.email
    ).first()

    if not user_exist:
        return None

    password_correct = bcrypt.checkpw(
        user.password.encode(),
        user_exist.hashed_password.encode()
    )

    if not password_correct:
        return None

    return user_exist


def change_password(db: Session, user, new_password: str):

    hashed = bcrypt.hashpw(
        new_password.encode(),
        bcrypt.gensalt()
    ).decode("utf-8")

    user.hashed_password = hashed

    db.commit()
    db.refresh(user)

    return user


def search_books(db: Session, search_term: str):

    search = f"%{search_term}%"

    return db.query(models.Book).filter(
        (models.Book.title.ilike(search)) |
        (models.Book.author.ilike(search)) |
        (models.Book.category.ilike(search)) |
        (models.Book.publisher.ilike(search))
    ).all()


def borrow_book(
    db: Session,
    user_id: int,
    book_id: int
):

    book = db.query(models.Book).filter(
        models.Book.id == book_id
    ).first()

    if not book:
        return "BOOK_NOT_FOUND"

    if book.quantity <= 0:
        return "OUT_OF_STOCK"

    existing_borrow = db.query(models.BorrowedBook).filter(
        models.BorrowedBook.user_id == user_id,
        models.BorrowedBook.book_id == book_id,
        models.BorrowedBook.status == "borrowed"
    ).first()

    if existing_borrow:
        return "ALREADY_BORROWED"

    book.quantity -= 1

    borrowing = models.BorrowedBook(
        user_id=user_id,
        book_id=book_id,
        status="borrowed"
    )

    db.add(borrowing)
    db.commit()
    db.refresh(borrowing)

    return borrowing


def return_book(
    db: Session,
    user_id: int,
    book_id: int
):

    borrowing = db.query(models.BorrowedBook).filter(
        models.BorrowedBook.user_id == user_id,
        models.BorrowedBook.book_id == book_id,
        models.BorrowedBook.status == "borrowed"
    ).first()

    if not borrowing:
        return None

    book = db.query(models.Book).filter(
        models.Book.id == book_id
    ).first()

    if book:
        book.quantity += 1

    borrowing.status = "returned"
    borrowing.returned_at = datetime.utcnow()

    db.commit()
    db.refresh(borrowing)

    return borrowing


def get_my_borrowings(
    db: Session,
    user_id: int
):

    return db.query(models.BorrowedBook).filter(
        models.BorrowedBook.user_id == user_id
    ).order_by(
        models.BorrowedBook.borrowed_at.desc()
    ).all()


def get_all_borrowings(db: Session):

    return db.query(
        models.BorrowedBook
    ).order_by(
        models.BorrowedBook.borrowed_at.desc()
    ).all()


def get_dashboard_stats(db: Session):

    total_books = db.query(models.Book).count()

    total_users = db.query(models.User).count()

    total_borrowed = db.query(
        models.BorrowedBook
    ).filter(
        models.BorrowedBook.status == "borrowed"
    ).count()

    available_books = db.query(
        models.Book
    ).filter(
        models.Book.quantity > 0
    ).count()

    return {
        "total_books": total_books,
        "total_users": total_users,
        "total_borrowed": total_borrowed,
        "available_books": available_books
    }

def get_all_users(db: Session):

    return db.query(models.User).all()

def make_user_admin(
    db: Session,
    user_id: int
):

    user = db.query(models.User).filter(
        models.User.id == user_id
    ).first()

    if not user:
        return None

    user.is_admin = True

    db.commit()
    db.refresh(user)

    return user


def remove_user_admin(
    db: Session,
    user_id: int
):

    user = db.query(models.User).filter(
        models.User.id == user_id
    ).first()

    if not user:
        return None

    user.is_admin = False

    db.commit()
    db.refresh(user)

    return user