# 🚀 Get Started - YouTube Trends Explorer POC

Welcome! This guide will get you from zero to running semantic search in **under 10 minutes**.

---

## ✅ What You Have

A complete, production-ready POC for semantic search over YouTube trending videos:

- ✅ **Vector Database**: Qdrant for fast similarity search
- ✅ **Embeddings**: Local sentence-transformers (no API key needed)
- ✅ **Data Pipeline**: Automated ingestion and preprocessing
- ✅ **Semantic Search**: Natural language video discovery
- ✅ **Industry Structure**: Modular, scalable, maintainable code
- ✅ **Documentation**: Comprehensive guides and examples
- ✅ **Tests**: Unit tests for core functionality

---

## 🎯 Three Ways to Start

### Option 1: Quick Test (2 minutes)
Just verify everything works:
```powershell
cd "path\yotube-trends-poc-v1"
python -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt
docker-compose up -d
python scripts/quick_start.py
```

### Option 2: Full Setup (10 minutes)
Complete setup with real data:
1. Follow **Option 1** above
2. Download dataset from [Kaggle](https://www.kaggle.com/datasets/datasnaek/youtube-new/data)
3. Place CSV files in `data/raw/`
4. Run: `python scripts/ingest_data.py`
5. Run: `python scripts/search_demo.py`

### Option 3: Read First (5 minutes)
Understand before diving in:
1. Read `README.md` - Project overview
2. Read `ARCHITECTURE.md` - System design
3. Read `QUICKSTART.md` - Setup steps
4. Then choose Option 1 or 2

---

## 📋 Prerequisites

Before starting, ensure you have:

- [ ] **Python 3.9 or higher** - Check: `python --version`
- [ ] **Docker Desktop** - Must be running
- [ ] **2GB free space** - For dependencies and data
- [ ] **Internet connection** - To download models and data

---

## 🏃 Quick Start (Step by Step)

### Step 1: Setup Environment (2 min)

```powershell
# Navigate to project
cd "path\yotube-trends-poc-v1"

# Create virtual environment
python -m venv venv

# Activate it (you'll see (venv) in prompt)
.\venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

**Expected output**: All packages install successfully

### Step 2: Configure (30 sec)

```powershell
# Copy environment template
copy .env.example .env
```

**No editing needed** - defaults use local embeddings (no API key required)

### Step 3: Start Qdrant (1 min)

```powershell
# Start vector database
docker-compose up -d

# Verify it's running
docker ps
```

**Expected output**: Container named `qdrant` is running

**Verify in browser**: http://localhost:6333/dashboard

### Step 4: Verify Setup (1 min)

```powershell
# Run verification script
python scripts/quick_start.py
```

**Expected output**: All checks pass ✓

### Step 5: Get Data (5 min)

**Option A - Sample Data (for testing)**
The quick_start script already tested with sample data. Skip to Step 6.

**Option B - Real Data (recommended)**
1. Go to: https://www.kaggle.com/datasets/datasnaek/youtube-new/data
2. Login/signup to Kaggle (free)
3. Download the dataset (click Download button)
4. Extract the ZIP file
5. Copy CSV files (USvideos.csv, GBvideos.csv, etc.) to `data/raw/`

### Step 6: Ingest Data (5-15 min)

```powershell
# Run full ingestion pipeline
python scripts/ingest_data.py
```

**What happens**:
1. ✓ Loads CSV files
2. ✓ Cleans and preprocesses data
3. ✓ Generates embeddings (downloads model on first run)
4. ✓ Indexes in Qdrant

**Time**: 5-15 minutes depending on data size and CPU

### Step 7: Search! (30 sec)

```powershell
# Run interactive search demo
python scripts/search_demo.py
```

**Choose**:
- **Option 1**: Demo queries (pre-defined searches)
- **Option 2**: Interactive mode (type your own queries)

**Try these queries**:
- "funny cat videos"
- "gaming tutorials and walkthroughs"
- "cooking recipes and food"
- "music concerts and performances"
- "technology reviews and unboxing"

---

## 🎓 What to Explore Next

### 1. Understand the Code

**Start here**: `src/search/semantic_search.py`
```python
from src.search import SemanticSearch

search = SemanticSearch()
results = search.search("funny cat videos", limit=10)
```

**Key modules**:
- `src/data/` - Data loading and preprocessing
- `src/embeddings/` - Vector embeddings
- `src/vectordb/` - Qdrant integration
- `src/search/` - Semantic search

### 2. Try the Notebook

```powershell
# Install jupyter if needed
pip install jupyter

# Start notebook
jupyter notebook notebooks/exploratory_analysis.ipynb
```

Interactive exploration with visualizations!

### 3. Run Tests

```powershell
# Run all tests
pytest tests/

# Run with verbose output
pytest tests/ -v

# Run with coverage
pytest tests/ --cov=src
```

### 4. Experiment with Code

**Example: Custom search script**
```python
# my_search.py
from src.search import SemanticSearch

search = SemanticSearch()

# Basic search
results = search.search("gaming", limit=5)
for r in results:
    print(f"{r['title']} - {r['score']:.3f}")

# Search by category
results = search.search_by_category("tutorials", "Gaming", limit=5)

# Search popular videos
results = search.search_popular("music", min_views=1000000, limit=5)

# Find similar videos
results = search.find_similar_videos("video_id_here", limit=5)
```

### 5. Read Documentation

- **README.md** - Features and overview
- **ARCHITECTURE.md** - System design (highly recommended!)
- **ROADMAP.md** - Future plans (RAG, graphs, API, UI)
- **SETUP.md** - Detailed setup and troubleshooting

---

## 🔧 Common Issues & Solutions

### Issue: "Docker is not running"
**Solution**: Start Docker Desktop and wait for it to fully initialize

### Issue: "Port 6333 already in use"
**Solution**: 
```powershell
docker-compose down
docker-compose up -d
```

### Issue: "No CSV files found"
**Solution**: Download dataset and place in `data/raw/` folder

### Issue: "Out of memory during ingestion"
**Solution**: Edit `.env` and set `BATCH_SIZE=50`

### Issue: "Module not found"
**Solution**: 
```powershell
pip install -r requirements.txt --upgrade
```

### Issue: "Slow embedding generation"
**Solution**: 
- First run downloads model (~80MB) - be patient
- Use fewer CSV files for testing
- Consider using GPU if available

---

## 📊 Understanding the Results

### Search Scores
- **0.8 - 1.0**: Highly relevant (exact match)
- **0.6 - 0.8**: Very relevant (similar meaning)
- **0.4 - 0.6**: Somewhat relevant
- **< 0.4**: Less relevant

### Metadata Available
Each result includes:
- `title` - Video title
- `channel` - Channel name
- `category` - Category (Gaming, Music, etc.)
- `views`, `likes`, `dislikes` - Engagement metrics
- `tags` - Video tags
- `score` - Similarity score (0-1)

### Filtering Options
```python
# By category
search.search("query", filters={'category': 'Gaming'})

# By minimum views
search.search("query", filters={'min_views': 100000})

# By country (if available in data)
search.search("query", filters={'country': 'US'})

# Combined filters
search.search("query", filters={
    'category': 'Gaming',
    'min_views': 500000
})
```

---

## 🎯 Success Checklist

You're ready when:

- [x] Virtual environment activated (`(venv)` in prompt)
- [x] All packages installed (no errors)
- [x] Qdrant running (`docker ps` shows container)
- [x] Dashboard accessible (http://localhost:6333/dashboard)
- [x] Quick start passes all checks
- [x] Data ingested successfully
- [x] Search demo returns results

---

## 📈 Performance Tips

### Faster Ingestion
- Use fewer CSV files initially
- Increase batch size: `BATCH_SIZE=200` in `.env`
- Use GPU if available (auto-detected)

### Better Search Results
- Index more videos (use all CSV files)
- Adjust score threshold: `search.search(query, score_threshold=0.5)`
- Use specific queries (not too broad)

### Optimize for Scale
- Use incremental indexing for updates
- Enable caching for frequent queries
- Consider Qdrant cluster for production

---

## 🚀 What's Next?

### Immediate Next Steps
1. ✅ Complete POC setup (you're here!)
2. 🧪 Test with your own queries
3. 📊 Analyze search quality
4. 📝 Document findings

### Future Enhancements (See ROADMAP.md)
- **Phase 1**: RAG with LLM (natural language responses)
- **Phase 2**: Neo4j graph database (relationships)
- **Phase 3**: REST API with FastAPI
- **Phase 4**: React web UI
- **Phase 5**: Advanced ML features

### Extend the POC
- Add more data sources
- Implement custom ranking
- Create visualizations
- Build a simple UI
- Add real-time updates

---

## 📚 Learning Resources

### Understanding Vector Search
- [Qdrant Documentation](https://qdrant.tech/documentation/)
- [Sentence-Transformers Guide](https://www.sbert.net/)

### Semantic Search Concepts
- Vector embeddings
- Cosine similarity
- Approximate nearest neighbors (ANN)
- HNSW indexing

### Related Technologies
- RAG (Retrieval-Augmented Generation)
- Knowledge graphs
- Hybrid search
- Multi-modal embeddings

---

## 💡 Pro Tips

1. **Start Small**: Test with 1-2 CSV files first
2. **Use Samples**: Create samples for quick iteration
3. **Monitor Logs**: Watch for errors during ingestion
4. **Check Dashboard**: Use Qdrant dashboard to verify data
5. **Experiment**: Try different queries and filters
6. **Read Code**: Best way to understand the system
7. **Run Tests**: Ensure everything works after changes

---

## 🤝 Contributing Ideas

Want to enhance the POC? Consider:

- [ ] Add more embedding models
- [ ] Implement query suggestions
- [ ] Create visualization dashboard
- [ ] Add batch search API
- [ ] Implement result ranking
- [ ] Add export functionality
- [ ] Create performance benchmarks
- [ ] Write more tests

---

## 📞 Need Help?

### Check These First
1. **SETUP.md** - Detailed setup guide
2. **ARCHITECTURE.md** - System design
3. **PROJECT_STRUCTURE.txt** - File organization
4. Logs in terminal for error messages

### Debugging Steps
1. Verify Qdrant is running: `docker ps`
2. Check collection exists: Visit dashboard
3. Review logs for errors
4. Test with sample data first
5. Verify environment variables in `.env`

---

## 🎉 Congratulations!

You now have a working semantic search system for YouTube videos!

**What you've built**:
- ✅ Production-quality code structure
- ✅ Scalable vector database
- ✅ Semantic search capability
- ✅ Extensible architecture
- ✅ Complete documentation

**What you can do**:
- Search videos by meaning, not just keywords
- Find similar content
- Filter by metadata
- Analyze trends
- Build upon this foundation

---

## 📄 Quick Reference

### Key Commands
```powershell
# Activate environment
.\venv\Scripts\activate

# Start Qdrant
docker-compose up -d

# Verify setup
python scripts/quick_start.py

# Ingest data
python scripts/ingest_data.py

# Search demo
python scripts/search_demo.py

# Run tests
pytest

# Stop Qdrant
docker-compose down
```

### Key Files
- `src/search/semantic_search.py` - Main search interface
- `scripts/search_demo.py` - Example usage
- `.env` - Configuration
- `docker-compose.yml` - Qdrant setup

### Key URLs
- Qdrant Dashboard: http://localhost:6333/dashboard
- Kaggle Dataset: https://www.kaggle.com/datasets/datasnaek/youtube-new/data

---

**Ready to explore YouTube trends with AI?** 🚀

Start with: `python scripts/search_demo.py`

Happy searching! 🔍✨
