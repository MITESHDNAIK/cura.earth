# Cura.Earth

> **AI Environmental Scientist & Ecological Reasoning Engine**

Cura.Earth is an AI-powered environmental reasoning platform designed to reason about ecosystems using structured environmental data, scientific knowledge, multi-metric relationships, evidence-backed recommendations, and counterfactual **What-If Ecology** simulations.

The project was built for the **Darukaa.Earth hackathon challenge** and focuses on environmental reasoning rather than generic LLM chat.

---

## 🌱 What is Cura.Earth?

Environmental problems rarely affect only one variable.

For example:

- Low soil organic carbon can reduce water retention.
- Poor water retention can increase crop stress.
- Monoculture can reduce habitat diversity.
- Habitat degradation can affect biodiversity.
- Land-use changes can increase fragmentation.
- Climate stress can amplify these effects.

Cura.Earth therefore treats an environmental situation as a connected system.

Instead of simply answering:

> "What should I do?"

Cura.Earth attempts to answer:

> **What is happening → Why is it happening → Which environmental variables are connected → What intervention can help → What measurable changes could occur → What scientific evidence supports the reasoning?**

---

# ✨ Core Features

## 1. Conversational Environmental Scientist

Users can describe an environmental situation using natural language.

Example:

```text
My farm has very low soil organic carbon, low rainfall and wheat is
grown continuously as a monoculture.
```

Cura.Earth extracts relevant environmental information and builds an environmental profile.

The system can also identify incomplete information and request additional context instead of immediately producing a recommendation.

---

## 2. Structured Environmental Input

The platform supports structured environmental parameters including:

- Soil Organic Carbon (SOC)
- Soil pH
- Soil moisture
- Rainfall
- Temperature
- Crop / land use
- Cropping pattern
- Biodiversity condition
- Habitat fragmentation
- Pollution
- Region / landscape context
- Geographic coordinates

This allows the reasoning engine to operate on structured environmental state rather than relying entirely on free-form language.

---

## 3. Multi-Metric Ecological Reasoning

This is one of the core differentiators of Cura.Earth.

The system does not intentionally treat environmental variables as isolated values.

It reasons across relationships such as:

```text
Soil Health
     ↓
Water Retention
     ↓
Vegetation / Crop Stress
     ↓
Habitat Quality
     ↓
Biodiversity
```

and:

```text
Land Use
    ↓
Habitat Structure
    ↓
Fragmentation
    ↓
Species Movement
    ↓
Biodiversity
```

Recommendations are therefore evaluated across multiple environmental dimensions.

---

# 🧠 System Architecture

```text
                         ┌──────────────────────┐
                         │     React Frontend   │
                         │                      │
                         │ Chat / Structured    │
                         │ Input / Simulator    │
                         └──────────┬───────────┘
                                    │
                                    ▼
                         ┌──────────────────────┐
                         │      FastAPI API     │
                         └──────────┬───────────┘
                                    │
                ┌───────────────────┼───────────────────┐
                │                   │                   │
                ▼                   ▼                   ▼
       ┌────────────────┐  ┌─────────────────┐  ┌────────────────┐
       │ Conversation   │  │ Reasoning       │  │ What-If        │
       │ Service        │  │ Engine          │  │ Simulator      │
       └───────┬────────┘  └────────┬────────┘  └────────────────┘
               │                    │
               ▼                    ▼
       ┌────────────────┐   ┌──────────────────┐
       │ Context /      │   │ Recommendation   │
       │ Memory         │   │ Engine            │
       └────────────────┘   └─────────┬────────┘
                                      │
                                      ▼
                             ┌─────────────────┐
                             │ Evidence Linker │
                             └────────┬────────┘
                                      │
                                      ▼
                         ┌────────────────────────┐
                         │ RAG Knowledge System   │
                         │                        │
                         │ Embeddings             │
                         │ ChromaDB                │
                         │ Scientific Documents   │
                         └────────────────────────┘
```

---

# 🏗️ Repository Structure

