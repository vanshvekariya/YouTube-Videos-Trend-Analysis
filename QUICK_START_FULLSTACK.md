# 🚀 Quick Start - Full Stack

Get the YouTube Trends Explorer running in 5 minutes!

## ⚡ Prerequisites Check

```bash
# Check Python
python --version  # Should be 3.9+

# Check Node.js
node --version    # Should be 18+

# Check Docker
docker --version
```

## 📦 Installation

### 1. Backend Setup (2 minutes)

```bash
# Create and activate virtual environment
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/Mac

# Install dependencies
pip install -r requirements.txt

# Configure environment
copy .env.example .env
# Edit .env and add your OPENAI_API_KEY

# Start Qdrant
docker-compose up -d
```

### 2. Frontend Setup (1 minute)

```bash
# Navigate to frontend
cd frontend

# Install dependencies
npm install

# Configure environment
copy .env.example .env
```

## 🎯 Running the Application

### Option 1: PowerShell Script (Easiest - Windows)

```bash
.\start_fullstack.ps1
```

This will open two windows:
- Backend API on http://localhost:8000
- Frontend UI on http://localhost:5173

### Option 2: Manual Start

**Terminal 1 - Backend:**
```bash
python run_api.py
```

**Terminal 2 - Frontend:**
```bash
cd frontend
npm run dev
```

## ✅ Verify It's Working

1. **Check Backend**: http://localhost:8000/health
   - Should return `{"status": "healthy"}`

2. **Check Frontend**: http://localhost:5173
   - Should show the YouTube Trends Explorer UI

3. **Try a Query**:
   - Type: "Top 10 trending videos"
   - Click Search
   - See results!

## 🎨 What You'll See

### Frontend Features
- 🔍 **Smart Search Bar** with autocomplete examples
- 💡 **Example Queries** to get started
- 📊 **Beautiful Results** with video cards
- 🤖 **Agent Transparency** showing which AI processed your query
- ⚡ **Real-time Processing** with loading animations
- 📈 **System Info** panel with configuration details

### Backend Features
- 🔌 **REST API** at http://localhost:8000
- 📚 **Interactive Docs** at http://localhost:8000/docs
- 🤖 **Multi-Agent System** (SQL + Vector agents)
- 🎯 **Smart Routing** based on query type

## 🧪 Test Queries

Try these to see different agent types:

**SQL/Analytical:**
```
Top 10 channels by views
Which category has the most videos?
Average likes for Gaming category
```

**Vector/Semantic:**
```
Find cooking tutorial videos
Videos about fitness and wellness
Content similar to tech reviews
```

**Hybrid:**
```
Most popular gaming videos about Minecraft
Top educational programming content
Trending cooking videos with high engagement
```

## 🛑 Stopping the Application

### If using PowerShell script:
- Close both PowerShell windows

### If running manually:
- Press `Ctrl+C` in both terminals

### Stop Qdrant:
```bash
docker-compose down
```

## 🐛 Common Issues

### "Port 8000 already in use"
```bash
# Windows
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# Linux/Mac
lsof -ti:8000 | xargs kill -9
```

### "Failed to connect to backend"
1. Ensure backend is running: `curl http://localhost:8000/health`
2. Check `.env` file has correct API key
3. Verify Qdrant is running: `docker ps`

### "Module not found" (Frontend)
```bash
cd frontend
rm -rf node_modules package-lock.json
npm install
```

### "OpenAI API key not found"
1. Check `.env` file exists in project root
2. Verify `OPENAI_API_KEY=sk-...` is set
3. Restart backend after adding key

## 📁 Project Structure

```
YouTube-Videos-Trend-Analysis/
├── frontend/              # React frontend
│   ├── src/
│   │   ├── components/   # UI components
│   │   ├── services/     # API client
│   │   └── App.jsx       # Main app
│   └── package.json
├── src/
│   ├── api/              # FastAPI backend
│   ├── agents/           # AI agents
│   └── main.py
├── run_api.py            # Backend starter
├── start_fullstack.ps1   # Full stack starter
└── requirements.txt
```

## 🎓 Next Steps

1. **Explore the UI**: Try different query types
2. **Check API Docs**: http://localhost:8000/docs
3. **View System Info**: Click "System Info" button in UI
4. **Read Full Docs**: See [FULLSTACK_SETUP.md](FULLSTACK_SETUP.md)
5. **Customize**: Modify colors in `frontend/tailwind.config.js`

## 📊 Performance Tips

- Use `gpt-4o-mini` for faster responses (already default)
- Limit results to 10-20 for best performance
- Keep Qdrant running to avoid startup delays

## 🔗 Important URLs

| Service | URL | Description |
|---------|-----|-------------|
| Frontend | http://localhost:5173 | Main UI |
| Backend API | http://localhost:8000 | API endpoint |
| API Docs | http://localhost:8000/docs | Swagger UI |
| Qdrant | http://localhost:6333/dashboard | Vector DB |

## 💡 Pro Tips

1. **Use Example Queries**: Click them instead of typing
2. **Watch Agent Routing**: See which agent handles your query
3. **Check Processing Time**: Shown in results metadata
4. **System Health**: Green badge = all systems operational
5. **Keyboard Shortcuts**: Press Enter to submit query

## 🎉 You're All Set!

The full stack is now running. Enjoy exploring YouTube trends with AI! 🚀

For detailed documentation:
- [Full Stack Setup Guide](FULLSTACK_SETUP.md)
- [API Documentation](API_GUIDE.md)
- [Frontend README](frontend/README.md)

---

**Need Help?** Check the logs in the `logs/` directory or review the troubleshooting section above.
