from langchain_chroma import Chroma
import os

class VectorStore:
    def __init__(self, persist_directory, embedding_function):
        self.persist_directory = persist_directory
        self.embedding_function = embedding_function
        self.vectorstore = self.load_vector_store()

    def load_vector_store(self):
        # Create the directory if it doesn't exist
        os.makedirs(self.persist_directory, exist_ok=True)
        
        # Initialize ChromaDB vector store
        vectorstore = Chroma(
            persist_directory=self.persist_directory,
            embedding_function=self.embedding_function
        )
        return vectorstore

    def index_documents(self, documents, embeddings=None):
        # Index documents into the vector store
        if hasattr(documents[0], 'page_content'):
            # If documents are LangChain Document objects
            self.vectorstore.add_documents(documents)
        else:
            # If documents are strings
            self.vectorstore.add_texts(documents)

    def retrieve(self, query, k=3):
        # Retrieve the top k documents based on the query
        return self.vectorstore.similarity_search(query, k=k)

    def as_retriever(self, search_type="similarity", search_kwargs=None):
        # Return a LangChain-compatible retriever
        if search_kwargs is None:
            search_kwargs = {"k": 3}
        return self.vectorstore.as_retriever(search_type=search_type, search_kwargs=search_kwargs)

    def persist(self):
        # Persist the vector store to disk (ChromaDB handles this automatically)
        pass