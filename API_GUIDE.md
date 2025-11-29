# API Guide - YouTube Trends Explorer

Complete guide to the FastAPI backend for the YouTube Trends Analysis system.

## 📋 Overview

The backend provides a RESTful API for querying YouTube trending video data using a multi-agent AI system.

### Base URL

```
http://localhost:8000
```

### Interactive Documentation

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 🔌 Endpoints

### 1. Root Endpoint

**GET /**

Returns basic API information.

**Response:**
```json
{
  "message": "YouTube Trends Analysis API",
  "version": "1.0.0",
  "docs": "/docs",
  "health": "/health"
}
```

---

### 2. Health Check

**GET /health**

Check the health status of the API and its dependencies.

**Response:**
```json
{
  "status": "healthy",
  "version": "1.0.0",
  "agents_available": ["SQL Agent", "Vector Agent"],
  "database_connected": true
}
```

**Status Codes:**
- `200 OK` - System is healthy
- `503 Service Unavailable` - System has issues

---

### 3. Process Query

**POST /query**

Process a natural language query about YouTube trends.

**Request Body:**
```json
{
  "query": "Top 10 gaming videos",
  "max_results": 10
}
```

**Parameters:**
- `query` (string, required): Natural language query
- `max_results` (integer, optional): Maximum number of results (1-100, default: 10)

**Response:**
```json
{
  "query": "Top 10 gaming videos",
  "answer": "Here are the top 10 gaming videos based on views...",
  "success": true,
  "metadata": {
    "query_type": "sql",
    "agents_used": ["SQL Agent"],
    "confidence": 0.95
  },
  "results": [
    {
      "title": "Epic Gaming Montage",
      "channel_title": "ProGamer",
      "views": 5000000,
      "likes": 250000,
      "comment_count": 15000,
      "category": "Gaming",
      "trending_date": "2024-01-15",
      "score": 0.98
    }
  ],
  "processing_time": 2.34,
  "error": null
}
```

**Status Codes:**
- `200 OK` - Query processed successfully
- `400 Bad Request` - Invalid query parameters
- `500 Internal Server Error` - Processing failed
- `503 Service Unavailable` - System not initialized

---

### 4. System Information

**GET /system/info**

Get information about the system and available agents.

**Response:**
```json
{
  "orchestrator": "Multi-Agent Orchestrator",
  "agents": {
    "sql_agent": {
      "name": "SQL Agent",
      "type": "sql",
      "description": "Handles structured queries and analytics"
    },
    "vector_agent": {
      "name": "Vector Agent",
      "type": "vector",
      "description": "Handles semantic search and similarity"
    }
  },
  "configuration": {
    "llm_model": "gpt-4o-mini",
    "sql_database": "youtube_trends_canada.db",
    "vector_db": "Qdrant (localhost:6333)",
    "embedding_model": "all-MiniLM-L6-v2"
  }
}
```

**Status Codes:**
- `200 OK` - Information retrieved successfully
- `500 Internal Server Error` - Failed to get info
- `503 Service Unavailable` - System not initialized

---

### 5. Example Queries

**GET /examples**

Get example queries to help users understand system capabilities.

**Response:**
```json
[
  {
    "category": "SQL/Analytical",
    "query": "Which category has the most trending videos?",
    "description": "Get statistics about video categories"
  },
  {
    "category": "Vector/Semantic",
    "query": "Find videos about cooking tutorials",
    "description": "Semantic search based on content"
  },
  {
    "category": "Hybrid",
    "query": "Most popular gaming videos about Minecraft",
    "description": "Combine semantic search with analytics"
  }
]
```

**Status Codes:**
- `200 OK` - Examples retrieved successfully

---

## 🔍 Query Types

The system automatically routes queries to appropriate agents:

### SQL/Analytical Queries

Best for:
- Statistics and aggregations
- Top N queries
- Filtering by specific criteria
- Comparisons between categories

**Examples:**
- "Top 10 channels by views"
- "Average likes for Gaming category"
- "Videos with more than 1M views"
- "Compare Music vs Sports categories"

### Vector/Semantic Queries

Best for:
- Content-based search
- Finding similar videos
- Topic discovery
- Semantic similarity

**Examples:**
- "Find cooking tutorial videos"
- "Videos about fitness and wellness"
- "Content similar to tech reviews"
- "Motivational content"

### Hybrid Queries

Combines both approaches for:
- Filtered semantic search
- Content discovery with constraints
- Complex multi-criteria queries

**Examples:**
- "Popular gaming videos about Minecraft"
- "Top educational programming content"
- "Trending cooking videos with high engagement"

---

## 🔐 Authentication

Currently, the API does not require authentication. For production use, consider adding:

- API key authentication
- OAuth 2.0
- Rate limiting
- User management

---

## 📊 Response Metadata

The `metadata` field in query responses provides insights:

```json
{
  "query_type": "sql|vector|hybrid",
  "agents_used": ["SQL Agent", "Vector Agent"],
  "confidence": 0.95,
  "execution_time": 1.23,
  "sql_query": "SELECT * FROM videos...",  // If SQL agent used
  "vector_score": 0.87  // If vector agent used
}
```

---

## 🚨 Error Handling

### Error Response Format

```json
{
  "detail": "Error message",
  "error": "Detailed error information"
}
```

### Common Errors

**400 Bad Request**
```json
{
  "detail": "Query must be at least 1 character long"
}
```

**500 Internal Server Error**
```json
{
  "detail": "Query processing failed: Database connection error"
}
```

**503 Service Unavailable**
```json
{
  "detail": "Application not initialized"
}
```

---

## 💡 Usage Examples

### Python

```python
import requests

# Process a query
response = requests.post(
    "http://localhost:8000/query",
    json={
        "query": "Top 10 gaming videos",
        "max_results": 10
    }
)

data = response.json()
print(data["answer"])
```

### JavaScript/Fetch

```javascript
const response = await fetch('http://localhost:8000/query', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    query: 'Top 10 gaming videos',
    max_results: 10
  })
});

const data = await response.json();
console.log(data.answer);
```

### cURL

```bash
curl -X POST http://localhost:8000/query \
  -H "Content-Type: application/json" \
  -d '{
    "query": "Top 10 gaming videos",
    "max_results": 10
  }'
```

### Axios (React)

```javascript
import axios from 'axios';

const processQuery = async (query) => {
  try {
    const response = await axios.post('http://localhost:8000/query', {
      query: query,
      max_results: 10
    });
    return response.data;
  } catch (error) {
    console.error('Query failed:', error);
    throw error;
  }
};
```

---

## ⚙️ Configuration

### CORS Settings

The API allows requests from:
- `http://localhost:5173` (Vite dev server)
- `http://localhost:3000` (Alternative dev port)
- `http://127.0.0.1:5173`

To add more origins, edit `src/api/main.py`:

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "https://your-production-domain.com"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### Timeout Settings

Default timeout: 60 seconds

Adjust in `src/api/main.py` if needed for longer queries.

---

## 🔧 Development

### Running the API

```bash
# Development mode with auto-reload
python run_api.py

# Or using uvicorn directly
uvicorn src.api.main:app --reload --host 0.0.0.0 --port 8000
```

### Testing Endpoints

```bash
# Health check
curl http://localhost:8000/health

# Get examples
curl http://localhost:8000/examples

# Process query
curl -X POST http://localhost:8000/query \
  -H "Content-Type: application/json" \
  -d '{"query": "test query"}'
```

### Logs

Logs are stored in `logs/` directory with rotation:
- Max size: 100 MB per file
- Retention: 10 days
- Format: JSON with timestamps

---

## 📈 Performance

### Response Times

Typical response times:
- **SQL queries**: 0.5-2 seconds
- **Vector queries**: 1-3 seconds
- **Hybrid queries**: 2-5 seconds

Factors affecting performance:
- LLM model speed
- Database size
- Query complexity
- Network latency

### Optimization Tips

1. Use `gpt-4o-mini` for faster responses
2. Limit `max_results` to needed amount
3. Cache frequent queries (future enhancement)
4. Use connection pooling for databases

---

## 🔒 Security Best Practices

For production deployment:

1. **Enable HTTPS**: Use SSL/TLS certificates
2. **Add authentication**: Implement API keys or OAuth
3. **Rate limiting**: Prevent abuse
4. **Input validation**: Already implemented via Pydantic
5. **CORS restrictions**: Limit to known domains
6. **Environment variables**: Never hardcode secrets
7. **Logging**: Monitor for suspicious activity

---

## 📦 Deployment

### Production Checklist

- [ ] Set `reload=False` in uvicorn
- [ ] Use production ASGI server (gunicorn + uvicorn workers)
- [ ] Configure proper CORS origins
- [ ] Set up monitoring and logging
- [ ] Enable HTTPS
- [ ] Add authentication
- [ ] Set up database backups
- [ ] Configure rate limiting
- [ ] Use environment variables for secrets

### Example Production Command

```bash
gunicorn src.api.main:app \
  --workers 4 \
  --worker-class uvicorn.workers.UvicornWorker \
  --bind 0.0.0.0:8000 \
  --timeout 120
```

---

## 🆘 Troubleshooting

### API Won't Start

1. Check if port 8000 is available
2. Verify virtual environment is activated
3. Ensure all dependencies are installed
4. Check `.env` file configuration

### Queries Failing

1. Verify Qdrant is running
2. Check database file exists
3. Validate API key in `.env`
4. Review logs in `logs/` directory

### CORS Errors

1. Check allowed origins in `src/api/main.py`
2. Verify frontend URL matches exactly
3. Restart API after CORS changes

---

## 📚 Additional Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Pydantic Models](https://docs.pydantic.dev/)
- [Uvicorn Server](https://www.uvicorn.org/)
- [Full Stack Setup Guide](FULLSTACK_SETUP.md)
