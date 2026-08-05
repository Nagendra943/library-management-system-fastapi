from sqlalchemy import Column, Integer, String, Float
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


