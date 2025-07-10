# Threat Inspector

Threat Inspector is a AI application designed to analyze vulnerabilities in codebases by fetching CVE (Common Vulnerabilities and Exposures) information and assessing the potential impact on the code. The application utilizes retrieval-augmented generation (RAG) techniques to provide detailed analysis and recommendations based on the context of the code.

## Features

- Fetches CVE information from the OSV API.
- Analyzes codebases for potential vulnerabilities.
- Provides actionable recommendations for remediation.
- Supports various programming languages.

## Project Structure

```
threat-inspector
├── src
│   ├
│   ├── main.py                # Entry point of the application
│   ├── core                   # Core functionality
│   │   ├
│   │   ├── analyzer.py        # Analyzes vulnerabilities in code
│   │   ├── embeddings.py      # Manages embedding models
│   │   ├── vector_store.py    # Handles document embeddings storage
│   │   └── rag_chain.py       # Creates the RAG chain for querying
│   ├── services               # Services for fetching and processing data
│   │   ├
│   │   ├── cve_service.py     # Fetches CVE information
│   │   └── document_service.py # Loads and processes code documents
│   ├── utils                  # Utility functions and constants
│   │   ├
│   │   ├── constants.py       # Defines constants used in the application
│   │   └── helpers.py         # Utility functions for various tasks
│   └── cli                    # Command-line interface
│       ├
│       └── argument_parser.py  # Handles command-line argument parsing
├── unit_tests                 # Unit tests for the application
│   ├
│   ├── test_analyzer.py       # Tests for the Analyzer class
│   ├── test_cve_service.py    # Tests for the CVEService class
│   └── test_document_service.py # Tests for the DocumentService class
├── integration_tests          # Integration tests for end-to-end testing
│   ├── test.py               # Main integration test suite
│   ├── run_tests.py          # Test runner script
│   └── data                  # Sample vulnerable code files for testing
│       ├── 2017_18342.py     
│       ├── 2023_43364.py     
│       └── 2024‑45848.py     
├── inspector.py              # Alternative entry point
├── requirements.txt          # Project dependencies
├── setup.py                  # Setup script for the project
└── README.md                 # Project documentation
```

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/threat-inspector.git
   cd threat-inspector
   ```

2. Install the required dependencies:
   
   You can install dependencies using either of these two methods:
   
   **Method 1: Using requirements.txt** (recommended for users)
   ```
   pip install -r requirements.txt
   ```
   
   **Method 2: Using setup.py** (recommended for development)
   ```
   pip install -e .
   ```
   
   The second method installs the package in development mode, making it importable from anywhere in your Python environment.


### Install and Run AI

**Option 1: Automated Setup (Recommended)**

We provide setup scripts to automate the Ollama installation and configuration:

**For Linux:**
```bash
python3 setup_ollama.py
```

**For Windows:**
```batch
setup_ollama.bat
```

**Option 2: Manual Setup**

If you prefer to set up Ollama manually:

1. **Install Ollama:**

   **For Linux:**
   ```bash
   curl -fsSL https://ollama.com/install.sh | sh
   ```
   
   **For macOS:**
   ```bash
   brew install ollama
   ```
   
   **For Windows:**
   Download and install from [https://ollama.com/download](https://ollama.com/download)

2. **Install required models:**

   ```bash
   ollama pull mistral:latest
   ollama pull all-minilm:latest
   ```

3. **Start Ollama service:**

   **For Linux/macOS:**
   ```bash
   ollama serve
   ```
   
   **For Windows:**
   The Ollama service should start automatically. If not, you can start it from the system tray or by running `ollama serve` in Command Prompt.

## Usage

To run the application, use the following command:

```
python src/main.py <CVE_ID> --path <path_to_code_directory>
```

Replace `<CVE_ID>` with the CVE identifier (e.g., CVE-2021-44228) and `<path_to_code_directory>` with the path to the codebase you want to analyze.

## Testing

The project includes comprehensive test suites to ensure reliability and correctness:

### Unit Tests

Unit tests are located in the `unit_tests/` directory and test individual components:

```bash
# Run all unit tests
python -m pytest unit_tests/ -v

