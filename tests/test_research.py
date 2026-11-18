import unittest

from select_markets_explorer.research import (
    research_signal, signals_from_observations,
)


class MockFinder:
    def search(self, phrase):
        return [{"url": "https://example.org/approved", "terms_url":
                 "https://example.org/terms", "permitted": True,
                 "description": phrase},
                {"url": "https://example.org/blocked", "permitted": False}]


class MockSampler:
    def sample(self, source, *, limit):
        return [{"id": str(i), "price": i+100} for i in range(min(limit, 8))]


class ResearchTests(unittest.TestCase):
    def test_novel_niche_end_to_end_no_fixed_list(self):
        rows = [{"market_tags": ["subsea survey instruments"]},
                {"market_tags": ["subsea survey instruments"]}]
        [signal] = signals_from_observations(rows)
        self.assertEqual(signal.name, "subsea survey instruments")
        dossier = research_signal(signal, MockFinder(), MockSampler())
        self.assertEqual(dossier["status"], "research")
        self.assertEqual(dossier["sample_size"], 0)
        self.assertEqual(len(dossier["rejected_sources"]), 1)
        self.assertFalse(dossier["viability_demonstrated"])

    def test_zero_verified_sources_abstains(self):
        [signal] = signals_from_observations([{"market_tags": ["new-niche"]},{"market_tags":["new-niche"]}])
        class NoneFinder:
            def search(self, phrase):
                return []
        result = research_signal(signal, NoneFinder(), MockSampler())
        self.assertEqual(result["status"], "research")


if __name__ == "__main__":
    unittest.main()
