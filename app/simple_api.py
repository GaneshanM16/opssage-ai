import json
from http.server import BaseHTTPRequestHandler, HTTPServer

from app.services.incident_analyzer import IncidentAnalyzer


analyzer = IncidentAnalyzer()


class OpsSageRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self) -> None:
        if self.path != "/health":
            self._send_json({"error": "Not found"}, status=404)
            return

        self._send_json(
            {
                "status": "ok",
                "documents_loaded": len(analyzer.documents),
                "embedding_model": analyzer.embedding_model.name,
            }
        )

    def do_POST(self) -> None:
        if self.path != "/analyze-incident":
            self._send_json({"error": "Not found"}, status=404)
            return

        try:
            content_length = int(self.headers.get("Content-Length", "0"))
            body = self.rfile.read(content_length).decode("utf-8")
            payload = json.loads(body)
            incident = str(payload.get("incident", "")).strip()

            if len(incident) < 5:
                self._send_json(
                    {"error": "incident must contain at least 5 characters"},
                    status=400,
                )
                return

            analysis = analyzer.analyze(incident)
            self._send_json(analysis.model_dump())
        except json.JSONDecodeError:
            self._send_json({"error": "Request body must be valid JSON"}, status=400)

    def log_message(self, format: str, *args) -> None:
        return

    def _send_json(self, payload: dict, status: int = 200) -> None:
        response = json.dumps(payload, indent=2).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(response)))
        self.end_headers()
        self.wfile.write(response)


def main() -> None:
    host = "127.0.0.1"
    port = 8000
    print("Loading OpsSage analyzer...", flush=True)
    server = HTTPServer((host, port), OpsSageRequestHandler)
    print(f"OpsSage simple API running at http://{host}:{port}", flush=True)
    print("Try GET /health or POST /analyze-incident", flush=True)
    server.serve_forever()


if __name__ == "__main__":
    main()
