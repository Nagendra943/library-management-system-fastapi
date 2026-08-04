from sqlalchemy.orm import Session   # NEed session fro everey operarion
import models
import schemas


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

def get_books_by_category(db : Session, category : str):
    return db.query(models.Book).filter(
        models.Book.category == category
    ).all()

def get_books_by_author(db : Session, author_name : str):
    return db.query(models.Book).filter(
        models.Book.author == author_name
    ).all()

def get_books_by_publisher(db : Session, publisher_name : str):
    return db.query(models.Book).filter(
        models.Book.publisher == publisher_name
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

    


