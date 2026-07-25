# Meets: FastAPI

A modern, high-performance REST API built with FastAPI, SQLAlchemy, and SQLite for managing form data with full CRUD operations.

## UPD. LIST
24.07.26 - **RELEASE (init)**
25.07.26 - **Layered Architecture UPDATE**

## Tech Stack

- Framework: **FastAPI**
- ORM: **SQLAlchemy 2.0**
- Database: **SQLite**
- Validation: **Pydantic v2**
- Language: **Python 3.10+**

## API Endpoints

| Method | Endpoint | Description | Status Codes |
|--------|----------|-------------|--------------|
| `GET` | `/forms` | Return a list of forms | 200
| `GET` | `/forms/random` | Get a random form | 200, 404 |
| `POST` | `/forms` | Create a new form | 201 |
| `PATCH` | `/forms?form_id={id}` | Update an existing form | 200, 404 |
| `DELETE` | `/forms?form_id={id}` | Delete a form | 204, 404 |