```text
curaearth/
│
├── .github/
│
├── backend/
│   ├── .env.example
│   ├── pyproject.toml
│   ├── requirements.txt
│   │
│   ├── data/
│   │   ├── documents/
│   │   ├── knowledge/
│   │   └── structured/
│   │
│   └── app/
│       ├── __init__.py
│       ├── main.py
│       ├── config.py
│       │
│       ├── api/
│       │   └── v1/
│       │       ├── router.py
│       │       └── endpoints/
│       │           ├── chat.py
│       │           ├── reasoning.py
│       │           ├── simulator.py
│       │           ├── knowledge.py
│       │           └── conversation.py
│       │
│       ├── core/
│       │   ├── conversation.py
│       │   ├── schema.py
│       │   └── __init__.py
│       │
│       ├── rag/
│       │   ├── __init__.py
│       │   ├── chunking.py
│       │   ├── embeddings.py
│       │   ├── vector_store.py
│       │   ├── service.py
│       │   ├── retriever.py
│       │   └── schema.py
│       │
│       ├── reasoning/
│       │   ├── engine.py
│       │   ├── profile_builder.py
│       │   ├── relationship_engine.py
│       │   ├── intervention_engine.py
│       │   ├── metrics.py
│       │   ├── rules.py
│       │   ├── extractor.py
│       │   ├── completeness.py
│       │   ├── conversation_service.py
│       │   └── confidence.py
│       │
│       ├── recommendations/
│       │   ├── engine.py
│       │   └── evidence_linker.py
│       │
│       └── simulator/
│           ├── __init__.py
│           ├── ecology_sim.py
│           ├── scenarios.py
│           └── intervention_mapper.py
│
├── frontend/
│
├── Dockerfile.backend
├── Dockerfile.frontend
├── docker-compose.yml
├── README.md
└── .gitignore
```

---

# 🔬 Environmental Data Model

Cura.Earth organizes environmental information into several conceptual groups.

## Soil

```text
organic_carbon_pct
pH
moisture_pct
```

## Climate

```text
rainfall
rainfall_category
temperature
```

## Land Use / Agriculture

```text
crop
cropping_pattern
land_use
```

## Biodiversity

```text
biodiversity_status
habitat_fragmentation
```

## Human Impact

```text
pollution
deforestation
disturbance
```

## Geography

```text
region
latitude
longitude
```

These values are converted into an environmental profile used by downstream reasoning components.

---

# 🔄 Reasoning Pipeline

The general reasoning flow is:

```text
User Input
    │
    ▼
Information Extraction
    │
    ▼
Environmental Profile
    │
    ▼
Completeness Check
    │
    ├── Incomplete ──► Clarification
    │
    ▼
Stress / Condition Detection
    │
    ▼
Relationship Analysis
    │
    ▼
Intervention Matching
    │
    ▼
Recommendation Scoring
    │
    ▼
Scientific Evidence Linking
    │
    ▼
Environmental Recommendation
```

---

# 💬 Conversational Context

Cura.Earth supports multi-turn interaction.

A conversation can progressively build an environmental profile.

Example:

### User

```text
My farm has low soil organic carbon.
```

### Cura.Earth

```text
What is the approximate rainfall in the area, and what crop is
currently being cultivated?
```

### User

```text
Rainfall is low and I grow wheat continuously.
```

The system combines information from the conversation rather than treating every message as a completely independent query.

The conversational layer maintains an in-memory environmental context for the active conversation.

---

# 📚 Knowledge System / RAG

Cura.Earth contains a retrieval-based scientific knowledge layer.

The current knowledge base includes environmental documents covering areas such as:

- Soil organic carbon
- Biodiversity
- Land degradation
- Ecosystem relationships

The pipeline is:

```text
Scientific Documents
        │
        ▼
Document Ingestion
        │
        ▼
Chunking
        │
        ▼
Embeddings
        │
        ▼
ChromaDB
        │
        ▼
Semantic Retrieval
        │
        ▼
Evidence Chunks
        │
        ▼
Recommendation / Reasoning Layer
```

The system uses **Sentence Transformers** for semantic embeddings and **ChromaDB** for vector retrieval.

---

# 🗃️ Vector Database

Cura.Earth currently uses ChromaDB.

The vector store is configured through:

```text
CHROMA_PERSIST_DIRECTORY
CHROMA_COLLECTION_NAME
```

The knowledge base is small enough for the hackathon MVP to be initialized during application startup.

For a larger production system, an externally managed vector database would be preferable.

---

# 🧾 Evidence Structure

Recommendations are designed to expose more than a generic action.

A recommendation can contain:

```text
Action
Why it is recommended
Impacted environmental metrics
Expected time horizon
Measurable improvements
Confidence
Scientific evidence
```

Example conceptual structure:

