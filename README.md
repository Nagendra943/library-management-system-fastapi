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


Library_Management_System/
│── main.py
│── database.py
│── models.py
│── schemas.py
│── crud.py
│── requirements.txt
│── README.md
```



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


<img width="1920" height="1080" alt="Screenshot (115)" src="https://github.com/user-attachments/assets/2d323563-774f-4a97-b991-355857392bc8" />
<img width="1920" height="1080" alt="Screenshot (114)" src="https://github.com/user-attachments/assets/4ef423e9-39c1-4ee0-829d-dd0d04f15cc6" />
<img width="1920" height="1080" alt="Screenshot (113)" src="https://github.com/user-attachments/assets/c9f88027-36dc-49f8-a9d7-a86594825fe2" />
<img width="1920" height="1080" alt="Screenshot (112)" src="https://github.com/user-attachments/assets/55ccbb1e-1436-4315-856f-5b3d4144ee0a" />
<img width="1920" height="1080" alt="Screenshot (111)" src="https://github.com/user-attachments/assets/7b84b01f-9bd5-42ab-ab01-6ab331632141" />
<img width="1920" height="1080" alt="Screenshot (110)" src="https://github.com/user-attachments/assets/d8d6344a-d4c4-44b3-8e1b-85e9fa1a9dfc" />
<img width="1920" height="1080" alt="Screenshot (109)" src="https://github.com/user-attachments/assets/c3daefc0-7554-4366-99df-e93358efc010" />
<img width="1920" height="1080" alt="Screenshot (108)" src="https://github.com/user-attachments/assets/ec7c9d22-ebaa-4267-9137-6a4cf545f27c" />
<img width="1920" height="1080" alt="Screenshot (107)" src="https://github.com/user-attachments/assets/24dd22ef-a0d6-4408-9517-6a5f460e8a04" />
<img width="1920" height="1080" alt="Screenshot (106)" src="https://github.com/user-attachments/assets/685936f8-1c0e-4b52-af34-36f3174dad8a" />
json
{
  "title": "Atomic Habits",
  "author": "James Clear",
  "category": "Self Help",
  "price": 799.0,
  "quantity": 15,
  "publisher": "Penguin"
}


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
