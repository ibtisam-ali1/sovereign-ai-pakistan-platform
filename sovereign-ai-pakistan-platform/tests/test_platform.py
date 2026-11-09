"""
Automated QA & Integration Test Suite
"""

import unittest
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

from central_router import CentralSupervisorRouter
from ingestion_pipeline import DataIngestionPipeline

class TestSovereignPlatform(unittest.TestCase):
    def setUp(self):
        self.router = CentralSupervisorRouter()
        self.ingestion = DataIngestionPipeline()

    def test_federal_routing(self):
        res = self.router.classify_and_route("What is the federal tax rate under FBR?")
        self.assertEqual(res["jurisdiction"], "FEDERAL")
        self.assertGreaterEqual(res["confidence"], 0.70)
        self.assertEqual(res["next_action"], "route_to_agent")

    def test_provincial_routing(self):
        res = self.router.classify_and_route("How to register a hospital in Sindh Health Department?")
        self.assertEqual(res["jurisdiction"], "PROVINCIAL")
        self.assertEqual(res["province"], "Sindh")

    def test_shared_jurisdiction_fallback(self):
        res = self.router.classify_and_route("What are the inter-provincial river water management laws?")
        self.assertEqual(res["jurisdiction"], "SHARED_JURISDICTION")
        self.assertEqual(res["next_action"], "ask_clarification")

    def test_empty_query_exception(self):
        with self.assertRaises(ValueError):
            self.router.classify_and_route("")

    def test_ingestion_pipeline(self):
        res = self.ingestion.ingest("doc_001", "pk-fed:mof", "Federal budget guidelines for fiscal year 2026.")
        self.assertEqual(res["status"], "SUCCESS")
        self.assertEqual(res["total_chunks"], 1)

if __name__ == "__main__":
    unittest.main()
