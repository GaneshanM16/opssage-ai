import json
import sys

from app.services.incident_analyzer import IncidentAnalyzer


def main() -> None:
    incident = " ".join(sys.argv[1:]).strip()
    if not incident:
        incident = "ORA-01652 unable to extend temp segment in tablespace TEMP"

    analyzer = IncidentAnalyzer()
    analysis = analyzer.analyze(incident)
    print(json.dumps(analysis.model_dump(), indent=2))


if __name__ == "__main__":
    main()

