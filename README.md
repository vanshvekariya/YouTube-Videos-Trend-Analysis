# YouTube Trends Explorer 🚀

A full-stack AI-powered application for analyzing YouTube trending videos using multi-agent systems, vector embeddings, and modern web technologies.

## 🎯 Project Overview

**Complete Full-Stack Application** featuring:
- 🤖 **Multi-Agent AI System**: Intelligent query routing between SQL and Vector agents
- 🎨 **Modern React Frontend**: Beautiful, responsive UI with TailwindCSS
- ⚡ **FastAPI Backend**: High-performance REST API with auto-documentation
- 🔍 **Hybrid Search**: Combines semantic search with analytical queries
- 📊 **Interactive Visualizations**: Real-time results with rich metadata
- 🎯 **Smart Query Routing**: Automatically selects the best agent for your question

> 🎉 **NEW**: Full-stack UI now available! See [QUICK_START_FULLSTACK.md](QUICK_START_FULLSTACK.md) to get started in 5 minutes.

## ✨ What's New

- ✅ **React Frontend** with modern UI/UX
- ✅ **FastAPI REST API** with interactive documentation
- ✅ **Multi-Agent System** (SQL + Vector agents)
- ✅ **Example Queries** for quick onboarding
- ✅ **System Monitoring** with health checks
- ✅ **Beautiful Results Display** with video cards
- ✅ **One-Click Startup** with PowerShell script

## 📁 Project Structure

```
YouTube-Videos-Trend-Analysis/
├── frontend/                     # 🎨 React Frontend
│   ├── src/
│   │   ├── components/          # UI components
│   │   │   ├── ui/              # Reusable components
│   │   │   ├── QueryInput.jsx   # Search interface
│   │   │   └── ResultsDisplay.jsx
│   │   ├── services/
│   │   │   └── api.js           # API client
│   │   ├── App.jsx              # Main app
│   │   └── index.css            # Styles
│   ├── package.json
│   └── vite.config.js
├── src/                          # 🔧 Backend
│   ├── api/                     # FastAPI endpoints
│   │   ├── main.py              # API server
│   │   └── models.py            # Pydantic models
│   ├── agents/                  # AI agents
│   │   ├── orchestrator.py      # Multi-agent system
│   │   ├── sql_agent.py         # SQL queries
│   │   └── vector_agent.py      # Semantic search
│   ├── config/
│   ├── data/
│   ├── embeddings/
│   ├── vectordb/
│   └── main.py                  # CLI interface
├── scripts/                      # Utility scripts
├── tests/                        # Test suite
├── run_api.py                   # API startup
├── start_fullstack.ps1          # Full-stack launcher
├── requirements.txt
└── docker-compose.yml
```

## 🚀 Quick Start (Full Stack)

### Prerequisites
- Python 3.9+
- Node.js 18+
- Docker & Docker Compose
- OpenAI API key

### Installation (5 minutes)

```bash
# 1. Backend setup
python -m venv venv
venv\Scripts\activate          # Windows
pip install -r requirements.txt

# 2. Configure environment
copy .env.example .env
# Edit .env and add your OPENAI_API_KEY

# 3. Start Qdrant
docker-compose up -d

# 4. Frontend setup
cd frontend
npm install
cd ..
```

### Run the Application

**Option 1: One-Click Start (Windows)**
```bash
.\start_fullstack.ps1
```

**Option 2: Manual Start**
```bash
# Terminal 1 - Backend
python run_api.py

# Terminal 2 - Frontend
cd frontend
npm run dev
```

### Access the Application
- 🎨 **Frontend UI**: http://localhost:5173
- 🔌 **Backend API**: http://localhost:8000
- 📚 **API Docs**: http://localhost:8000/docs

### Try It Out
1. Open http://localhost:5173
2. Click an example query or type your own
3. See AI-powered results instantly!

> 📖 **Detailed Guide**: See [QUICK_START_FULLSTACK.md](QUICK_START_FULLSTACK.md) for complete instructions.

## 📊 Dataset Information

The Kaggle YouTube dataset includes:
- **video_id**: Unique video identifier
- **title**: Video title
- **channel_title**: Channel name
- **category_id**: Video category
- **tags**: Video tags
- **views**: View count
- **likes**: Like count
- **dislikes**: Dislike count
- **comment_count**: Number of comments
- **trending_date**: Date when video was trending
- **country**: Country code

## 🔍 Features

### Frontend (React + Vite)
- ✅ **Modern UI**: Beautiful, responsive design with TailwindCSS
- ✅ **Smart Search**: Autocomplete with example queries
- ✅ **Real-time Results**: Live updates with loading animations
- ✅ **Video Cards**: Rich display with stats and metadata
- ✅ **Agent Transparency**: See which AI processed your query
- ✅ **System Monitoring**: Health status and configuration
- ✅ **Mobile Responsive**: Works on all devices

