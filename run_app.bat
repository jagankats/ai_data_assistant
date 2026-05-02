@echo off
echo Starting AI Data Assistant Production App
echo Make sure Ollama is running: ollama serve
echo.

REM Add Node.js to PATH
set PATH=C:\Program Files\nodejs;%PATH%

echo Starting FastAPI backend on http://localhost:8000
start "Backend" cmd /k "cd /d D:\Python\AI_Data_Engineer\rag_data_assistant && D:\Python\.venv\Scripts\Activate.ps1 && python backend/api.py"
timeout /t 3 /nobreak > nul
echo Starting React frontend on http://localhost:3000
cd /d D:\Python\AI_Data_Engineer\rag_data_assistant\frontend
npm start