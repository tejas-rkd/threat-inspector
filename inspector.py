import argparse
import json
import sys
import urllib.request
import urllib.error
from langchain_community.document_loaders import DirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_ollama import OllamaEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
import shutil
import os

CHROMA_PATH = "./.chroma_db" # Directory to store ChromaDB data

def fetch_cve_info(cve_id):
    print(f"Fetching information for {cve_id}...")
    """
    Fetch vulnerability information for a given CVE ID from the OSV API.
    
    Args:
        cve_id (str): The CVE identifier (e.g., CVE-2021-44228)
        
    Returns:
        dict: The JSON response from the API
    """
    url = f"https://api.osv.dev/v1/vulns/{cve_id}"
    
    try:
        with urllib.request.urlopen(url) as response:
            return json.loads(response.read().decode('utf-8'))
    except urllib.error.HTTPError as e:
        if e.code == 404:
            print(f"Error: CVE {cve_id} not found")
        else:
            print(f"Error: HTTP {e.code} - {e.reason}")
        sys.exit(1)
    except urllib.error.URLError as e:
        print(f"Error: Could not connect to the API - {e.reason}")
        sys.exit(1)
    except json.JSONDecodeError:
        print("Error: Invalid response received from the API")
        sys.exit(1)

def display_vulnerability_info(vuln_data):
    """
    Display the relevant vulnerability information from the API response.
    
    Args:
        vuln_data (dict): The vulnerability data from the API
    """
    # Print all fields in vuln_data as formatted JSON
    print("\nFull Vulnerability Data:")
    print(json.dumps(vuln_data, indent=2))

    # # Create a map of all JSON fields and their values
    # field_map = {k: v for k, v in vuln_data.items()}
    # print("\nField Map (key-value pairs):")
    # for key, value in field_map.items():
    #     print(f"{key}: {value}")
    
    # # Extract the required fields
    # vuln_id = vuln_data.get('id', 'N/A')
    # summary = vuln_data.get('summary', 'No summary available')
    # affected = vuln_data.get('affected', [])

    # # Print the information
    # print(f"\nVulnerability ID: {vuln_id}")
    # print(f"Summary: {summary}")

    # if affected:
    #     print("\nAffected Packages:")
    #     for pkg in affected:
    #         package_name = pkg.get('package', {}).get('name', 'Unknown')
    #         package_ecosystem = pkg.get('package', {}).get('ecosystem', 'Unknown')
            
    #         print(f"  - {package_ecosystem}: {package_name}")
            
    #         # Print versions if available
    #         if 'versions' in pkg:
    #             print(f"    Versions: {', '.join(pkg['versions'])}")
            
    #         # Print ranges if available
    #         if 'ranges' in pkg:
    #             for range_data in pkg['ranges']:
    #                 range_type = range_data.get('type', 'Unknown')
    #                 print(f"    Range Type: {range_type}")
                    
    #                 if 'events' in range_data:
    #                     events = range_data['events']
    #                     for event in events:
    #                         event_str = ", ".join([f"{k}: {v}" for k, v in event.items()])
    #                         print(f"      Event: {event_str}")
    # else:
    #     print("\nNo affected packages information available")

def load_codebase(path):
    print(path)
    # Use the provided path and a list of glob patterns
    patterns = [
        '*.go', '*.js', '*.py', '*.ts', '*.java', '*.c', '*.cpp', '*.h', '*.hpp', '*.php', '*.sql'
    ]
    loader = DirectoryLoader(path, glob=patterns, recursive=True, show_progress=True)
    documents = loader.load()
    print(f"Loaded {len(documents)} page(s) from {path}")
    return documents

def split_documents(documents):
    """Splits documents into smaller chunks."""
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len,
        is_separator_regex=False,
    )
    all_splits = text_splitter.split_documents(documents)
    print(f"Split into {len(all_splits)} chunks")
    return all_splits

def get_embedding_function(model_name="all-minilm:latest"):
    """Initializes the Ollama embedding function."""
    # Ensure Ollama server is running (ollama serve)
    embeddings = OllamaEmbeddings(model=model_name)
    print(f"Initialized Ollama embeddings with model: {model_name}")
    return embeddings

