# Vector Agent - Sample Test Queries

This document contains sample queries specifically designed to test all features of the Vector Database Agent.

---

## 1. Basic Semantic Search Queries

Test natural language understanding and content-based search:

```
- "funny cat videos"
- "cooking tutorials for beginners"
- "machine learning explained"
- "motivational speeches"
- "travel vlogs in Europe"
- "videos about artificial intelligence"
- "content related to fitness and workout"
- "gaming highlights and montages"
- "music covers and performances"
- "educational content about space"
```

### How to Test:
```python
from src.agents import VectorAgent

agent = VectorAgent()
result = agent.process_query("funny cat videos", limit=5)
print(result['data']['answer'])
```

---

## 2. Category-Filtered Search Queries

Test semantic search within specific categories:

### Gaming Category:
```
- "competitive gameplay and strategies" (category: Gaming)
- "game reviews and walkthroughs" (category: Gaming)
- "esports tournaments" (category: Gaming)
```

### Music Category:
```
- "acoustic guitar covers" (category: Music)
- "electronic dance music" (category: Music)
- "live concert performances" (category: Music)
```

### Education Category:
```
- "programming tutorials" (category: Education)
- "science experiments" (category: Education)
- "math lessons" (category: Education)
```

### Entertainment Category:
```
- "movie reviews and analysis" (category: Entertainment)
- "celebrity interviews" (category: Entertainment)
- "comedy sketches" (category: Entertainment)
```

### Science & Technology:
```
- "latest tech gadgets" (category: Science & Technology)
- "smartphone comparisons" (category: Science & Technology)
- "AI developments" (category: Science & Technology)
```

### How to Test:
```python
result = agent.search_by_category(
    query="programming tutorials",
    category="Education",
    limit=10
)
```

---

## 3. Popular Video Search Queries

Test filtering by view counts:

```
- "viral challenges" (min_views: 1,000,000)
- "trending music videos" (min_views: 5,000,000)
- "gaming highlights" (min_views: 500,000)
- "cooking recipes" (min_views: 100,000)
- "tech reviews" (min_views: 250,000)
- "workout videos" (min_views: 50,000)
- "travel destinations" (min_views: 200,000)
```

### How to Test:
```python
result = agent.search_popular_videos(
    query="gaming highlights",
    min_views=500000,
    limit=5
)
```

---

## 4. Hybrid Search Queries

Test combining semantic search with multiple filters:

### Semantic + Category + Views:
```
- "beginner tutorials" (category: Education, min_views: 50,000)
- "funny moments compilation" (category: Entertainment, min_views: 100,000, max_views: 1,000,000)
- "workout routines" (category: Howto & Style, min_views: 10,000)
- "game trailers" (category: Gaming, min_views: 500,000)
- "music production tutorials" (category: Music, min_views: 25,000, max_views: 500,000)
```

### How to Test:
```python
result = agent.hybrid_search(
    query="beginner tutorials",
    category="Education",
    min_views=50000,
    limit=10
)
```

---

## 5. Advanced Semantic Queries

Test complex natural language understanding:

```
- "videos explaining the difference between AI and machine learning"
- "content about sustainable fashion and ethical clothing"
- "tutorials on building web applications with React"
- "documentaries about ocean conservation"
- "videos discussing the future of renewable energy"
- "fitness and nutrition advice for beginners"
- "travel tips and budget planning"
- "photography techniques and camera settings"
- "entrepreneurship and startup advice"
- "mental health and stress management"
```

### How to Test:
```python
result = agent.process_query(
    "videos explaining the difference between AI and machine learning",
    limit=5,
    score_threshold=0.4
)
```

---

## 6. Find Similar Videos

Test content-based recommendations:

### How to Test:
```python
# First, get a video ID from a search
result = agent.process_query("gaming videos", limit=1)
video_id = result['data']['results'][0]['video_id']

# Then find similar videos
similar = agent.find_similar_videos(video_id, limit=5)
print(f"Videos similar to: {similar['data']['reference_video']['title']}")
```

---

## 7. Edge Case Queries

Test robustness with special cases:

### Very Specific Queries:
```
- "Counter Strike Global Offensive competitive matches"
- "Italian cooking recipes with pasta"
- "Python programming for data science"
- "electric vehicle reviews and comparisons"
- "yoga for back pain relief"
```

### Broad Queries:
```
- "videos"
- "content"
- "popular"
```

### Special Characters:
```
- "C++ programming tutorials"
- "React.js vs Vue.js comparison"
- "How to make $1000 online"
```

