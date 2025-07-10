# Threat Inspector

Threat Inspector is a Python application designed to analyze vulnerabilities in codebases by fetching CVE (Common Vulnerabilities and Exposures) information and assessing the potential impact on the code. The application utilizes retrieval-augmented generation (RAG) techniques to provide detailed analysis and recommendations based on the context of the code.

## Features

- Fetches CVE information from the OSV API.
- Analyzes codebases for potential vulnerabilities.
- Provides actionable recommendations for remediation.
- Supports various programming languages.

## Project Structure

```
threat-inspector
├── src
│   ├── __init__.py
│   ├── main.py                # Entry point of the application
│   ├── core                   # Core functionality
│   │   ├── __init__.py
│   │   ├── analyzer.py        # Analyzes vulnerabilities in code
│   │   ├── embeddings.py      # Manages embedding models
│   │   ├── vector_store.py    # Handles document embeddings storage
│   │   └── rag_chain.py       # Creates the RAG chain for querying
│   ├── services               # Services for fetching and processing data
│   │   ├── __init__.py
│   │   ├── cve_service.py     # Fetches CVE information
│   │   └── document_service.py # Loads and processes code documents
│   ├── utils                  # Utility functions and constants
│   │   ├── __init__.py
│   │   ├── constants.py       # Defines constants used in the application
│   │   └── helpers.py         # Utility functions for various tasks
│   └── cli                    # Command-line interface
│       ├── __init__.py
│       └── argument_parser.py  # Handles command-line argument parsing
├── unit_tests                      # Unit tests for the application
│   ├── __init__.py
│   ├── test_analyzer.py       # Tests for the Analyzer class
│   ├── test_cve_service.py     # Tests for the CVEService class
│   └── test_document_service.py # Tests for the DocumentService class
├── requirements.txt           # Project dependencies
├── setup.py                   # Setup script for the project
└── README.md                  # Project documentation
```

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/threat-inspector.git
   cd threat-inspector
   ```

2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

## Usage

To run the application, use the following command:

```
python src/main.py <CVE_ID> --path <path_to_code_directory>
```

Replace `<CVE_ID>` with the CVE identifier (e.g., CVE-2021-44228) and `<path_to_code_directory>` with the path to the codebase you want to analyze.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any enhancements or bug fixes.

## License

This project is licensed under the MIT License. See the LICENSE file for more details.