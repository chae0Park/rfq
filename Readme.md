# RFQ Automation

> **An AI-assisted RFQ Automation Platform for Market Research Operations**

RFQ Automation is an end-to-end RFQ (Request for Quotation) automation system designed to reduce repetitive manual work in market research operations.

The system processes incoming client RFQ emails, extracts structured project requirements using an LLM, validates required information, calculates quotations using deterministic pricing rules, compares generated prices against market benchmark data, routes quotations through human approval, and generates client-ready Gmail drafts.

It also supports incomplete RFQs across multiple emails in the same Gmail thread, allowing missing information to be requested and later merged into the existing RFQ.

The project focuses on combining **LLM-assisted automation with deterministic business logic, human-in-the-loop controls, evaluation, and operational monitoring**.

---

## Problem

RFQ processing in market research operations often requires manually:

- Reading incoming client emails
- Extracting project specifications
- Checking whether required information is missing
- Following up with clients for missing information
- Calculating project costs
- Reviewing whether the quotation looks reasonable
- Getting internal approval
- Preparing a client response
- Tracking the RFQ throughout the process

RFQ information also does not always arrive in a single complete email. Clients may provide missing project details through later replies, requiring operators to track and consolidate information across an email thread.

These repetitive steps increase processing time and create opportunities for manual errors.

RFQ Automation automates this workflow while keeping pricing calculations, benchmark references, and final approval under explicit operational control.

---

## Workflow

![WORKFLOW](backend/docs/images/workflow.png)

The workflow follows the RFQ lifecycle from email intake to a human-reviewed client response:

```text
Client Email
     ↓
Gmail / n8n
     ↓
RFQ Detection & Thread Routing
     ↓
LLM Structured Extraction
     ↓
Validation
     │
     ├── Missing Required Information
     │       ↓
     │   Clarification
     │       ↓
     │   WAITING_FOR_CLIENT
     │       ↓
     │   Same-thread Client Reply
     │       ↓
     │   Existing RFQ Updated
     │       └──────────────→ Validation
     │
     ▼
Deterministic Quotation Engine
     ↓
Market Benchmark Price Review
     ↓
Human Approval
     ↓
Workflow Resume
     ↓
Client-ready Email Generation
     ↓
Gmail Draft
     ↓
Operator Notification
```

---

## Architecture

```text
                         Gmail
                           │
                           ▼
                          n8n
                  Workflow Orchestration
                           │
                           ▼
                    FastAPI Backend
                           │
        ┌──────────────────┼──────────────────┐
        │                  │                  │
        ▼                  ▼                  ▼
   OpenAI API        Business Logic      PostgreSQL
        │                  │             / Supabase
        │           ┌──────┴──────┐
        │           │             │
        ▼           ▼             ▼
 RFQ Extraction  Quotation    Market Price
                   Engine        Review
                     │             │
                     │             ▼
                     │       Market Benchmark
                     │             Data
                     │
                     └─────────────┐
                                   │
                                   ▼
                           Next.js Dashboard
                                   │
                                   ▼
                            Human Approval
                                   │
                                   ▼
                           Workflow Resume
                                   │
                                   ▼
                           Email Generation
                                   │
                                   ▼
                              Gmail Draft
```

### Design Principle

RFQ Automation deliberately separates **probabilistic AI tasks** from **deterministic business logic**.

LLMs are used for:

- Understanding unstructured RFQ emails
- Converting email content into structured RFQ data
- Drafting client communication

Deterministic software is used for:

- RFQ validation
- Pricing calculations
- Cost multipliers
- Fees and margins
- Currency conversion
- Market benchmark comparison
- Workflow state handling
- Gmail thread-based RFQ matching

Humans retain control over:

- Correcting extracted information
- Reviewing quotation and benchmark results
- Approving or rejecting quotations
- Reviewing client-facing communication

> **AI interprets. Software calculates. Humans decide.**

---

## Key Features

### AI-assisted RFQ Extraction

