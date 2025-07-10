#!/usr/bin/env python3
"""
Threat Inspector - Ollama Setup Script
This script automates the installation and setup of Ollama with required models for Linux systems.
"""

import os
import sys
import subprocess
import time
import requests
import platform
from pathlib import Path


def print_step(message):
    """Print a step message with emoji."""
    print(f"🔧 {message}")


def print_success(message):
    """Print a success message with emoji."""
    print(f"✅ {message}")


def print_error(message):
    """Print an error message with emoji."""
    print(f"❌ {message}")


def print_info(message):
    """Print an info message with emoji."""
    print(f"ℹ️  {message}")


def run_command(cmd, check=True, capture_output=False):
    """Run a shell command and handle errors."""
    try:
        result = subprocess.run(
            cmd, 
            shell=True, 
            check=check, 
            capture_output=capture_output, 
            text=True
        )
        return result
    except subprocess.CalledProcessError as e:
        print_error(f"Command failed: {cmd}")
        print_error(f"Error: {e}")
        return None


def command_exists(command):
    """Check if a command exists in the system PATH."""
    try:
        subprocess.run(
            f"command -v {command}", 
            shell=True, 
            check=True, 
            capture_output=True
        )
        return True
    except subprocess.CalledProcessError:
        return False


def is_ollama_running():
    """Check if Ollama service is running."""
    try:
        response = requests.get("http://localhost:11434/api/version", timeout=5)
        return response.status_code == 200
    except requests.RequestException:
        return False


def install_ollama_linux():
    """Install Ollama on Linux."""
    print_step("Installing Ollama on Linux...")
    
    # Check if curl is available
    if not command_exists("curl"):
        print_error("curl is not installed. Please install curl first:")
        print("  sudo apt update && sudo apt install curl  # For Ubuntu/Debian")
        print("  sudo yum install curl                     # For CentOS/RHEL")
        return False
    
    # Download and run the install script
    cmd = "curl -fsSL https://ollama.com/install.sh | sh"
    result = run_command(cmd)
    
    if result and result.returncode == 0:
        print_success("Ollama installed successfully")
        return True
    else:
        print_error("Failed to install Ollama")
        return False


def start_ollama():
    """Start Ollama service."""
    print_step("Starting Ollama service...")
    
    if is_ollama_running():
        print_success("Ollama is already running")
        return True
    
    print_info("Starting Ollama in the background...")
    
    # Start Ollama in background
    try:
        subprocess.Popen(
            ["ollama", "serve"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
    except FileNotFoundError:
        print_error("Ollama command not found. Installation may have failed.")
        return False
    
    # Wait for Ollama to start
    print_info("Waiting for Ollama to start...")
    for i in range(30):
        time.sleep(1)
        if is_ollama_running():
            print_success("Ollama started successfully")
            return True
        if i == 10:
            print_info("Still waiting for Ollama to start...")
    
    print_error("Failed to start Ollama service")
    return False


def pull_models():
    """Pull required models."""
    print_step("Pulling required models...")
    
    models = [
        ("mistral:latest", "Mistral model (this may take a while)"),
        ("all-minilm:latest", "all-minilm embedding model")
    ]
    
    for model, description in models:
        print_info(f"Pulling {description}...")
        result = run_command(f"ollama pull {model}")
        
        if not result or result.returncode != 0:
            print_error(f"Failed to pull {model}")
            return False
    
    print_success("All models downloaded successfully")
    return True


def verify_installation():
    """Verify that everything is installed correctly."""
    print_step("Verifying installation...")
    
    # Check if Ollama command exists
    if not command_exists("ollama"):
        print_error("Ollama command not found")
        return False
    
    # Check if service is running
    if not is_ollama_running():
        print_error("Ollama service is not running")
        return False
    
    # Check if models are available
    result = run_command("ollama list", capture_output=True)
    if not result:
        print_error("Failed to list models")
        return False
    
    models_output = result.stdout
    required_models = ["mistral:latest", "all-minilm:latest"]
    
    for model in required_models:
        if model not in models_output:
            print_error(f"{model} model not found")
            return False
    
    print_success("Installation verified successfully")
    return True


def check_system_requirements():
    """Check if the system meets requirements."""
    print_step("Checking system requirements...")
    
    # Check OS
    if platform.system() != "Linux":
        print_error("This script is designed for Linux systems only")
        print_info("For other operating systems, please install Ollama manually:")
        print_info("  macOS: brew install ollama")
        print_info("  Windows: Download from https://ollama.com/download")
        return False
    
    # Check Python version
    if sys.version_info < (3, 6):
        print_error("Python 3.6 or higher is required")
        return False
    
    print_success("System requirements met")
    return True


def main():
    """Main function."""
    print("🚀 Starting Ollama setup for Threat Inspector...")
    print()
    
    # Check system requirements
    if not check_system_requirements():
        sys.exit(1)
    
    # Check if Ollama is already installed
    if command_exists("ollama"):
        print_success("Ollama is already installed")
    else:
        if not install_ollama_linux():
            sys.exit(1)
    
    # Start Ollama service
    if not start_ollama():
        sys.exit(1)
    
    # Pull required models
    if not pull_models():
        sys.exit(1)
    
    # Verify installation
    if not verify_installation():
        sys.exit(1)
    
    print()
    print("🎉 Ollama setup completed successfully!")
    print()
    print("You can now run Threat Inspector with:")
    print("   python src/main.py <CVE_ID> --path <path_to_code>")
    print()
    print("To stop Ollama service later, run: pkill ollama")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print()
        print_info("Setup interrupted by user")
        sys.exit(1)
    except Exception as e:
        print()
        print_error(f"Unexpected error: {e}")
        sys.exit(1)
