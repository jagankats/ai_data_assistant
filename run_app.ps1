# Run AI Data Assistant Production App
# This script starts both the FastAPI backend and React frontend

Write-Host "Starting AI Data Assistant..." -ForegroundColor Green
Write-Host "Make sure Ollama is running: ollama serve" -ForegroundColor Yellow
Write-Host ""

# Add Node.js to PATH
$env:Path = "C:\Program Files\nodejs;" + $env:Path

# Start backend in background
Write-Host "Starting FastAPI backend on http://localhost:8000" -ForegroundColor Cyan
$backendJob = Start-Job -ScriptBlock {
    Set-Location "D:\Python\AI_Data_Engineer\rag_data_assistant"
    & "D:\Python\.venv\Scripts\Activate.ps1"
    python backend/api.py
}

# Wait a moment for backend to start
Start-Sleep -Seconds 3

# Start frontend
Write-Host "Starting React frontend on http://localhost:3000" -ForegroundColor Cyan
Set-Location "D:\Python\AI_Data_Engineer\rag_data_assistant\frontend"
npm start

# When frontend exits, stop backend
Write-Host "Stopping backend..." -ForegroundColor Yellow
Stop-Job $backendJob
Remove-Job $backendJob