Incoming RFQ emails are converted into structured data using the OpenAI API with structured outputs.

Extracted fields include:

- Country / Countries
- Sample Size
- Target Audience
- LOI
- Incidence Rate
- Methodology
- Timeline
- Programming Requirements
- Translation Requirements
- Languages
- Rush Requirements
- Client Information
- Currency

The system supports RFQ information arriving across multiple emails in the same Gmail thread.

The Gmail thread identifier is used to locate an existing RFQ so that newly provided information can be merged into the same record rather than creating duplicate RFQs.

---

### RFQ Detection, Validation & Clarification

Incoming emails are first routed through the n8n workflow to determine whether they should enter RFQ processing and whether they belong to an existing RFQ thread.

Required project information is then validated before quotation generation.

When required information is missing:

1. The missing fields are identified.
2. Clarification is requested from the client.
3. The RFQ is marked as `WAITING_FOR_CLIENT`.
4. Processing pauses while waiting for additional information.
5. A reply in the same Gmail thread triggers a new workflow execution.
6. The backend finds the existing RFQ using the Gmail thread identifier.
7. Newly extracted information is merged into the existing RFQ.
8. Once the required information is complete, the RFQ can continue through quotation processing.

This allows incomplete RFQs to be progressively completed without restarting the workflow or creating duplicate requests.

---

### Deterministic Quotation Engine

Quotation calculation is handled through explicit Python business rules rather than an LLM.

Pricing components include:

- Country base cost
- Panel CPI
- Sample size
- LOI multiplier
- IR multiplier
- Programming fee
- Translation fee
- Project management fee
- Rush fee
- Margin
- Client discount
- Currency conversion
- Multi-country pricing

This keeps financial calculations predictable, reproducible, and auditable.

When optional pricing inputs such as LOI or IR are unavailable, the quotation engine applies defined fallback behavior rather than failing the workflow.

These values can later be reviewed or added by an operator through the dashboard, after which the quotation can be recalculated using the same deterministic pricing rules.

---

### Market Benchmark Price Review

After the quotation engine generates a price, the calculated quotation is compared against stored market benchmark data.

Benchmark matching considers project attributes such as:

- Country
- Sample size
- LOI
- Incidence rate
- Programming requirements
- Translation requirements
- Rush requirements

The review classifies a quotation as:

- `BELOW_BENCHMARK`
- `WITHIN_BENCHMARK`
- `ABOVE_BENCHMARK`
- `NO_BENCHMARK`

When sufficient information is not available to select an appropriate benchmark, the system returns `NO_BENCHMARK` rather than forcing an arbitrary comparison.

The benchmark review does **not** determine or modify the quotation itself. It provides an additional reference point for human review.

#### Benchmark Governance

Market benchmark data is treated as **controlled reference data**, rather than being automatically updated from every newly processed RFQ.

New RFQ and quotation records do not automatically become future pricing benchmarks. This prevents individual or anomalous quotations from immediately influencing subsequent price reviews.

For production use, new quotation records can instead provide evidence for periodic benchmark reviews. A team can evaluate historical quotations alongside market conditions and operational experience before agreeing on changes to the benchmark dataset.

```text
New RFQ & Quotation Records
            ↓
Historical Pricing Evidence
            ↓
Periodic Team Review
            ↓
Agreed Benchmark Update
            ↓
Market Benchmark Dataset
            ↓
Future RFQ Reviews
```

This keeps changes to pricing reference data under explicit human governance.

---

### Human-in-the-Loop Approval

Quotation decisions require explicit human review.

Users can:

- Review RFQ information
- Inspect the calculated quotation
- Review market benchmark results
- Correct RFQ information
- Approve or reject the quotation
- Add reviewer comments

For the approval workflow, n8n stores a workflow resume URL and pauses execution while waiting for the operator's decision.

```text
Quotation + Benchmark Review
            ↓
Save Workflow Resume URL
            ↓
Slack Approval Notification
            ↓
Wait for Human Approval
          ↙   ↘
      Reject   Approve
        ↓         ↓
       End    Resume Workflow
                  ↓
           Generate Draft
```

