# EcoReason: AI Environmental Scientist

> **Darukaa.Earth Hackathon Submission**  
> AI Biodiversity Intelligence Chatbot Challenge

EcoReason is an AI-powered environmental intelligence system designed to act as an **AI Environmental Scientist**, not just a conversational chatbot. It grounds ecological analysis in peer-reviewed scientific literature and empirical models, combines at least 3 environmental variables simultaneously in every recommendation, provides measurable improvement projections, and offers an interactive What-If Ecology Simulator.

---

## 1. System Architecture

```
                                 ┌─────────────────────────┐
                                 │   React Frontend (UI)   │
                                 │  - Conversational Chat  │
                                 │  - Structured Form/Map  │
                                 │  - What-If Simulator    │
                                 └───────────┬─────────────┘
                                             │ HTTP / JSON
                                             ▼
                                 ┌─────────────────────────┐
                                 │  FastAPI Backend (API)  │
                                 │       /api/v1/...       │
                                 └───────────┬─────────────┘
                                             │
      ┌──────────────────────────────────────┼──────────────────────────────────────┐
      │                                      │                                      │
      ▼                                      ▼                                      ▼
┌───────────────────────────┐  ┌───────────────────────────┐  ┌───────────────────────────┐
│ Conversational Intel Layer│  │ Multi-Metric Reasoner     │  │  What-If Ecology Sim      │
│ - Memory & State Tracker  │  │ - 3+ Variable Interconnect│  │  - Baseline vs Action     │
│ - Clarification Trigger   │  │ - Soil ↔ Water ↔ Habitat  │  │  - 1-5 Yr Cascade Proj.   │
└─────────────┬─────────────┘  └─────────────┬─────────────┘  └─────────────┬─────────────┘
              │                              │                              │
              └──────────────────────────────┼──────────────────────────────┘
                                             │
                                             ▼
                               ┌───────────────────────────┐
                               │ RAG & Grounding Engine    │
                               │ - Vector Store (Chroma)   │
                               │ - Structured Matrices     │
                               │ - FAO / IPCC / IPBES Docs │
                               └───────────────────────────┘
```

### Core Architecture Components

1. **FastAPI Backend (`backend/`)**: High-performance asynchronous API delivering endpoints for multi-turn chat, multi-metric reasoning, evidence lookup, and ecological simulation.
2. **React Frontend (`frontend/`)**: Modern interface supporting text prompts, structured parameter entry (pH, SOC, rainfall, land use, coordinates), clarification dialogs, and scenario comparison.
3. **Structured Knowledge & RAG (`backend/app/rag/` & `backend/data/`)**: Hybrid knowledge layer indexing scientific reports (FAO, IPCC, IPBES) and deterministic ecological matrices (soil organic carbon thresholds, soil microbial dynamics, habitat fragmentation metrics).
4. **Multi-Metric Reasoning Engine (`backend/app/reasoning/`)**: Ensures responses connect multiple interrelated ecological variables (e.g. soil health ↔ water retention ↔ biodiversity richness) rather than single-variable answers.
5. **Evidence-Backed Recommendation Engine (`backend/app/recommendations/`)**: Packages actionable interventions with scientific justification, time horizons, measurable target deltas, and academic citations.
6. **Conversational Intelligence & Memory (`backend/app/core/`)**: Tracks conversation context across turns, detects incomplete parameter sets, and prompts for targeted missing data before prescribing interventions.
7. **What-If Ecology Simulator (`backend/app/simulator/`)**: Allows users to simulate dynamic ecological interventions (e.g. cover crops, rotational grazing, agroforestry) and view projected multi-year trajectories.

---

## 2. Knowledge Base & Schemas

### Environmental Input Schema
- `soil`: `organic_carbon_pct`, `ph`, `moisture_pct`, `texture`
- `climate`: `rainfall_mm`, `temperature_celsius`, `aridity_index`
- `land_use`: `current_cover`, `crop_type`, `tillage_practice`, `fragmentation_index`
- `spatial`: `latitude`, `longitude`, `ecoregion`, `biome`

### Recommendation Output Schema
- `action`: Concrete ecological intervention (e.g. legume-based intercropping).
- `scientific_reasoning`: Causal mechanism linking intervention to ecosystem dynamics.
- `impacted_metrics`: List of primary and secondary metrics affected.
- `measurable_improvements`: Estimated numerical range (e.g. +15–25% SOC over 2–3 years).
- `time_horizon`: Short-term (0–1 yr), Medium-term (2–3 yrs), Long-term (4+ yrs).
- `confidence_level`: Calibrated confidence score (Low, Medium, High) with rationale.
- `evidence`: Citations referencing FAO, IPCC, IPBES, or peer-reviewed studies.

---

## 3. Local Setup & Installation

### Prerequisites
- Python 3.11+
- Node.js 18+ and npm
- (Optional) Docker & Docker Compose

### Running with Docker (Recommended)
```bash
# Build and run backend and frontend
docker-compose up --build
```
- Frontend: `http://localhost:5173`
- Backend API: `http://localhost:8000`
- API Docs (Swagger): `http://localhost:8000/docs`

### Manual Setup

#### Backend
```bash
cd backend
python -m venv venv
# On Windows:
.\venv\Scripts\activate
# On Linux/macOS:
source venv/bin/activate

pip install -r requirements.txt
cp .env.example .env
uvicorn app.main:app --reload --port 8000
```

#### Frontend
```bash
cd frontend
npm install
cp .env.example .env
npm run dev
```

---

## 4. Running Tests

```bash
cd backend
pytest -v
```

Test coverage includes:
- `test_api.py`: API route contracts and payload validation
- `test_reasoning.py`: Multi-variable correlation and constraint enforcement
- `test_recommendations.py`: Mandatory evidence linking and study citations
- `test_memory.py`: Multi-turn session context and missing variable prompts
- `test_simulator.py`: What-If ecological projection math
- `test_rag.py`: Knowledge retrieval pipeline

---

## 5. CI/CD Pipeline

The project includes an automated GitHub Actions CI workflow in `.github/workflows/ci.yml`:
- **Backend**: Python 3.11 environment setup, dependency caching, pytest test execution.
- **Frontend**: Node.js 20 environment setup, dependency installation, Vite production bundle build.

---

## 6. Repository Access & Evaluation Guidelines

Per submission guidelines, if this repository is private, access is granted to:
- `ankita.dasgupta@darukaa.com`
- `harsh.kumar@darukaa.com`
- `utkarsh.gauniyal@darukaa.com`
- `guneet.mutreja@darukaa.com`
