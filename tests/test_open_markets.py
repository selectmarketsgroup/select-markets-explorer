import unittest
from datetime import datetime,timezone,timedelta
from select_markets_explorer.research import research_signal
from select_markets_explorer.engine import Signal
from select_markets_explorer.market_research import explore_open_markets

NOW=datetime(2026,11,18,12,tzinfo=timezone.utc)
class Finder:
    def __init__(self,sources=2):self.sources=sources
    def search(self,phrase):
        return [{"url":f"https://approved.example/s-{i}","terms_url":"https://approved.example/terms",
                 "permitted":True,"description":f"fixture source {i}"} for i in range(self.sources)]
class Sampler:
    def sample(self,source,*,limit):
        return [{"id":str(i),"price":100+i,"currency":"EUR","available":True,
                 "observed_at":NOW.isoformat(),
                 "url":source["url"]+"/p/"+str(i)}
                for i in range(min(limit,6))]
class Research:
    def search(self,seed,limit=5):
        return [{"url":"https://openalex.org/W1","topics":["Underwater positioning systems"],
                 "keywords":["Subsea robotics"]},
                {"url":"https://openalex.org/W2","topics":["Underwater positioning systems"],
                 "keywords":["Subsea robotics"]}]

class FullResearchTests(unittest.TestCase):
    def test_novel_niche_is_found_without_a_category_whitelist(self):
        dossiers=explore_open_markets(["geospatial surveying"],Research(),
                                     Finder(),Sampler(),now=NOW)
        self.assertEqual([d["market"] for d in dossiers],
                         ["Subsea robotics","Underwater positioning systems"])
        for d in dossiers:
            self.assertEqual(d["status"],"test")
            self.assertEqual(d["sample_size"],12)
            self.assertEqual(d["independent_sources"],2)
            self.assertFalse(d["viability_demonstrated"])
            self.assertEqual(len(d["hypothesis_origin"]["research_urls"]),2)
    def test_one_feed_never_qualifies_as_independent_market(self):
        signal=Signal("unknown niche","candidate","private market")
        d=research_signal(signal,Finder(1),Sampler(),now=NOW)
        self.assertEqual(d["status"],"research")
        self.assertEqual(d["independent_sources"],1)
    def test_invalid_outdated_or_unpriced_offers_abstain(self):
        class Stale:
            def sample(self,source,*,limit):
                return [{"id":"x","price":"NaN","currency":"EUR","available":True,
                         "observed_at":NOW.isoformat(),"url":"https://approved.example/x"},
                        {"id":"old","price":100,"currency":"EUR","available":True,
                         "observed_at":(NOW-timedelta(days=180)).isoformat(),
                         "url":"https://approved.example/old"}]
        d=research_signal(Signal("niche","candidate","private market"),
                          Finder(),Stale(),now=NOW)
        self.assertEqual(d["sample_size"],0)
        self.assertEqual(d["status"],"research")
    def test_no_invented_new_segments_when_no_research_concepts(self):
        class Empty:
            def search(self,seed,limit=5):return [{"url":"https://openalex.org/W4"}]
        self.assertEqual(explore_open_markets(["surveys"],Empty(),Finder(),Sampler(),
                                              now=NOW),[])
