# Vector Agent - Quick Start Guide

## 🚀 Quick Start

```python
from src.agents import VectorAgent

# Initialize
agent = VectorAgent()

# Search
result = agent.process_query("funny cat videos", limit=5)

# Print results
print(result['data']['answer'])
for video in result['data']['results']:
    print(f"- {video['title']} ({video['score']:.2%} match)")
```

---

## 📋 Common Operations

### 1. Basic Search
```python
result = agent.process_query("gaming videos")
```

### 2. Search with Limit
```python
result = agent.process_query("music", limit=10)
```

### 3. Search by Category
```python
result = agent.search_by_category("tutorials", "Education")
```

### 4. Search Popular Videos
```python
result = agent.search_popular_videos("funny videos", min_views=100000)
```

### 5. Hybrid Search (Multiple Filters)
```python
result = agent.hybrid_search(
    "cooking",
    category="Howto & Style",
    min_views=10000,
    max_views=500000
)
```

### 6. Find Similar Videos
```python
result = agent.find_similar_videos("video_id_123", limit=5)
```

---

## 🎯 Filter Options

```python
filters = {
    'category': 'Gaming',        # Category name
    'min_views': 100000,         # Minimum views
    'max_views': 1000000,        # Maximum views
    'country': 'CA'              # Country code
}

result = agent.process_query("query", filters=filters)
```

---

## 📊 Categories

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

---

## 🔍 Response Structure

```python
{
    'success': True,
    'data': {
        'answer': "Natural language answer...",
        'results': [
            {
                'rank': 1,
                'score': 0.8542,
                'video_id': 'abc123',
                'title': 'Video Title',
                'channel': 'Channel Name',
                'category': 'Gaming',
                'views': 1500000,
                'likes': 45000,
                'tags': ['tag1', 'tag2', ...]
            },
            # ... more results
        ],
        'query_type': 'vector',
        'source': 'semantic_search'
    },
    'metadata': {
        'query': 'original query',
        'limit': 5,
        'num_results': 5,
        'avg_score': 0.7234
    }
}
```

---

## 🛠️ Utility Methods

```python
# Get statistics
stats = agent.get_stats()
print(f"Total videos: {stats['total_videos']}")

# Health check
health = agent.health_check()
print(f"Status: {health['agent']}")

# Capabilities
caps = agent.get_capabilities()
print(f"Features: {caps['capabilities']}")
```

---

## ⚙️ Configuration

```python
agent = VectorAgent(
    api_key="your_key",           # Optional: Override env
    model="gpt-4",                 # Optional: LLM model
    default_limit=10,              # Default result count
    min_score_threshold=0.4        # Minimum similarity
)
```

---

## 🐛 Troubleshooting

### No Results?
```python
# Lower threshold
result = agent.process_query("query", score_threshold=0.1)

# Check database
stats = agent.get_stats()
print(f"Total videos: {stats['total_videos']}")
```

### Connection Error?
```python
# Check health
health = agent.health_check()
print(health)
```

### Slow Search?
```python
# Reduce limit
result = agent.process_query("query", limit=5)
```

---

## 📚 Full Documentation

See `VECTOR_AGENT_GUIDE.md` for complete documentation.

---

## 🧪 Test

```bash
python scripts/test_vector_agent.py
```

---

## 💡 Tips

1. **Be Specific**: Use descriptive queries for better results
2. **Use Filters**: Narrow down with category/views filters
3. **Adjust Threshold**: Higher = stricter, Lower = more results
4. **Appropriate Limits**: Balance between speed and completeness
5. **Check Health**: Run health checks if issues occur

---

## 📞 Quick Help

```python
# Check if working
agent.health_check()

# See what it can do
agent.get_capabilities()

# Get database info
agent.get_stats()
```

---

**Ready to search!** 🎉
