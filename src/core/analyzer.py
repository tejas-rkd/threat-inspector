import json
from utils.constants import CVE_ANALYSIS_PROMPT

class Analyzer:
    def __init__(self, cve_service, document_service, embedding_service, vector_store, rag_chain):
        self.cve_service = cve_service
        self.document_service = document_service
        self.embedding_service = embedding_service
        self.vector_store = vector_store
        self.rag_chain = rag_chain

    def analyze(self, cve_id, path):
        vuln_data = self.cve_service.fetch_cve_info(cve_id)
        code_documents = self.document_service.load_codebase()
        chunks = self.document_service.split_documents(code_documents)
        embeddings = self.embedding_service.get_embeddings(chunks)
        self.vector_store.index_documents(chunks, embeddings)
        question = self.generate_question(vuln_data)
        response = self.rag_chain.query(question)
        return response

    def generate_question(self, vuln_data):
        question = CVE_ANALYSIS_PROMPT.format(vuln_data=json.dumps(vuln_data, indent=2))
        return question