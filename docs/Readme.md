
# Document Summarizer Agent

An end-to-end **AI-powered document summarization and question-answering system** built using a **Retrieval-Augmented Generation (RAG)** architecture.  
The system ingests large documents, processes them asynchronously, stores semantic embeddings, and generates high-quality summaries and answers using an LLM.

This project is designed with **scalability, modularity, and production readiness** in mind.

---

## 🚀 What This Project Does

The **Document Summarizer Agent** allows users to:

- Upload documents (PDF, DOCX, TXT, etc.)
- Extract and chunk document text
- Generate vector embeddings for semantic understanding
- Store embeddings in a vector database
- Generate document summaries using an LLM
- Ask questions about uploaded documents (RAG-based Q&A)
- Retrieve summaries and answers later via APIs

All heavy operations are handled **asynchronously** to keep the API responsive.

---

## 🧠 High-Level Architecture

Client │ ▼ FastAPI (API Layer) │ ├── Upload Document │ ├── Trigger Background Task │        │ │        ▼ │   Celery Worker (Async Processing) │        │ │        ├── Text Extraction │        ├── Chunking │        ├── Embedding Generation │        └── LLM Summarization │ ├── MongoDB (Metadata, Summaries) └── Chroma DB (Vector Embeddings)

---

## 🧩 Key Features

- **Retrieval-Augmented Generation (RAG)**
- **FastAPI-based backend**
- **Asynchronous task processing with Celery**
- **Redis message broker**
- **Chroma vector database**
- **MongoDB for structured storage**
- **Filesystem storage for uploaded documents**
- **Dockerized development environment**
- **CI/CD workflows via GitHub Actions**

---

## 🛠️ Tech Stack

### Backend
- **Python**
- **FastAPI**
- **Celery**
- **Redis**
- **MongoDB**

### AI / ML
- **LLM (Gemini / OpenAI compatible design)**
- **Embedding models**
- **RAG pipeline**

### Storage
- **Chroma DB** – vector embeddings
- **MongoDB** – metadata, summaries
- **Local filesystem** – raw documents

### DevOps
- **Docker & Docker Compose**
- **GitHub Actions**
- **Pre-commit hooks**

---

## 📁 Project Structure

. ├── api/                  # FastAPI route definitions ├── app/                  # Core application logic ├── chroma_db/            # Vector database storage/config ├── config/               # Environment and config files ├── docs/                 # Detailed markdown documentation ├── frontend/             # UI for document interaction ├── infra/                # Infrastructure & deployment configs ├── models/               # Database models and schemas ├── scripts/              # Utility & helper scripts ├── storage/              # Uploaded document storage ├── tasks/                # Celery background tasks ├── tests/                # Automated tests ├── logs/                 # Application logs ├── run.py                # Application entry point ├── docker-compose.dev.yml └── README.md

---

## 🔄 Detailed Data Flow (Under the Hood)

### 1️⃣ Document Upload
- User uploads a document via FastAPI endpoint.
- File is saved to the `storage/` directory.
- Metadata is stored in MongoDB.

### 2️⃣ Background Processing
- FastAPI triggers a **Celery task**.
- Celery worker performs:
  - Text extraction
  - Cleaning & normalization
  - Chunking into manageable segments

### 3️⃣ Embedding Generation
- Each chunk is converted into a vector embedding.
- Embeddings are stored in **Chroma DB**.

### 4️⃣ Summarization
- Relevant chunks are retrieved from Chroma.
- Context is sent to the LLM.
- Summary is generated and stored in MongoDB.

### 5️⃣ Question Answering (RAG)
- User asks a question.
- Question is embedded.
- Semantic search retrieves relevant chunks.
- LLM generates a grounded answer using retrieved context.

---

## ⚙️ Environment Configuration

Create a `.env` file using the template in `config/`.

Example:

MONGO_URI=mongodb://localhost:27017 REDIS_URL=redis://localhost:6379 LLM_API_KEY=your_api_key_here CHROMA_PERSIST_PATH=./chroma_db

---

## 🧪 Running the Project (Local)

### 1️⃣ Clone the Repository
```bash
git clone https://github.com/Aka-Nine/Document-Summarizer-Agent.git
cd Document-Summarizer-Agent

2️⃣ Start Services

docker-compose -f docker-compose.dev.yml up --build

3️⃣ Start API

python run.py

4️⃣ Start Celery Worker

celery -A tasks.worker worker --loglevel=info


---

🔌 API Overview

Upload Document

POST /documents/upload

Get Summary

GET /documents/{document_id}/summary

Ask Question

POST /documents/{document_id}/query


---

🧠 Design Decisions & Trade-offs

Celery chosen for reliable async processing over background threads.

Chroma DB used for fast local vector search.

MongoDB chosen for flexible schema and rapid iteration.

RAG approach ensures answers are grounded in document content.

Modular folder structure enables easy extension (new LLMs, DBs, UIs).



---

🧪 Testing

Unit tests located in /tests

API routes and background tasks tested independently

CI pipeline ensures linting and test validation



---

🚧 Known Limitations

Large documents may increase processing time

LLM cost depends on document size

Currently single-node deployment (can be scaled)



---

🔮 Future Improvements

Streaming summaries

Multi-document querying

User authentication & access control

Cloud vector DB support (Pinecone, Weaviate)

Improved frontend UX

Caching frequent queries



---

🤝 Contributing

Contributions are welcome.

1. Fork the repo


2. Create a feature branch


3. Commit changes


4. Open a pull request




---

📜 License

MIT License


---

⭐ Final Note

This project demonstrates real-world AI system design, combining:

Async systems

Vector search

LLM orchestration

Scalable backend architecture


