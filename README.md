# 📚 Library Management System API

A RESTful Library Management System built using **FastAPI**, **SQLAlchemy**, and **MySQL**. This project provides CRUD operations and search APIs for managing books in a library.

---

## 🚀 Technologies Used

- Python 3
- FastAPI
- SQLAlchemy
- MySQL
- PyMySQL
- Pydantic
- Uvicorn

---

## 📂 Project Structure

```
Library_Management_System/
│── main.py
│── database.py
│── models.py
│── schemas.py
│── crud.py
│── requirements.txt
│── README.md
```

---

## ✨ Features

- Add a New Book
- View All Books
- View Book by ID
- Update Book Details
- Delete Book
- Search Books by Category
- Search Books by Author
- Search Books by Publisher
- Search Books by Price
- Search Books by Quantity
- Search Books by Price Range

---

## 🗄 Database Schema

**Table:** `books`

| Column | Type |
|---------|------|
| id | Integer |
| title | String |
| author | String |
| category | String |
| price | Float |
| quantity | Integer |
| publisher | String |

---

## ⚙️ Installation

### Clone the repository

```bash
git clone <your-repository-url>
```

### Navigate to the project folder

```bash
cd Library_Management_System
```

### Create a virtual environment

```bash
python -m venv venv
```

### Activate the virtual environment

**Windows**

```bash
venv\Scripts\activate
```

### Install dependencies

```bash
pip install -r requirements.txt
```

### Start the server

```bash
uvicorn main:app --reload
```

---

## 📄 API Documentation

Swagger UI:

```
http://127.0.0.1:8000/docs
```

ReDoc:

```
http://127.0.0.1:8000/redoc
```

---

## 📌 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/books` | Add a new book |
| GET | `/books` | Get all books |
| GET | `/books/{book_id}` | Get book by ID |
| PUT | `/books/{book_id}` | Update a book |
| DELETE | `/books/{book_id}` | Delete a book |
| GET | `/books/category/{category}` | Search by category |
| GET | `/books/author/{author_name}` | Search by author |
| GET | `/books/publisher/{publisher_name}` | Search by publisher |
| GET | `/books/price/{price}` | Search by price |
| GET | `/books/quantity/{quantity}` | Search by quantity |
| GET | `/books/price-range?min_price=500&max_price=2000` | Search by price range |

---

## 🧪 Example JSON Request

```json
{
  "title": "Atomic Habits",
  "author": "James Clear",
  "category": "Self Help",
  "price": 799.0,
  "quantity": 15,
  "publisher": "Penguin"
}
```

---

## 📖 Future Improvements

- Partial Update (PATCH)
- Pagination
- Sorting
- JWT Authentication
- Book Borrow & Return
- User Management
- Search by Multiple Filters

---

## 👨‍💻 Author

**Nagendra Babu Gunakala**

Backend Developer (Python | FastAPI | SQLAlchemy | MySQL)

---

## ⭐ Project Status

✅ Version 1.0 Completed