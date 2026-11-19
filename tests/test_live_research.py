"""Real research boundary: open scholarly topics never become market facts."""
import unittest

from select_markets_explorer.live_research import (
    discover_candidates, submit_hypotheses,
)


class FakeResearch:
    def search(self, seed, limit=5):
        return [
            {"url": "https://openalex.org/W1",
             "topics": ["Rare industrial inspection equipment"]},
            {"url": "https://openalex.org/W2",
             "topics": ["Rare industrial inspection equipment"]},
        ]


class ResearchTests(unittest.TestCase):
    def test_genuine_topic_without_approved_price_sources_remains_research(self):
        dossiers = discover_candidates(["geospatial surveying"], research=FakeResearch())
        self.assertEqual(len(dossiers), 1)
        self.assertEqual(dossiers[0]["status"], "research")
        self.assertEqual(dossiers[0]["sample_size"], 0)
        self.assertFalse(dossiers[0]["viability_demonstrated"])
        self.assertEqual(len(dossiers[0]["hypothesis_origin"]["research_urls"]), 2)

    def test_unbounded_or_empty_seeds_refused(self):
        for seeds in [[], ["x"], ["a" * 101], ["valid"] * 11]:
            with self.assertRaises(ValueError):
                discover_candidates(seeds, research=FakeResearch())

    def test_submission_requires_private_url_and_token(self):
        with self.assertRaises(ValueError):
            submit_hypotheses([], "http://localhost:5000", "secret")


if __name__ == "__main__":
    unittest.main()
