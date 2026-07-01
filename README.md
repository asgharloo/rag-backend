# Rug AI Backend

> 🚧 **Work in Progress**

A modular AI backend for building intelligent assistants with long-term memory, semantic retrieval, and context-aware response generation.

---

## Overview

Rug AI Backend is a FastAPI-based backend designed for AI-powered mental health conversations.

The system provides secure user authentication, persistent chat sessions, long-term memory, semantic retrieval using vector embeddings, AI-generated responses, and psychological assessment support.

The project is designed with scalability and maintainability in mind and serves as the backend foundation for an intelligent mental health platform.

---

## Features

- User authentication with OTP and JWT
- User profile management
- Chat session management
- AI-powered conversation engine
- Long-term memory storage
- Semantic memory retrieval using vector embeddings (pgvector)
- Rule-based response engine
- Automatic session summarization
- Psychological assessment support
- PostgreSQL database
- Database versioning with Alembic
- Dockerized deployment

---

## Technology Stack

- Python 3
- FastAPI
- SQLAlchemy 2.0
- PostgreSQL
- pgvector
- Alembic
- Pydantic v2
- Docker & Docker Compose
- OpenAI Compatible API

---

## Project Structure

```text
.
├── app
│   ├── crud
│   ├── models
│   ├── routers
│   ├── schemas
│   ├── services
│   ├── utils
│   ├── config.py
│   ├── database.py
│   ├── dependencies.py
│   └── main.py
├── alembic
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── README.md
```

---

## Getting Started

### Clone the repository

```bash
git clone https://github.com/asgharloo/rug-ai-backend.git
cd rug-ai-backend
```

### Install dependencies

```bash
pip install -r requirements.txt
```

### Configure environment variables

Create a `.env` file and configure your application settings.

### Run database migrations

```bash
alembic upgrade head
```

### Run the application

```bash
uvicorn app.main:app --reload
```

### Run with Docker

```bash
docker compose up --build
```

---

## API Documentation

After starting the application, Swagger UI is available at:

```
http://localhost:8000/docs
```

---

## Database

This project uses:

- PostgreSQL
- pgvector extension
- Alembic migrations

---

## Roadmap

- [ ] Improve long-term memory retrieval
- [ ] Enhance AI reasoning workflow
- [ ] Add automated tests
- [ ] CI/CD pipeline
- [ ] Production deployment
- [ ] Kubernetes deployment

---

## License

This project is provided for educational and demonstration purposes.
