# OpsSage AI Interview Notes

Use this file to explain OpsSage AI in interviews.

## 30-Second Explanation

OpsSage AI is a RAG-based incident analysis assistant for production support.
When a user provides an incident, log, or error message, the system retrieves
the most relevant runbooks or past incidents using semantic search. It then
uses an LLM-style generation layer to produce a structured troubleshooting
response with severity, probable causes, checks, fix steps, grounding notes,
and retrieved source documents.

## Child-Level Explanation

Imagine an engineer has a notebook of old problems and fixes. When a new
problem happens, OpsSage AI searches the notebook for similar problems, reads
the matching pages, and suggests what the engineer should check next.

It does not magically know the answer. It first finds useful documents, then
uses those documents to help write the answer.

## Problem It Solves

Production support teams often waste time searching through runbooks, old
incident notes, and error references. OpsSage AI reduces that search time by
retrieving the closest operational knowledge and turning it into a structured
incident response.

## System Design

```txt
Incident/log text
    |
    v
Document loader
Loads runbooks and past incidents from Markdown files
    |
    v
Embedding model
Turns text into vectors
    |
    v
Vector store
Finds similar documents
    |
    v
Retriever
Returns top matching runbooks/incidents
    |
    v
LLM prompt
Combines user incident and retrieved context
    |
    v
Structured response
Summary, severity, causes, checks, fixes, grounding
```

## Main Components

| Component | File | Purpose |
| --- | --- | --- |
| Document loader | `app/services/document_loader.py` | Reads Markdown runbooks and incidents |
| Embedding model | `app/services/embedding.py` | Converts text into vectors |
| Vector store | `app/services/vector_store.py` | Searches similar document vectors |
| LLM layer | `app/services/llm.py` | Builds prompt and generates response |
| Analyzer | `app/services/incident_analyzer.py` | Connects retrieval and generation |
| Simple API | `app/simple_api.py` | Runs a local API without FastAPI |
| FastAPI app | `app/main.py` | Optional production-style API |
| Evaluation | `scripts/evaluate_retrieval.py` | Tests retrieval accuracy |

## Algorithms And Approaches Used

### 1. Embeddings

Embeddings convert text into numerical vectors.

Example:

```txt
"Database connection timeout" -> [0.12, -0.44, 0.08, ...]
```

The project uses `sentence-transformers/all-MiniLM-L6-v2` when available.
This is a pretrained transformer-based sentence embedding model from Hugging
Face.

Interview explanation:

```txt
I used a pretrained sentence-transformer model to represent incidents and
runbooks as vectors, so similar meanings are close together in vector space.
```

### 2. Vector Search

Vector search finds the closest document vectors to the incident vector.

The project uses FAISS when available, with fallback cosine similarity for
beginner-friendly execution.

Interview explanation:

```txt
After converting the incident into an embedding, I used vector search to
retrieve the most semantically similar runbooks and past incidents.
```

### 3. RAG

RAG means Retrieval Augmented Generation.

In this project:

```txt
Retrieve relevant runbooks first.
Then generate the incident response using that context.
```

Interview explanation:

```txt
I chose RAG because operational knowledge changes often. Updating Markdown
runbooks is faster and safer than fine-tuning a model every time support
knowledge changes.
```

### 4. Grounded Reporting

The system includes `retrieval_confidence` and `grounding_note`.

This avoids overclaiming. Instead of saying:

```txt
The root cause is wrong credentials.
```

It says:

```txt
Possible causes include listener outage, credential issue, network issue, or
connection pool exhaustion. Validate checks before confirming root cause.
```

Interview explanation:

```txt
I added grounding fields and cautious report generation because incident
systems should not claim a root cause is confirmed unless evidence proves it.
```

## Why Not Fine-Tuning First?

Fine-tuning is useful when you have many labeled examples and want the model to
learn a repeated behavior.

For this project, RAG is better first because:

- runbooks change often
- support knowledge should be auditable
- source documents should be visible
- no large training dataset is required
- updates are faster and cheaper

Future fine-tuning can be added for:

- severity classification
- incident category classification
- incident report writing style

## Hugging Face Usage

Current usage:

```txt
Pretrained embedding model from Hugging Face
```

Possible future usage:

```txt
Public log datasets such as HDFS, BGL, OpenStack, Apache, or AIOps datasets
```

Important explanation:

```txt
I do not need to train a dataset for the MVP. I use pretrained embeddings and
my own runbooks as the knowledge base. Hugging Face datasets can later provide
more sample logs for testing and evaluation.
```

## Evaluation

The project includes retrieval evaluation:

```bash
python scripts/evaluate_retrieval.py
```

Current sample result:

```txt
Passed: 5/5
Top-1 retrieval accuracy: 100%
```

How to explain it:

```txt
I created sample incident test cases and checked whether the system retrieved
the expected runbook or matching past incident as the top result.
```

## Limitations

Be honest about these in interviews:

- small sample knowledge base
- confidence thresholds are simple and need calibration
- no persistent vector index yet
- no frontend yet
- FastAPI mode may need Python 3.11/3.12 for smoother dependency support
- current evaluation is small and should be expanded
- generated fix steps still require human validation

## Future Improvements

- Add persistent FAISS index files
- Add more real-world runbooks
- Add Hugging Face log datasets for testing
- Add citations per fix step
- Add Docker setup
- Add CI workflow to run retrieval evaluation
- Add a small frontend
- Add severity/category classifier
- Add fine-tuning after collecting labeled incident examples

## Interview Questions And Answers

### What is OpsSage AI?

OpsSage AI is a RAG-based incident analysis assistant. It retrieves relevant
runbooks or past incidents and generates structured troubleshooting guidance.

### Why did you use RAG?

I used RAG because operational support knowledge changes frequently. With RAG,
I can update the knowledge base by editing runbooks instead of retraining a
model.

### What model did you use?

For embeddings, I used a pretrained Hugging Face sentence-transformer model:
`sentence-transformers/all-MiniLM-L6-v2`. For generation, the project supports
Ollama/Llama-style local LLM generation and includes fallback behavior.

### What is FAISS doing?

FAISS performs vector similarity search. It finds the runbooks whose embeddings
are closest to the incident embedding.

### How do you reduce hallucination?

I retrieve source documents first, include them in the prompt, add grounding
notes, normalize the output schema, and avoid claiming a root cause is confirmed
unless the incident evidence proves it.

### How do you evaluate the system?

I use retrieval evaluation. For known incident inputs, I check whether the
expected runbook or past incident is retrieved as the top result.

### What did you learn?

I learned how to design a RAG pipeline, use pretrained embeddings, perform
vector search, structure LLM outputs, add grounding, and evaluate retrieval
quality.

## Resume Bullet

```txt
Built OpsSage AI, a RAG-based incident analysis assistant using Python,
Hugging Face sentence-transformer embeddings, FAISS vector search, and
local LLM-compatible generation to retrieve runbooks, classify incident
severity, suggest validation checks, and generate grounded troubleshooting
reports.
```

