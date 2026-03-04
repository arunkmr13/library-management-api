# Library Management System (FastAPI)

A RESTful Library Management API built using **FastAPI** and **MongoDB**.  
The system supports managing authors, books, users, and book borrowing.

---

## Features

- Author CRUD operations
- Book CRUD operations with author reference
- User registration and login
- JWT authentication
- Borrow and return books
- Loan tracking system
- MongoDB integration using Motor
- FastAPI automatic documentation (Swagger)

---

## Project Structure

fastapi-project
│
├── main.py
├── database.py
├── auth.py
├── schemas.py
│
├── routers
│   ├── authors.py
│   ├── books.py
│   ├── users.py
│   └── loans.py
│
├── tests
│   ├── test_api.py
│   └── test_books.py
│
└── README.md


---

## Requirements

- Python 3.10+
- MongoDB
- FastAPI
- Uvicorn
- Motor (MongoDB async driver)

---


