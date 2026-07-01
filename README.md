# OpsSage AI

OpsSage AI is a beginner-friendly RAG project for incident analysis.

The app accepts a production incident, log, or error message, retrieves relevant
runbooks, and generates a structured troubleshooting response.

## What You Are Building

```txt
Incident text
-> embedding model
-> vector search
-> relevant runbooks
-> LLM prompt
-> structured incident analysis
```

## Beginner Explanation

Imagine OpsSage AI has a notebook of old problems and fixes. When a new issue
comes in, it finds the most similar notes, reads them, and explains what to do.

## First Learning Modules

1. `data/runbooks/` stores troubleshooting knowledge.
2. `app/services/document_loader.py` reads those files.
3. `app/services/embedding.py` turns text into vectors.
4. `app/services/vector_store.py` searches for similar documents.
5. `app/services/llm.py` asks Ollama to generate the final answer.
6. `app/services/incident_analyzer.py` connects the whole flow.
7. `app/main.py` exposes the FastAPI endpoint.

## Quick Demo Without Installing Anything

This uses the fallback local search and rule-based answer generator:

```bash
python -m app.demo "ORA-01652 unable to extend temp segment in tablespace TEMP"
```

Run it from this folder:

```bash
cd opssage-ai
```

## Run A Local API Without FastAPI

If your Python version cannot install FastAPI/Pydantic yet, run the plain-Python
API:

```bash
python -m app.simple_api
```

Health check:

```bash
curl http://127.0.0.1:8000/health
```

Analyze an incident:

```bash
curl -X POST http://127.0.0.1:8000/analyze-incident ^
  -H "Content-Type: application/json" ^
  -d "{\"incident\":\"Application cannot connect to database and connection timeout error is showing\"}"
```

## Portfolio Mode

Install the RAG dependencies first:

```bash
pip install -r requirements.txt
```

Install the API dependencies after the RAG install works:

```bash
pip install -r requirements-api.txt
```

Or install everything at once:

```bash
pip install -r requirements-full.txt
```

Start Ollama in another terminal and pull a model:

```bash
ollama pull llama3.2
```

Start the API:

```bash
uvicorn app.main:app --reload
```

Test:

```bash
curl -X POST http://127.0.0.1:8000/analyze-incident ^
  -H "Content-Type: application/json" ^
  -d "{\"incident\":\"ORA-01652 unable to extend temp segment in tablespace TEMP\"}"
```

## Evaluate Retrieval

Run the retrieval evaluation script:

```bash
python scripts/evaluate_retrieval.py
```

This checks whether OpsSage retrieves the expected top runbook for sample
incidents and prints top-1 retrieval accuracy.

## Examples

Sample requests and responses are available in:

```txt
examples/
```

Use these files to quickly explain the project in interviews or on GitHub.

## Why RAG First

RAG is the right first version because operational knowledge changes often.
Instead of fine-tuning a model every time a runbook changes, we update the
documents and rebuild/search the knowledge base.

Future versions can add fine-tuning for severity classification or incident
category prediction.
