# Enhanced Data Ingestion with Unified Processing

## Overview

The data ingestion pipeline has been refactored to use the `EnhancedYouTubeDataProcessor` for consistent data processing across both SQL and Vector databases. This ensures that the same cleaned, processed data is used for both storage systems, eliminating inconsistencies.

## Key Improvements

### 1. **Unified Data Processing**
- Single source of truth: `enhanced_processor.py` handles all data processing
- Same cleaning, transformation, and feature engineering for both SQL and Vector DB
- Consistent metadata across both storage systems

### 2. **Optimized Vector Database Metadata**

The vector database now stores comprehensive metadata for each document, enabling powerful filtering:

#### Core Identifiers
- `video_id`: Unique video identifier
- `title`: Video title
- `channel`: Channel name

#### Category Information
- `category`: Category name (e.g., "Gaming", "Music")
- `category_id`: Numeric category ID

#### Geographic & Language
- `country`: Country code (e.g., "CA", "US")
- `language`: Detected language (e.g., "English", "French")

#### Engagement Metrics
- `views`: Total view count
- `likes`: Total like count
- `comment_count`: Total comment count

#### Temporal Features
- `publish_time`: Original publish timestamp
- `first_trend_date`: First date video trended
- `last_trend_date`: Last date video trended
- `days_trending_unique`: Total unique days trending
- `longest_consecutive_streak_days`: Longest consecutive trending streak

#### Content
- `tags`: List of video tags (for filtering)
- `description`: Video description (truncated to 500 chars)
- `text`: Searchable text used for embeddings

### 3. **Advanced Filtering Capabilities**

The vector database now supports comprehensive filtering:

```python
# Example: Search with multiple filters
results = db_ops.search(
    query_embedding,
    limit=10,
    filters={
        'category': 'Gaming',           # Exact category match
        'country': 'CA',                # Country filter
        'language': 'English',          # Language filter
        'min_views': 1000000,           # Minimum views
        'max_views': 10000000,          # Maximum views
        'min_likes': 50000,             # Minimum likes
        'min_days_trending': 5,         # Minimum days trending
        'channel': 'ChannelName',       # Specific channel
        'tags': ['gaming', 'fps']       # Tag matching
    }
)
```

#### Available Filter Types

| Filter | Type | Description |
|--------|------|-------------|
| `category` | Exact Match | Filter by category name |
| `category_id` | Exact Match | Filter by category ID |
| `country` | Exact Match | Filter by country code |
| `language` | Exact Match | Filter by language |
| `channel` | Exact Match | Filter by channel name |
| `min_views` | Range | Minimum view count |
| `max_views` | Range | Maximum view count |
| `min_likes` | Range | Minimum like count |
| `max_likes` | Range | Maximum like count |
| `min_days_trending` | Range | Minimum days trending |
| `max_days_trending` | Range | Maximum days trending |
| `tags` | List Match | Match any tag in list |

## Usage

### 1. Data Ingestion

Run the enhanced ingestion script:

```bash
python scripts/ingest_data.py
```

This will:
1. Load CSV data from `data/raw/`
2. Process data using `EnhancedYouTubeDataProcessor`
3. Create SQL database with cleaned data
4. Generate vector embeddings
5. Index in Qdrant with full metadata

### 2. Testing Enhanced Search

Run the test script to see filtering in action:

```bash
python scripts/test_enhanced_search.py
```

This demonstrates:
- Basic semantic search
- Category filtering
- View count filtering
- Multiple simultaneous filters
- Country/language filtering
- Engagement metrics filtering

### 3. Programmatic Usage

```python
from src.data.enhanced_processor import EnhancedYouTubeDataProcessor
from src.embeddings import get_embedding_model
from src.vectordb import QdrantManager, VectorDBOperations

# Initialize
embedding_model = get_embedding_model()
processor = EnhancedYouTubeDataProcessor(
    db_path="youtube_trends.db",
    embedding_model=embedding_model
)

# Process data
sql_df, vector_documents, embeddings = processor.process_csv_file(
    csv_path="data/raw/CAvideos.csv",
    country="CA",
    create_sql=True,
    prepare_vector=True,
    generate_embeddings=True
)

# Index in Qdrant
qdrant_manager = QdrantManager()
qdrant_manager.create_collection(
    vector_size=embedding_model.get_dimension(),
    recreate=True
)

db_ops = VectorDBOperations(qdrant_manager)
db_ops.index_documents(vector_documents, embeddings)

# Search with filters
query_embedding = embedding_model.encode_single("gaming videos")
results = db_ops.search(
    query_embedding,
    limit=10,
    filters={'category': 'Gaming', 'min_views': 100000}
)
```