### Backend (FastAPI + Multi-Agent AI)
- ✅ **REST API**: Fast, documented endpoints
- ✅ **Multi-Agent System**: SQL + Vector agents
- ✅ **Smart Routing**: Automatic query type detection
- ✅ **Hybrid Search**: Combines semantic + analytical
- ✅ **RAG with LLM**: GPT-4 powered responses
- ✅ **Vector Database**: Qdrant for semantic search
- ✅ **SQL Analytics**: Complex aggregations and stats

### Data & Search
- ✅ Data ingestion from CSV files
- ✅ Text preprocessing and cleaning
- ✅ Vector embeddings (Sentence-Transformers)
- ✅ Semantic similarity search
- ✅ Metadata filtering
- ✅ Category-based queries

## 🛠️ Technology Stack

### Frontend
- **Framework**: React 18 with Vite
- **Styling**: TailwindCSS + Custom Design System
- **UI Components**: Custom components (shadcn/ui patterns)
- **Icons**: Lucide React
- **Animations**: Framer Motion
- **HTTP Client**: Axios
- **Notifications**: React Hot Toast

### Backend
- **API Framework**: FastAPI
- **AI/LLM**: LangChain + OpenAI GPT-4
- **Vector Database**: Qdrant
- **SQL Database**: SQLite
- **Embeddings**: Sentence-Transformers (all-MiniLM-L6-v2)
- **Data Processing**: Pandas, NumPy
- **Validation**: Pydantic
- **Server**: Uvicorn

### Infrastructure
- **Containerization**: Docker & Docker Compose
- **Logging**: Loguru
- **Testing**: Pytest

## 📝 Usage Examples

### Via Web UI (Recommended)

1. Open http://localhost:5173
2. Try example queries:
   - **SQL**: "Top 10 channels by views"
   - **Vector**: "Find cooking tutorial videos"
   - **Hybrid**: "Popular gaming videos about Minecraft"

### Via API

```bash
curl -X POST http://localhost:8000/query \
  -H "Content-Type: application/json" \
  -d '{"query": "Top 10 trending videos", "max_results": 10}'
```

### Via Python

```python
import requests

response = requests.post(
    "http://localhost:8000/query",
    json={"query": "Find fitness videos", "max_results": 10}
)

data = response.json()
print(data["answer"])
for result in data["results"]:
    print(f"- {result['title']}")
```

### Via CLI

```bash
python -m src.main --query "Which category has the most videos?"
```

## 📚 Documentation

- **[QUICK_START_FULLSTACK.md](QUICK_START_FULLSTACK.md)** - 5-minute quick start guide
- **[FULLSTACK_SETUP.md](FULLSTACK_SETUP.md)** - Complete setup and deployment guide
- **[API_GUIDE.md](API_GUIDE.md)** - Comprehensive API documentation
- **[frontend/README.md](frontend/README.md)** - Frontend-specific documentation
- **[FRONTEND_BACKEND_SUMMARY.md](FRONTEND_BACKEND_SUMMARY.md)** - Architecture overview

## 🎯 Query Types

The system intelligently routes queries to the appropriate agent:

### SQL/Analytical Queries
- "Top 10 channels by views"
- "Which category has the most videos?"
- "Average likes for Gaming category"

### Vector/Semantic Queries
- "Find cooking tutorial videos"
- "Videos about fitness and wellness"
- "Content similar to tech reviews"

### Hybrid Queries
- "Most popular gaming videos about Minecraft"
- "Top educational programming content"
- "Trending cooking videos with high engagement"

## 🧪 Testing

```bash
# Backend tests
pytest

# Frontend tests
cd frontend
npm test
```

## 📈 Performance

- **SQL Queries**: 0.5-2 seconds
- **Vector Queries**: 1-3 seconds
- **Hybrid Queries**: 2-5 seconds

## 🚀 Deployment

### Frontend
```bash
cd frontend
npm run build
# Deploy dist/ to Netlify, Vercel, etc.
```

### Backend
```bash
# Production server
gunicorn src.api.main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker
```

## 🤝 Contributing

Contributions welcome! This project demonstrates:
- Multi-agent AI systems
- Full-stack development
- Modern web technologies
- Vector databases and semantic search

## 📄 License

MIT License

## 🔗 Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [React Documentation](https://react.dev/)
- [Qdrant Documentation](https://qdrant.tech/documentation/)
- [LangChain Documentation](https://python.langchain.com/)
- [TailwindCSS Documentation](https://tailwindcss.com/)