```json
{
  "action": "Introduce agroforestry",
  "reason": "Low soil carbon and water stress indicate a need to improve soil-water interactions and diversify the agricultural system.",
  "impacted_metrics": [
    "soil organic carbon",
    "water retention",
    "biodiversity"
  ],
  "time_horizon": "multi-year",
  "confidence": "moderate",
  "evidence": [
    "FAO soil carbon literature",
    "IPCC land degradation literature"
  ]
}
```

The simulator's quantitative outputs are illustrative scenario estimates rather than claims of field-level prediction.

---

# 🌾 Benchmark Environmental Scenario

The challenge benchmark describes a semi-arid agricultural scenario with:

```text
Soil Organic Carbon: 0.3%
Rainfall: Low
Crop: Wheat
Cropping Pattern: Monoculture
Landscape: Semi-arid agricultural system
```

The expected reasoning direction is toward interventions such as:

- Agroforestry
- Intercropping

The important aspect is not merely naming an intervention.

The system should connect the intervention to multiple environmental effects, for example:

```text
Intervention
    │
    ├── Soil Carbon
    │
    ├── Water Retention
    │
    ├── Crop / Vegetation Diversity
    │
    └── Biodiversity
```

Scientific sources in the knowledge base are used to provide supporting evidence.

---

# 🔗 Ecological Relationship Engine

The relationship layer is designed to capture interactions between environmental variables.

Examples include:

## Soil Carbon → Water

Higher soil organic matter can influence soil structure and water-related properties.

```text
SOC
 ↓
Soil Structure
 ↓
Water Retention
 ↓
Plant Water Availability
```

## Land Diversity → Biodiversity

Diversified agricultural landscapes can provide additional habitat structure and resources.

```text
Crop / Habitat Diversity
 ↓
Habitat Complexity
 ↓
Species Resources
 ↓
Biodiversity
```

## Fragmentation → Habitat Connectivity

Landscape fragmentation can influence habitat connectivity and species movement.

```text
Fragmentation
 ↓
Connectivity
 ↓
Species Movement
 ↓
Biodiversity
```

These relationships are used as reasoning signals rather than presented as universal deterministic laws.

---

# 🔮 What-If Ecology Simulator

One of Cura.Earth's main differentiating features is the **What-If Ecology Simulator**.

Instead of only saying:

> "Try agroforestry."

the system can explore:

> "What could happen if agroforestry were introduced?"

The simulator compares environmental trajectories under different interventions.

Current intervention scenarios include:

```text
Agroforestry
Legume Intercropping
Cover Cropping
Native Hedgerows
```

The simulator tracks multiple environmental dimensions, including:

```text
Soil Organic Carbon
Water / Moisture
Biodiversity
Crop Diversity
Habitat Fragmentation
```

Conceptual flow:

```text
Current Environmental State
          │
          ▼
      Intervention
          │
          ▼
    Scenario Model
          │
          ▼
   Multi-Year Trajectory
          │
          ▼
 Metric-by-Metric Comparison
```

The simulator is intended as an explanatory **counterfactual scenario tool**, not a substitute for calibrated ecological or agronomic field models.

---

# 🧪 Current Simulator Scenarios

The backend currently supports scenario families including:

```text
semi_arid_monoculture_agroforestry
regenerative_riparian_buffer
```

Intervention mappings include:

```text
agroforestry
legume_intercropping
cover_cropping
native_hedgerows
```

The simulation engine produces differentiated trajectories for multiple environmental metrics.

---

# 🖥️ Frontend

The frontend is implemented using React and Vite.

Main product areas include:

```text
Chat
Structured Environmental Analysis
What-If Simulator
Knowledge Search
```

The frontend communicates with the FastAPI backend through the API service layer.

---

# 🔌 API

The backend exposes versioned API routes under:

```text
/api/v1
```

Important endpoints include:

```text
GET  /health
GET  /

POST /api/v1/conversation/conversation
POST /api/v1/reasoning/reason
POST /api/v1/simulator/simulate
POST /api/v1/knowledge/query
```

FastAPI also provides interactive API documentation through:

```text
/docs
```

and:

```text
/openapi.json
```

---

# 🧰 Technology Stack

## Frontend

```text
React
Vite
JavaScript
CSS
```

## Backend

```text
Python
FastAPI
Pydantic
Uvicorn
```

## AI / ML

```text
Sentence Transformers
NumPy
scikit-learn compatible reasoning components
```

## RAG

```text
ChromaDB
Sentence Transformers
Semantic Retrieval
```

## Development

