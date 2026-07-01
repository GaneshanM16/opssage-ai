import json
import urllib.error
import urllib.request
from typing import List

from app.config import OLLAMA_MODEL, OLLAMA_URL
from app.services.vector_store import SearchResult


def generate_analysis(incident: str, results: List[SearchResult]) -> dict:
    prompt = _build_prompt(incident, results)

    try:
        payload = json.dumps(
            {
                "model": OLLAMA_MODEL,
                "prompt": prompt,
                "stream": False,
                "format": "json",
            }
        ).encode("utf-8")

        request = urllib.request.Request(
            OLLAMA_URL,
            data=payload,
            headers={"Content-Type": "application/json"},
            method="POST",
        )

        with urllib.request.urlopen(request, timeout=60) as response:
            body = json.loads(response.read().decode("utf-8"))
            return json.loads(body.get("response", "{}"))
    except (urllib.error.URLError, TimeoutError, json.JSONDecodeError, KeyError):
        return _fallback_analysis(incident, results)


def _build_prompt(incident: str, results: List[SearchResult]) -> str:
    context = "\n\n".join(
        f"Document: {result.document.title}\n{result.document.text}"
        for result in results
    )

    return f"""
You are OpsSage AI, an incident response assistant.

Use only the provided context. If the context is not enough, say what should be
checked next. Do not invent timestamps, ticket IDs, people, or status values.
Return valid JSON with these exact keys:
summary, severity, probable_causes, checks, fix_steps, incident_report.

Rules:
- summary must be a string.
- severity must be a string.
- probable_causes, checks, and fix_steps must be arrays of strings.
- incident_report must be one short string, not an object.
- Use cautious words like possible, likely, may, and requires validation.
- Do not claim a root cause is confirmed unless the incident explicitly proves it.
- Do not add extra keys.

Incident:
{incident}

Retrieved context:
{context}
""".strip()


def _fallback_analysis(incident: str, results: List[SearchResult]) -> dict:
    best = results[0].document if results else None
    title = best.title if best else "No matching runbook"

    return {
        "summary": f"OpsSage found the closest runbook: {title}.",
        "severity": "Needs human review",
        "probable_causes": [
            "The retrieved runbook contains the closest known issue pattern.",
            "Use the checks below to confirm the exact root cause.",
        ],
        "checks": [
            "Compare the incident symptoms with the retrieved runbook.",
            "Check recent changes, resource usage, and related service health.",
            "Collect exact error codes, timestamps, and affected users.",
        ],
        "fix_steps": [
            "Follow the matched runbook after validating the symptoms.",
            "Escalate if the issue affects production users or critical jobs.",
            "Document the final root cause and resolution for future retrieval.",
        ],
        "incident_report": (
            f"Incident analyzed: {incident}. Closest knowledge source: {title}. "
            "Possible causes should be validated through the recommended checks."
        ),
    }