## Architecture

### Data Flow

```
CSV Files
    ↓
EnhancedYouTubeDataProcessor
    ├── Data Cleaning & Transformation
    ├── Language Detection
    ├── Category Mapping
    ├── Temporal Feature Engineering
    └── Searchable Text Generation
    ↓
    ├─→ SQL Database (SQLite)
    │   └── Structured data for analytics
    │
    └─→ Vector Database (Qdrant)
        ├── Embeddings (semantic search)
        └── Metadata (filtering & ranking)
```

### Key Components

1. **EnhancedYouTubeDataProcessor** (`src/data/enhanced_processor.py`)
   - Core data processing logic
   - Handles both SQL and vector preparation
   - Generates embeddings using provided model

2. **VectorDBOperations** (`src/vectordb/operations.py`)
   - Enhanced filtering support
   - Metadata-rich search results
   - Filter statistics and utilities

3. **Ingestion Script** (`scripts/ingest_data.py`)
   - Orchestrates the entire pipeline
   - Uses enhanced processor for consistency
   - Indexes data in both databases

## Benefits

### 1. **Data Consistency**
- Same processing pipeline for SQL and Vector DB
- No discrepancies between storage systems
- Single source of truth for data transformations

### 2. **Optimized Vector Search**
- Rich metadata enables precise filtering
- Combine semantic search with structured filters
- Better relevance through multi-dimensional filtering

### 3. **Scalability**
- Batch processing for embeddings
- Efficient indexing with progress tracking
- Support for multiple CSV files

### 4. **Maintainability**
- Single processor class to maintain
- Clear separation of concerns
- Easy to extend with new features

## Migration Notes

### Changes from Previous Version

1. **Removed**: Old `DataPreprocessor` usage in ingestion
2. **Added**: `EnhancedYouTubeDataProcessor` with embedding support
3. **Enhanced**: Vector DB operations with comprehensive filters
4. **Improved**: Metadata structure for better filtering

### Backward Compatibility

- SQL database schema remains unchanged
- Existing SQL queries continue to work
- Vector DB collection needs to be recreated with new metadata

### Re-indexing Required

If you have existing data, you need to re-run the ingestion:

```bash
# This will recreate both SQL and Vector databases
python scripts/ingest_data.py
```

## Performance Considerations

### Embedding Generation
- Uses batch processing (default: 100 documents/batch)
- Shows progress bar for long operations
- Configurable batch size via settings

### Vector Indexing
- Batch uploads to Qdrant (default: 100 points/batch)
- Efficient for large datasets
- Progress tracking with tqdm

### Filtering Performance
- Qdrant filters are highly optimized
- Indexed metadata fields for fast filtering
- Combine multiple filters without performance penalty

## Future Enhancements

Potential improvements:
- [ ] Support for multiple CSV files in single ingestion
- [ ] Incremental updates (add new videos without full re-index)
- [ ] Custom embedding models per use case
- [ ] Advanced tag filtering (AND/OR logic)
- [ ] Date range filtering for temporal queries
- [ ] Hybrid search combining SQL and Vector results

## Troubleshooting

### Issue: "Embedding model not initialized"
**Solution**: Pass embedding model to processor constructor:
```python
processor = EnhancedYouTubeDataProcessor(embedding_model=embedding_model)
```

### Issue: "Collection does not exist"
**Solution**: Run ingestion script first:
```bash
python scripts/ingest_data.py
```

### Issue: "No CSV files found"
**Solution**: Download dataset and place in `data/raw/`:
- Dataset: https://www.kaggle.com/datasets/datasnaek/youtube-new/data
- Expected format: `CAvideos.csv`, `USvideos.csv`, etc.

### Issue: Slow embedding generation
**Solution**: Adjust batch size in settings or use GPU-enabled model:
```python
# In .env or settings
BATCH_SIZE=200  # Increase for faster processing
```

## Support

For issues or questions:
1. Check this documentation
2. Review test script: `scripts/test_enhanced_search.py`
3. Examine processor code: `src/data/enhanced_processor.py`
4. Check vector operations: `src/vectordb/operations.py`
