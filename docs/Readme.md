# 🤖 Document Summarizer Agent

> **An enterprise-grade AI system for intelligent document summarization and question answering, powered by Retrieval-Augmented Generation (RAG).**

[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=flat&logo=python&logoColor=white)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-009688?style=flat&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![Celery](https://img.shields.io/badge/Celery-Async-37814A?style=flat&logo=celery&logoColor=white)](https://docs.celeryq.dev)
[![MongoDB](https://img.shields.io/badge/MongoDB-Atlas-47A248?style=flat&logo=mongodb&logoColor=white)](https://mongodb.com)
[![Redis](https://img.shields.io/badge/Redis-Broker-DC382D?style=flat&logo=redis&logoColor=white)](https://redis.io)
[![Docker](https://img.shields.io/badge/Docker-Compose-2496ED?style=flat&logo=docker&logoColor=white)](https://docker.com)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

---

## 📋 Table of Contents

- [Overview](#-overview)
- [Architecture Diagram](#-architecture-diagram)
- [Features](#-features)
- [Tech Stack](#️-tech-stack)
- [Project Structure](#-project-structure)
- [Data Flow](#-data-flow)
- [API Endpoints](#-api-endpoints)
- [Database Schema](#-database-schema)
- [Security Architecture](#-security-architecture)
- [Getting Started](#-getting-started)
- [Environment Variables](#-environment-variables)
- [Running with Docker](#-running-with-docker)
- [Running Locally](#-running-locally)
- [Testing](#-testing)
- [Deployment](#-deployment)
- [Performance](#-performance)
- [Known Limitations](#-known-limitations)
- [Roadmap](#-roadmap)
- [Contributing](#-contributing)

---

## 🧠 Overview

The **Document Summarizer Agent** is a production-ready, end-to-end AI platform that allows users to upload documents, extract semantic meaning, and query them using natural language. Built on a **Retrieval-Augmented Generation (RAG)** pipeline, it leverages state-of-the-art vector embeddings and large language models to deliver grounded, context-aware summaries and answers.

The platform is designed with **scalability**, **modularity**, and **production readiness** in mind — featuring async task processing, multi-cloud integrations, a secure REST API with JWT authentication, and a full observability stack.

**What can it do?**

- Upload PDF, DOCX, and TXT documents via a REST API or frontend UI
- Asynchronously extract, chunk, and embed document content
- Generate document-level summaries using Gemini LLM
- Answer natural language questions grounded in document content (RAG)
- Retrieve past summaries and query history via authenticated APIs
- Monitor system health across all connected services

---

## 🏛️ Architecture Diagram

![System Architecture]()<svg viewBox="0 0 1000 720" xmlns="http://www.w3.org/2000/svg" font-family="'Segoe UI', system-ui, sans-serif">
  <defs>
    <linearGradient id="bgGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" style="stop-color:#0f1117;stop-opacity:1" />
      <stop offset="100%" style="stop-color:#1a1f2e;stop-opacity:1" />
    </linearGradient>
    <linearGradient id="clientGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" style="stop-color:#3b82f6" />
      <stop offset="100%" style="stop-color:#1d4ed8" />
    </linearGradient>
    <linearGradient id="apiGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" style="stop-color:#8b5cf6" />
      <stop offset="100%" style="stop-color:#6d28d9" />
    </linearGradient>
    <linearGradient id="celeryGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" style="stop-color:#f59e0b" />
      <stop offset="100%" style="stop-color:#d97706" />
    </linearGradient>
    <linearGradient id="dbGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" style="stop-color:#10b981" />
      <stop offset="100%" style="stop-color:#059669" />
    </linearGradient>
    <linearGradient id="llmGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" style="stop-color:#ef4444" />
      <stop offset="100%" style="stop-color:#dc2626" />
    </linearGradient>
    <linearGradient id="redisGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" style="stop-color:#f97316" />
      <stop offset="100%" style="stop-color:#ea580c" />
    </linearGradient>
    <filter id="glow">
      <feGaussianBlur stdDeviation="3" result="coloredBlur"/>
      <feMerge>
        <feMergeNode in="coloredBlur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
    <filter id="shadow">
      <feDropShadow dx="0" dy="4" stdDeviation="8" flood-color="#000" flood-opacity="0.5"/>
    </filter>
    <marker id="arrow" markerWidth="10" markerHeight="7" refX="10" refY="3.5" orient="auto">
      <polygon points="0 0, 10 3.5, 0 7" fill="#4b5563"/>
    </marker>
    <marker id="arrowBlue" markerWidth="10" markerHeight="7" refX="10" refY="3.5" orient="auto">
      <polygon points="0 0, 10 3.5, 0 7" fill="#60a5fa"/>
    </marker>
    <marker id="arrowYellow" markerWidth="10" markerHeight="7" refX="10" refY="3.5" orient="auto">
      <polygon points="0 0, 10 3.5, 0 7" fill="#fbbf24"/>
    </marker>
    <marker id="arrowGreen" markerWidth="10" markerHeight="7" refX="10" refY="3.5" orient="auto">
      <polygon points="0 0, 10 3.5, 0 7" fill="#34d399"/>
    </marker>
  </defs>

  <!-- Background -->
  <rect width="1000" height="720" fill="url(#bgGrad)"/>

  <!-- Title -->
  <text x="500" y="38" text-anchor="middle" font-size="20" font-weight="700" fill="#f9fafb" letter-spacing="1">Document Summarizer Agent — System Architecture</text>
  <line x1="60" y1="50" x2="940" y2="50" stroke="#2d3748" stroke-width="1"/>

  <!-- ── LAYER LABELS ── -->
  <text x="28" y="120" font-size="10" fill="#6b7280" transform="rotate(-90,28,120)" text-anchor="middle">CLIENT</text>
  <text x="28" y="230" font-size="10" fill="#6b7280" transform="rotate(-90,28,230)" text-anchor="middle">API LAYER</text>
  <text x="28" y="390" font-size="10" fill="#6b7280" transform="rotate(-90,28,390)" text-anchor="middle">ASYNC WORKERS</text>
  <text x="28" y="570" font-size="10" fill="#6b7280" transform="rotate(-90,28,570)" text-anchor="middle">DATA LAYER</text>

  <!-- Horizontal lane dividers -->
  <rect x="50" y="62" width="900" height="2" rx="1" fill="#1e2535" opacity="0.8"/>
  <rect x="50" y="155" width="900" height="2" rx="1" fill="#1e2535" opacity="0.8"/>
  <rect x="50" y="285" width="900" height="2" rx="1" fill="#1e2535" opacity="0.8"/>
  <rect x="50" y="490" width="900" height="2" rx="1" fill="#1e2535" opacity="0.8"/>
  <rect x="50" y="650" width="900" height="2" rx="1" fill="#1e2535" opacity="0.8"/>

  <!-- ═══ CLIENT LAYER ═══ -->
  <!-- Browser / UI -->
  <rect x="190" y="72" width="130" height="72" rx="10" fill="url(#clientGrad)" filter="url(#shadow)"/>
  <text x="255" y="97" text-anchor="middle" font-size="12" font-weight="700" fill="white">🌐 Browser</text>
  <text x="255" y="113" text-anchor="middle" font-size="10" fill="#bfdbfe">React / TypeScript</text>
  <text x="255" y="128" text-anchor="middle" font-size="10" fill="#bfdbfe">Frontend UI</text>

  <!-- REST Client -->
  <rect x="400" y="72" width="130" height="72" rx="10" fill="url(#clientGrad)" filter="url(#shadow)"/>
  <text x="465" y="97" text-anchor="middle" font-size="12" font-weight="700" fill="white">📡 REST Client</text>
  <text x="465" y="113" text-anchor="middle" font-size="10" fill="#bfdbfe">cURL / Postman</text>
  <text x="465" y="128" text-anchor="middle" font-size="10" fill="#bfdbfe">API Testing</text>

  <!-- Swagger UI -->
  <rect x="610" y="72" width="130" height="72" rx="10" fill="url(#clientGrad)" filter="url(#shadow)"/>
  <text x="675" y="97" text-anchor="middle" font-size="12" font-weight="700" fill="white">📋 Swagger UI</text>
  <text x="675" y="113" text-anchor="middle" font-size="10" fill="#bfdbfe">/docs · /redoc</text>
  <text x="675" y="128" text-anchor="middle" font-size="10" fill="#bfdbfe">Interactive Docs</text>

  <!-- Arrows client → API -->
  <line x1="255" y1="144" x2="370" y2="180" stroke="#60a5fa" stroke-width="1.5" stroke-dasharray="5,3" marker-end="url(#arrowBlue)"/>
  <line x1="465" y1="144" x2="465" y2="172" stroke="#60a5fa" stroke-width="1.5" stroke-dasharray="5,3" marker-end="url(#arrowBlue)"/>
  <line x1="675" y1="144" x2="590" y2="180" stroke="#60a5fa" stroke-width="1.5" stroke-dasharray="5,3" marker-end="url(#arrowBlue)"/>

  <!-- ═══ API LAYER ═══ -->
  <!-- Middleware stack -->
  <rect x="150" y="165" width="180" height="108" rx="10" fill="#1e2535" stroke="#374151" stroke-width="1.2" filter="url(#shadow)"/>
  <text x="240" y="186" text-anchor="middle" font-size="11" font-weight="700" fill="#c4b5fd">⚙️ Middleware Stack</text>
  <text x="240" y="203" text-anchor="middle" font-size="9" fill="#9ca3af">JWT Auth · Rate Limit</text>
  <text x="240" y="218" text-anchor="middle" font-size="9" fill="#9ca3af">CORS · Security Headers</text>
  <text x="240" y="233" text-anchor="middle" font-size="9" fill="#9ca3af">GZip · Request ID</text>
  <text x="240" y="248" text-anchor="middle" font-size="9" fill="#9ca3af">Structured Logging</text>
  <text x="240" y="263" text-anchor="middle" font-size="9" fill="#9ca3af">7 Layers Total</text>

  <!-- FastAPI Core -->
  <rect x="380" y="165" width="180" height="108" rx="10" fill="url(#apiGrad)" filter="url(#shadow)"/>
  <text x="470" y="190" text-anchor="middle" font-size="13" font-weight="700" fill="white">⚡ FastAPI Core</text>
  <text x="470" y="208" text-anchor="middle" font-size="9" fill="#e9d5ff">POST /documents/upload</text>
  <text x="470" y="222" text-anchor="middle" font-size="9" fill="#e9d5ff">GET  /documents/{id}/summary</text>
  <text x="470" y="236" text-anchor="middle" font-size="9" fill="#e9d5ff">POST /documents/{id}/query</text>
  <text x="470" y="250" text-anchor="middle" font-size="9" fill="#e9d5ff">POST /auth/register · /login</text>
  <text x="470" y="264" text-anchor="middle" font-size="9" fill="#e9d5ff">16 Endpoints Total</text>

  <!-- Auth Service -->
  <rect x="610" y="165" width="180" height="108" rx="10" fill="#1e2535" stroke="#374151" stroke-width="1.2" filter="url(#shadow)"/>
  <text x="700" y="186" text-anchor="middle" font-size="11" font-weight="700" fill="#c4b5fd">🔐 Auth Service</text>
  <text x="700" y="203" text-anchor="middle" font-size="9" fill="#9ca3af">JWT Token Generation</text>
  <text x="700" y="218" text-anchor="middle" font-size="9" fill="#9ca3af">bcrypt Password Hashing</text>
  <text x="700" y="233" text-anchor="middle" font-size="9" fill="#9ca3af">Token Expiry Handling</text>
  <text x="700" y="248" text-anchor="middle" font-size="9" fill="#9ca3af">Bearer Token Validation</text>
  <text x="700" y="263" text-anchor="middle" font-size="9" fill="#9ca3af">User Session Context</text>

  <!-- Arrows API layer internal -->
  <line x1="330" y1="219" x2="378" y2="219" stroke="#7c3aed" stroke-width="1.5" marker-end="url(#arrow)"/>
  <line x1="560" y1="219" x2="608" y2="219" stroke="#7c3aed" stroke-width="1.5" marker-end="url(#arrow)"/>

  <!-- ═══ Arrows API → Workers ═══ -->
  <!-- FastAPI → Redis (broker) -->
  <line x1="420" y1="273" x2="330" y2="340" stroke="#fbbf24" stroke-width="2" stroke-dasharray="6,3" marker-end="url(#arrowYellow)"/>
  <text x="358" y="322" font-size="9" fill="#fbbf24">enqueue task</text>

  <!-- ═══ ASYNC WORKERS LAYER ═══ -->
  <!-- Redis Broker -->
  <rect x="100" y="300" width="160" height="80" rx="10" fill="url(#redisGrad)" filter="url(#shadow)"/>
  <text x="180" y="328" text-anchor="middle" font-size="12" font-weight="700" fill="white">🔴 Redis</text>
  <text x="180" y="345" text-anchor="middle" font-size="9" fill="#fed7aa">Message Broker</text>
  <text x="180" y="360" text-anchor="middle" font-size="9" fill="#fed7aa">Task Queue · Cache</text>
  <text x="180" y="372" text-anchor="middle" font-size="9" fill="#fed7aa">Session Store</text>

  <!-- Arrow Redis → Celery -->
  <line x1="260" y1="340" x2="320" y2="340" stroke="#fbbf24" stroke-width="2" marker-end="url(#arrowYellow)"/>

  <!-- Celery Worker -->
  <rect x="322" y="296" width="350" height="188" rx="12" fill="#1a1225" stroke="#d97706" stroke-width="1.5" filter="url(#shadow)"/>
  <text x="497" y="320" text-anchor="middle" font-size="13" font-weight="700" fill="#fbbf24">⚙️ Celery Worker — Document Processing Pipeline</text>

  <!-- Pipeline steps inside Celery -->
  <rect x="338" y="330" width="70" height="40" rx="6" fill="#292435" stroke="#7c3aed" stroke-width="1"/>
  <text x="373" y="347" text-anchor="middle" font-size="9" font-weight="600" fill="#c4b5fd">📄 Text</text>
  <text x="373" y="360" text-anchor="middle" font-size="9" fill="#9ca3af">Extract</text>

  <text x="416" y="352" text-anchor="middle" font-size="14" fill="#4b5563">→</text>

  <rect x="425" y="330" width="70" height="40" rx="6" fill="#292435" stroke="#7c3aed" stroke-width="1"/>
  <text x="460" y="347" text-anchor="middle" font-size="9" font-weight="600" fill="#c4b5fd">✂️ Chunk</text>
  <text x="460" y="360" text-anchor="middle" font-size="9" fill="#9ca3af">Split</text>

  <text x="503" y="352" text-anchor="middle" font-size="14" fill="#4b5563">→</text>

  <rect x="512" y="330" width="70" height="40" rx="6" fill="#292435" stroke="#7c3aed" stroke-width="1"/>
  <text x="547" y="347" text-anchor="middle" font-size="9" font-weight="600" fill="#c4b5fd">🔢 Embed</text>
  <text x="547" y="360" text-anchor="middle" font-size="9" fill="#9ca3af">384-dim</text>

  <text x="590" y="352" text-anchor="middle" font-size="14" fill="#4b5563">→</text>

  <rect x="598" y="330" width="60" height="40" rx="6" fill="#292435" stroke="#7c3aed" stroke-width="1"/>
  <text x="628" y="347" text-anchor="middle" font-size="9" font-weight="600" fill="#c4b5fd">🧠 LLM</text>
  <text x="628" y="360" text-anchor="middle" font-size="9" fill="#9ca3af">Summarize</text>

  <!-- Sub-label: HuggingFace model -->
  <text x="547" y="392" text-anchor="middle" font-size="9" fill="#6b7280">HuggingFace: all-MiniLM-L6-v2</text>

  <!-- RAG subsystem inside celery box -->
  <rect x="338" y="400" width="320" height="72" rx="8" fill="#12192b" stroke="#3b82f6" stroke-width="1" stroke-dasharray="4,2"/>
  <text x="498" y="418" text-anchor="middle" font-size="10" font-weight="700" fill="#60a5fa">🔍 RAG Pipeline (Query Time)</text>
  <text x="380" y="435" text-anchor="middle" font-size="9" fill="#9ca3af">Q→Embed</text>
  <text x="415" y="435" text-anchor="middle" font-size="12" fill="#4b5563">→</text>
  <text x="458" y="435" text-anchor="middle" font-size="9" fill="#9ca3af">Vector Search</text>
  <text x="503" y="435" text-anchor="middle" font-size="12" fill="#4b5563">→</text>
  <text x="548" y="435" text-anchor="middle" font-size="9" fill="#9ca3af">Top-K Chunks</text>
  <text x="593" y="435" text-anchor="middle" font-size="12" fill="#4b5563">→</text>
  <text x="636" y="435" text-anchor="middle" font-size="9" fill="#9ca3af">LLM Answer</text>
  <text x="498" y="460" text-anchor="middle" font-size="9" fill="#6b7280">Grounded answers with source references</text>

  <!-- LLM Cloud box -->
  <rect x="720" y="296" width="160" height="80" rx="10" fill="url(#llmGrad)" filter="url(#shadow)"/>
  <text x="800" y="323" text-anchor="middle" font-size="12" font-weight="700" fill="white">🤖 Gemini LLM</text>
  <text x="800" y="340" text-anchor="middle" font-size="9" fill="#fecaca">Google Cloud AI</text>
  <text x="800" y="355" text-anchor="middle" font-size="9" fill="#fecaca">Summarization</text>
  <text x="800" y="368" text-anchor="middle" font-size="9" fill="#fecaca">Q&amp;A Generation</text>

  <!-- Arrow Celery → LLM -->
  <line x1="672" y1="360" x2="718" y2="348" stroke="#ef4444" stroke-width="1.5" stroke-dasharray="4,2" marker-end="url(#arrow)"/>

  <!-- ═══ DATA LAYER ═══ -->
  <!-- MongoDB -->
  <rect x="100" y="510" width="185" height="125" rx="10" fill="url(#dbGrad)" filter="url(#shadow)"/>
  <text x="193" y="535" text-anchor="middle" font-size="12" font-weight="700" fill="white">🍃 MongoDB Atlas</text>
  <text x="193" y="553" text-anchor="middle" font-size="9" fill="#d1fae5">users collection</text>
  <text x="193" y="567" text-anchor="middle" font-size="9" fill="#d1fae5">documents collection</text>
  <text x="193" y="581" text-anchor="middle" font-size="9" fill="#d1fae5">queries collection</text>
  <text x="193" y="595" text-anchor="middle" font-size="9" fill="#a7f3d0">Metadata · Summaries</text>
  <text x="193" y="610" text-anchor="middle" font-size="9" fill="#a7f3d0">User Accounts · Results</text>
  <text x="193" y="625" text-anchor="middle" font-size="9" fill="#6ee7b7">Connection Pooling</text>

  <!-- Chroma DB -->
  <rect x="340" y="510" width="185" height="125" rx="10" fill="#1e2535" stroke="#7c3aed" stroke-width="1.5" filter="url(#shadow)"/>
  <text x="433" y="535" text-anchor="middle" font-size="12" font-weight="700" fill="#c4b5fd">🔮 Chroma DB</text>
  <text x="433" y="553" text-anchor="middle" font-size="9" fill="#a78bfa">Vector Embeddings</text>
  <text x="433" y="567" text-anchor="middle" font-size="9" fill="#a78bfa">384-dim float vectors</text>
  <text x="433" y="581" text-anchor="middle" font-size="9" fill="#a78bfa">Semantic Similarity Search</text>
  <text x="433" y="595" text-anchor="middle" font-size="9" fill="#8b5cf6">Collection: doc-intelligence</text>
  <text x="433" y="610" text-anchor="middle" font-size="9" fill="#8b5cf6">Chunk IDs · Metadata</text>
  <text x="433" y="625" text-anchor="middle" font-size="9" fill="#7c3aed">Chroma Cloud / Local</text>

  <!-- File Storage -->
  <rect x="580" y="510" width="185" height="125" rx="10" fill="#1e2535" stroke="#374151" stroke-width="1.2" filter="url(#shadow)"/>
  <text x="673" y="535" text-anchor="middle" font-size="12" font-weight="700" fill="#d1d5db">📁 File Storage</text>
  <text x="673" y="553" text-anchor="middle" font-size="9" fill="#9ca3af">Raw Document Store</text>
  <text x="673" y="567" text-anchor="middle" font-size="9" fill="#9ca3af">PDF · DOCX · TXT</text>
  <text x="673" y="581" text-anchor="middle" font-size="9" fill="#9ca3af">Local Filesystem</text>
  <text x="673" y="595" text-anchor="middle" font-size="9" fill="#9ca3af">storage/ directory</text>
  <text x="673" y="610" text-anchor="middle" font-size="9" fill="#6b7280">Multipart Upload</text>
  <text x="673" y="625" text-anchor="middle" font-size="9" fill="#6b7280">Type Validation</text>

  <!-- CI/CD box -->
  <rect x="810" y="510" width="150" height="125" rx="10" fill="#1e2535" stroke="#374151" stroke-width="1.2" filter="url(#shadow)"/>
  <text x="885" y="535" text-anchor="middle" font-size="11" font-weight="700" fill="#d1d5db">🚀 DevOps</text>
  <text x="885" y="553" text-anchor="middle" font-size="9" fill="#9ca3af">GitHub Actions CI/CD</text>
  <text x="885" y="567" text-anchor="middle" font-size="9" fill="#9ca3af">Docker Compose</text>
  <text x="885" y="581" text-anchor="middle" font-size="9" fill="#9ca3af">Render Deploy</text>
  <text x="885" y="595" text-anchor="middle" font-size="9" fill="#9ca3af">Pre-commit Hooks</text>
  <text x="885" y="610" text-anchor="middle" font-size="9" fill="#6b7280">LangSmith Tracing</text>
  <text x="885" y="625" text-anchor="middle" font-size="9" fill="#6b7280">Terraform (infra/)</text>

  <!-- Arrows: Workers → Data -->
  <line x1="420" y1="484" x2="260" y2="510" stroke="#34d399" stroke-width="1.5" stroke-dasharray="4,2" marker-end="url(#arrowGreen)"/>
  <text x="308" y="504" font-size="8" fill="#34d399">save metadata</text>

  <line x1="497" y1="484" x2="450" y2="510" stroke="#a78bfa" stroke-width="1.5" stroke-dasharray="4,2" marker-end="url(#arrow)"/>
  <text x="462" y="504" font-size="8" fill="#a78bfa">store vectors</text>

  <line x1="450" y1="273" x2="193" y2="510" stroke="#34d399" stroke-width="1" stroke-dasharray="3,3" opacity="0.6" marker-end="url(#arrowGreen)"/>

  <!-- File upload: FastAPI → Storage -->
  <line x1="510" y1="273" x2="673" y2="510" stroke="#6b7280" stroke-width="1" stroke-dasharray="3,3" opacity="0.6" marker-end="url(#arrow)"/>

  <!-- Legend -->
  <rect x="60" y="658" width="880" height="54" rx="8" fill="#111827" stroke="#1f2937" stroke-width="1"/>
  <text x="90" y="676" font-size="10" fill="#6b7280" font-weight="600">LEGEND:</text>
  <line x1="140" y1="673" x2="175" y2="673" stroke="#60a5fa" stroke-width="1.5" stroke-dasharray="5,3"/>
  <text x="180" y="676" font-size="9" fill="#9ca3af">HTTP Request</text>
  <line x1="260" y1="673" x2="295" y2="673" stroke="#fbbf24" stroke-width="1.5" stroke-dasharray="6,3"/>
  <text x="300" y="676" font-size="9" fill="#9ca3af">Task Dispatch</text>
  <line x1="380" y1="673" x2="415" y2="673" stroke="#34d399" stroke-width="1.5" stroke-dasharray="4,2"/>
  <text x="420" y="676" font-size="9" fill="#9ca3af">DB Write</text>
  <line x1="490" y1="673" x2="525" y2="673" stroke="#a78bfa" stroke-width="1.5" stroke-dasharray="4,2"/>
  <text x="530" y="676" font-size="9" fill="#9ca3af">Vector Write</text>
  <line x1="620" y1="673" x2="655" y2="673" stroke="#ef4444" stroke-width="1.5" stroke-dasharray="4,2"/>
  <text x="660" y="676" font-size="9" fill="#9ca3af">LLM API Call</text>
  <line x1="740" y1="673" x2="775" y2="673" stroke="#7c3aed" stroke-width="1.5"/>
  <text x="780" y="676" font-size="9" fill="#9ca3af">Internal Service</text>

  <!-- Second legend row -->
  <text x="90" y="700" font-size="9" fill="#6b7280">Stack:</text>
  <text x="125" y="700" font-size="9" fill="#60a5fa">Python · FastAPI · Celery · Redis</text>
  <text x="320" y="700" font-size="9" fill="#c4b5fd">·  MongoDB Atlas · Chroma DB  ·</text>
  <text x="495" y="700" font-size="9" fill="#fca5a5">Google Gemini LLM  ·</text>
  <text x="610" y="700" font-size="9" fill="#86efac">HuggingFace Embeddings  ·</text>
  <text x="765" y="700" font-size="9" fill="#94a3b8">Docker · GitHub Actions</text>
</svg>
![architecture](https://github.com/user-attachments/assets/3ce426b7-8035-4ef7-98b2-9be2b5ba0bbc)

> The system is organized into four horizontal layers: **Client**, **API Layer**, **Async Workers**, and **Data Layer**. Each layer communicates through well-defined interfaces, enabling independent scaling and testing.

### Layer Breakdown

**Client Layer** — React/TypeScript frontend, REST clients (cURL/Postman), and Swagger UI at `/docs`.

**API Layer** — FastAPI application with a 7-layer middleware stack (JWT Auth, Rate Limiting, CORS, Security Headers, GZip, Request ID tracing, Structured Logging). Routes are versioned under `/api/v1/`.

**Async Workers Layer** — Celery workers consume tasks from a Redis message broker. The document processing pipeline runs entirely asynchronously: text extraction → chunking → embedding generation → LLM summarization. The RAG pipeline also runs here at query time.

**Data Layer** — Three storage systems: MongoDB Atlas (metadata, user accounts, summaries), Chroma DB (384-dimensional vector embeddings for semantic search), and local filesystem storage (raw uploaded documents).

---

## ✨ Features

- **RAG-based Q&A** — Semantic vector search retrieves top-K chunks before sending context to the LLM, grounding answers in document facts
- **Async Document Processing** — Celery + Redis ensures the API stays responsive while processing runs in the background
- **Multi-format Support** — Ingests PDF, DOCX, and TXT files with automatic content extraction
- **JWT Authentication** — All protected endpoints require a valid Bearer token; bcrypt password hashing for user credentials
- **Rate Limiting** — SlowAPI middleware enforces per-IP rate limits, returning 429 on breach
- **Structured Logging** — Every request gets a UUID; logs are emitted in JSON with full request context
- **Security Headers** — 7 HTTP security headers applied on every response (HSTS, CSP, X-Frame-Options, etc.)
- **Health Checks** — `/health` endpoint verifies connectivity to MongoDB, Redis, Chroma, and filesystem
- **LangSmith Tracing** — Optional LLM call tracing and observability
- **Dockerized** — Full `docker-compose.dev.yml` for one-command local setup
- **CI/CD** — GitHub Actions workflow for linting, testing, and deployment
- **Render Deployment** — `render.yaml` config for cloud deployment out of the box

---

## 🛠️ Tech Stack

### Backend

| Technology | Role |
|---|---|
| **Python 3.10+** | Core language |
| **FastAPI** | Async REST API framework |
| **Pydantic** | Request/response validation and settings management |
| **Celery** | Distributed async task queue |
| **Redis** | Celery message broker + session/cache store |
| **Uvicorn** | ASGI server |
| **SlowAPI** | Rate limiting middleware |
| **python-jose** | JWT token generation and validation |
| **passlib + bcrypt** | Password hashing |
| **structlog** | Structured JSON logging |

### AI / ML

| Technology | Role |
|---|---|
| **Google Gemini** | LLM for summarization and Q&A generation |
| **HuggingFace `all-MiniLM-L6-v2`** | Sentence embedding model (384-dim vectors) |
| **LangChain** | RAG pipeline orchestration |
| **LangSmith** | LLM call tracing and observability |
| **Chroma DB** | Vector database for semantic similarity search |

### Document Processing

| Technology | Role |
|---|---|
| **PyMuPDF / pdfplumber** | PDF text extraction |
| **docx2txt / python-docx** | DOCX text extraction |
| **LangChain TextSplitter** | Semantic document chunking |

### Storage & Database

| Technology | Role |
|---|---|
| **MongoDB Atlas** | User accounts, document metadata, query history |
| **Chroma DB** | Vector embeddings (cloud or local persistence) |
| **Local Filesystem** | Raw uploaded document files (`storage/`) |

### DevOps & Infrastructure

| Technology | Role |
|---|---|
| **Docker & Docker Compose** | Containerized development environment |
| **GitHub Actions** | CI/CD pipeline (lint, test, deploy) |
| **Render** | Cloud deployment target (`render.yaml`) |
| **Terraform (HCL)** | Infrastructure-as-code (`infra/`) |
| **Pre-commit** | Git hooks for code quality enforcement |

---

## 📁 Project Structure

```
Document-Summarizer-Agent/
│
├── api/                        # FastAPI route definitions
│   ├── v1/
│   │   ├── auth.py             # /auth/register, /auth/login
│   │   ├── documents.py        # /documents/upload, /documents/{id}
│   │   ├── query.py            # /documents/{id}/query
│   │   ├── search.py           # /search
│   │   └── analytics.py        # /analytics
│
├── app/                        # Core application logic
│   ├── main.py                 # FastAPI app init, middleware registration
│   ├── dependencies.py         # FastAPI Depends() injectors
│   └── middleware/             # Custom middleware (logging, rate limit, etc.)
│
├── tasks/                      # Celery background tasks
│   ├── worker.py               # Celery app definition
│   ├── document_tasks.py       # Text extract, chunk, embed, summarize
│   └── embedding_tasks.py      # Vector generation tasks
│
├── models/                     # Pydantic & MongoDB models
│   ├── user.py                 # User schema
│   ├── document.py             # Document schema
│   └── query.py                # Query/response schema
│
├── config/                     # Configuration management
│   ├── settings.py             # Pydantic settings (reads .env)
│   └── .env.example            # Environment variable template
│
├── chroma_db/                  # Chroma vector DB local storage/config
│
├── frontend/                   # React + TypeScript UI
│   ├── src/
│   │   ├── components/         # UI components
│   │   ├── pages/              # Page views
│   │   └── api/                # API client calls
│   ├── package.json
│   └── tsconfig.json
│
├── storage/                    # Uploaded document files (raw)
│
├── infra/                      # Terraform infrastructure configs
│
├── scripts/                    # Utility scripts (health checks, migrations)
│
├── tests/                      # Automated test suite
│   ├── test_api.py             # API route tests
│   └── local_test_client.py    # In-process FastAPI TestClient
│
├── docs/                       # Extended documentation
│   ├── API_TESTING_WITH_CURL.sh
│   ├── API_Testing_PowerShell.ps1
│   └── Postman_Collection.json
│
├── .github/workflows/          # GitHub Actions CI/CD
├── docker-compose.dev.yml      # Development Docker Compose
├── render.yaml                 # Render deployment config
├── .pre-commit-config.yaml     # Pre-commit hooks
└── run.py                      # Application entry point
```

---

## 🔄 Data Flow

### 1. Document Upload Flow

```
User (POST /api/v1/documents/upload)
    │
    ├─▶ [JWT Auth Middleware] — validate Bearer token
    ├─▶ [Rate Limit Middleware] — check request quota
    ├─▶ File Validation — check MIME type (PDF/DOCX/TXT)
    ├─▶ Save file → storage/ directory
    ├─▶ Create document record in MongoDB (status: "processing")
    ├─▶ Dispatch Celery task (document_id)
    └─▶ Return 202 Accepted + document_id

Celery Worker picks up task:
    ├─▶ Extract raw text (PyMuPDF / docx2txt)
    ├─▶ Clean & normalize text
    ├─▶ Split into semantic chunks (LangChain TextSplitter)
    ├─▶ Generate 384-dim embeddings per chunk (HuggingFace)
    ├─▶ Upsert vectors into Chroma DB
    ├─▶ Send chunks to Gemini LLM → generate summary
    └─▶ Update MongoDB document record (status: "ready", summary saved)
```

### 2. RAG Query Flow

```
User (POST /api/v1/documents/{id}/query)
    │  Body: { "question": "What are the key findings?" }
    │
    ├─▶ [Auth + Rate Limit Middleware]
    ├─▶ Embed the user question (HuggingFace)
    ├─▶ Run semantic similarity search in Chroma DB
    ├─▶ Retrieve Top-K relevant chunks
    ├─▶ Assemble context window from chunks
    ├─▶ Construct prompt: context + question → Gemini LLM
    ├─▶ Receive LLM-generated answer
    ├─▶ Save query + answer to MongoDB (queries collection)
    └─▶ Return 200 OK + { answer, sources }
```

### 3. Authentication Flow

```
User (POST /api/v1/auth/register)
    ├─▶ Validate email uniqueness in MongoDB
    ├─▶ Hash password with bcrypt
    └─▶ Create user document → return user_id

User (POST /api/v1/auth/login)
    ├─▶ Lookup user by email in MongoDB
    ├─▶ Verify password hash
    ├─▶ Generate JWT (signed, with expiry)
    └─▶ Return access_token

Protected requests:
    ├─▶ Extract Bearer token from Authorization header
    ├─▶ Verify JWT signature + expiry
    └─▶ Populate request context with user_id
```

---

## 🔌 API Endpoints

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| `POST` | `/api/v1/auth/register` | ❌ | Register a new user |
| `POST` | `/api/v1/auth/login` | ❌ | Login and receive JWT |
| `POST` | `/api/v1/documents/upload` | ✅ | Upload a document for processing |
| `GET` | `/api/v1/documents` | ✅ | List all user documents |
| `GET` | `/api/v1/documents/{id}` | ✅ | Get document metadata |
| `GET` | `/api/v1/documents/{id}/summary` | ✅ | Retrieve generated summary |
| `POST` | `/api/v1/documents/{id}/query` | ✅ | Ask a question (RAG) |
| `GET` | `/api/v1/documents/{id}/queries` | ✅ | Get query history for document |
| `DELETE` | `/api/v1/documents/{id}` | ✅ | Delete document and vectors |
| `GET` | `/api/v1/search` | ✅ | Semantic search across documents |
| `GET` | `/api/v1/analytics` | ✅ | Usage analytics |
| `GET` | `/health` | ❌ | System health check (all services) |
| `GET` | `/docs` | ❌ | Swagger interactive API docs |
| `GET` | `/redoc` | ❌ | ReDoc API reference |

---

## 🗄️ Database Schema

### MongoDB — `users` collection

```json
{
  "_id": "ObjectId",
  "email": "string (unique)",
  "hashed_password": "string (bcrypt)",
  "full_name": "string",
  "created_at": "datetime",
  "updated_at": "datetime",
  "is_active": "boolean"
}
```

### MongoDB — `documents` collection

```json
{
  "_id": "ObjectId",
  "user_id": "ObjectId (ref: users)",
  "filename": "string",
  "content_type": "string",
  "file_path": "string",
  "text_content": "string",
  "summary": "string",
  "chunk_count": "integer",
  "status": "processing | ready | failed",
  "created_at": "datetime",
  "metadata": {
    "page_count": "integer",
    "word_count": "integer",
    "language": "string"
  }
}
```

### MongoDB — `queries` collection

```json
{
  "_id": "ObjectId",
  "user_id": "ObjectId (ref: users)",
  "document_id": "ObjectId (ref: documents)",
  "question": "string",
  "answer": "string",
  "context_chunks": ["string"],
  "model_used": "string",
  "created_at": "datetime",
  "response_time_ms": "integer",
  "tokens_used": "integer"
}
```

### Chroma DB — `document-intelligence` collection

```
ids:        [string]          → chunk-level unique identifiers
embeddings: [[float x 384]]   → HuggingFace all-MiniLM-L6-v2 vectors
documents:  [string]          → raw chunk text
metadatas:  [{
  document_id:  string,
  chunk_index:  integer,
  source:       string
}]
```

---

## 🔐 Security Architecture

The platform applies security at every layer:

**Authentication** — JWT-based Bearer tokens required on all `/api/v1/*` routes. Tokens carry expiry and are validated on every request by the `HTTPBearer` middleware.

**Password Security** — Passwords are hashed with bcrypt before storage. Raw passwords are never persisted.

**Rate Limiting** — SlowAPI enforces per-IP request limits. Requests exceeding the threshold receive HTTP 429.

**HTTP Security Headers** — Applied globally on every response:

```
X-Content-Type-Options:        nosniff
X-Frame-Options:               SAMEORIGIN
X-XSS-Protection:              1; mode=block
Strict-Transport-Security:     max-age=31536000; includeSubDomains
Content-Security-Policy:       default-src 'self'; script-src 'self' 'unsafe-inline'
Referrer-Policy:               strict-origin-when-cross-origin
Permissions-Policy:            geolocation=(), microphone=(), camera=()
```

**CORS** — Configurable allowed origins. Credentials are supported for frontend integration.

**Input Validation** — All request bodies are validated via Pydantic models before any processing begins.

---

## 🚀 Getting Started

### Prerequisites

- Python 3.10+
- Docker & Docker Compose
- Node.js 18+ (for frontend)
- A MongoDB Atlas account (or local MongoDB)
- A Redis instance (local, Docker, or Redis Cloud)
- A Google Gemini API key
- A Chroma DB account (or local Chroma)

---

## ⚙️ Environment Variables

Create a `.env` file in the `config/` directory. Use `config/.env.example` as a template:

```env
# Application
APP_ENV=development
SECRET_KEY=your-very-secret-jwt-key-here
ACCESS_TOKEN_EXPIRE_MINUTES=60

# MongoDB
MONGO_URI=mongodb+srv://<user>:<password>@cluster.mongodb.net/
MONGO_DB_NAME=document_summarizer

# Redis
REDIS_URL=redis://localhost:6379/0

# Chroma DB
CHROMA_PERSIST_PATH=./chroma_db
# For Chroma Cloud:
# CHROMA_API_KEY=ck-xxxx
# CHROMA_TENANT=your-tenant
# CHROMA_DATABASE=your-database

# LLM (Google Gemini)
LLM_PROVIDER=gemini
GEMINI_API_KEY=your-gemini-api-key-here
GEMINI_MODEL=gemini-pro

# Embeddings
EMBEDDING_MODEL=all-MiniLM-L6-v2

# LangSmith (optional observability)
LANGCHAIN_TRACING_V2=true
LANGCHAIN_API_KEY=your-langsmith-key
LANGCHAIN_PROJECT=document-summarizer-agent

# Storage
UPLOAD_DIR=./storage
MAX_FILE_SIZE_MB=50
```

---

## 🐳 Running with Docker

The fastest way to get the full stack running locally:

```bash
# 1. Clone the repository
git clone https://github.com/Aka-Nine/Document-Summarizer-Agent.git
cd Document-Summarizer-Agent

# 2. Set up environment variables
cp config/.env.example config/.env
# Edit config/.env with your API keys

# 3. Build and start all services
docker-compose -f docker-compose.dev.yml up --build

# Services started:
# - FastAPI API         → http://localhost:8000
# - Swagger UI          → http://localhost:8000/docs
# - Redis               → localhost:6379
# - Celery Worker       → background process
```

To run in detached mode:

```bash
docker-compose -f docker-compose.dev.yml up --build -d
```

To view logs:

```bash
docker-compose -f docker-compose.dev.yml logs -f
```

---

## 💻 Running Locally (Without Docker)

### Step 1 — Install Python dependencies

```bash
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### Step 2 — Start Redis

```bash
# macOS
brew install redis && brew services start redis

# Ubuntu/Debian
sudo apt install redis-server && sudo service redis start

# Windows — use WSL or Docker:
docker run -d -p 6379:6379 redis:alpine
```

### Step 3 — Start MongoDB

Either use MongoDB Atlas (set `MONGO_URI` in `.env`) or run locally:

```bash
docker run -d -p 27017:27017 mongo:6
```

### Step 4 — Start the Celery Worker

```bash
# Linux / macOS
celery -A tasks.worker worker --loglevel=info

# Windows (use solo pool to avoid multiprocessing issues)
celery -A tasks.worker worker --loglevel=info --pool=solo
```

### Step 5 — Start the FastAPI Server

```bash
python run.py
# API available at: http://localhost:8000
# Swagger UI at:    http://localhost:8000/docs
```

### Step 6 — (Optional) Start the Frontend

```bash
cd frontend
npm install
npm run dev
# Frontend at: http://localhost:3000
```

---

## 🧪 Testing

The project includes five testing approaches:

### 1. Python Test Suite

```bash
pytest tests/test_api.py -v
```

Covers: user registration, login, document upload, document retrieval, RAG queries, query history, auth errors, rate limiting, and health checks.

### 2. FastAPI TestClient (in-process, fastest)

```bash
python tests/local_test_client.py
```

### 3. cURL Examples

```bash
# Register
curl -X POST http://localhost:8000/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email": "user@example.com", "password": "secret", "full_name": "Jane Doe"}'

# Login and capture token
TOKEN=$(curl -s -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email": "user@example.com", "password": "secret"}' | jq -r '.access_token')

# Upload a document
curl -X POST http://localhost:8000/api/v1/documents/upload \
  -H "Authorization: Bearer $TOKEN" \
  -F "file=@/path/to/your/document.pdf"

# Query a document
curl -X POST http://localhost:8000/api/v1/documents/{document_id}/query \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"question": "What is the main conclusion of this document?"}'
```

More examples in `docs/API_TESTING_WITH_CURL.sh`.

### 4. PowerShell (Windows)

```powershell
# Run the provided test script
.\docs\API_Testing_PowerShell.ps1
```

### 5. Postman Collection

Import `docs/Postman_Collection.json` directly into Postman for a complete, ready-to-use API collection with environment variable support.

---

## ☁️ Deployment

### Render (Recommended)

The repository includes a `render.yaml` for one-click deployment:

```bash
# Push to GitHub, then connect repo in Render dashboard
# render.yaml handles service definitions automatically
```

### Manual Deployment Checklist

- [ ] Set all environment variables in production secrets manager
- [ ] Use MongoDB Atlas (not local) for production
- [ ] Use Redis Cloud for production broker/cache
- [ ] Use Chroma Cloud or a managed vector DB
- [ ] Set up SSL/TLS via a reverse proxy (Nginx/Caddy)
- [ ] Configure `ALLOWED_HOSTS` and `CORS_ORIGINS` for production domains
- [ ] Set `APP_ENV=production` to disable debug features
- [ ] Enable LangSmith tracing for LLM observability
- [ ] Set up uptime monitoring on `/health` endpoint

---

## 📈 Performance

| Operation | Typical Response Time |
|---|---|
| Health check | < 10 ms |
| User login | 50 – 100 ms |
| Document list | 100 – 200 ms |
| Vector similarity search | 200 – 500 ms |
| RAG query (end-to-end) | 2 – 5 seconds |
| Document processing (async) | 5 – 30 seconds (background) |

The API itself never blocks on document processing — Celery handles that asynchronously. The `/health` endpoint confirms readiness of all backing services.

---

## ⚠️ Known Limitations

- Large documents (100+ pages) significantly increase Celery processing time
- LLM token costs scale with document size; long documents consume more Gemini quota
- Chroma DB in local mode does not support horizontal scaling (use Chroma Cloud for multi-instance deployments)
- Current deployment is single-node; add a load balancer + multiple Uvicorn workers for high traffic
- No streaming responses yet — the LLM response is returned all at once

---

## 🔮 Roadmap

- [ ] **Streaming Summaries** — Stream LLM responses token-by-token via SSE
- [ ] **Multi-document Querying** — RAG across a corpus of documents simultaneously
- [ ] **User Authentication Tiers** — Free / Pro usage quotas
- [ ] **Cloud Vector DB Support** — Pinecone, Weaviate, Qdrant adapters
- [ ] **Improved Frontend UX** — Upload progress, real-time processing status
- [ ] **Query Caching** — Redis-based response cache for frequently asked questions
- [ ] **Batch Upload** — Process multiple documents in a single request
- [ ] **Export** — Download summaries as PDF or DOCX
- [ ] **Webhook Notifications** — Notify clients when async processing completes

---

## 🤝 Contributing

Contributions are welcome! To get started:

```bash
# 1. Fork the repo and clone your fork
git clone https://github.com/<your-username>/Document-Summarizer-Agent.git

# 2. Create a feature branch
git checkout -b feature/your-feature-name

# 3. Install pre-commit hooks
pip install pre-commit
pre-commit install

# 4. Make your changes and run tests
pytest tests/ -v

# 5. Commit and push
git commit -m "feat: describe your change"
git push origin feature/your-feature-name

# 6. Open a Pull Request
```

Please ensure your code passes linting (`pre-commit run --all-files`) and all tests pass before opening a PR.

---

## 📜 License

This project is licensed under the [MIT License](LICENSE).

---

## 🙏 Acknowledgements

- [FastAPI](https://fastapi.tiangolo.com/) — the async API framework that powers the backend
- [LangChain](https://python.langchain.com/) — RAG pipeline orchestration
- [Chroma DB](https://www.trychroma.com/) — fast, developer-friendly vector database
- [HuggingFace](https://huggingface.co/) — `all-MiniLM-L6-v2` embedding model
- [Google Gemini](https://deepmind.google/technologies/gemini/) — LLM powering summaries and Q&A
- [MongoDB Atlas](https://www.mongodb.com/atlas) — managed database layer
- [Celery](https://docs.celeryq.dev/) — distributed task queue

---

<div align="center">

**Built with ❤️ — combining async systems, vector search, LLM orchestration, and scalable backend architecture.**

[⭐ Star this repo](https://github.com/Aka-Nine/Document-Summarizer-Agent) · [🐛 Report a bug](https://github.com/Aka-Nine/Document-Summarizer-Agent/issues) · [💡 Request a feature](https://github.com/Aka-Nine/Document-Summarizer-Agent/issues)

</div>
