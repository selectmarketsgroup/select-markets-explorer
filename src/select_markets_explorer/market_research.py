"""Open-world hypothesis generation via research concepts, never fixed category lists."""
from collections import Counter
from typing import Protocol
from .engine import Signal
from .research import research_signal, Finder, Sampler


class ResearchFeed(Protocol):
    def search(self, phrase: str, limit: int = 5) -> list[dict]: ...


def explore_open_markets(seeds: list[str], research: ResearchFeed, finder: Finder,
                         sampler: Sampler, *, max_hypotheses: int = 4,
                         research_per_seed: int = 6, now=None) -> list[dict]:
    """Research adjacent markets not present in seeds; validate every discovery."""
    if not 1 <= len(seeds) <= 10 or not 1 <= max_hypotheses <= 10:
        raise ValueError("Bounded seed and hypothesis limits required")
    canonical_seeds = {s.strip().casefold() for s in seeds if len(s.strip()) >= 3}
    concepts = Counter()
    origins = {}
    for seed in list(canonical_seeds):
        for item in research.search(seed, limit=research_per_seed):
            for name in (item.get("topics") or []) + (item.get("keywords") or []):
                name = str(name).strip()
                if not 4 <= len(name) <= 120 or name.casefold() in canonical_seeds:
                    continue
                concepts[name] += 1
                if item.get("url"):
                    origins.setdefault(name, set()).add(item["url"])
    candidates = sorted(concepts, key=lambda n: (-concepts[n], n.casefold()))
    dossiers = []
    for candidate in candidates[:max_hypotheses]:
        signal = Signal(name=candidate, description=f"Mercado candidato: {candidate}",
                        potential_use="Investigar ofertas e revenda privada")
        dossier = research_signal(signal, finder, sampler, now=now)
        dossier["hypothesis_origin"] = {
            "research_count": concepts[candidate],
            "research_urls": sorted(origins.get(candidate, set()))[:8],
            "seed_topics": sorted(canonical_seeds),
        }
        dossiers.append(dossier)
    return dossiers
