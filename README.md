# Smart Credit Analysis — OpenAI

The project contains a containerized FastAPI backend and a React frontend to demonstrate a stateless pipeline for extracting transaction data from bank statements and producing a PDF Credit Trust Score report enriched by OpenAI.

## Key features
- OpenAI integration for natural-language analysis and structured insights.
- Environment-driven configuration (OPENAI_API_KEY, OPENAI_MODEL).

## Environment variables (backend)
- OPENAI_API_KEY — **required** to enable the OpenAI enrichment
- OPENAI_MODEL — optional (default: gpt-4o-mini)

## Run locally (dev)
1. Set OPENAI_API_KEY in your environment or create a .env with `OPENAI_API_KEY=sk-...`.
2. Backend (recommended virtualenv):
   ```bash
   cd backend
   pip install -r app/requirements.txt
   uvicorn app.main:app --reload --port 8080
   ```
3. Frontend (vite):
   ```bash
   cd frontend
   npm install
   npm run dev
   ```
   