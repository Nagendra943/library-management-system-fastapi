from sqlalchemy import Column, Integer, String, Float, Boolean
from database import Base

class Book(Base):
    # def __repr__(self):
    # return f"<Book(title='{self.title}', author='{self.author}')>"
    __tablename__ = "books"

    id = Column(Integer, primary_key = True, index = True)
    title = Column(String(150), nullable = False)
    author = Column(String(100), nullable = False)
    category = Column(String(100), nullable = False)
    price = Column(Float, nullable = False)
    quantity = Column(Integer, nullable = False)
    publisher = Column(String(150), nullable = False)
    

class User(Base):

    __tablename__ = "users"

    id = Column(Integer, primary_key = True, index = True)

    username = Column(String(100), nullable = False, unique = True)

    email = Column(String(100), nullable = False, unique = True)

    hashed_password = Column(String(300), nullable = False)

    is_admin = Column(Boolean, default = False, nullable = False)
