# AI Contact Recognition

> Turn any printed contact source — business cards, event posters, flyers, banners, billboards — into structured, searchable digital contacts in seconds.

![Python](https://img.shields.io/badge/Python-3.14-3776AB?logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-0.136-009688?logo=fastapi&logoColor=white)
![LangChain](https://img.shields.io/badge/LangChain-1.3-1C3C3C?logo=langchain&logoColor=white)
![MongoDB](https://img.shields.io/badge/MongoDB-8-47A248?logo=mongodb&logoColor=white)
![Vue](https://img.shields.io/badge/Vue-3.5-42B883?logo=vuedotjs&logoColor=white)
![Vite](https://img.shields.io/badge/Vite-8-646CFF?logo=vite&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-Compose-2496ED?logo=docker&logoColor=white)
![License](https://img.shields.io/badge/License-Not%20specified-lightgrey)

---

## About The Project

**AI Contact Recognition** is a full-stack, production-oriented application that uses a **Vision Large Language Model** to automatically parse contact information from images such as business cards, event posters, flyers, banners, and billboards. It targets sales teams, event organizers, and anyone who digitizes offline networking materials, removing the manual data-entry burden of CRM and contact management workflows.

Upload an image, review and correct the AI-extracted result, and persist it as a structured contact card — complete with company info, positions, services, addresses, and unified digital contact methods — hosted in the cloud and searchable in a gallery-style web UI.

---

## Key Tech Stack

**Backend**

- **Python 3.14+** & **FastAPI 0.136** — async REST API
- **LangChain 1.3** + **langchain-groq 1.1** — orchestration of the **Llama-4-Scout-17B** Vision LLM (Groq) with Pydantic structured output
- **Pydantic 2 / pydantic-settings** — schema validation & typed configuration
- **Dishka 1.10** — async dependency injection container
- **Uvicorn** — ASGI server
- **Poetry + pre-commit (Ruff)** — dependency management & code quality

**Database & Storage**

- **MongoDB 8** — document store for contact cards (`pymongo` `AsyncMongoClient`)
- **Cloudinary** — CDN image hosting for uploaded card images

**Frontend**

- **Vue 3.5** + **TypeScript** + **Vite 8**
- **Tailwind CSS 4** + **reka-ui** — shadcn-style component library
- **yup** — form validation, **vue-sonner** — toasts, **@vueuse/core** — debounced search

**DevOps / Deployment**

- **Docker + Docker Compose** (multi-stage builds, healthchecks, volume persistence)
- **nginx-style static serving** via `serve` for the SPA

---

## Core Features

- **AI-powered contact extraction** — Vision LLM (Llama-4-Scout via Groq) parses images into a structured Pydantic schema with hallucination-resistant prompting rules.
- **Unified digital contact model** — all phone/email/website/social handles normalized into a typed `digital_contacts` list (phone, email, website, telegram, linkedin, whatsapp, viber, instagram, facebook, x, vk…).
- **Image integrity validation** — Pillow-based verification before extraction and before persistence.
- **Cloudinary image hosting** — secure CDN URLs stored with each card.
- **Full CRUD API** — create, list (paginated + multi-word search), read, update (partial PATCH), and delete contact cards.
- **Multi-word search** — case-insensitive regex across company and person name fields.
- **Modern SPA UI** — card gallery grid, skeletons/spinners, detail & edit modals, dynamic formsets for repeatable fields (positions, services, addresses, digital contacts), per-type input validation, and debounced search.
- **Consistent API error model** — typed HTTP exceptions with auto-generated OpenAPI examples.
- **Structured logging** — convention-enforcing logger with uniform `executing…` / `finished.` message formats.

---

## Architecture & Engineering Highlights

- **Clean Architecture layering** — `presentation` (API routers) → `services` (usecase interactors + abstract interfaces) → `infrastructure` (MongoDB repository, Cloudinary adapter) → `core` (schemas, config, exceptions). Dependency rule enforced via abstract boundaries in `src/services/interfaces.py`.
- **Interface segregation & inversion of control** — every dependency (extractor, cloudinary, repository) is behind an ABC and wired through **Dishka** DI with `APP` scope singletons, keeping modules decoupled and testable.
- **Structured LLM output** — `with_structured_output(ContactExtractionSchema)` enforces JSON adherence to the Pydantic schema at the model level, with explicit anti-hallucination and field-placement rules in the system prompt.
- **Async everywhere** — `AsyncMongoClient` for non-blocking DB access; blocking Cloudinary SDK calls are wrapped with `asyncio.to_thread` to preserve async compliance.
- **First-class error handling** — a custom `DefaultHTTPException` hierarchy with metaclass-enforced abstract fields, centralized exception handlers, and an `ExamplesGenerator` that automatically injects accurate error examples into the OpenAPI docs for every endpoint.
- **Pagination & search** — cursor-based `skip/limit` pagination sorted by `created_at` desc, plus word-wise `$and/$or` regex search.
- **Config as code** — `pydantic-settings` singleton with `.env` support and typed defaults (Groq, MongoDB, Cloudinary, server binding).

---

## Quick Start / Getting Started

### Prerequisites

- **Python 3.14+** and **Poetry**
- **Node.js 22+** and **pnpm** (for frontend development)
- **Docker** + **Docker Compose**
- A **Groq API key** (https://console.groq.com)
- A **Cloudinary** account (cloud name, API key, API secret)

### 1. Clone & configure environment variables

```bash
git clone <repository-url>
cd ai-contact-recognition
cp backend/.env.example backend/.env
```

Edit `backend/.env` and fill in at least:

```env
GROQ_API_KEY=your_groq_api_key_here
CLOUDINARY_CLOUD_NAME=your_cloudinary_cloud_name_here
CLOUDINARY_API_KEY=your_cloudinary_api_key_here
CLOUDINARY_API_SECRET=your_cloudinary_api_secret_here
```

### 2. Run with Docker Compose (recommended)

```bash
docker-compose up --build
```

This starts three services:

| Service   | Container port | Exposed port |
| --------- | -------------- | ------------ |
| MongoDB   | 27017          | 27018        |
| Backend   | 8000           | 9211         |
| Frontend  | 80             | 9210         |

- **Web UI:** http://localhost:9210
- **API:** http://localhost:9211
- **Swagger UI:** http://localhost:9211/docs
- **ReDoc:** http://localhost:9211/redoc

### 3. Local development (backend)

```bash
cd backend
make install      # poetry install + pre-commit hooks
make run          # uvicorn dev server on http://127.0.0.1:9211
```

Useful `make` targets: `make lint`, `make format`, `make clean`.

### 4. Local development (frontend)

```bash
cd frontend
pnpm install
pnpm dev
```

---

## API Endpoints Overview

| Method | Endpoint           | Description                                                       |
| ------ | ------------------ | ----------------------------------------------------------------- |
| `POST` | `/contacts/extract` | Upload an image and extract structured contact info via Vision LLM (no persistence) |
| `POST` | `/contacts`         | Save a contact card (base64 image → Cloudinary, data → MongoDB)    |
| `GET`  | `/contacts`         | Paginated list of scanned cards (`page`, `limit`, `search` params) |
| `GET`  | `/contacts/{card_id}` | Fetch full extracted details for one card                         |
| `PATCH`| `/contacts/{card_id}` | Partially update a card (optionally re-upload a new image)        |
| `DELETE` | `/contacts/{card_id}` | Permanently delete a card                                        |

Interactive OpenAPI documentation is available at **`/docs`** (Swagger UI) and **`/redoc`** (ReDoc) once the backend is running.

---

## Future Roadmap

- **Authentication & multi-tenant workspaces** — add JWT/OAuth2 auth with per-user contact libraries to make the system enterprise-ready.
- **Test & CI/CD hardening** — unit/integration test suites (pytest for usecases + repositories, Vitest/Vue Test Utils for the UI) and a GitHub Actions pipeline for lint, test, and Docker image publishing.
- **Advanced search & retrieval** — introduce full-text/Atlas Search indexes and fuzzy matching (e.g., phone/email normalization) to replace regex scans on large datasets, plus optional background OCR caching and LLM rate-limit retry/backoff.

---

## License

No license has been specified for this repository.
