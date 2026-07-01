# OpsSage AI

OpsSage AI is a RAG-based incident analysis assistant for production support
and infrastructure troubleshooting. It accepts an incident, log snippet, or
error message, retrieves relevant runbooks or past incidents, and returns a
structured troubleshooting response with probable causes, validation checks,
fix steps, retrieval confidence, and a grounded incident report.

## Why This Project Exists

Production support teams often solve repeat issues by searching old runbooks,
incident notes, and error references. OpsSage AI turns that workflow into a
small AI system:

```txt
Search the right operational knowledge first.
Then use an LLM to generate a structured response.
```

This keeps the system easier to update than fine-tuning because new knowledge
can be added by editing Markdown runbooks.

## Features

- RAG pipeline for incident analysis
- Hugging Face sentence-transformer embeddings when available
- FAISS vector search when available
- fallback local embedding/search mode for beginner-friendly execution
- Ollama/Llama-compatible generation layer
- grounded reporting to avoid overconfident root-cause claims
- retrieval confidence and source document previews
- plain-Python local API for Python 3.14 compatibility
- FastAPI entry point for portfolio/API mode
- retrieval evaluation script with sample test cases
- example request/response files for GitHub review

## Architecture

```txt
User incident/log
      |
      v
IncidentAnalyzer
      |
      v
Embedding model
Hugging Face sentence-transformer or fallback hashing
      |
      v
Vector search
FAISS or fallback cosine similarity
      |
      v
Top matching runbooks/incidents
      |
      v
Prompt + local LLM
Ollama / Llama 3.2 when available
      |
      v
Structured incident analysis
```

## Tech Stack

| Layer | Tools |
| --- | --- |
| Language | Python |
| API | Plain Python HTTP server, FastAPI optional |
| Embeddings | `sentence-transformers/all-MiniLM-L6-v2` |
| Vector Search | FAISS, fallback cosine similarity |
| LLM | Ollama + Llama 3.2 compatible |
| Data Format | Markdown runbooks, JSON evaluation cases |
| Evaluation | Top-1 retrieval accuracy |

## Project Structure

```txt
opssage-ai/
  app/
    demo.py
    simple_api.py
    main.py
    schemas.py
    services/
      document_loader.py
      embedding.py
      vector_store.py
      llm.py
      incident_analyzer.py
  data/
    runbooks/
    incidents/
  evaluation/
    retrieval_cases.json
  examples/
    *_request.json
    *_response.json
  scripts/
    build_index.py
    evaluate_retrieval.py
```

## Quick Start

Run from the project folder:

```bash
cd opssage-ai
```

Run a single incident analysis:

```bash
python -m app.demo "ORA-01652 unable to extend temp segment in tablespace TEMP"
```

This works even without the full API stack because the project includes fallback
embedding and search behavior.

## Run The Local API

Use this option if FastAPI/Pydantic is not working on a newer Python version:

```bash
python -m app.simple_api
```

Expected startup output:

```txt
Loading OpsSage analyzer...
OpsSage simple API running at http://127.0.0.1:8000
Try GET /health or POST /analyze-incident
```

In a second terminal, test the API:

```powershell
curl http://127.0.0.1:8000/health
```

PowerShell request example:

```powershell
$body = @{ incident = 'Application cannot connect to database and connection timeout error is showing' } | ConvertTo-Json
Invoke-RestMethod -Uri 'http://127.0.0.1:8000/analyze-incident' -Method Post -ContentType 'application/json' -Body $body
```

## Portfolio Mode

Install RAG dependencies:

```bash
pip install -r requirements.txt
```

Install API dependencies:

```bash
pip install -r requirements-api.txt
```

Or install everything:

```bash
pip install -r requirements-full.txt
```

Start Ollama and pull a local model:

```bash
ollama pull llama3.2
```

Run the FastAPI app:

```bash
uvicorn app.main:app --reload
```

Open:

```txt
http://127.0.0.1:8000/docs
```

Note: if you are on Python 3.14 and Pydantic/FastAPI packages fail to install,
use `app.simple_api` or create a Python 3.11/3.12 environment for API mode.

## Example Output

Input:

```json
{
  "incident": "Application cannot connect to database and connection timeout error is showing"
}
```

Output shape:

```json
{
  "summary": "Application cannot connect to database with connection timeout error",
  "severity": "High",
  "retrieval_confidence": "Medium",
  "grounding_note": "Grounded on 'Database Connection Failure' with medium retrieval confidence. Validate the checks before confirming the root cause.",
  "probable_causes": [
    "Database listener is down",
    "Wrong database credentials",
    "Network issue between app and database",
    "Connection pool is exhausted"
  ],
  "checks": [
    "Check database listener status",
    "Verify database host and port",
    "Check application connection pool",
    "Review database alert logs"
  ],
  "fix_steps": [
    "Restart listener after approval",
    "Correct connection string if misconfigured",
    "Scale or reset connection pool if exhausted",
    "Escalate to DBA team if database is unavailable"
  ]
}
```

More examples are available in:

```txt
examples/
```

## Evaluate Retrieval

Run:

```bash
python scripts/evaluate_retrieval.py
```

Current sample result:

```txt
Passed: 5/5
Top-1 retrieval accuracy: 100%
```

The evaluation checks whether OpsSage retrieves the expected runbook or matching
past incident for known incident inputs.

## How RAG Works Here

1. Markdown runbooks and incident notes are loaded from `data/`.
2. Each document is converted into an embedding.
3. The user incident is converted into an embedding.
4. Vector search retrieves the closest documents.
5. Retrieved context is passed to the LLM prompt.
6. The response is normalized into a stable JSON-like schema.
7. Grounding fields explain which document supported the answer.

## Why RAG Instead Of Fine-Tuning First

Operational knowledge changes often. With RAG, new knowledge can be added by
updating a runbook file instead of retraining a model.

Fine-tuning can be added later for narrower tasks such as:

- severity classification
- incident category prediction
- incident report writing style

## Learning Notes

This project intentionally includes a [TRAINING_GUIDE.md](TRAINING_GUIDE.md)
for beginners. It explains each module, the algorithmic idea behind it, and the
takeaway from building it.

For interview preparation, see [docs/interview-notes.md](docs/interview-notes.md).

## Roadmap

- Add a Python 3.11/3.12 virtual environment guide
- Add a small frontend after backend behavior is stable
- Add source citations per generated fix step
- Add persistent FAISS index storage
- Add Hugging Face log dataset ingestion
- Add severity/category classifier
- Add Docker setup
- Add CI workflow for retrieval evaluation
