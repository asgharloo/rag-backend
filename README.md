# Rag AI Backend

> 🚧 **Work in Progress**

A modular AI backend for building intelligent assistants with long-term memory, semantic retrieval, and context-aware response generation.

---

## Overview

Rug AI Backend is a FastAPI-based backend for building AI-powered assistants.

The platform provides secure authentication, persistent conversations, long-term memory, semantic retrieval using vector embeddings, AI-generated responses, and an extensible architecture that can be adapted to different domains such as healthcare, education, customer support, coaching, or personal assistants.
---


## Features

- Secure authentication (OTP & JWT)
- Conversation and session management
- AI-powered response generation
- Long-term memory
- Semantic retrieval using pgvector
- Context-aware response generation
- Rule-based workflow engine
- Conversation summarization
- Extensible architecture for domain-specific assistants
- PostgreSQL + Alembic
- Docker support

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
