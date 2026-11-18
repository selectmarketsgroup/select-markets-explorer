"""Market hypothesis screening with real, attributable evidence."""
from dataclasses import dataclass
from hashlib import sha256
from urllib.parse import urlparse


@dataclass(frozen=True)
class Evidence:
    url: str
    description: str
    observed_at: str
    permitted: bool
    sample_count: int = 0

    @classmethod
    def validated(cls, raw: dict) -> "Evidence":
        e = cls(**raw)
        if urlparse(e.url).scheme != "https" or not e.description or not e.observed_at:
            raise ValueError("Evidence requires HTTPS URL, description and date")
        if e.sample_count < 0:
            raise ValueError("Sample count cannot be negative")
        return e


@dataclass(frozen=True)
class Signal:
    name: str
    description: str
    potential_use: str

    @classmethod
    def from_dict(cls, raw: dict) -> "Signal":
        s = cls(**raw)
        if len(s.name.strip()) < 3 or not s.description or not s.potential_use:
            raise ValueError("Incomplete market signal")
        return s


def identify_signals(events: list[dict]) -> list[Signal]:
    """Never require a closed list of segments, brands or symbols."""
    unique = {}
    for event in events:
        try:
            signal = Signal.from_dict(event)
        except (ValueError, TypeError):
            continue
        unique.setdefault(signal.name.strip().casefold(), signal)
    return list(unique.values())


def evaluate_market(signal: Signal, evidence: list[Evidence],
                    available_budget_eur: int | None = None) -> dict:
    permitted = [x for x in evidence if x.permitted]
    sample = sum(x.sample_count for x in permitted)
    if available_budget_eur is not None and available_budget_eur < 0:
        raise ValueError("Budget cannot be negative")
    # No claim of market size or returns: this is a screening decision.
    if not permitted:
        state = "research"
        rationale = "No licensed or permitted evidence source has been verified"
    elif sample < 5:
        state = "test"
        rationale = "Permitted source identified, but too few verified observations"
    else:
        state = "test"
        rationale = "Sample sufficient for a controlled pilot; economic merit remains unproven"
    if available_budget_eur == 0:
        rationale += "; paid sources and paid experiments are excluded"
    return {"market": signal.name, "title": signal.description[:250],
            "status": state, "rationale": rationale,
            "evidence": [{"url": e.url, "description": e.description,
                          "observed_at": e.observed_at, "permitted": e.permitted,
                          "sample_count": e.sample_count} for e in evidence]}


def proposal_identity(signal: Signal) -> str:
    return sha256(signal.name.strip().casefold().encode()).hexdigest()


def route_to_existing_unit(category: str | None) -> str | None:
    """Advisory mapping. Unknown niches intentionally remain unclassified."""
    if category in ("real_estate", "property"):
        return "homes"
    if category in ("vehicle", "automotive"):
        return "motors"
    if category in ("goods", "equipment", "products"):
        return "deals"
    return None
