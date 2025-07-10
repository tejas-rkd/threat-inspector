from langchain_community.document_loaders import DirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from utils.constants import SUPPORTED_PATTERNS

class DocumentService:
    def __init__(self, path, supported_patterns=SUPPORTED_PATTERNS):
        self.path = path
        self.supported_patterns = supported_patterns

    def load_codebase(self):
        print(f"Loading codebase from: {self.path}")
        loader = DirectoryLoader(self.path, glob=self.supported_patterns, recursive=True, show_progress=True)
        documents = loader.load()
        print(f"Loaded {len(documents)} page(s) from {self.path}")
        return documents

    def split_documents(self, documents):
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            length_function=len,
            is_separator_regex=False,
        )
        all_splits = text_splitter.split_documents(documents)
        print(f"Split into {len(all_splits)} chunks")
        return all_splits