Only an approved quotation proceeds to client email generation.

This prevents fully autonomous client-facing pricing decisions.

---

### RFQ Editing & Recalculation

Extracted RFQ values can be corrected from the dashboard.

When pricing-related fields such as LOI or IR are modified, the updated RFQ is passed back through the deterministic quotation engine and the quotation is recalculated.

This allows human operators to:

- Correct extraction results
- Add internally determined values
- Reflect changes in client requirements

without restarting the RFQ from the beginning.

---

### Client-ready Email Generation

Approved quotations can be converted into professional client-facing email drafts.

The generated draft can incorporate:

- Client information
- Project requirements
- Approved quotation
- Sender information

The workflow creates a **Gmail draft rather than automatically sending the quotation**.

This preserves a final human review point before any quotation becomes external client communication.

After the draft is created, the workflow can notify the operator that the client response is ready for review.

---

## LLM Evaluation

RFQ Automation includes a Golden Set-based evaluation workflow for RFQ extraction.

```text
Golden Set
    │
    ▼
RFQ Extractor
    │
    ▼
Predicted Structured Output
    │
    ▼
Expected vs Actual Comparison
    │
    ▼
Evaluation Metrics
```

The Golden Set contains RFQ examples paired with expected structured outputs.

The evaluation layer makes extraction quality measurable rather than relying only on manual prompt testing.

This supports identifying:

- Incorrect extractions
- Missing information
- Prompt regressions
- Model behavior changes

and provides a repeatable way to evaluate extraction behavior as the AI component changes.

---

## LLM Monitoring

LLM calls are logged for operational monitoring.

Tracked information includes:

- Task type
- Model
- Success / failure
- Input tokens
- Output tokens
- Latency
- Estimated API cost
- Error information

A monitoring dashboard provides aggregated metrics such as:

- Total LLM calls
- Success rate
- Token usage
- Average latency
- Estimated cost

This provides visibility into both **LLM behavior and operational cost**, rather than treating the LLM as a black box.

---

## Dashboard

The Next.js dashboard provides an operational interface for managing RFQs.

It supports:

- RFQ overview
- Search and status filtering
- RFQ status visualization
- RFQ detail inspection
- Quotation breakdown
- Market benchmark review results
- RFQ editing
- Quotation recalculation
- Human approval / rejection
- Draft email preview
- LLM monitoring

This turns the backend automation into a workflow that operators can inspect and control.

---

## Tech Stack

| Category | Technologies |
|---|---|
| Frontend | Next.js, TypeScript |
| Backend | FastAPI, Python |
| AI | OpenAI API, Structured Outputs |
| Database | PostgreSQL, Supabase |
| ORM / Migration | SQLAlchemy, Alembic |
| Workflow Automation | n8n |
| Email Integration | Gmail |
| Notifications | Slack |
| Infrastructure | Docker Compose |
| Backend Deployment | Railway |
| Frontend Deployment | Vercel |
| Evaluation | Golden Set-based extraction evaluation |

---

## Project Structure

```text
backend/
├── app/
│   ├── api/
│   ├── config/
│   ├── db/
│   │   ├── mappers/
│   │   ├── models/
│   │   └── repositories/
│   ├── models/
│   ├── prompts/
│   ├── services/
│   └── utils/
│
├── data/
└── evaluation/
    ├── evaluate_extraction.py
    └── golden_set.json

frontend/
├── app/
├── components/
├── services/
└── types/

n8n
└── Workflow orchestration
```

The backend follows a layered structure separating:

```text
API
 ↓
Service
 ↓
Repository
 ↓
Database
```

Business logic such as quotation calculation and market benchmark comparison remains in the service layer, while database access is isolated through repositories.

---

## Screenshots

### RFQ Dashboard

![RFQ Dashboard](backend/docs/images/dashboard.png)

### RFQ Detail & Quotation

![RFQ Detail](backend/docs/images/rfq-detail.png)

