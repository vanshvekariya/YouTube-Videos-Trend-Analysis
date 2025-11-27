# YouTube Trends Explorer - POC

A proof-of-concept for building a semantic search system over YouTube trending videos using vector embeddings and Qdrant vector database.

## 🎯 Project Overview

This POC demonstrates:
- **Vector Database Integration**: Using Qdrant for efficient similarity search
- **Semantic Search**: Find videos based on meaning, not just keywords
- **Data Pipeline**: Ingest and process YouTube trending data from Kaggle
- **Embeddings**: Generate vector representations using sentence-transformers or OpenAI
- **Enhanced Metadata Filtering**: Rich filtering capabilities with consistent SQL and Vector DB data

> 📖 **New**: See [ENHANCED_INGESTION.md](ENHANCED_INGESTION.md) for details on the unified data processing pipeline with advanced filtering capabilities.

## 📁 Project Structure

```
yotube-trends-poc-v1/
├── src/
│   ├── __init__.py
│   ├── config/
│   │   ├── __init__.py
│   │   └── settings.py          # Configuration management
│   ├── data/
│   │   ├── __init__.py
│   │   ├── loader.py             # Data loading utilities
│   │   └── preprocessor.py      # Data preprocessing
│   ├── embeddings/
│   │   ├── __init__.py
│   │   ├── base.py               # Base embedding interface
│   │   ├── local_embeddings.py  # Sentence-transformers
│   │   └── openai_embeddings.py # OpenAI embeddings
│   ├── vectordb/
│   │   ├── __init__.py
│   │   ├── client.py             # Qdrant client wrapper
│   │   └── operations.py         # CRUD operations
│   └── search/
│       ├── __init__.py
│       └── semantic_search.py    # Search functionality
├── scripts/
│   ├── ingest_data.py            # Data ingestion script
│   ├── create_embeddings.py      # Generate embeddings
│   └── search_demo.py            # Demo search queries
├── notebooks/
│   └── exploratory_analysis.ipynb
├── tests/
│   ├── __init__.py
│   ├── test_embeddings.py
│   └── test_vectordb.py
├── data/
│   ├── raw/                      # Place Kaggle CSV files here
│   └── processed/                # Processed data
├── docker-compose.yml
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md
```

## 🚀 Quick Start

### 1. Prerequisites

- Python 3.9+
- Docker & Docker Compose
- Kaggle YouTube dataset (download from [here](https://www.kaggle.com/datasets/datasnaek/youtube-new/data))

### 2. Setup

```bash
# Clone or navigate to project directory
cd yotube-trends-poc-v1

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Copy environment file
copy .env.example .env

# Edit .env with your configuration
```

### 3. Start Qdrant

```bash
# Start Qdrant using Docker Compose
docker-compose up -d

# Verify Qdrant is running
# Open browser: http://localhost:6333/dashboard
```

### 4. Prepare Data

1. Download the YouTube dataset from Kaggle
2. Place CSV files in `data/raw/` directory
3. Run data ingestion:

```bash
python scripts/ingest_data.py
```

### 5. Create Embeddings & Index

```bash
# Generate embeddings and upload to Qdrant
python scripts/create_embeddings.py
```

### 6. Run Semantic Search Demo

```bash
# Try some search queries
python scripts/search_demo.py
```

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

### Current POC Features
- ✅ Data ingestion from CSV files
- ✅ Text preprocessing and cleaning
- ✅ Vector embeddings generation (local or OpenAI)
- ✅ Qdrant vector database integration
- ✅ Semantic search functionality
- ✅ Similarity-based video recommendations

### Future Enhancements (Post-POC)
- 🔄 RAG (Retrieval-Augmented Generation) with LLM
- 🔄 Hybrid search (vector + keyword filtering)
- 🔄 Neo4j graph database integration
- 🔄 Network analytics and graph insights
- 🔄 Interactive visualizations
- 🔄 REST API with FastAPI
- 🔄 Web UI dashboard

## 🛠️ Technology Stack

- **Vector Database**: Qdrant
- **Embeddings**: Sentence-Transformers (all-MiniLM-L6-v2) or OpenAI
- **Data Processing**: Pandas, NumPy
- **API Framework**: FastAPI (for future use)
- **Containerization**: Docker

## 📝 Usage Examples

### Basic Semantic Search

```python
from src.search.semantic_search import SemanticSearch

# Initialize search
search = SemanticSearch()

# Search for videos
results = search.search(
    query="funny cat videos",
    limit=10
)

for result in results:
    print(f"Title: {result['title']}")
    print(f"Channel: {result['channel']}")
    print(f"Score: {result['score']}")
    print("---")
```

### Filter by Metadata

```python
# Search with filters
results = search.search(
    query="gaming tutorials",
    limit=10,
    filters={
        "category": "Gaming",
        "min_views": 100000
    }
)
```

## 🧪 Testing

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src tests/
```

## 📈 Performance Considerations

- **Batch Processing**: Data is processed in batches for memory efficiency
- **Embedding Model**: Using `all-MiniLM-L6-v2` (384 dimensions) for speed/quality balance
- **Indexing**: Qdrant uses HNSW algorithm for fast approximate nearest neighbor search

## 🤝 Contributing

This is a POC project. Feel free to experiment and extend functionality.

## 📄 License

MIT License

## 🔗 Resources

- [Qdrant Documentation](https://qdrant.tech/documentation/)
- [Sentence-Transformers](https://www.sbert.net/)
- [YouTube Dataset](https://www.kaggle.com/datasets/datasnaek/youtube-new/data)
