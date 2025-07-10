
import argparse
import json
import sys
import urllib.request
import urllib.error
import shutil
import os
from langchain_community.document_loaders import DirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_ollama import OllamaEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser


# Constants
CHROMA_PATH = "./.chroma_db"  # Directory to store ChromaDB data
OSV_API_URL = "https://api.osv.dev/v1/vulns/{}"
SUPPORTED_PATTERNS = [
    "*.go", "*.js", "*.py", "*.ts", "*.java", "*.c", "*.cpp", "*.h", "*.hpp", "*.php", "*.sql"
]
DEFAULT_EMBEDDING_MODEL = "all-minilm:latest"
DEFAULT_LLM_MODEL = "mistral:latest"
DEFAULT_CONTEXT_WINDOW = 8192
PROMPT_TEMPLATE = (
    "Answer the question based ONLY on the following context:\n"
    "{context}\n\n"
    "Question: {question}\n"
)


def fetch_cve_info(cve_id):
    print(f"Fetching information for {cve_id}...")
    url = OSV_API_URL.format(cve_id)
    try:
        with urllib.request.urlopen(url) as response:
            return json.loads(response.read().decode("utf-8"))
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



def load_codebase(path):
    print(f"Loading codebase from: {path}")
    loader = DirectoryLoader(path, glob=SUPPORTED_PATTERNS, recursive=True, show_progress=True)
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


def get_embedding_function(model_name=DEFAULT_EMBEDDING_MODEL):
    """Initializes the Ollama embedding function."""
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
    vectorstore = Chroma.from_documents(
        documents=chunks,
        embedding=embedding_function,
        persist_directory=persist_directory
    )
    # vectorstore.persist()  # Ensure data is saved
    print(f"Indexing complete. Data saved to: {persist_directory}")
    return vectorstore


def create_rag_chain(
    vector_store,
    llm_model_name=DEFAULT_LLM_MODEL,
    context_window=DEFAULT_CONTEXT_WINDOW
):
    """Creates the RAG chain."""
    llm = ChatOllama(
        model=llm_model_name,
        temperature=0,  # Lower temperature for more factual RAG answers
        num_ctx=context_window
    )
    print(f"Initialized ChatOllama with model: {llm_model_name}, context window: {context_window}")

    retriever = vector_store.as_retriever(
        search_type="similarity",
        search_kwargs={"k": 3}
    )
    print("Retriever initialized.")

    prompt = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)
    print("Prompt template created.")

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


def generate_question(vuln_data):
    question = (
        """
You are a cybersecurity expert analyzing a vulnerability (CVE) and its potential impact on a specific codebase.

VULNERABILITY INFORMATION:
{}"""
        "\n\nANALYSIS REQUEST:\nPlease provide a detailed analysis covering:\n"
        "\n1. CVE ANALYSIS:\n"
        "   - Explain what this vulnerability is and how it works\n"
        "   - Detail which dependencies/packages are affected\n"
        "   - Assess the severity and potential attack vectors\n"
        "\n2. CODEBASE IMPACT ASSESSMENT:\n"
        "   - Check if any dependencies in this codebase match the affected packages\n"
        "   - Identify potential vulnerable components based on the file structure\n"
        "   - Assess the risk level for this specific codebase\n"
        "   - Provide specific recommendations for remediation\n"
        "\n3. ACTIONABLE RECOMMENDATIONS:\n"
        "   - List specific steps to check for vulnerability presence\n"
        "   - Recommend version updates or patches if applicable\n"
        "   - Suggest security best practices to prevent similar issues\n"
        "\nKeep your analysis practical and actionable. If the codebase doesn't appear to be affected, clearly state that and explain why.\n"
    ).format(json.dumps(vuln_data, indent=2))
    return question


def run_analysis(cve_id, path):
    vuln_data = fetch_cve_info(cve_id)
    code = load_codebase(path)
    chunks = split_documents(code)
    embedding_function = get_embedding_function()
    vector_store = index_documents(chunks, embedding_function)
    if not vector_store:
        print("No code found to analyze. Exiting analysis.")
        return
    rag_chain = create_rag_chain(vector_store)
    question = generate_question(vuln_data)
    query_rag(rag_chain, question)
    return


def main():
    parser = argparse.ArgumentParser(
        description="Fetch and display vulnerability information for a CVE ID in context of your code"
    )
    parser.add_argument("cve_id", help="The CVE identifier (e.g., CVE-2021-44228)")
    parser.add_argument(
        "--path",
        default=".",
        help="Path to the code directory (default: current directory)"
    )

    args = parser.parse_args()

    # Ensure the CVE ID is properly formatted
    cve_id = args.cve_id.upper()
    if not cve_id.startswith("CVE-"):
        print("Warning: CVE ID should be in the format 'CVE-YYYY-NNNNN'")
        sys.exit(1)

    # Ensure the Path is valid
    path = args.path
    if not os.path.exists(path) or not os.path.isdir(path):
        print(f"Error: The specified path '{path}' does not exist or is not a directory.")
        sys.exit(1)

    run_analysis(cve_id, path)
    cleanup()


if __name__ == "__main__":
    main()

