import unittest
from src.core.analyzer import Analyzer

class TestAnalyzer(unittest.TestCase):

    def setUp(self):
        self.analyzer = Analyzer()

    def test_load_codebase(self):
        # Test loading a codebase from a valid path
        path = "path/to/valid/codebase"
        documents = self.analyzer.load_codebase(path)
        self.assertIsInstance(documents, list)
        self.assertGreater(len(documents), 0)

    def test_split_documents(self):
        # Test splitting documents into chunks
        documents = ["This is a test document."] * 5
        chunks = self.analyzer.split_documents(documents)
        self.assertIsInstance(chunks, list)
        self.assertGreater(len(chunks), 0)

    def test_generate_question(self):
        # Test generating a question based on vulnerability data
        vuln_data = {"id": "CVE-2021-44228", "description": "Test vulnerability"}
        question = self.analyzer.generate_question(vuln_data)
        self.assertIn("VULNERABILITY INFORMATION:", question)
        self.assertIn("CVE ANALYSIS:", question)

if __name__ == "__main__":
    unittest.main()