# Run specific test file
python -m pytest unit_tests/test_analyzer.py -v
```

### Integration Tests

Integration tests are located in the `integration_tests/` directory and test the complete application workflow with real CVE data:

```bash
# Run integration tests using the test runner
cd integration_tests
python run_tests.py

# Or run using pytest
python -m pytest integration_tests/test.py -v

# Or run using unittest
cd integration_tests
python -m unittest test.py -v
```

The integration tests automatically:
- Extract CVE IDs from test data filenames (e.g., `2017_18342.py` → `CVE-2017-18342`)
- Run the main application with each CVE ID and corresponding vulnerable code file
- Verify that the application runs successfully and produces meaningful output
- Test error handling for invalid inputs

#### Test Data

The `integration_tests/data/` directory contains sample vulnerable code files:
- `2017_18342.py` - YAML deserialization vulnerability (CVE-2017-18342)
- `2023_43364.py` - Code injection vulnerability (CVE-2023-43364)  
- `2024‑45848.py` - Eval injection vulnerability (CVE-2024-45848)

These files demonstrate common vulnerability patterns and serve as test cases for the threat analysis functionality.

## Design Rationale

This section explains the key architectural and technology choices made in developing Threat Inspector:

### Architecture Decisions

**Modular Structure**: The project is organized into distinct modules (`core`, `services`, `utils`, `cli`) to promote separation of concerns and maintainability. Each module has a specific responsibility:
- `core`: Contains the main business logic for vulnerability analysis
- `services`: Handles external data fetching and document processing
- `utils`: Provides shared utilities and constants
- `cli`: Manages command-line interface functionality

**Service Layer Pattern**: CVE data fetching and document processing are abstracted into service classes (`CVEService`, `DocumentService`) to enable easy testing, mocking, and potential future integration with different data sources.

### Technology Stack

**Python**: Chosen for its robust ecosystem of libraries for text processing, machine learning, and API integration. Python's readability and extensive community support make it ideal for security analysis tools.

**Ollama for Local LLM**: We chose Ollama over cloud-based LLM services for several reasons:
- **Privacy**: Code analysis often involves sensitive or proprietary code that shouldn't be sent to external services
- **Cost**: No per-request charges for analysis
- **Reliability**: No dependency on internet connectivity or external service availability
- **Control**: Full control over model versions and configurations

**Retrieval-Augmented Generation (RAG)**: Implemented to combine the power of large language models with specific CVE knowledge:
- Provides contextually relevant vulnerability analysis
- Reduces hallucination by grounding responses in factual CVE data
- Allows for dynamic knowledge updates without retraining models

**Vector Store Approach**: Used for efficient similarity search and retrieval of relevant vulnerability information, enabling fast matching between code patterns and known vulnerabilities.

### Model Choices

**Mistral**: Selected as the primary LLM for its strong performance on code analysis tasks while maintaining reasonable resource requirements for local deployment.

**all-minilm**: Chosen for embeddings due to its balance of quality and speed, making it suitable for real-time code analysis without requiring excessive computational resources.

### Testing Strategy

**Comprehensive Test Coverage**: Includes both unit and integration tests to ensure reliability:
- **Unit Tests**: Verify individual component functionality in isolation
- **Integration Tests**: Test end-to-end workflows with real CVE data
- **Real Vulnerability Samples**: Test data includes actual vulnerable code patterns to validate practical effectiveness

### API Integration

**OSV API**: Selected for CVE data because:
- Comprehensive vulnerability database
- Well-maintained and regularly updated
- Free access without rate limiting concerns
- Structured JSON responses suitable for programmatic processing

This design prioritizes security, maintainability, and practical usability while keeping the solution lightweight and deployable in various environments.

## AI Usage:
Files related to testing, installation and README have been generated by AI.\
Ref: https://www.freecodecamp.org/news/build-a-local-ai/
