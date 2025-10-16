# Quick Start Guide

Get up and running in 5 minutes!

## Prerequisites Check

- [ ] Python 3.9+ installed
- [ ] Docker Desktop installed and running
- [ ] 2GB free disk space

## Setup (5 minutes)

### 1. Install Dependencies

```powershell
# Navigate to project
cd "path\yotube-trends-poc-v1"

# Create and activate virtual environment
python -m venv venv
.\venv\Scripts\activate

# Install packages
pip install -r requirements.txt
```

### 2. Configure Environment

```powershell
# Copy environment file
copy .env.example .env

# No changes needed for default setup (uses local embeddings)
```

### 3. Start Qdrant

```powershell
# Start Qdrant vector database
docker-compose up -d

# Verify it's running
docker ps
```

**Check**: Open http://localhost:6333/dashboard in your browser

### 4. Verify Setup

```powershell
# Run quick start verification
python scripts/quick_start.py
```

This will check:
- ✓ All dependencies installed
- ✓ Qdrant is running
- ✓ Embeddings work
- ✓ Run a mini demo

## Get Data

### Option A: Use Sample Data (Quick Test)

The quick_start script already tested with sample data. You can modify scripts to use samples.

### Option B: Full Dataset (Recommended)

1. Download from: https://www.kaggle.com/datasets/datasnaek/youtube-new/data
2. Extract CSV files
3. Place in `data/raw/` folder
4. Run ingestion:

```powershell
python scripts/ingest_data.py
```

**Time**: 5-15 minutes depending on data size

## Run Search Demo

```powershell
python scripts/search_demo.py
```

Choose:
- **Option 1**: Pre-defined demo queries
- **Option 2**: Interactive search mode

## Example Queries

Try these searches:
- "funny cat videos"
- "gaming tutorials"
- "cooking recipes"
- "music concerts"
- "technology reviews"

## What's Next?

### Explore the Code
```
src/
├── data/          # Data loading and preprocessing
├── embeddings/    # Vector embeddings
├── vectordb/      # Qdrant integration
└── search/        # Semantic search
```

### Try the Notebook
```powershell
jupyter notebook notebooks/exploratory_analysis.ipynb
```

### Run Tests
```powershell
pytest tests/
```

### Read Documentation
- `README.md` - Project overview
- `SETUP.md` - Detailed setup guide
- `ARCHITECTURE.md` - System design
- `ROADMAP.md` - Future plans

## Troubleshooting

### Qdrant not starting?
```powershell
docker-compose down
docker-compose up -d
```

### Import errors?
```powershell
pip install -r requirements.txt --upgrade
```

### Out of memory?
Edit `.env` and set:
```
BATCH_SIZE=50
```

## Key Commands

```powershell
# Start Qdrant
docker-compose up -d

# Stop Qdrant
docker-compose down

# Activate environment
.\venv\Scripts\activate

# Deactivate environment
deactivate

# Ingest data
python scripts/ingest_data.py

# Search demo
python scripts/search_demo.py

# Quick verification
python scripts/quick_start.py

# Run tests
pytest
```

## Project Structure

```
yotube-trends-poc-v1/
├── src/                    # Source code
├── scripts/                # Executable scripts
├── data/raw/              # Place CSV files here
├── tests/                  # Unit tests
├── notebooks/              # Jupyter notebooks
├── docker-compose.yml      # Qdrant setup
├── requirements.txt        # Dependencies
└── .env                    # Configuration
```

## Success Indicators

You're ready when:
- ✅ `docker ps` shows qdrant running
- ✅ `python scripts/quick_start.py` passes all checks
- ✅ `python scripts/search_demo.py` returns results
- ✅ http://localhost:6333/dashboard is accessible

## Getting Help

1. Check logs for errors
2. Verify Qdrant is running: `docker ps`
3. Review `SETUP.md` for detailed instructions
4. Check `ARCHITECTURE.md` for system design

---

**You're all set!** 🚀

Start searching YouTube trends with semantic AI!
