<<<<<<< HEAD
# AI Data Assistant - RAG-Based LLM Query Engine

A production-ready AI Data Assistant that converts natural language questions into SQL queries. Uses **Ollama** (free local LLM) and **PostgreSQL** for 100% offline operation.

## ✨ Key Features

| Feature | Details |
|---------|---------|
| **💰 100% Free** | Local Ollama LLM - no API keys or subscriptions |
| **🔒 Offline** | All data stays on your machine |
| **🚀 Production Ready** | FastAPI with async, error handling, CORS |
| **🎨 Modern UI** | React frontend with responsive design |
| **📊 Multiple Datasets** | SAP sales orders + Salesforce marketing leads |
| **🧠 Smart Queries** | Semantic understanding of natural language |
| **⚡ Window Functions** | Handles complex GROUP BY and per-group queries |

## 🎯 Quick Start (5 minutes)

### 1️⃣ Install Ollama
Download from https://ollama.ai/download, then:
```bash
ollama pull mistral
```

### 2️⃣ Clone & Setup
```bash
git clone https://github.com/YOUR_USERNAME/rag_data_assistant.git
cd rag_data_assistant

# Python setup
python -m venv .venv
.venv\Scripts\activate  # Windows
pip install -r requirements.txt

# Database setup
python database_setup.py

# Frontend setup
cd frontend && npm install && cd ..
```

### 3️⃣ Run the App
```bash
# Terminal 1
python backend/api.py

# Terminal 2
cd frontend && npm start
```

Access at: http://localhost:3000

## 📚 Usage Examples

**Sales Data:**
- "Top 5 products by revenue"
- "Country wise top 2 products"
- "Which region has highest profit?"

**Marketing Data:**
- "Top lead sources by conversion"
- "High-scoring leads by industry"

## 📖 Documentation

- [ARCHITECTURE.md](ARCHITECTURE.md) - System design & technical details
- [SETUP_WINDOWS.md](SETUP_WINDOWS.md) - Windows-specific setup guide

## 🏗️ Project Structure

```
├── backend/api.py              # FastAPI server
├── frontend/src/               # React UI
├── config.py                   # Configuration
├── database_setup.py           # DB initialization
├── requirements.txt            # Python dependencies
└── *.csv                        # Sample datasets
```

## 🔧 Configuration

Edit `.env` to customize database and Ollama settings.

## 📄 License

MIT License - see [LICENSE](LICENSE)

## 🚀 What This Does

Ask questions in English:
```
▶ "Country wise top 2 products by revenue"
▶ "Top lead sources by conversion rate"  
▶ "Which region has highest profit?"
```

The AI automatically:
1. Understands your question semantically
2. Generates correct SQL queries
3. Executes against PostgreSQL
4. Returns natural language answers

## 🙏 Built With

- **Ollama** - Free local LLM
- **FastAPI** - Python web framework
- **PostgreSQL** - Database
- **React** - Frontend UI
=======
# AI Data Assistant - RAG-Based LLM Query Engine

A production-ready AI Data Assistant that converts natural language questions into SQL queries. Uses **Ollama** (free local LLM) and **PostgreSQL** for 100% offline operation.

## ✨ Key Features

| Feature | Details |
|---------|---------|
| **💰 100% Free** | Local Ollama LLM - no API keys or subscriptions |
| **🔒 Offline** | All data stays on your machine |
| **🚀 Production Ready** | FastAPI with async, error handling, CORS |
| **🎨 Modern UI** | React frontend with responsive design |
| **📊 Multiple Datasets** | SAP sales orders + Salesforce marketing leads |
| **🧠 Smart Queries** | Semantic understanding of natural language |
| **⚡ Window Functions** | Handles complex GROUP BY and per-group queries |

## 🎯 Quick Start (5 minutes)

### 1️⃣ Install Ollama
Download from https://ollama.ai/download, then:
```bash
ollama pull mistral
```

### 2️⃣ Clone & Setup
```bash
git clone https://github.com/YOUR_USERNAME/rag_data_assistant.git
cd rag_data_assistant

# Python setup
python -m venv .venv
.venv\Scripts\activate  # Windows
pip install -r requirements.txt

# Database setup
python database_setup.py

# Frontend setup
cd frontend && npm install && cd ..
```

### 3️⃣ Run the App
```bash
# Terminal 1
python backend/api.py

# Terminal 2
cd frontend && npm start
```

Access at: http://localhost:3000

## 📚 Usage Examples

**Sales Data:**
- "Top 5 products by revenue"
- "Country wise top 2 products"
- "Which region has highest profit?"

**Marketing Data:**
- "Top lead sources by conversion"
- "High-scoring leads by industry"

## 📖 Documentation

- [ARCHITECTURE.md](ARCHITECTURE.md) - System design & technical details
- [SETUP_WINDOWS.md](SETUP_WINDOWS.md) - Windows-specific setup guide

## 🏗️ Project Structure

```
├── backend/api.py              # FastAPI server
├── frontend/src/               # React UI
├── config.py                   # Configuration
├── database_setup.py           # DB initialization
├── requirements.txt            # Python dependencies
└── *.csv                        # Sample datasets
```

## 🔧 Configuration

Edit `.env` to customize database and Ollama settings.

## 📄 License

MIT License - see [LICENSE](LICENSE)

## 🚀 What This Does

Ask questions in English:
```
▶ "Country wise top 2 products by revenue"
▶ "Top lead sources by conversion rate"  
▶ "Which region has highest profit?"
```

The AI automatically:
1. Understands your question semantically
2. Generates correct SQL queries
3. Executes against PostgreSQL
4. Returns natural language answers

## 🙏 Built With

- **Ollama** - Free local LLM
- **FastAPI** - Python web framework
- **PostgreSQL** - Database
- **React** - Frontend UI
>>>>>>> 35262638c7d11c08573841d40dd9a2d8cf7a20f9
