# Vector Agent - Complete Guide

## Overview

The Vector Agent is a production-ready semantic search system for YouTube video content. It provides advanced search capabilities using vector embeddings and similarity matching.

## Features

### 1. **Semantic Search**
- Natural language query understanding
- Content-based similarity matching
- Fuzzy matching and concept search
- Multi-field search (title, description, tags, channel)

### 2. **Filtered Search**
- Category filtering
- View count ranges (min/max)
- Country filtering
- Hybrid semantic + metadata search

### 3. **Content Recommendations**
- Find similar videos by ID
- Content-based recommendations
- Similarity scoring

### 4. **Natural Language Responses**
- LLM-powered response generation
- Contextual answers
- Fallback to simple responses

## Architecture

```
VectorAgent
├── Vector Database (Qdrant)
│   ├── Collection management
│   └── Similarity search
├── Embedding Model (Sentence Transformers)
│   ├── Text vectorization
│   └── Query encoding
├── DB Operations
│   ├── Search
│   ├── Filtering
│   └── Document retrieval
└── LLM (Optional)
    ├── Response generation
    └── Natural language synthesis
```

## API Reference

### Core Methods

#### `process_query(query: str, **kwargs) -> Dict[str, Any]`

Main entry point for semantic search.

**Parameters:**
- `query` (str): Natural language search query
- `limit` (int, optional): Number of results (default: 5)
- `score_threshold` (float, optional): Minimum similarity score 0-1 (default: 0.3)
- `filters` (dict, optional): Metadata filters
- `include_metadata` (bool, optional): Include full metadata in response

**Returns:**
```python
{
    'success': bool,
    'data': {
        'answer': str,  # Natural language answer
        'results': List[Dict],  # Search results
        'query_type': 'vector',
        'source': 'semantic_search'
    },
    'metadata': {
        'query': str,
        'limit': int,
        'num_results': int,
        'avg_score': float,
        'model': str
    }
}
```

**Example:**
```python
result = agent.process_query(
    "funny cat videos",
    limit=10,
    filters={'category': 'Entertainment', 'min_views': 100000}
)
```

---

#### `search_videos(query: str, limit: int = 10, score_threshold: float = None, filters: Dict = None) -> List[Dict]`

Perform semantic search and return raw results.

**Example:**
```python
results = agent.search_videos(
    "gaming tutorials",
    limit=5,
    score_threshold=0.5,
    filters={'category': 'Gaming'}
)
```

---

#### `find_similar_videos(video_id: str, limit: int = 10, exclude_self: bool = True) -> Dict[str, Any]`

Find videos similar to a given video.

**Example:**
```python
similar = agent.find_similar_videos("abc123xyz", limit=5)
```

---

#### `search_by_category(query: str, category: str, limit: int = 10) -> Dict[str, Any]`

Search within a specific category.

**Categories:**
- Film & Animation
- Music
- Gaming
- Education
- Science & Technology
- Entertainment
- Comedy
- Sports
- News & Politics
- Howto & Style
- People & Blogs
- Pets & Animals
- Travel & Events
- Autos & Vehicles
- Nonprofits & Activism

**Example:**
```python
result = agent.search_by_category("tutorials", "Education", limit=10)
```

---

#### `search_popular_videos(query: str, min_views: int = 100000, limit: int = 10) -> Dict[str, Any]`

Search for popular videos matching the query.

**Example:**
```python
result = agent.search_popular_videos("music videos", min_views=1000000)
```

---

#### `hybrid_search(query: str, category: str = None, min_views: int = None, max_views: int = None, limit: int = 10) -> Dict[str, Any]`

Perform hybrid search combining semantic search with multiple filters.

**Example:**
```python
result = agent.hybrid_search(
    "funny videos",
    category="Comedy",
    min_views=50000,
    max_views=500000,
    limit=10
)
```

---

### Utility Methods

#### `get_capabilities() -> Dict[str, Any]`

Get agent capabilities and configuration.

#### `get_stats() -> Dict[str, Any]`

Get vector database statistics.

#### `health_check() -> Dict[str, Any]`

Perform health check on all components.

---

## Usage Examples

### Basic Search

```python
from src.agents import VectorAgent

# Initialize agent
agent = VectorAgent()

# Simple search
result = agent.process_query("funny cat videos")
print(result['data']['answer'])

# View results
for video in result['data']['results']:
    print(f"{video['rank']}. {video['title']} ({video['score']:.2%} match)")
    print(f"   Channel: {video['channel']}")
    print(f"   Views: {video['views']:,}")
```

