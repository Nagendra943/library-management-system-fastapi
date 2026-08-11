from sqlalchemy import Column, Integer, String, Float, Boolean, ForeignKey, DateTime
from database import Base
from datetime import datetime
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

class BorrowedBook(Base):

    __tablename__ = "borrowed_books"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False
    )

    book_id = Column(
        Integer,
        ForeignKey("books.id"),
        nullable=False
    )

    borrowed_at = Column(
        DateTime,
        default=datetime.utcnow,
        nullable=False
    )

    returned_at = Column(
        DateTime,
        nullable=True
    )

    status = Column(
        String(20),
        default="borrowed",
        nullable=False
    )

class PasswordResetOTP(Base):
    __tablename__ = "password_reset_otps"

    id = Column(Integer, primary_key=True, index=True)

    email = Column(
        String(100),
        nullable=False,
        index=True
    )

    otp_hash = Column(
        String(300),
        nullable=False
    )

    expires_at = Column(
        DateTime,
        nullable=False
    )

    used = Column(
        Boolean,
        default=False,
        nullable=False
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow,
        nullable=False
    )