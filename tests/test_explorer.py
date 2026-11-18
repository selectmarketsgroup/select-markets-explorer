import unittest

from select_markets_explorer.engine import (
    Evidence, Signal, evaluate_market, identify_signals, proposal_identity,
    route_to_existing_unit,
)


class ExplorerTests(unittest.TestCase):
    def test_unknown_segment_does_not_require_code_change(self):
        [s] = identify_signals([{"name": "Underwater surveying instruments",
                                 "description": "Equipment with secondary markets",
                                 "potential_use": "Private evaluation"}])
        self.assertEqual(route_to_existing_unit("underwater_surveys"), None)
        self.assertEqual(proposal_identity(s), proposal_identity(s))

    def test_no_proven_sources_remains_research(self):
        s = Signal("New niche", "Demonstration", "Personal")
        result = evaluate_market(s, [])
        self.assertEqual(result["status"], "research")
        self.assertIn("No licensed", result["rationale"])

    def test_verifiable_sources_are_not_invented(self):
        s = Signal("New niche", "Demonstration", "Personal")
        source = Evidence.validated({"url": "https://example.org/feed",
                                     "description": "Permitted sample",
                                     "observed_at": "2026-11-18", "permitted": True,
                                     "sample_count": 7})
        result = evaluate_market(s, [source], 0)
        self.assertEqual(result["status"], "test")
        self.assertEqual(result["evidence"][0]["url"], source.url)

    def test_reject_bad_urls(self):
        with self.assertRaises(ValueError):
            Evidence.validated({"url": "file:///etc/passwd", "description": "data",
                                "observed_at": "2026-11-18", "permitted": True})


if __name__ == "__main__":
    unittest.main()
