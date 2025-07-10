from setuptools import setup, find_packages

setup(
    name="threat-inspector",
    version="0.1.0",
    author="Your Name",
    author_email="your.email@example.com",
    description="A tool for analyzing vulnerabilities in codebases based on CVE information.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/threat-inspector",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "langchain-core",
        "langchain-community", 
        "langchain-text-splitters",
        "langchain-ollama",
        "langchain-chroma",
        "requests",
        "jsonschema",
        "chromadb"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)