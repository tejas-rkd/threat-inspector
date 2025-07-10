#!/bin/bash

# Threat Inspector - Ollama Setup Script
# This script automates the installation and setup of Ollama with required models

set -e  # Exit on any error

echo "🚀 Starting Ollama setup for Threat Inspector..."

# Function to detect OS
detect_os() {
    if [[ "$OSTYPE" == "linux-gnu"* ]]; then
        echo "linux"
    elif [[ "$OSTYPE" == "darwin"* ]]; then
        echo "macos"
    elif [[ "$OSTYPE" == "msys" || "$OSTYPE" == "cygwin" ]]; then
        echo "windows"
    else
        echo "unknown"
    fi
}

# Function to check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Function to install Ollama on Linux
install_ollama_linux() {
    echo "📦 Installing Ollama on Linux..."
    curl -fsSL https://ollama.com/install.sh | sh
}

# Function to install Ollama on macOS
install_ollama_macos() {
    echo "📦 Installing Ollama on macOS..."
    if command_exists brew; then
        brew install ollama
    else
        echo "❌ Homebrew not found. Please install Homebrew first:"
        echo "   /bin/bash -c \"\$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)\""
        exit 1
    fi
}

# Function to check if Ollama is running
is_ollama_running() {
    curl -s http://localhost:11434/api/version >/dev/null 2>&1
}

# Function to start Ollama service
start_ollama() {
    echo "🔄 Starting Ollama service..."
    if is_ollama_running; then
        echo "✅ Ollama is already running"
    else
        echo "Starting Ollama in the background..."
        nohup ollama serve > /dev/null 2>&1 &
        
        # Wait for Ollama to start
        echo "⏳ Waiting for Ollama to start..."
        for i in {1..30}; do
            if is_ollama_running; then
                echo "✅ Ollama started successfully"
                return 0
            fi
            sleep 1
        done
        
        echo "❌ Failed to start Ollama service"
        exit 1
    fi
}

# Function to pull required models
pull_models() {
    echo "📥 Pulling required models..."
    
    echo "Pulling Mistral model (this may take a while)..."
    ollama pull mistral:latest
    
    echo "Pulling all-minilm embedding model..."
    ollama pull all-minilm:latest
    
    echo "✅ All models downloaded successfully"
}

# Function to verify installation
verify_installation() {
    echo "🔍 Verifying installation..."
    
    # Check if Ollama command exists
    if ! command_exists ollama; then
        echo "❌ Ollama command not found"
        exit 1
    fi
    
    # Check if service is running
    if ! is_ollama_running; then
        echo "❌ Ollama service is not running"
        exit 1
    fi
    
    # Check if models are available
    if ! ollama list | grep -q "mistral:latest"; then
        echo "❌ Mistral model not found"
        exit 1
    fi
    
    if ! ollama list | grep -q "all-minilm:latest"; then
        echo "❌ all-minilm model not found"
        exit 1
    fi
    
    echo "✅ Installation verified successfully"
}

# Main execution
main() {
    echo "🔍 Detecting operating system..."
    OS=$(detect_os)
    echo "Detected OS: $OS"
    
    # Check if Ollama is already installed
    if command_exists ollama; then
        echo "✅ Ollama is already installed"
    else
        case $OS in
            "linux")
                install_ollama_linux
                ;;
            "macos")
                install_ollama_macos
                ;;
            "windows")
                echo "❌ This script doesn't support Windows installation."
                echo "Please manually download and install Ollama from:"
                echo "https://ollama.com/download"
                exit 1
                ;;
            *)
                echo "❌ Unsupported operating system: $OS"
                exit 1
                ;;
        esac
    fi
    
    # Start Ollama service
    start_ollama
    
    # Pull required models
    pull_models
    
    # Verify everything is working
    verify_installation
    
    echo ""
    echo "🎉 Ollama setup completed successfully!"
    echo "You can now run Threat Inspector with:"
    echo "   python src/main.py <CVE_ID> --path <path_to_code>"
    echo ""
    echo "To stop Ollama service later, run: pkill ollama"
}

# Run main function
main "$@"
