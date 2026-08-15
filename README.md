# Amazon-Like E-Commerce Backend

A professional RESTful e-commerce backend built with Python and FastAPI. This project provides essential e-commerce functionality including user authentication, product management, shopping cart, order processing, inventory management, and payments.

This is an independent educational and portfolio project inspired by common e-commerce platforms and is not affiliated with Amazon.

## Features

- User registration and login
- JWT-based authentication
- Role-based authorization
- Customer, Seller, and Admin roles
- Product management
- Product search, filtering, sorting, and pagination
- Shopping cart management
- Order placement and order history
- Inventory and stock management
- Mock payment processing
- PostgreSQL database
- Redis integration
- Alembic database migrations
- Docker and Docker Compose support
- Pytest testing
- Interactive Swagger API documentation

## Tech Stack

- Python 3.12
- FastAPI
- PostgreSQL
- SQLAlchemy 2.x
- Pydantic
- JWT
- bcrypt
- Alembic
- Redis
- Pytest
- Docker
- Docker Compose

## Project Structure

```text
amazon_backend/
│
├── app/
│   ├── core/
│   ├── database/
│   ├── models/
│   ├── schemas/
│   ├── routers/
│   ├── services/
│   └── main.py
│
├── alembic/
├── scripts/
├── tests/
│
├── .env.example
├── .gitignore
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
├── alembic.ini
└── README.md