### Filtered Search

```python
# Search in specific category
result = agent.search_by_category(
    query="machine learning tutorials",
    category="Education",
    limit=10
)

# Search popular videos
result = agent.search_popular_videos(
    query="gaming highlights",
    min_views=1000000,
    limit=5
)

# Complex hybrid search
result = agent.hybrid_search(
    query="cooking recipes",
    category="Howto & Style",
    min_views=10000,
    max_views=1000000,
    limit=20
)
```

### Find Similar Videos

```python
# Find videos similar to a specific video
result = agent.find_similar_videos(
    video_id="dQw4w9WgXcQ",
    limit=10,
    exclude_self=True
)

print(f"Videos similar to: {result['data']['reference_video']['title']}")
for video in result['data']['similar_videos']:
    print(f"- {video['title']} ({video['score']:.2%} similarity)")
```

### Advanced Usage

```python
# Custom parameters
result = agent.process_query(
    query="artificial intelligence",
    limit=20,
    score_threshold=0.6,  # Higher threshold for better matches
    filters={
        'category': 'Science & Technology',
        'min_views': 50000
    },
    include_metadata=True  # Include full metadata
)

# Access detailed results
for video in result['data']['results']:
    print(f"Title: {video['title']}")
    print(f"Relevance: {video['score']:.2%}")
    print(f"Category: {video['category']}")
    print(f"Engagement: {video['likes']:,} likes, {video['views']:,} views")
    if 'metadata' in video:
        print(f"Tags: {', '.join(video['metadata']['tags'][:5])}")
```

---

## Filter Options

### Available Filters

```python
filters = {
    'category': str,        # Category name (e.g., "Gaming", "Music")
    'min_views': int,       # Minimum view count
    'max_views': int,       # Maximum view count
    'country': str,         # Country code (e.g., "CA", "US")
}
```

### Filter Examples

```python
# Category only
filters = {'category': 'Gaming'}

# View range
filters = {'min_views': 100000, 'max_views': 1000000}

# Combined filters
filters = {
    'category': 'Music',
    'min_views': 500000,
    'country': 'CA'
}
```

---

## Response Format

### Success Response

```python
{
    'success': True,
    'data': {
        'answer': "Found 5 videos matching 'funny cats'...",
        'results': [
            {
                'rank': 1,
                'score': 0.8542,
                'video_id': 'abc123',
                'title': 'Funny Cat Compilation 2024',
                'channel': 'Cat Videos Daily',
                'category': 'Entertainment',
                'views': 1500000,
                'likes': 45000,
                'tags': ['cats', 'funny', 'compilation', 'pets', 'animals']
            },
            # ... more results
        ],
        'query_type': 'vector',
        'source': 'semantic_search'
    },
    'metadata': {
        'query': 'funny cats',
        'limit': 5,
        'score_threshold': 0.3,
        'num_results': 5,
        'avg_score': 0.7234,
        'model': 'anthropic/claude-3-haiku',
        'filters_applied': False
    }
}
```

### Error Response

```python
{
    'success': False,
    'error': 'Vector search failed: Connection timeout',
    'data': None,
    'metadata': {}
}
```

---

## Configuration

### Environment Variables

```bash
# Required
OPENAI_API_KEY=your_api_key_here

# Optional
QDRANT_HOST=localhost
QDRANT_PORT=6333
QDRANT_COLLECTION_NAME=youtube_videos
VECTOR_SIZE=384
LLM_MODEL=anthropic/claude-3-haiku
```

### Initialization Options

```python
agent = VectorAgent(
    api_key="your_key",           # Override env API key
    model="gpt-4",                 # Override LLM model
    default_limit=10,              # Default result count
    min_score_threshold=0.4        # Minimum similarity score
)
```

---

## Best Practices

### 1. Query Optimization

```python
# ✅ Good: Specific, descriptive queries
agent.process_query("machine learning tutorial for beginners")

# ❌ Avoid: Too generic
agent.process_query("video")

# ✅ Good: Use filters for precision
agent.process_query(
    "cooking",
    filters={'category': 'Howto & Style', 'min_views': 10000}
)
```

### 2. Result Limits

```python
# For quick searches
agent.process_query("query", limit=5)

# For comprehensive results
agent.process_query("query", limit=50)

# Balance performance vs completeness
agent.process_query("query", limit=20)  # Recommended
```

### 3. Score Thresholds

