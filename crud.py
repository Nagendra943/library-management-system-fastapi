from sqlalchemy.orm import Session   # NEed session fro everey operarion
import models
import schemas
import bcrypt


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
