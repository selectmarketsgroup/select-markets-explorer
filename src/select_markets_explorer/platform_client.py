"""Persist and revise versioned hypotheses in Platform; no direct DB access."""
from urllib.request import Request, urlopen
import json


def save_hypothesis(base_url: str, token: str, dossier: dict,
                    *, hypothesis_id: str | None = None, transport=None) -> dict:
    if not base_url.startswith("https://") or not token:
        raise ValueError("Private HTTPS Platform and scoped token required")
    if hypothesis_id is None:
        method = "POST"
        path = "/v1/hypotheses"
    else:
        method = "PUT"
        path = "/v1/hypotheses/" + hypothesis_id
    payload = {key: dossier[key] for key in
               ("market", "title", "status", "rationale", "evidence")}
    # These diagnostics must survive the Platform persistence boundary.
    fields = ("sample_size", "independent_sources", "observed_price_median",
              "currency", "viability_demonstrated", "hypothesis_origin",
              "rejected_sources", "limitation", "source_limit")
    details = {key: dossier[key] for key in fields if key in dossier}
    details.update(dossier.get("research_details") or {})
    payload["research_details"] = details
    transport = transport or urlopen
    req = Request(base_url.rstrip("/") + path,
                  data=json.dumps(payload).encode(),
                  headers={"Authorization": "Bearer " + token,
                           "Content-Type": "application/json"}, method=method)
    with transport(req, timeout=20) as response:
        return json.loads(response.read())