### RFQ Editing & Recalculation

![RFQ Editing](backend/docs/images/rfq-edit.png)

### Draft Email Generation

![Draft Email](backend/docs/images/draft-email.png)

### LLM Monitoring

![LLM Monitoring](backend/docs/images/llm-monitoring.png)

### Workflow Orchestration

![n8n Workflow](backend/docs/images/n8n-workflow.png)

![n8n Workflow](backend/docs/images/n8n-workflow2.png)

![n8n Workflow](backend/docs/images/n8n-workflow3.png)

![n8n Workflow](backend/docs/images/n8n-workflow4.png)

![n8n Workflow](backend/docs/images/n8n-workflow5.png)

---

## Running Locally

### 1. Clone the repository

```bash
git clone <repository-url>
cd rfq
```

### 2. Configure environment variables

Create the required environment configuration for the backend.

Required services include:

- OpenAI API
- PostgreSQL database
- Gmail / n8n configuration where applicable
- Slack configuration where applicable

Do not commit secrets or local runtime data to the repository.

### 3. Start the application

```bash
docker compose up --build
```

### 4. Access the services

Frontend:

```text
http://localhost:3000
```

FastAPI documentation:

```text
http://localhost:8000/docs
```

n8n:

```text
http://localhost:5678
```

---

## Engineering Decisions

### Why not use an LLM for quotation calculation?

Pricing is financial business logic that needs to be deterministic and reproducible.

The LLM extracts unstructured information, while the actual quotation is calculated using explicit Python rules.

This separation prevents probabilistic model behavior from directly determining financial calculations.

---

### Why use deterministic market benchmark comparison?

A generated quotation should be reviewable against known pricing ranges without allowing an LLM to independently alter financial decisions.

RFQ Automation therefore compares calculated quotations against structured market benchmark data using deterministic matching rules.

If the available RFQ information is insufficient for an appropriate benchmark comparison, the system returns `NO_BENCHMARK` rather than selecting an arbitrary benchmark.

The comparison provides context for a human reviewer; it does not modify the quotation.

---

### Why not automatically learn benchmarks from new RFQs?

A newly processed quotation is not necessarily a reliable market reference.

Automatically feeding every new RFQ back into the benchmark dataset could allow unusual projects, temporary pricing decisions, or outliers to influence future reviews.

RFQ Automation therefore separates **operational quotation records** from **controlled benchmark reference data**.

For production use, historical quotation data can be reviewed periodically by the team alongside market conditions and operational experience. Only agreed changes would then be incorporated into the benchmark dataset.

This keeps benchmark evolution auditable and under human governance.

---

### Why support multi-email RFQs?

Real client requests are often incomplete.

Instead of treating every client reply as a new RFQ, the system uses the Gmail thread identifier to associate follow-up information with the existing RFQ.

This allows missing information to be progressively collected while preserving a single RFQ lifecycle.

---

### Why Human Approval?

Even when extraction and pricing are automated, sending a quotation directly to a client introduces operational and financial risk.

RFQ Automation therefore keeps the final decision behind a human approval gate and generates a Gmail draft rather than automatically sending the client response.

---

### Why add evaluation?

A successful API response does not mean an extraction is correct.

The Golden Set evaluation layer provides a repeatable way to measure extraction behavior and identify regressions when prompts or models change.

---

### Why monitor tokens, latency, and cost?

LLM workflows need operational observability just like traditional software systems.

Tracking these metrics makes model usage, performance, failures, and cost visible rather than treating the LLM as a black box.

---

## Status

**Core workflow complete.**

The system currently supports the RFQ lifecycle from incoming email detection and structured extraction through validation, multi-email clarification handling, deterministic quotation generation, market benchmark review, human approval, workflow resume, client-ready Gmail draft generation, database persistence, extraction evaluation, and LLM monitoring.

The final portfolio validation includes end-to-end testing across both complete and incomplete RFQ scenarios before final screenshots and case-study documentation are updated.