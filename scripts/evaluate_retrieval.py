import json
import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from app.services.incident_analyzer import IncidentAnalyzer, _retrieval_confidence


CASES_PATH = PROJECT_ROOT / "evaluation" / "retrieval_cases.json"


def main() -> None:
    cases = json.loads(CASES_PATH.read_text(encoding="utf-8"))
    analyzer = IncidentAnalyzer()
    passed = 0

    print("OpsSage AI Retrieval Evaluation")
    print("=" * 34)

    for index, case in enumerate(cases, start=1):
        results = analyzer.retrieve(case["incident"])
        top_document = results[0].document.title if results else "No document found"
        accepted = case["accepted_top_documents"]
        is_pass = top_document in accepted
        passed += int(is_pass)

        status = "PASS" if is_pass else "FAIL"
        print(f"\n{index}. {status}")
        print(f"Incident: {case['incident']}")
        print(f"Accepted: {', '.join(accepted)}")
        print(f"Actual:   {top_document}")
        print(f"Confidence: {_retrieval_confidence(results)}")

    accuracy = passed / len(cases) if cases else 0
    print("\nSummary")
    print("-" * 7)
    print(f"Passed: {passed}/{len(cases)}")
    print(f"Top-1 retrieval accuracy: {accuracy:.0%}")


if __name__ == "__main__":
    main()
