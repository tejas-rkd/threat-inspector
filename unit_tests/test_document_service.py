import unittest
from src.services.document_service import DocumentService

class TestDocumentService(unittest.TestCase):

    def setUp(self):
        self.service = DocumentService()

    def test_load_codebase(self):
        path = "path/to/test/codebase"
        documents = self.service.load_codebase(path)
        self.assertIsInstance(documents, list)
        self.assertGreater(len(documents), 0)

    def test_split_documents(self):
        documents = ["This is a test document."] * 5
        chunks = self.service.split_documents(documents)
        self.assertIsInstance(chunks, list)
        self.assertGreater(len(chunks), 0)

    def test_index_documents(self):
        chunks = ["chunk1", "chunk2", "chunk3"]
        vector_store = self.service.index_documents(chunks)
        self.assertIsNotNone(vector_store)

if __name__ == '__main__':
    unittest.main()