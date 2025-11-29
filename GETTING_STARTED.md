# 🎉 Getting Started with YouTube Trends Explorer

Welcome! This guide will help you get the full-stack application running quickly.

## 📋 What You're Getting

A complete AI-powered web application with:
- 🎨 Beautiful React frontend
- 🤖 Multi-agent AI backend
- 🔍 Hybrid search (SQL + Vector)
- 📊 Interactive results visualization

## ⚡ Quick Setup (5 Minutes)

### Step 1: Install Prerequisites

Make sure you have:
- ✅ Python 3.9 or higher
- ✅ Node.js 18 or higher
- ✅ Docker Desktop (running)
- ✅ OpenAI API key

### Step 2: Clone & Setup Backend

```bash
# Navigate to project
cd YouTube-Videos-Trend-Analysis

# Create virtual environment
python -m venv venv

# Activate it
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Mac/Linux

# Install Python packages
pip install -r requirements.txt

# Setup environment
copy .env.example .env
# Edit .env and add: OPENAI_API_KEY=sk-your-key-here

# Start Qdrant database
docker-compose up -d
```

### Step 3: Setup Frontend

```bash
# Navigate to frontend
cd frontend

# Install packages
npm install

# Go back to root
cd ..
```

### Step 4: Launch! 🚀

**Windows (Easiest):**
```bash
.\start_fullstack.ps1
```

**Manual (All Platforms):**

Terminal 1:
```bash
python run_api.py
```

Terminal 2:
```bash
cd frontend
npm run dev
```

### Step 5: Open & Explore

1. **Open your browser**: http://localhost:5173
2. **Try an example query** (click one of the suggestions)
3. **See the magic happen!** ✨

## 🎯 What to Try

### Example Queries

**Analytical (SQL Agent):**
- "Top 10 channels by total views"
- "Which category has the most trending videos?"
- "Average engagement rate for Gaming videos"

**Semantic (Vector Agent):**
- "Find videos about cooking tutorials"
- "Videos related to fitness and wellness"
- "Content similar to tech product reviews"

**Hybrid (Both Agents):**
- "Most popular gaming videos about Minecraft"
- "Top educational programming content"
- "Trending cooking videos with high engagement"

## 🎨 UI Features to Explore

1. **Search Bar**: Type or click examples
2. **System Info**: Click button in header
3. **Agent Badges**: See which AI processed your query
4. **Video Cards**: Rich results with stats
5. **Loading Animations**: Smooth transitions
6. **Health Status**: Green badge = all good!

## 📍 Important URLs

| What | Where | Why |
|------|-------|-----|
| **Main App** | http://localhost:5173 | Your beautiful UI |
| **API** | http://localhost:8000 | Backend endpoint |
| **API Docs** | http://localhost:8000/docs | Interactive API testing |
| **Qdrant** | http://localhost:6333/dashboard | Vector database |

## 🔧 Troubleshooting

### "Can't connect to backend"
```bash
# Check if API is running
curl http://localhost:8000/health

# Should return: {"status": "healthy"}
```

### "Port already in use"
```bash
# Windows - Kill process on port 8000
netstat -ano | findstr :8000
taskkill /PID <number> /F

# Mac/Linux
lsof -ti:8000 | xargs kill -9
```

### "OpenAI API error"
1. Check `.env` file has your API key
2. Verify key starts with `sk-`
3. Restart backend: `python run_api.py`

### "Frontend won't start"
```bash
cd frontend
rm -rf node_modules package-lock.json
npm install
npm run dev
```

## 📚 Next Steps

### Learn More
- **Full Setup Guide**: [FULLSTACK_SETUP.md](FULLSTACK_SETUP.md)
- **API Documentation**: [API_GUIDE.md](API_GUIDE.md)
- **Architecture**: [FRONTEND_BACKEND_SUMMARY.md](FRONTEND_BACKEND_SUMMARY.md)

### Customize
- **Change Colors**: Edit `frontend/tailwind.config.js`
- **Add Features**: Check component files in `frontend/src/components/`
- **Modify Agents**: See `src/agents/` directory

### Deploy
- **Frontend**: Build with `npm run build`, deploy to Netlify/Vercel
- **Backend**: Use gunicorn, deploy to Heroku/Railway/AWS

## 🎓 Understanding the System

### How It Works

```
You ask a question
        ↓
Frontend sends to API
        ↓
Orchestrator analyzes query
        ↓
    ┌───┴───┐
    ↓       ↓
SQL Agent  Vector Agent
    ↓       ↓
SQLite DB  Qdrant DB
    ↓       ↓
    └───┬───┘
        ↓
LLM generates answer
        ↓
Beautiful results in UI
```

### Agent Selection

- **SQL Agent**: Numbers, stats, rankings, comparisons
- **Vector Agent**: Meaning, similarity, topics, content
- **Hybrid**: Both combined for complex queries

## 💡 Pro Tips

1. **Use Example Queries**: Click instead of typing
2. **Watch the Badges**: Learn which agent handles what
3. **Check Processing Time**: See how fast AI works
4. **System Info Panel**: Understand your setup
5. **Try Different Query Types**: Explore capabilities

## 🎉 You're Ready!

You now have a fully functional AI-powered YouTube trends analyzer!

### What You Can Do

✅ Ask natural language questions
✅ Get AI-generated insights
✅ See detailed video results
✅ Understand which AI agent helped
✅ Monitor system health
✅ Explore different query types

### Share Your Experience

- Found a cool query? Try variations!
- Built something on top? Awesome!
- Have questions? Check the docs!

## 🚀 Happy Exploring!

The system is designed to be:
- **Intuitive**: Just ask questions naturally
- **Transparent**: See how AI processes queries
- **Fast**: Get results in seconds
- **Extensible**: Easy to customize and extend

---

**Need Help?**
- Check [FULLSTACK_SETUP.md](FULLSTACK_SETUP.md) for detailed setup
- Review [API_GUIDE.md](API_GUIDE.md) for API usage
- See logs in `logs/` directory for debugging

**Ready for More?**
- Explore the codebase
- Try custom queries
- Modify the UI
- Add new features

Enjoy your YouTube Trends Explorer! 🎊
