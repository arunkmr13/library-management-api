# Library Management System (FastAPI)

A RESTful Library Management API built using **FastAPI** and **MongoDB**.
The system supports managing authors, books, users, and a borrowing system with loan tracking.

---

# Features

* Author CRUD operations
* Book CRUD operations with author reference
* User registration and login
* JWT authentication
* Borrow and return books
* Loan tracking system
* Role-based access (admin / user)
* Pagination support for listing resources
* Validation to prevent borrowing unavailable books
* MongoDB integration using Motor (async driver)
* FastAPI automatic documentation (Swagger)

---

# Project Structure

```
library-management-api
│
├── main.py
├── database.py
├── auth.py
├── schemas.py
├── models.py
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
├── requirements.txt
├── README.md
└── .gitignore
```

---

# Requirements

* Python 3.10+
* MongoDB
* FastAPI
* Uvicorn
* Motor (MongoDB async driver)

---

# Installation

Clone the repository:

```
git clone https://github.com/arunkmr13/library-management-api.git
```

Navigate to the project folder:

```
cd library-management-api
```

Create a virtual environment:

```
python -m venv venv
```

Activate the environment:

Mac/Linux

```
source venv/bin/activate
```

Windows

```
venv\Scripts\activate
```

Install dependencies:

```
pip install -r requirements.txt
```

---

# Running the Application

Start the FastAPI server:

```
uvicorn main:app --reload
```

The API will run at:

```
http://127.0.0.1:8000
```

---

# API Documentation

FastAPI automatically generates interactive API documentation.

Swagger UI

```
http://127.0.0.1:8000/docs
```

ReDoc

```
http://127.0.0.1:8000/redoc
```

These interfaces allow you to test all endpoints directly from the browser.

---

# API Endpoints Overview

## Authors

| Method | Endpoint      | Description         |
| ------ | ------------- | ------------------- |
| POST   | /authors      | Create a new author |
| GET    | /authors      | List all authors    |
| GET    | /authors/{id} | Get author by ID    |
| PUT    | /authors/{id} | Update author       |
| DELETE | /authors/{id} | Delete author       |

---

## Books

| Method | Endpoint    | Description                  |
| ------ | ----------- | ---------------------------- |
| POST   | /books      | Create a book                |
| GET    | /books      | List books (with pagination) |
| GET    | /books/{id} | Get book by ID               |
| PUT    | /books/{id} | Update book                  |
| DELETE | /books/{id} | Delete book                  |

---

## Users

| Method | Endpoint        | Description                 |
| ------ | --------------- | --------------------------- |
| POST   | /users/register | Register a user             |
| POST   | /users/login    | Login and receive JWT token |

---

## Loans

| Method | Endpoint                | Description                                      |
| ------ | ----------------------- | ------------------------------------------------ |
| POST   | /loans/borrow/{book_id} | Borrow a book                                    |
| PUT    | /loans/return/{loan_id} | Return a book                                    |
| GET    | /loans                  | List loans (admin sees all, user sees own loans) |

---

# Borrowing Rules

* A user cannot borrow a book that is already borrowed.
* When a book is borrowed:

  * A loan record is created.
  * The book availability is set to **false**.
* When a book is returned:

  * The loan record is updated with the return date.
  * The book availability becomes **true**.

---

# Testing the API

You can test the API using:

* Swagger UI

Recommended testing order:

1. Register a user
2. Login to obtain JWT token
3. Create authors
4. Create books
5. Borrow a book
6. Return a book
7. Check loan records

---

# Authentication

Protected endpoints require a JWT token.


------

# Author

Arun Kumar

GitHub Repository
https://github.com/arunkmr13/library-management-api