def get_vector_store(embedding_function, persist_directory=CHROMA_PATH):
    """Initializes or loads the Chroma vector store."""
    vectorstore = Chroma(
        persist_directory=persist_directory,
        embedding_function=embedding_function
    )
    print(f"Vector store initialized/loaded from: {persist_directory}")
    return vectorstore

def index_documents(chunks, embedding_function, persist_directory=CHROMA_PATH):
    """Indexes document chunks into the Chroma vector store."""
    print(f"Indexing {len(chunks)} chunks...")
    if not chunks:
        print("No document chunks to index. Skipping vector store creation.")
        return None
    # Use from_documents for initial creation.
    # This will overwrite existing data if the directory exists but isn't a valid Chroma DB.
    # For incremental updates, initialize Chroma first and use vectorstore.add_documents().
    vectorstore = Chroma.from_documents(
        documents=chunks,
        embedding=embedding_function,
        persist_directory=persist_directory
    )
    vectorstore.persist() # Ensure data is saved
    print(f"Indexing complete. Data saved to: {persist_directory}")
    return vectorstore

def create_rag_chain(vector_store, llm_model_name="mistral:latest", context_window=8192):
    """Creates the RAG chain."""
    # Initialize the LLM
    llm = ChatOllama(
        model=llm_model_name,
        temperature=0, # Lower temperature for more factual RAG answers
        num_ctx=context_window # IMPORTANT: Set context window size
    )
    print(f"Initialized ChatOllama with model: {llm_model_name}, context window: {context_window}")

    # Create the retriever
    retriever = vector_store.as_retriever(
        search_type="similarity", # Or "mmr"
        search_kwargs={'k': 3} # Retrieve top 3 relevant chunks
    )
    print("Retriever initialized.")

    # Define the prompt template
    template = """Answer the question based ONLY on the following context:
{context}

Question: {question}
"""
    prompt = ChatPromptTemplate.from_template(template)
    print("Prompt template created.")

    # Define the RAG chain using LCEL
    rag_chain = (
        {"context": retriever, "question": RunnablePassthrough()}
| prompt
| llm
| StrOutputParser()
    )
    print("RAG chain created.")
    return rag_chain

def query_rag(chain, question):
    """Queries the RAG chain and prints the response."""
    print("\nQuerying RAG chain...")
    print(f"Question: {question}")
    response = chain.invoke(question)
    print("\nResponse:")
    print(response)

def cleanup():
    if os.path.exists(CHROMA_PATH):
        shutil.rmtree(CHROMA_PATH)
        print(f"Deleted vector store directory: {CHROMA_PATH}")
    else:
        print(f"No vector store directory found at: {CHROMA_PATH}")
    return






def run_analysis(cve_id, path):
    #vuln_data = fetch_cve_info(cve_id)
    code = load_codebase(path)
    chunks = split_documents(code)
    embedding_function = get_embedding_function()
    vector_store = index_documents(chunks, embedding_function)
    if not vector_store:
        print("No code found to analyze. Exiting analysis.")
        return
    rag_chain = create_rag_chain(vector_store)
    query_rag(rag_chain, "what language this code is in?")
    return

def main():
    parser = argparse.ArgumentParser(
        description="Fetch and display vulnerability information for a CVE ID from the OSV database"
    )
    parser.add_argument("cve_id", help="The CVE identifier (e.g., CVE-2021-44228)")
    parser.add_argument("--path", 
                       default=".", 
                       help="Path to the code directory (default: current directory)")
    
    args = parser.parse_args()
    
    # Ensure the CVE ID is properly formatted
    cve_id = args.cve_id
    if not cve_id.startswith("CVE-"):
        print("Warning: CVE ID should be in the format 'CVE-YYYY-NNNNN'")
    path = args.path
    
    run_analysis(cve_id, path)
    cleanup()
    # display_vulnerability_info(vuln_data)
    


if __name__ == "__main__":
    main()

