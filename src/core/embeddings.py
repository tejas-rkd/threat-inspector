from langchain_ollama import OllamaEmbeddings
from utils.constants import DEFAULT_EMBEDDING_MODEL

class EmbeddingService:
    def __init__(self, model_name=DEFAULT_EMBEDDING_MODEL):
        self.model_name = model_name
        self.embeddings = self.initialize_embeddings()

    def initialize_embeddings(self):
        embeddings = OllamaEmbeddings(model=self.model_name)
        print(f"Initialized embeddings with model: {self.model_name}")
        return embeddings

    def get_embeddings(self, documents):
        # Extract text content from Document objects if needed
        if hasattr(documents[0], 'page_content'):
            # If documents are LangChain Document objects
            texts = [doc.page_content for doc in documents]
        else:
            # If documents are already strings
            texts = documents
        
        return self.embeddings.embed_documents(texts)