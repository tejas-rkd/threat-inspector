@echo off
REM Threat Inspector - Ollama Setup Script for Windows
REM This script helps set up Ollama with required models on Windows

echo 🚀 Starting Ollama setup for Threat Inspector...

REM Check if Ollama is installed
where ollama >nul 2>nul
if %errorlevel% neq 0 (
    echo ❌ Ollama is not installed.
    echo Please download and install Ollama from:
    echo https://ollama.com/download
    echo.
    echo After installation, run this script again.
    pause
    exit /b 1
)

echo ✅ Ollama is installed

REM Check if Ollama service is running
curl -s http://localhost:11434/api/version >nul 2>nul
if %errorlevel% neq 0 (
    echo 🔄 Starting Ollama service...
    start /b ollama serve
    
    REM Wait for service to start
    echo ⏳ Waiting for Ollama to start...
    timeout /t 5 /nobreak >nul
    
    REM Check again
    curl -s http://localhost:11434/api/version >nul 2>nul
    if %errorlevel% neq 0 (
        echo ❌ Failed to start Ollama service
        echo Please start Ollama manually from the system tray
        pause
        exit /b 1
    )
)

echo ✅ Ollama service is running

echo 📥 Pulling required models...

echo Pulling Mistral model (this may take a while)...
ollama pull mistral:latest
if %errorlevel% neq 0 (
    echo ❌ Failed to pull Mistral model
    pause
    exit /b 1
)

echo Pulling all-minilm embedding model...
ollama pull all-minilm:latest
if %errorlevel% neq 0 (
    echo ❌ Failed to pull all-minilm model
    pause
    exit /b 1
)

echo ✅ All models downloaded successfully

echo 🔍 Verifying installation...

REM Check if models are available
ollama list | findstr "mistral:latest" >nul
if %errorlevel% neq 0 (
    echo ❌ Mistral model not found
    pause
    exit /b 1
)

ollama list | findstr "all-minilm:latest" >nul
if %errorlevel% neq 0 (
    echo ❌ all-minilm model not found
    pause
    exit /b 1
)

echo ✅ Installation verified successfully
echo.
echo 🎉 Ollama setup completed successfully!
echo You can now run Threat Inspector with:
echo    python src\main.py ^<CVE_ID^> --path ^<path_to_code^>
echo.
pause
