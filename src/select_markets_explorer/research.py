"""Open-signal market research with provider-injected permitted-source discovery."""
from collections import Counter
from datetime import datetime, timezone, timedelta
from decimal import Decimal, InvalidOperation
from statistics import median
from typing import Protocol
from urllib.parse import urlencode
from urllib.request import Request, urlopen
import json

from .engine import Signal, Evidence, evaluate_market


class Finder(Protocol):
    def search(self, phrase: str) -> list[dict]:
        """Return source URLs, terms, documented permission and quality indicators."""


class Sampler(Protocol):
    def sample(self, source: dict, *, limit: int) -> list[dict]:
        """Return bounded, legally accessible observed market items."""


def signals_from_observations(records: list[dict], min_occurrences: int = 2) -> list[Signal]:
    """Generate novel-market signals from external metadata, no hardcoded sectors."""
    counts = Counter()
    for record in records:
        for label in record.get("market_tags", [])[:10]:
            label = str(label).strip()
            if len(label) > 2:
                counts[label] += 1
    return [Signal(name=name, description=f"Investigar mercado emergente: {name}",
                   potential_use="Procura e comparação privadas de oportunidades")
            for name, count in counts.items() if count >= min_occurrences]



def _verified_sample(sample: dict, now: datetime) -> tuple[str, Decimal, str] | None:
    """Only recent, priced, identified, accessible offers count toward evidence."""
    try:
        ident = str(sample["id"]).strip()
        price = Decimal(str(sample["price"]))
        currency = str(sample["currency"])
        stamp = datetime.fromisoformat(str(sample["observed_at"]).replace("Z", "+00:00"))
        url = str(sample["url"])
        if (not ident or not price.is_finite() or price <= 0 or
                len(currency) != 3 or not currency.isupper() or
                stamp.tzinfo is None or not timedelta(0) <= now - stamp <= timedelta(days=90) or
                not url.startswith("https://") or sample.get("available") is not True):
            return None
        return (ident, price, currency)
    except (KeyError, ValueError, InvalidOperation, TypeError):
        return None


def research_signal(signal: Signal, finder: Finder, sampler: Sampler,
                    *, source_limit: int = 6, sample_limit: int = 12,
                    now: datetime | None = None) -> dict:
    """Conservative two-source viability dossier, never a profitability prediction."""
    if not 1 <= source_limit <= 20 or not 1 <= sample_limit <= 50:
        raise ValueError("Research limits out of range")
    now = now or datetime.now(timezone.utc)
    if now.tzinfo is None:
        raise ValueError("Research timestamp requires timezone")
    sources = finder.search(signal.name)
    evidence, rejected, market_samples, used_sources = [], [], [], set()
    global_ids = set()
    for source in sources[:source_limit]:
        url = str(source.get("url", ""))
        terms = str(source.get("terms_url", ""))
        if (source.get("permitted") is not True or not terms.startswith("https://") or
                not url.startswith("https://") or url in used_sources):
            rejected.append({"url": url, "reason": "permission, terms or unique source unverified"})
            continue
        used_sources.add(url)
        try:
            observations = sampler.sample(source, limit=sample_limit)
            verified = []
            for observation in observations[:sample_limit]:
                record = _verified_sample(observation, now)
                if record is None or (url, record[0]) in global_ids:
                    continue
                global_ids.add((url, record[0]))
                verified.append(record)
                market_samples.append(record)
            evidence.append(Evidence.validated({
                "url": url, "description": str(source.get("description") or signal.name),
                "observed_at": now.isoformat(), "permitted": True,
                "sample_count": len(verified),
            }))
        except (TimeoutError, ConnectionError, KeyError, ValueError, TypeError) as exc:
            rejected.append({"url": url, "reason": type(exc).__name__})
    dossier = evaluate_market(signal, evidence)
    source_count = sum(1 for entry in evidence if entry.sample_count >= 2)
    currencies = {currency for _, _, currency in market_samples}
    market_median = None
    if len(currencies) == 1 and market_samples:
        market_median = str(median([v for _, v, _ in market_samples]))
    qualified = (source_count >= 2 and len(market_samples) >= 6 and
                 len(currencies) == 1 and market_median is not None)
    # One feed or one category mention cannot establish an economically viable niche.
    dossier["status"] = "test" if qualified else "research"
    dossier["rationale"] = (
        "At least two permitted sources with recent independently observed price offers; "
        "controlled pilot may be considered, economics and liquidity unverified"
        if qualified else
        "Insufficient independent, recent, price-consistent permitted offers; more research required"
    )
    dossier["rejected_sources"] = rejected
    dossier["sample_size"] = len(market_samples)
    dossier["independent_sources"] = source_count
    dossier["source_limit"] = source_limit
    dossier["currency"] = next(iter(currencies)) if len(currencies) == 1 else None
    dossier["observed_price_median"] = market_median
    dossier["viability_demonstrated"] = False
    dossier["limitation"] = ("These are asking prices, not verified transactions, demand, "
                             "liquidity, purchase profitability or reuse rights beyond supplied metadata.")
    return dossier


class OpenAlexResearch:
    """Optional real scholarly research provider. Does not return sale listings."""

    def __init__(self, api_key: str | None = None, transport=None):
        self.api_key, self.transport = api_key, transport or urlopen

    def search(self, phrase: str, limit: int = 5) -> list[dict]:
        if not 1 <= limit <= 10:
            raise ValueError("Limit outside 1..10")
        query = urlencode({"search": phrase, "per-page": limit,
                           **({"api_key": self.api_key} if self.api_key else {})})
        url = "https://api.openalex.org/works?" + query
        with self.transport(Request(url, headers={"Accept": "application/json"}),timeout=15) as response:
            document = json.loads(response.read(2_000_000))
        return [{"url": item.get("id"), "title": item.get("display_name"),
                 "year": item.get("publication_year"), "source": "OpenAlex",
                 "topics": [
                     p.get("display_name") for p in item.get("topics", [])[:5]
                     if p.get("display_name")
                 ],
                 "keywords": [
                     p.get("display_name") for p in item.get("keywords", [])[:8]
                     if p.get("display_name")
                 ]}
                for item in document.get("results", [])]