```text
Git
GitHub
Docker
Docker Compose
```

---

# ⚙️ Local Setup

## Requirements

Install:

- Python 3.11+ recommended
- Node.js
- Git

---

## 1. Clone the repository

```bash
git clone https://github.com/MITESHDNAIK/cura.earth.git
cd cura.earth
```

---

# 🐍 Backend Setup

Move into the backend:

```bash
cd backend
```

Create a virtual environment:

### Windows

```powershell
python -m venv .venv
```

Activate:

```powershell
.\.venv\Scripts\Activate.ps1
```

### macOS / Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

# 🔐 Environment Configuration

Create a `.env` file inside:

```text
backend/.env
```

Example:

```env
ENVIRONMENT=production
DEBUG=false
PROJECT_NAME="Cura.Earth - AI Environmental Scientist"
API_V1_PREFIX=/api/v1
HOST=0.0.0.0
PORT=8000
CORS_ORIGINS=["http://localhost:5173","http://127.0.0.1:5173"]
CHROMA_PERSIST_DIRECTORY=./chroma_db
CHROMA_COLLECTION_NAME=curaearth_knowledge
EMBEDDING_MODEL_NAME=all-MiniLM-L6-v2
STRUCTURED_DATA_PATH=./data/structured
DOCUMENTS_DATA_PATH=./data/documents
```

For local development, `DEBUG=true` may be used.

---

# ▶️ Run Backend

From:

```text
backend/
```

run:

```bash
python -m uvicorn app.main:app --reload
```

The backend will normally be available at:

```text
http://127.0.0.1:8000
```

Health check:

```text
http://127.0.0.1:8000/health
```

Swagger documentation:

```text
http://127.0.0.1:8000/docs
```

---

# ⚛️ Frontend Setup

Open another terminal.

Move to:

```bash
cd frontend
```

Install dependencies:

```bash
npm install
```

Run:

```bash
npm run dev
```

The Vite development server will normally run at:

```text
http://localhost:5173
```

---

# 🔗 Frontend → Backend Configuration

The frontend API service supports:

```text
VITE_API_BASE_URL
```

For deployment, set:

```text
VITE_API_BASE_URL=https://YOUR-BACKEND-URL
```

where `YOUR-BACKEND-URL` is the deployed FastAPI backend.

---

# 🐳 Docker

The repository includes Docker-related files:

```text
Dockerfile.backend
Dockerfile.frontend
docker-compose.yml
```

A Docker-based workflow can be used for environments where containerized deployment is preferred.

---

# 🚀 Deployment

The intended hackathon deployment architecture is:

```text
                    Internet
                       │
              ┌────────┴────────┐
              │                 │
              ▼                 ▼
        Vercel Frontend    Render Backend
              │                 │
              └────────┬────────┘
                       │
                       ▼
                  FastAPI APIs
                       │
                       ▼
                  ChromaDB / RAG
```

## Frontend

Recommended platform:

```text
Vercel
```

Build command:

```bash
npm run build
```

Output directory:

```text
dist
```

Root directory:

```text
frontend
```

Environment variable:

```text
VITE_API_BASE_URL=https://YOUR-RENDER-BACKEND-URL
```

---

## Backend

Recommended platform:

```text
Render
```

Root directory:

```text
backend
```

Build command:

```bash
pip install -r requirements.txt
```

Start command:

```bash
uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

The backend CORS configuration must include the deployed frontend domain.

---

# ⚠️ Deployment Note: ChromaDB

The current hackathon MVP uses a local ChromaDB persistence directory.

The knowledge base is intentionally small and is initialized from the repository's scientific documents during backend startup.

This approach is suitable for the MVP/demo architecture.

For a larger production system, use a managed/external vector database or persistent storage rather than relying on ephemeral application storage.

---

# 🧪 Testing

Run backend tests from:

```text
backend/
```

with:

```bash
pytest
```

The repository contains tests for components including:

- API health
- RAG retrieval
- reasoning
- recommendations
- simulation

The project prioritizes the working product flow and deployment readiness; some legacy tests may require alignment with the current simulator/recommendation interfaces.

---

# 📖 Scientific Knowledge Sources

The current knowledge layer contains documents based on environmental/scientific material including:

```text
FAO
IPCC
IPBES
```

The repository's document files are located under:

```text
backend/data/documents/
```

These documents are ingested and indexed for semantic retrieval.

---

# 🔎 Knowledge Retrieval Example

Example request:

```text
How does low soil organic carbon affect biodiversity and water retention
in dry agricultural systems?
```

The knowledge API can return relevant evidence chunks from the indexed knowledge base.

Conceptually:

```text
Query
 ↓
