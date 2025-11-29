# Full-Stack Setup Guide

Complete guide to running the YouTube Trends Explorer with both backend API and frontend UI.

## 📋 Table of Contents

- [Overview](#overview)
- [Prerequisites](#prerequisites)
- [Backend Setup](#backend-setup)
- [Frontend Setup](#frontend-setup)
- [Running the Full Stack](#running-the-full-stack)
- [API Documentation](#api-documentation)
- [Troubleshooting](#troubleshooting)

## 🎯 Overview

The YouTube Trends Explorer consists of:

- **Backend**: Python FastAPI server with multi-agent AI system
- **Frontend**: React + Vite modern web application
- **Database**: SQLite for structured data, Qdrant for vector embeddings

### Architecture

```
┌─────────────────┐
│  React Frontend │ (Port 5173)
│   (Vite + UI)   │
└────────┬────────┘
         │ HTTP/REST
         ▼
┌─────────────────┐
│  FastAPI Server │ (Port 8000)
│  Multi-Agent AI │
└────────┬────────┘
         │
    ┌────┴────┐
    ▼         ▼
┌────────┐ ┌─────────┐
│ SQLite │ │ Qdrant  │
│   DB   │ │ Vector  │
└────────┘ └─────────┘
```

## ✅ Prerequisites

### Required Software

- **Python 3.9+** with pip
- **Node.js 18+** with npm
- **Docker** and Docker Compose (for Qdrant)
- **Git** (optional)

### API Keys

- OpenAI API key or OpenRouter API key (for LLM)

## 🔧 Backend Setup

### 1. Navigate to Project Root

```bash
cd YouTube-Videos-Trend-Analysis
```

### 2. Create Python Virtual Environment

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Python Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

```bash
# Copy example env file
copy .env.example .env

# Edit .env file with your settings
```

Required variables in `.env`:
```env
OPENAI_API_KEY=your_api_key_here
LLM_MODEL=gpt-4o-mini
SQL_DB_PATH=youtube_trends_canada.db
QDRANT_HOST=localhost
QDRANT_PORT=6333
```

### 5. Start Qdrant Vector Database

```bash
docker-compose up -d
```

Verify Qdrant is running: http://localhost:6333/dashboard

### 6. Prepare Data (If Not Already Done)

```bash
# Ingest data into SQLite
python scripts/ingest_data.py

# Create embeddings and index in Qdrant
python scripts/create_embeddings.py
```

### 7. Test Backend

```bash
# Test the multi-agent system
python -m src.main --query "Top 10 trending videos"
```

## 🎨 Frontend Setup

### 1. Navigate to Frontend Directory

```bash
cd frontend
```

### 2. Install Node Dependencies

```bash
npm install
```

### 3. Configure Environment

```bash
# Copy example env file
copy .env.example .env
```

The `.env` file should contain:
```env
VITE_API_URL=http://localhost:8000
```

## 🚀 Running the Full Stack

### Option 1: Run Both Servers Separately

**Terminal 1 - Backend API:**
```bash
# From project root
python run_api.py
```

Backend will be available at: http://localhost:8000
API Documentation: http://localhost:8000/docs

**Terminal 2 - Frontend:**
```bash
# From frontend directory
cd frontend
npm run dev
```

Frontend will be available at: http://localhost:5173

### Option 2: Using PowerShell Script (Windows)

Create a script `start_fullstack.ps1`:
```powershell
# Start backend in new window
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$PWD'; .\venv\Scripts\activate; python run_api.py"

# Wait for backend to start
Start-Sleep -Seconds 5

# Start frontend in new window
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$PWD\frontend'; npm run dev"
```

Run it:
```bash
.\start_fullstack.ps1
```

### Option 3: Using Bash Script (Linux/Mac)

Create a script `start_fullstack.sh`:
```bash
#!/bin/bash

# Start backend in background
source venv/bin/activate
python run_api.py &
BACKEND_PID=$!

# Wait for backend to start
sleep 5

# Start frontend
cd frontend
npm run dev

# Cleanup on exit
trap "kill $BACKEND_PID" EXIT
```

Run it:
```bash
chmod +x start_fullstack.sh
./start_fullstack.sh
```

## 📚 API Documentation

### Interactive API Docs

Once the backend is running, visit:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

### Key Endpoints

#### POST /query
Process a natural language query.

**Request:**
```json
{
  "query": "Top 10 gaming videos",
  "max_results": 10
}
```

**Response:**
```json
{
  "query": "Top 10 gaming videos",
  "answer": "Here are the top 10 gaming videos...",
  "success": true,
  "metadata": {
    "query_type": "sql",
    "agents_used": ["SQL Agent"],
    "confidence": 0.95
  },
  "results": [...],
  "processing_time": 2.34
}
```

#### GET /health
Check system health.

**Response:**
```json
{
  "status": "healthy",
  "version": "1.0.0",
  "agents_available": ["SQL Agent", "Vector Agent"],
  "database_connected": true
}
```

#### GET /examples
Get example queries.

**Response:**
```json
[
  {
    "category": "SQL/Analytical",
    "query": "Which category has the most trending videos?",
    "description": "Get statistics about video categories"
  },
  ...
]
```

## 🔍 Testing the System

### 1. Check Backend Health

```bash
curl http://localhost:8000/health
```

### 2. Test a Query via API

```bash
curl -X POST http://localhost:8000/query \
  -H "Content-Type: application/json" \
  -d '{"query": "Top 10 trending videos", "max_results": 10}'
```

### 3. Test Frontend

1. Open http://localhost:5173
2. Try an example query
3. Verify results display correctly

## 🐛 Troubleshooting

### Backend Issues

**Problem**: `ModuleNotFoundError`
```bash
# Solution: Ensure virtual environment is activated
venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac
```

**Problem**: `Connection refused` to Qdrant
```bash
# Solution: Start Qdrant
docker-compose up -d

# Check if running
docker ps
```

**Problem**: `OpenAI API key not found`
```bash
# Solution: Check .env file
cat .env  # Linux/Mac
type .env  # Windows
```

### Frontend Issues

**Problem**: `Failed to connect to backend`
```bash
# Solution 1: Ensure backend is running
curl http://localhost:8000/health

# Solution 2: Check CORS settings in backend
# Verify frontend URL is in allowed origins
```

**Problem**: `Module not found` errors
```bash
# Solution: Reinstall dependencies
cd frontend
rm -rf node_modules package-lock.json
npm install
```

**Problem**: Blank page or build errors
```bash
# Solution: Clear Vite cache
cd frontend
rm -rf node_modules/.vite
npm run dev
```

### CORS Issues

If you see CORS errors in browser console:

1. Check backend `src/api/main.py` CORS settings:
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Add your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

2. Restart backend after changes

### Port Conflicts

**Backend (8000) already in use:**
```bash
# Windows
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# Linux/Mac
lsof -ti:8000 | xargs kill -9
```

**Frontend (5173) already in use:**
```bash
# Change port in vite.config.js
server: {
  port: 5174,  // Use different port
}
```

## 📊 Performance Tips

### Backend Optimization

1. **Use appropriate LLM model**:
   - Development: `gpt-4o-mini` (faster, cheaper)
   - Production: `gpt-4` (better quality)

2. **Batch processing**: Process multiple queries in parallel if needed

3. **Caching**: Consider adding Redis for query caching

### Frontend Optimization

1. **Build for production**:
```bash
cd frontend
npm run build
npm run preview
```

2. **Enable compression**: Use nginx or similar for production

3. **Lazy loading**: Components are already optimized

## 🔒 Security Considerations

1. **API Keys**: Never commit `.env` files to git
2. **CORS**: Restrict origins in production
3. **Rate Limiting**: Add rate limiting to API endpoints
4. **Input Validation**: Already implemented in Pydantic models
5. **HTTPS**: Use HTTPS in production

## 📦 Deployment

### Backend Deployment

Options:
- **Heroku**: Use `Procfile` with gunicorn
- **AWS EC2**: Run with systemd service
- **Docker**: Create Dockerfile for containerization
- **Railway/Render**: Direct Python deployment

### Frontend Deployment

Options:
- **Netlify**: `npm run build` → Deploy `dist/`
- **Vercel**: Connect GitHub repo
- **AWS S3 + CloudFront**: Static hosting
- **GitHub Pages**: For static deployment

### Environment Variables in Production

**Backend:**
- Set via platform environment variables
- Use secrets management (AWS Secrets Manager, etc.)

**Frontend:**
- Set `VITE_API_URL` to production API URL
- Rebuild after changing env vars

## 🎉 Success Checklist

- [ ] Qdrant running on port 6333
- [ ] Backend API running on port 8000
- [ ] Frontend running on port 5173
- [ ] Can access http://localhost:8000/docs
- [ ] Can access http://localhost:5173
- [ ] Health check returns "healthy"
- [ ] Example query works end-to-end
- [ ] Results display correctly in UI

## 📞 Support

If you encounter issues:

1. Check logs in `logs/` directory
2. Review error messages in browser console
3. Verify all prerequisites are installed
4. Ensure all services are running
5. Check environment variables

## 🔗 Additional Resources

- [Backend README](README.md)
- [Frontend README](frontend/README.md)
- [Multi-Agent Setup](MULTI_AGENT_SETUP.md)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [React Documentation](https://react.dev/)
- [Vite Documentation](https://vitejs.dev/)
