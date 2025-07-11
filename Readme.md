# Document Summarization Agent

## Overview
A scalable document processing API with LLM-powered summarization and Q&A, supporting file uploads, user authentication, and background processing with Celery.

## Features
- User registration and authentication
- Secure file upload with validation
- Asynchronous document processing (Celery + Redis)
- MinIO for file storage
- PostgreSQL for metadata
- Nginx reverse proxy with rate limiting
- Dockerized for easy deployment

## Quick Start (Docker Compose)

1. **Clone the repository**

2. **Set up environment variables**
   - Copy `.env.example` to `.env` and fill in your secrets (or set them in your deployment environment).

3. **Build and start all services:**
   ```bash
   docker-compose up --build
   ```

4. **Access the API:**
   - API: http://localhost:80
   - Flower (Celery monitoring): http://localhost:5555
   - MinIO Console: http://localhost:9001

## Environment Variables
See `config/setting.py` for all supported variables. Key ones:
- `SECRET_KEY` (required)
- `DATABASE_URL` (default: postgresql://postgres:postgres@postgres:5432/docprocessing)
- `REDIS_URL` (default: redis://redis:6379)
- `MINIO_ENDPOINT`, `MINIO_ACCESS_KEY`, `MINIO_SECRET_KEY`, `BUCKET_NAME`
- `GROQ_API_KEY` (for LLM)

## Useful Commands
- **Run migrations:** (if using Alembic)
  ```bash
  alembic upgrade head
  ```
- **View logs:**
  ```bash
  docker-compose logs -f
  ```

## Production Notes
- Change CORS and allowed hosts in `config/setting.py` for your domain.
- Use strong secrets in production.
- Set up SSL certificates in the `ssl/` directory for HTTPS.

---

For more details, see the code and comments in each file.
