"""Live, bounded market-candidate discovery using OpenAlex scholarly metadata.

A scholarly topic is a hypothesis, not proof of commercial viability.
No source without documented collection and reuse permission is sampled.
"""
import argparse
import json
import os
from urllib.parse import urlsplit
from urllib.request import Request, urlopen

from .market_research import explore_open_markets
from .research import OpenAlexResearch


class NoApprovedSources:
    def search(self, phrase: str):
        return []


class NoApprovedSamples:
    def sample(self, source: dict, *, limit: int):
        return []


def discover_candidates(seeds: list[str], *, research=None,
                        finder=None, sampler=None, max_hypotheses=4) -> list[dict]:
    if not seeds or len(seeds) > 10 or any(not 3 <= len(x.strip()) <= 100 for x in seeds):
        raise ValueError("Specify 1 to 10 bounded research seeds")
    provider = research or OpenAlexResearch(api_key=os.getenv("OPENALEX_API_KEY"))
    dossiers = explore_open_markets(seeds, provider, finder or NoApprovedSources(),
                                   sampler or NoApprovedSamples(),
                                   max_hypotheses=max_hypotheses)
    for dossier in dossiers:
        if dossier.get("independent_sources", 0) < 2:
            dossier["viability_demonstrated"] = False
            dossier["status"] = "research"
    return dossiers


def submit_hypotheses(dossiers: list[dict], base_url: str, token: str, *,
                      transport=urlopen) -> int:
    parsed = urlsplit(base_url)
    if (parsed.scheme != "https" or not parsed.hostname or parsed.username
            or parsed.password or parsed.query or parsed.fragment
            or parsed.hostname.endswith((".invalid", ".test", ".example"))
            or not token):
        raise ValueError("A private HTTPS Platform endpoint and token are required")
    count = 0
    for dossier in dossiers:
        # Never promote a niche directly from scholarly topic metadata.
        if dossier.get("status") not in ("research", "test"):
            raise ValueError("Unsafe hypothesis status")
        request = Request(base_url.rstrip("/") + "/v1/hypotheses",
            data=json.dumps(dossier).encode(),
            headers={"Authorization": "Bearer " + token,
                     "Content-Type": "application/json", "Accept": "application/json"},
            method="POST")
        with transport(request, timeout=20) as response:
            if response.status not in (200, 201):
                raise RuntimeError("Platform refused research submission")
            response.read(128_000)
        count += 1
    return count


def main() -> int:
    parser = argparse.ArgumentParser(description="Bounded OpenAlex market research")
    parser.add_argument("--seed", action="append", required=True)
    parser.add_argument("--max-hypotheses", type=int, default=4)
    parser.add_argument("--commit", action="store_true",
                        help="Explicitly persist research hypotheses to private Platform")
    args = parser.parse_args()
    dossiers = discover_candidates(args.seed, max_hypotheses=args.max_hypotheses)
    if args.commit:
        submit_hypotheses(dossiers, os.environ["SELECT_PLATFORM_URL"],
                          os.environ["SELECT_API_TOKEN"])
    print(json.dumps({"hypotheses": dossiers, "persisted": bool(args.commit)},
                     ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