### Multi-language Concepts:
```
- "anime reviews and recommendations"
- "K-pop music videos and performances"
- "Bollywood movie trailers"
```

---

## 8. Score Threshold Testing

Test different similarity thresholds:

```python
query = "machine learning tutorials"

# Loose matching (more results)
result = agent.process_query(query, score_threshold=0.2, limit=10)

# Balanced (recommended)
result = agent.process_query(query, score_threshold=0.4, limit=10)

# Strict matching (high quality)
result = agent.process_query(query, score_threshold=0.7, limit=10)
```

---

## 9. Result Limit Testing

Test different result counts:

```python
query = "gaming videos"

# Quick results
result = agent.process_query(query, limit=3)

# Standard
result = agent.process_query(query, limit=10)

# Comprehensive
result = agent.process_query(query, limit=50)
```

---

## 10. Multi-Concept Queries

Test understanding of multiple concepts in one query:

```
- "fitness and nutrition advice for beginners"
- "travel tips and budget planning"
- "photography techniques and camera settings"
- "cooking and meal prep for weight loss"
- "gaming setup and streaming equipment"
- "home office design and productivity tips"
- "guitar lessons and music theory"
- "digital marketing and social media strategy"
```

---

## Complete Test Examples

### Example 1: Basic Search Flow
```python
from src.agents import VectorAgent

# Initialize
agent = VectorAgent()

# Simple search
result = agent.process_query("funny cat videos", limit=5)

# Print results
if result['success']:
    print(result['data']['answer'])
    for video in result['data']['results']:
        print(f"{video['rank']}. {video['title']} ({video['score']:.2%})")
```

### Example 2: Filtered Search
```python
# Search with category filter
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
```

### Example 3: Hybrid Search
```python
# Complex hybrid search
result = agent.hybrid_search(
    query="cooking recipes",
    category="Howto & Style",
    min_views=10000,
    max_views=1000000,
    limit=20
)
```

### Example 4: Similar Videos
```python
# Find similar videos
result = agent.find_similar_videos(
    video_id="abc123xyz",
    limit=10,
    exclude_self=True
)
```

---

## Testing Utilities

### Check Agent Health:
```python
health = agent.health_check()
print(f"Agent: {health['agent']}")
print(f"Vector DB: {health['components']['vector_db']}")
print(f"Embeddings: {health['components']['embedding_model']}")
```

### Get Statistics:
```python
stats = agent.get_stats()
print(f"Total Videos: {stats['total_videos']:,}")
print(f"Collection: {stats['collection_name']}")
```

### Get Capabilities:
```python
caps = agent.get_capabilities()
print(f"Features: {', '.join(caps['capabilities'])}")
```

---

## Running the Test Suite

### Quick Test (3 queries):
```bash
python tests/test_vector_agent_queries.py --mode quick
```

### Full Test Suite (all features):
```bash
python tests/test_vector_agent_queries.py --mode full
```

### Custom Testing:
```python
from tests.test_vector_agent_queries import *

# Run specific test
agent = VectorAgent()
test_semantic_search(agent)
test_category_search(agent)
test_popular_videos(agent)
test_hybrid_search(agent)
```

---

## Expected Results Format

### Success Response:
```python
{
    'success': True,
    'data': {
        'answer': 'Natural language answer...',
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

## Tips for Testing

1. **Start Simple**: Begin with basic semantic queries to verify the agent works
2. **Test Filters**: Add filters one at a time to isolate issues
3. **Check Scores**: Monitor similarity scores to understand relevance
4. **Vary Limits**: Test with different result counts (3, 5, 10, 20)
5. **Use Thresholds**: Adjust score thresholds based on your needs
6. **Monitor Health**: Run health checks if queries fail
7. **Check Stats**: Verify database has data before testing

---

## Common Issues & Solutions

### No Results Found:
- Lower the score threshold: `score_threshold=0.2`
- Remove filters: `filters=None`
- Check database has data: `agent.get_stats()`

### Low Relevance Scores:
- Use more specific queries
- Increase score threshold: `score_threshold=0.6`
- Add category filters for precision

### Slow Searches:
- Reduce result limit: `limit=5`
- Use more specific queries
- Add filters to narrow search space

---

## Categories Available

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

## Next Steps

1. Run the quick test to verify basic functionality
2. Test each feature category systematically
3. Experiment with different parameters
4. Monitor scores and adjust thresholds
5. Test edge cases and error handling
6. Integrate into your application

For detailed API documentation, see `VECTOR_AGENT_GUIDE.md`
