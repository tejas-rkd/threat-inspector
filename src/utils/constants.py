
CHROMA_PATH = "./.chroma_db"
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
CVE_ANALYSIS_PROMPT = (
    "You are a cybersecurity expert analyzing a vulnerability (CVE) and its potential impact on a specific codebase.\n\n"
    "VULNERABILITY INFORMATION:\n{vuln_data}\n\n"
    "ANALYSIS REQUEST:\nPlease provide a detailed analysis covering:\n"
    "1. CVE ANALYSIS:\n"
    "   - Explain what this vulnerability is and how it works\n"
    "   - Detail which dependencies/packages are affected\n"
    "   - Assess the severity and potential attack vectors\n"
    "2. CODEBASE IMPACT ASSESSMENT:\n"
    "   - Check if any dependencies in this codebase match the affected packages\n"
    "   - Identify potential vulnerable components based on the file structure\n"
    "   - Assess the risk level for this specific codebase\n"
    "   - Provide specific recommendations for remediation\n"
    "3. ACTIONABLE RECOMMENDATIONS:\n"
    "   - List specific steps to check for vulnerability presence\n"
    "   - Recommend version updates or patches if applicable\n"
    "   - Suggest security best practices to prevent similar issues\n"
    "Keep your analysis practical and actionable. If the codebase doesn't appear to be affected, clearly state that and explain why."
)