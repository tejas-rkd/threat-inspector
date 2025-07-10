import os
import shutil
import json
from .constants import CHROMA_PATH, CVE_ANALYSIS_PROMPT

def cleanup():
    if os.path.exists(CHROMA_PATH):
        shutil.rmtree(CHROMA_PATH)
        # print(f"Deleted vector store directory: {CHROMA_PATH}")
    else:
        print(f"No vector store directory found at: {CHROMA_PATH}")
    return


def generate_question(vuln_data):
    question = CVE_ANALYSIS_PROMPT.format(vuln_data=json.dumps(vuln_data, indent=2))
    return question