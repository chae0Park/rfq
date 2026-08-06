# PromptOps

> **An AI-powered RFQ Automation Platform for Market Research Operations**

PromptOps automates the RFQ (Request for Quotation) workflow by extracting information from client emails, validating project requirements, generating quotations, supporting human approval, and creating professional email drafts.

---

## Workflow

```text
Client Email
      ↓
RFQ Extraction
      ↓
Validation
      ↓
Quotation Engine
      ↓
GPT Price Review
      ↓
Human Approval
      ↓
Draft Email
      ↓
Dashboard
```

---

## Architecture

```text
Next.js Dashboard
        │
        ▼
FastAPI Backend
        │
 ┌──────┼────────┐
 ▼      ▼        ▼
PostgreSQL   OpenAI API   Business Rules
        │
        ▼
Quotation Engine
        │
        ▼
Email Draft
```

---

## Key Features

* 📧 Extract RFQ information from client emails using LLM
* ✅ Validate required project information
* 💰 Generate quotations with configurable pricing rules
* 🤖 Review quotation with GPT
* 👤 Human approval workflow
* ✉️ Generate professional client-ready email drafts
* 📊 Dashboard for RFQ management and review

---

## Tech Stack

| Category   | Technologies                        |
| ---------- | ----------------------------------- |
| Frontend   | Next.js, TypeScript                 |
| Backend    | FastAPI, Python                     |
| Database   | PostgreSQL                          |
| AI         | OpenAI API                          |
| Deployment | Docker, Railway, Vercel *(Planned)* |
| Automation | n8n, Gmail, Slack *(Planned)*       |

---

## Screenshots

### Dashboard

> **Insert Dashboard Screenshot Here**

---

### RFQ Detail

> **Insert RFQ Detail Screenshot Here**

---

### Draft Email Preview

> **Insert Draft Email Preview Screenshot Here**

---

## Quick Start

```bash
git clone https://github.com/<your-username>/promptops.git

cd promptops

docker compose up --build
```

Backend

```
http://localhost:8000/docs
```

Frontend

```
http://localhost:3000
```

---

## Roadmap

* [x] RFQ Extraction
* [x] Validation
* [x] Quotation Engine
* [x] Human Approval
* [x] Draft Email Generation
* [x] Dashboard
* [x] Docker
* [x] Deployment (Railway / Vercel)
* [ ] n8n Workflow
* [ ] Gmail Integration
* [ ] Slack Notification
