# Setup Guide - YouTube Trends Explorer POC

This guide will walk you through setting up the YouTube Trends Explorer POC from scratch.

## Prerequisites

- **Python 3.9+** installed
- **Docker Desktop** installed and running
- **Git** (optional, for version control)
- At least **2GB free disk space**

## Step-by-Step Setup

### 1. Navigate to Project Directory

```powershell
cd "path\yotube-trends-poc-v1"
```

### 2. Create Virtual Environment

```powershell
# Create virtual environment
python -m venv venv

# Activate it
.\venv\Scripts\activate

# You should see (venv) in your prompt
```

### 3. Install Dependencies

```powershell
# Upgrade pip first
python -m pip install --upgrade pip

# Install all requirements
pip install -r requirements.txt
```

This will install:
- Qdrant client for vector database
- Sentence-transformers for embeddings
- Pandas for data processing
- FastAPI for future API development
- And other dependencies

### 4. Configure Environment

```powershell
# Copy the example environment file
copy .env.example .env

# Edit .env if needed (optional)
notepad .env
```

**Default configuration uses local embeddings (no API key needed)**. If you want to use OpenAI embeddings instead, set:
```
USE_LOCAL_EMBEDDINGS=false
OPENAI_API_KEY=your_key_here
```

### 5. Start Qdrant Vector Database

```powershell
# Start Qdrant using Docker Compose
docker-compose up -d

# Verify it's running
docker ps
```

You should see a container named `qdrant` running.

**Verify Qdrant Dashboard**: Open browser and go to http://localhost:6333/dashboard

### 6. Download YouTube Dataset

1. Go to: https://www.kaggle.com/datasets/datasnaek/youtube-new/data
2. Download the dataset (you'll need a Kaggle account)
3. Extract the CSV files
4. Place them in the `data/raw/` directory

The dataset includes files like:
- `USvideos.csv`
- `GBvideos.csv`
- `CAvideos.csv`
- etc.

**You can start with just one or two CSV files for the POC.**

### 7. Ingest Data and Create Embeddings

```powershell
# Run the ingestion pipeline
python scripts/ingest_data.py
```

This will:
1. Load CSV files from `data/raw/`
2. Preprocess and clean the data
3. Generate embeddings using sentence-transformers
4. Index everything in Qdrant

**Note**: This may take 5-15 minutes depending on:
- Number of CSV files
- Your CPU/GPU
- Number of videos

**For faster testing**, you can modify the script to use a sample:
```python
# In scripts/ingest_data.py, after loading data:
df = df.sample(n=1000, random_state=42)  # Use only 1000 videos
```

### 8. Test Semantic Search

```powershell
# Run the interactive search demo
python scripts/search_demo.py
```

Choose option 1 for demo queries or option 2 for interactive search.

## Verification Checklist

- [ ] Virtual environment activated
- [ ] All packages installed without errors
- [ ] Qdrant running (check http://localhost:6333/dashboard)
- [ ] CSV files in `data/raw/`
- [ ] Data ingested successfully
- [ ] Search demo works

## Common Issues & Solutions

### Issue: Docker not running
**Solution**: Start Docker Desktop and wait for it to fully start.

### Issue: Port 6333 already in use
**Solution**: 
```powershell
# Stop any existing Qdrant containers
docker-compose down

# Or change port in docker-compose.yml and .env
```

### Issue: Out of memory during embedding generation
**Solution**: 
- Reduce batch size in `.env`: `BATCH_SIZE=50`
- Use fewer CSV files
- Use a sample of data

### Issue: Sentence-transformers download slow
**Solution**: The first run downloads the model (~80MB). Be patient or use a different mirror.

### Issue: CSV encoding errors
**Solution**: The loader handles most encoding issues, but if you see errors, try:
- Using only US/GB CSV files (better encoding)
- Manually checking CSV file encoding

## Project Structure Overview

```
yotube-trends-poc-v1/
├── src/                    # Source code
│   ├── config/            # Configuration management
│   ├── data/              # Data loading and preprocessing
│   ├── embeddings/        # Embedding models
│   ├── vectordb/          # Qdrant integration
│   └── search/            # Semantic search
├── scripts/               # Executable scripts
│   ├── ingest_data.py    # Main ingestion pipeline
│   └── search_demo.py    # Search demo
├── data/                  # Data directory
│   ├── raw/              # Place CSV files here
│   └── processed/        # Processed data (auto-created)
├── tests/                 # Unit tests
├── notebooks/             # Jupyter notebooks
├── docker-compose.yml     # Qdrant setup
├── requirements.txt       # Python dependencies
└── .env                   # Configuration (create from .env.example)
```

## Next Steps

After successful setup:

1. **Explore the code**: Check out `src/` modules
2. **Try the notebook**: Open `notebooks/exploratory_analysis.ipynb`
3. **Run tests**: `pytest tests/`
4. **Experiment with queries**: Modify `scripts/search_demo.py`
5. **Add more data**: Include more CSV files from Kaggle

## Performance Tips

### For faster ingestion:
- Use GPU if available (sentence-transformers will auto-detect)
- Increase batch size: `BATCH_SIZE=200`
- Use smaller embedding model (already using the smallest good one)

### For better search results:
- Index more videos (use all CSV files)
- Try different embedding models in `.env`
- Adjust similarity thresholds

## Getting Help

If you encounter issues:

1. Check logs for error messages
2. Verify Qdrant is running: `docker ps`
3. Check collection exists: Visit http://localhost:6333/dashboard
4. Review configuration in `.env`

## Cleanup

To stop and remove everything:

```powershell
# Stop Qdrant
docker-compose down

# Remove Qdrant data (optional)
Remove-Item -Recurse -Force qdrant_storage

# Deactivate virtual environment
deactivate
```

---

**You're all set!** 🚀

The POC demonstrates:
✅ Vector database integration with Qdrant
✅ Semantic embeddings generation
✅ Similarity-based search
✅ Metadata filtering
✅ Scalable architecture

Ready for next phase: RAG, graph integration, and visualizations!
