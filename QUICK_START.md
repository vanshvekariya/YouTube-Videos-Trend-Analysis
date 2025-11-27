# Quick Start Guide - Enhanced Ingestion

## 🚀 Quick Setup

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Start Qdrant (Docker)
```bash
docker run -p 6333:6333 qdrant/qdrant
```

### 3. Download Data
Download YouTube trending dataset from Kaggle:
- URL: https://www.kaggle.com/datasets/datasnaek/youtube-new/data
- Place CSV files in: `data/raw/`
- Example: `data/raw/CAvideos.csv`

### 4. Run Ingestion
```bash
python scripts/ingest_data.py
```

This will:
- ✅ Process data with enhanced processor
- ✅ Create SQL database with cleaned data
- ✅ Generate vector embeddings
- ✅ Index in Qdrant with full metadata

### 5. Test Enhanced Search
```bash
python scripts/test_enhanced_search.py
```

## 📊 Quick Examples

### Basic Search
```python
from src.embeddings import get_embedding_model
from src.vectordb import QdrantManager, VectorDBOperations

# Initialize
embedding_model = get_embedding_model()
qdrant_manager = QdrantManager()
db_ops = VectorDBOperations(qdrant_manager)

# Search
query_embedding = embedding_model.encode_single("funny cat videos")
results = db_ops.search(query_embedding, limit=5)

for result in results:
    print(f"{result['title']} - {result['views']:,} views")
```

### Search with Filters
```python
# Search gaming videos with high engagement
query_embedding = embedding_model.encode_single("gaming highlights")
results = db_ops.search(
    query_embedding,
    limit=10,
    filters={
        'category': 'Gaming',
        'min_views': 1000000,
        'min_likes': 50000,
        'country': 'CA'
    }
)
```

### Available Filters
```python
filters = {
    # Exact Match
    'category': 'Gaming',           # Category name
    'category_id': 20,              # Category ID
    'country': 'CA',                # Country code
    'language': 'English',          # Language
    'channel': 'ChannelName',       # Channel name
    
    # Range Filters
    'min_views': 1000000,           # Minimum views
    'max_views': 10000000,          # Maximum views
    'min_likes': 50000,             # Minimum likes
    'max_likes': 500000,            # Maximum likes
    'min_days_trending': 5,         # Min days trending
    'max_days_trending': 30,        # Max days trending
    
    # List Match
    'tags': ['gaming', 'fps']       # Match any tag
}
```

## 🔍 Common Use Cases

### 1. Find Popular Videos in Category
```python
query = "trending videos"
filters = {
    'category': 'Entertainment',
    'min_views': 500000,
    'min_days_trending': 3
}
results = db_ops.search(
    embedding_model.encode_single(query),
    limit=10,
    filters=filters
)
```

### 2. Find Viral Videos
```python
query = "viral content"
filters = {
    'min_likes': 100000,
    'min_days_trending': 7,
    'longest_consecutive_streak_days': 5
}
results = db_ops.search(
    embedding_model.encode_single(query),
    limit=10,
    filters=filters
)
```

### 3. Country-Specific Search
```python
query = "news and politics"
filters = {
    'country': 'CA',
    'category': 'News & Politics',
    'language': 'English'
}
results = db_ops.search(
    embedding_model.encode_single(query),
    limit=10,
    filters=filters
)
```

### 4. Channel Analysis
```python
query = "latest uploads"
filters = {
    'channel': 'SpecificChannelName',
    'min_views': 10000
}
results = db_ops.search(
    embedding_model.encode_single(query),
    limit=20,
    filters=filters
)
```

## 📈 Get Filter Statistics
```python
from src.vectordb import QdrantManager, VectorDBOperations

qdrant_manager = QdrantManager()
db_ops = VectorDBOperations(qdrant_manager)

# Get available filter values
stats = db_ops.get_filter_statistics()

print(f"Total documents: {stats['total_documents']}")
print(f"Categories: {stats['available_categories']}")
print(f"Countries: {stats['available_countries']}")
print(f"Languages: {stats['available_languages']}")
print(f"Total channels: {stats['total_channels']}")
```

## 🔧 Configuration

### Environment Variables (.env)
```bash
# Qdrant
QDRANT_HOST=localhost
QDRANT_PORT=6333
QDRANT_COLLECTION_NAME=youtube_trends

# SQL Database
SQL_DB_PATH=youtube_trends_canada.db
SQL_TABLE_NAME=videos

# Embeddings
USE_LOCAL_EMBEDDINGS=true
LOCAL_EMBEDDING_MODEL=all-MiniLM-L6-v2
BATCH_SIZE=100

# Vector Configuration
VECTOR_SIZE=384
```

## 🐛 Troubleshooting

### Issue: "Collection does not exist"
```bash
# Solution: Run ingestion first
python scripts/ingest_data.py
```

### Issue: "No CSV files found"
```bash
# Solution: Download and place CSV files
# 1. Download from Kaggle
# 2. Place in data/raw/
# 3. Verify: ls data/raw/*.csv
```

### Issue: "Qdrant connection failed"
```bash
# Solution: Start Qdrant
docker run -p 6333:6333 qdrant/qdrant

# Or check if already running
docker ps | grep qdrant
```

### Issue: Slow embedding generation
```python
# Solution: Increase batch size
# In .env:
BATCH_SIZE=200

# Or in code:
embeddings = processor.generate_embeddings(documents, batch_size=200)
```

## 📚 Documentation

- **Full Documentation**: [ENHANCED_INGESTION.md](ENHANCED_INGESTION.md)
- **Changes Summary**: [CHANGES_SUMMARY.md](CHANGES_SUMMARY.md)
- **Test Script**: [scripts/test_enhanced_search.py](scripts/test_enhanced_search.py)

## 🎯 Next Steps

1. ✅ Run ingestion: `python scripts/ingest_data.py`
2. ✅ Test search: `python scripts/test_enhanced_search.py`
3. ✅ Explore filters: Try different filter combinations
4. ✅ Build your app: Use the search API in your application
5. ✅ Read docs: Check [ENHANCED_INGESTION.md](ENHANCED_INGESTION.md) for advanced usage

## 💡 Tips

- **Start Simple**: Begin with basic search, then add filters
- **Use Statistics**: Call `get_filter_statistics()` to see available values
- **Combine Filters**: Multiple filters work together (AND logic)
- **Test Incrementally**: Test each filter type individually first
- **Check Metadata**: All fields are available in search results

## 🚀 Performance Tips

1. **Batch Processing**: Use larger batch sizes for faster ingestion
2. **GPU Acceleration**: Use GPU-enabled embedding models if available
3. **Filter Early**: Apply filters to reduce search space
4. **Limit Results**: Use appropriate `limit` parameter
5. **Cache Embeddings**: Reuse query embeddings for similar searches

## 📞 Support

For issues or questions:
1. Check [ENHANCED_INGESTION.md](ENHANCED_INGESTION.md)
2. Review [CHANGES_SUMMARY.md](CHANGES_SUMMARY.md)
3. Run test script: `python scripts/test_enhanced_search.py`
4. Check code examples in this guide

Happy searching! 🎉