Embedding
 ↓
Semantic Search
 ↓
Top-K Evidence
 ↓
Retrieved Scientific Context
```

The system currently supports configurable `top_k` retrieval.

---

# 🧠 Why Cura.Earth Is Not a Generic Chatbot

A generic LLM workflow might look like:

```text
User Question
      ↓
LLM
      ↓
Answer
```

Cura.Earth is designed as:

```text
User Input
      ↓
Structured Environmental Extraction
      ↓
Environmental Profile
      ↓
Condition / Stress Detection
      ↓
Ecological Relationship Reasoning
      ↓
Intervention Matching
      ↓
Evidence Retrieval
      ↓
Recommendation
      ↓
Optional Counterfactual Simulation
```

The architecture therefore makes environmental state and ecological relationships explicit parts of the system.

---

# 🎯 Challenge Alignment

The project was designed around the major challenge requirements.

| Requirement | Cura.Earth |
|---|---|
| Conversational interaction | Implemented |
| Structured environmental knowledge | Implemented |
| Soil parameters | Implemented |
| Climate parameters | Implemented |
| Land-use context | Implemented |
| Biodiversity context | Implemented |
| Human impact context | Implemented |
| RAG / semantic retrieval | Implemented |
| Vector database | ChromaDB |
| Clarification logic | Implemented |
| Multi-turn context | Implemented |
| Evidence-backed recommendations | Implemented |
| Multi-metric reasoning | Implemented |
| Geographic input | Supported |
| What-If simulation | Implemented |

---

# 🧩 Design Philosophy

Cura.Earth follows five principles.

### 1. Environment is interconnected

Environmental decisions should consider multiple variables together.

### 2. Missing information matters

When the environmental profile is insufficient, the system should ask for additional information rather than blindly assuming values.

### 3. Recommendations should be actionable

The output should explain what action can be taken and why.

### 4. Evidence should be visible

Scientific sources should be retrievable and connected to recommendations.

### 5. Interventions should be explorable

The What-If simulator allows users to explore possible environmental trajectories instead of receiving only a static recommendation.

---

# 🏆 Key Differentiator

The central product concept is:

> **Cura.Earth does not just answer environmental questions — it builds an environmental state, reasons across connected ecological variables, links recommendations to scientific evidence, and allows users to explore intervention scenarios.**

This combination of:

```text
Conversation
+
Structured Environmental State
+
Multi-Metric Reasoning
+
Scientific RAG
+
Evidence
+
Counterfactual Simulation
```

forms the core of Cura.Earth.

---

# 📌 Current Project Status

```text
Conversational Interface        ✅
Structured Environmental Input  ✅
Multi-Turn Context              ✅
Clarification Logic             ✅
Environmental Parameter
Extraction                       ✅
Multi-Metric Reasoning          ✅
Recommendation Engine           ✅
Scientific Knowledge / RAG      ✅
ChromaDB Retrieval              ✅
What-If Ecology Simulator       ✅
React Frontend                  ✅
FastAPI Backend                 ✅
GitHub Repository               ✅
Deployment                      🚧
```

---

# 🔗 Project Links

## GitHub

https://github.com/MITESHDNAIK/cura.earth

## Live Demo

```text
To be added after deployment.
```

---

# 👥 Repository Access

For private repository evaluation, grant access to the required Darukaa.Earth evaluator accounts.

If the repository is public, the GitHub link above can be used directly.

---

# 📝 Hackathon Submission

The final submission should include:

```text
GitHub Repository
Live Demo URL
README
Architecture / Technical Overview
Database / Schema Information
Local Setup Instructions
CI/CD Information
Additional Links
Credentials / Notes where applicable
```

---

# 🌍 Vision

Cura.Earth aims to make environmental reasoning more accessible by combining AI, structured environmental data, scientific knowledge, and ecological systems thinking.

The long-term vision is a system that can help users move from:

```text
Environmental Observation
        ↓
Understanding
        ↓
Evidence
        ↓
Intervention
        ↓
Scenario Exploration
        ↓
Better Environmental Decisions
```

---

## Cura.Earth

**AI Environmental Scientist & Ecological Reasoning Engine**

```text
Understand the ecosystem.
Reason across the variables.
Act with evidence.
Explore the future.
```