```python
# Strict matching (high quality)
agent.process_query("query", score_threshold=0.7)

# Balanced (recommended)
agent.process_query("query", score_threshold=0.4)

# Loose matching (more results)
agent.process_query("query", score_threshold=0.2)
```

### 4. Error Handling

```python
try:
    result = agent.process_query("your query")
    
    if result['success']:
        # Process results
        for video in result['data']['results']:
            print(video['title'])
    else:
        # Handle error
        print(f"Error: {result['error']}")
        
except Exception as e:
    logger.error(f"Unexpected error: {e}")
```

---

## Performance Tips

1. **Batch Searches**: For multiple queries, reuse the same agent instance
2. **Appropriate Limits**: Don't request more results than needed
3. **Use Filters**: Narrow down search space with metadata filters
4. **Score Thresholds**: Set appropriate thresholds to reduce irrelevant results
5. **Connection Pooling**: Agent maintains persistent connections to Qdrant

---

## Troubleshooting

### Common Issues

#### 1. No Results Found

```python
# Check if collection exists
stats = agent.get_stats()
print(f"Total videos: {stats['total_videos']}")

# Lower score threshold
result = agent.process_query("query", score_threshold=0.1)

# Remove filters
result = agent.process_query("query", filters=None)
```

#### 2. Connection Errors

```python
# Check health
health = agent.health_check()
print(health)

# Verify Qdrant is running
# docker ps | grep qdrant
```

#### 3. Slow Searches

```python
# Reduce limit
result = agent.process_query("query", limit=5)

# Use more specific queries
result = agent.process_query("specific detailed query")
```

---

## Monitoring

### Get Statistics

```python
stats = agent.get_stats()
print(f"Collection: {stats['collection_name']}")
print(f"Total videos: {stats['total_videos']}")
print(f"Status: {stats['status']}")
print(f"Embedding dimension: {stats['embedding_dimension']}")
```

### Health Check

```python
health = agent.health_check()
print(f"Agent status: {health['agent']}")
print(f"Vector DB: {health['components']['vector_db']}")
print(f"Embeddings: {health['components']['embedding_model']}")
print(f"LLM: {health['components']['llm']}")
```

### Capabilities

```python
caps = agent.get_capabilities()
print(f"Agent: {caps['name']}")
print(f"Type: {caps['type']}")
print(f"Features: {', '.join(caps['capabilities'])}")
```

---

## Integration Examples

### With Flask API

```python
from flask import Flask, request, jsonify
from src.agents import VectorAgent

app = Flask(__name__)
agent = VectorAgent()

@app.route('/search', methods=['POST'])
def search():
    data = request.json
    result = agent.process_query(
        query=data['query'],
        limit=data.get('limit', 10),
        filters=data.get('filters')
    )
    return jsonify(result)

@app.route('/similar/<video_id>', methods=['GET'])
def similar(video_id):
    limit = request.args.get('limit', 10, type=int)
    result = agent.find_similar_videos(video_id, limit=limit)
    return jsonify(result)
```

### With Streamlit

```python
import streamlit as st
from src.agents import VectorAgent

agent = VectorAgent()

st.title("YouTube Video Search")

query = st.text_input("Search for videos:")
category = st.selectbox("Category", ["All", "Gaming", "Music", "Education"])
min_views = st.number_input("Minimum views", value=0)

if st.button("Search"):
    filters = {}
    if category != "All":
        filters['category'] = category
    if min_views > 0:
        filters['min_views'] = min_views
    
    result = agent.process_query(query, filters=filters)
    
    if result['success']:
        st.write(result['data']['answer'])
        
        for video in result['data']['results']:
            st.write(f"**{video['title']}**")
            st.write(f"Channel: {video['channel']} | Views: {video['views']:,}")
            st.write(f"Relevance: {video['score']:.2%}")
            st.write("---")
```

---

## Testing

```python
# Run tests
python -m pytest tests/test_vector_agent.py

# Test specific functionality
python scripts/test_vector_search.py
```

---

## Support

For issues or questions:
1. Check logs for detailed error messages
2. Verify Qdrant is running: `docker ps`
3. Check collection exists: `agent.get_stats()`
4. Run health check: `agent.health_check()`

---

## Changelog

### v2.0.0 (2025-11-12)
- Complete rewrite with production-ready architecture
- Added comprehensive error handling
- Implemented multiple search methods
- Added filtering and hybrid search
- Improved response generation
- Added health checks and monitoring
- Full documentation and type hints
- Industry-standard code practices
