"""The Platform client must preserve meaningful source/research provenance."""
import io
import json
import unittest
from select_markets_explorer.platform_client import save_hypothesis


class APITransport:
    def __init__(self):
        self.calls=[]
    def __call__(self,request,timeout):
        self.calls.append({
            "url":request.full_url,"method":request.get_method(),
            "headers":dict(request.header_items()),
            "payload":json.loads(request.data)
        })
        return io.BytesIO(b'{"id":"test-hypothesis","revision":1}')


class ClientTests(unittest.TestCase):
    def test_research_provenance_is_not_lost(self):
        api=APITransport()
        dossier={
            "market":"Subsea surveying equipment",
            "title":"Market candidate from research",
            "status":"research",
            "rationale":"Needs independent sources",
            "evidence":[{"url":"https://example.org/source","sample_count":0}],
            "sample_size":0,
            "independent_sources":0,
            "observed_price_median":None,
            "viability_demonstrated":False,
            "hypothesis_origin":{
                "seed_topics":["surveying"],
                "research_urls":["https://openalex.org/W1"]},
            "rejected_sources":[{"url":"https://bad.example/","reason":"No reuse license"}],
            "limitation":"No verified demand evidence"
        }
        result=save_hypothesis("https://private.example","scoped-token",dossier,
                               transport=api)
        self.assertEqual(result["revision"],1)
        payload=api.calls[0]["payload"]
        self.assertEqual(payload["research_details"]["sample_size"],0)
        self.assertFalse(payload["research_details"]["viability_demonstrated"])
        self.assertEqual(payload["research_details"]["hypothesis_origin"]["research_urls"],
                         ["https://openalex.org/W1"])
        self.assertEqual(api.calls[0]["method"],"POST")

    def test_revision_preserves_details_and_requires_https(self):
        api=APITransport()
        dossier={"market":"Industrial cameras","title":"Research",
                 "status":"test","rationale":"Controlled trial",
                 "evidence":[],"independent_sources":2}
        save_hypothesis("https://private.example","scoped-token",dossier,
                        hypothesis_id="hypothesis-id",transport=api)
        self.assertEqual(api.calls[0]["method"],"PUT")
        self.assertEqual(api.calls[0]["payload"]["research_details"]["independent_sources"],2)
        with self.assertRaises(ValueError):
            save_hypothesis("http://insecure.example","token",dossier,
                            transport=api)


if __name__=="__main__":
    unittest.main()
