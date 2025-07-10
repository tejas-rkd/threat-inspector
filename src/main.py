import argparse
from cli.argument_parser import ArgumentParser
from services.cve_service import CVEService
from services.document_service import DocumentService
from core.analyzer import Analyzer
from core.embeddings import EmbeddingService
from core.vector_store import VectorStore
from core.rag_chain import RAGChain
from utils.helpers import cleanup
from utils.constants import CHROMA_PATH

def main():
    parser = ArgumentParser()
    args = parser.parse_arguments()

    # Initialize services
    cve_service = CVEService()
    document_service = DocumentService(args.path)
    embedding_service = EmbeddingService()
    
    # Initialize vector store
    vector_store = VectorStore(CHROMA_PATH, embedding_service.embeddings)
    
    # Initialize RAG chain
    rag_chain = RAGChain(vector_store)
    
    # Initialize analyzer with all required dependencies
    analyzer = Analyzer(cve_service, document_service, embedding_service, vector_store, rag_chain)
    
    # Run the analysis
    analysis_results = analyzer.analyze(args.cve_id, args.path)
    print(analysis_results.content)

    cleanup()

if __name__ == "__main__":
    main()