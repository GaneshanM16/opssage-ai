# OpsSage AI Training Guide

Use this guide as your learning path while building the project.

## Module 1: Problem Definition

OpsSage AI solves this problem:

```txt
Given an incident or log message, find relevant troubleshooting knowledge and
generate a structured response.
```

Child-level explanation:

```txt
The app has a notebook of known problems. When a new problem appears, it finds
similar notebook pages and explains what to do.
```

## Module 2: Knowledge Base

Location:

```txt
data/runbooks/
data/incidents/
```

What it stores:

- symptoms
- likely causes
- checks
- fix steps
- severity

Approach used:

```txt
Document-based knowledge base
```

Takeaway:

You learn how AI systems use external documents instead of depending only on
model memory.

## Module 3: Embeddings

File:

```txt
app/services/embedding.py
```

What embeddings do:

```txt
Text -> numbers that represent meaning
```

Portfolio model:

```txt
sentence-transformers/all-MiniLM-L6-v2
```

Algorithm family:

```txt
Transformer-based sentence embedding
```

Current fallback:

```txt
Hashing-based embedding
```

Takeaway:

You learn how semantic search understands similar meaning even when words are
different.

## Module 4: Vector Search

File:

```txt
app/services/vector_store.py
```

What it does:

```txt
Finds documents whose vectors are closest to the incident vector.
```

Portfolio tool:

```txt
FAISS
```

Algorithm:

```txt
Nearest neighbor search
```

Current fallback:

```txt
Cosine similarity over local vectors
```

Takeaway:

You learn the core idea behind vector databases and semantic retrieval.

## Module 5: RAG

RAG means:

```txt
Retrieval Augmented Generation
```

Flow:

```txt
User incident
-> retrieve similar documents
-> put documents into prompt
-> LLM generates answer
```

Takeaway:

You learn when to use RAG instead of fine-tuning.

## Module 6: LLM Generation

File:

```txt
app/services/llm.py
```

Portfolio tool:

```txt
Ollama + Llama 3.2
```

Algorithm family:

```txt
Transformer decoder language model
```

Takeaway:

You learn how to send context to a local LLM and request structured JSON output.

## Module 7: FastAPI

File:

```txt
app/main.py
```

What it does:

```txt
Turns the project into an API that other apps can call.
```

Endpoint:

```txt
POST /analyze-incident
```

Takeaway:

You learn backend API design for AI applications.

Beginner fallback:

```txt
app/simple_api.py
```

This uses Python's built-in HTTP server. It is not as professional as FastAPI,
but it teaches the same API idea while avoiding Python package issues.

## Module 8: Evaluation

Files:

```txt
evaluation/retrieval_cases.json
scripts/evaluate_retrieval.py
```

What evaluation does:

```txt
Checks whether the system retrieves the expected runbook for known incidents.
```

Metric:

```txt
Top-1 retrieval accuracy
```

Child-level explanation:

```txt
We give the app a quiz. For each problem, we already know the correct notebook
page or a correct past incident. If the app picks one of those first, it gets
one point.
```

Takeaway:

You learn how to test an AI system instead of trusting one good demo.

## Hugging Face Dataset Plan

Use Hugging Face later for sample logs, not for training at first.

Good search terms:

```txt
LogHub
HDFS logs
BGL logs
OpenStack logs
Apache logs
Linux logs
AIOps anomaly detection
```

Beginner-friendly approach:

```txt
Use public logs as sample inputs.
Use your own runbooks as solution knowledge.
```

## Future Fine-Tuning Plan

Do not fine-tune in version 1.

Fine-tune later only after collecting structured examples like:

```json
{
  "incident": "ORA-01652 unable to extend temp segment",
  "category": "Oracle TEMP tablespace",
  "severity": "High",
  "resolution": "Check TEMP usage and add tempfile after approval"
}
```

Possible future fine-tuning tasks:

- severity classification
- incident category classification
- incident report writing style
