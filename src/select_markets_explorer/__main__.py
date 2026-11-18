"""Single manually-invoked market screening; does not conduct web searches."""
import json
import sys

from .engine import Evidence, Signal, evaluate_market


def main():
    payload = json.load(sys.stdin)
    signal = Signal.from_dict(payload["signal"])
    evidence = [Evidence.validated(x) for x in payload.get("evidence", [])]
    result = evaluate_market(signal, evidence, payload.get("budget_eur"))
    print(json.dumps(result))


if __name__ == "__main__":
    main()
