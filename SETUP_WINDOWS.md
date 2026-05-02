# Windows Setup Guide - Production AI Data Assistant

## Quick Setup (10 minutes)

### Step 1: Install Ollama on Windows
1. Download: https://ollama.ai/download/windows
2. Run the installer and follow the prompts
3. Restart your computer

### Step 2: Install Node.js
1. Download: https://nodejs.org/ (LTS version)
2. Run the installer and follow the prompts
3. Restart your terminal/command prompt

### Step 3: Start Ollama
After installation, Ollama runs automatically on `http://localhost:11434`

Verify it's running by opening a terminal and typing:
```powershell
curl http://localhost:11434
```

### Step 4: Pull a Model
Open PowerShell and run one of these commands (first run downloads the model):

```powershell
# Option 1: Mistral (recommended, 7GB, faster)
ollama pull mistral

# Option 2: Llama2 (7GB, good quality)
ollama pull llama2

# Option 3: Neural Chat (3GB, lightweight)
ollama pull neural-chat
```

### Step 5: Install Python Packages
```powershell
cd d:\Python\AI_Data_Engineer\rag_data_assistant
pip install -r requirements.txt
```

### Step 6: Install Node.js Packages
```powershell
cd frontend
npm install
cd ..
```

### Step 7: Setup Database
```powershell
python database_setup.py
```

### Step 8: Run the Application
```powershell
# Option 1: PowerShell script (recommended)
.\run_app.ps1

# Option 2: Batch file
run_app.bat

# Option 3: Manual (separate terminals)
# Terminal 1: python backend/api.py
# Terminal 2: cd frontend && npm start
```

The app will open at http://localhost:3000

## Troubleshooting

### "Cannot connect to Ollama"
- Make sure Ollama is running: Open PowerShell and type `ollama serve`
- Check http://localhost:11434 in your browser

### "Model not found"
- Run `ollama pull mistral` (or your chosen model)
- Wait for download to complete

### Slow responses
- Smaller models are faster: Use `neural-chat` instead of `llama2`
- Ollama uses GPU if available, CPU otherwise

## Available Models

| Model | Size | Speed | Quality |
|-------|------|-------|---------|
| mistral | 7GB | Fast | Good |
| llama2 | 7GB | Medium | Excellent |
| neural-chat | 3GB | Fast | Good |
| dolphin-mixtral | 26GB | Slow | Best |

## Example Queries
Once running, try:
- "Top 5 products by revenue"
- "Which country has highest sales?"
- "What is the total profit by region?"
- "Show me top customers by segment"
- "Top lead sources by conversion rate"
- "High-scoring leads by industry"
- "Which campaigns have the most qualified leads?"

## Model Selection
**For POC**: Use `mistral` or `neural-chat` - fast and sufficient quality
**For production**: Use `llama2` or `dolphin-mixtral` - better accuracy
