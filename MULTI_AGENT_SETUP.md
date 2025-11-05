# Multi-Agent System Setup Guide

## Overview

This project implements a sophisticated multi-agent system for YouTube trends analysis using **LangChain** and **LangGraph**. The system intelligently routes queries to specialized agents based on query type.

## Architecture

```
User Query
    ↓
Query Router (LLM-based classifier)
    ↓
┌─────────────┬──────────────┬─────────────┐
│  SQL Agent  │ Vector Agent │   Hybrid    │
└─────────────┴──────────────┴─────────────┘
    ↓              ↓               ↓
LangGraph Orchestrator (Workflow Management)
    ↓
Response Synthesizer (LLM)
    ↓
Final Answer to User
```

## Components

### 1. **Query Router** (`src/agents/query_router.py`)
- **Purpose**: Classifies incoming queries using LLM
- **Types**: SQL, Vector, Hybrid, Unknown
- **Method**: Structured output with Pydantic models
- **Fallback**: Rule-based classifier when LLM unavailable

### 2. **SQL Agent** (`src/agents/sql_agent.py`)
- **Purpose**: Handles structured, analytical queries
- **Technology**: LangChain SQL Agent + SQLite
- **Capabilities**:
  - Aggregations (COUNT, SUM, AVG, MAX, MIN)
  - Filtering and sorting
  - Statistical analysis
  - Temporal queries
  - Top N rankings

### 3. **Vector Agent** (`src/agents/vector_agent.py`)
- **Purpose**: Handles semantic, content-based queries
- **Technology**: Qdrant + Sentence Transformers
- **Capabilities**:
  - Semantic similarity search
  - Content recommendations
  - Topic-based search
  - Fuzzy matching

### 4. **LangGraph Orchestrator** (`src/agents/orchestrator.py`)
- **Purpose**: Manages multi-agent workflow
- **Features**:
  - State management
  - Parallel/sequential execution
  - Response synthesis
  - Error handling

### 5. **Enhanced Data Processor** (`src/data/enhanced_processor.py`)
- **Purpose**: Processes raw CSV data
- **Outputs**: 
  - SQL database (SQLite)
  - Vector-ready data (for Qdrant)
- **Features**:
  - Language detection
  - Text cleaning
  - Temporal feature engineering
  - De-duplication

## Installation

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Set Up Environment Variables

Create a `.env` file:

```env
# Required: OpenAI/OpenRouter API Key
OPENAI_API_KEY=your_api_key_here

# Optional: LLM Configuration
OPENAI_BASE_URL=https://openrouter.ai/api/v1
LLM_MODEL=anthropic/claude-3-haiku
LLM_TEMPERATURE=0.0

# Optional: Database Configuration
SQL_DB_PATH=youtube_trends_canada.db
SQL_TABLE_NAME=videos

# Optional: Qdrant Configuration
QDRANT_HOST=localhost
QDRANT_PORT=6333
QDRANT_COLLECTION_NAME=youtube_trends

# Optional: Embedding Configuration
USE_LOCAL_EMBEDDINGS=true
LOCAL_EMBEDDING_MODEL=all-MiniLM-L6-v2
```

### 3. Start Qdrant (Vector Database)

Using Docker:
```bash
docker-compose up -d
```

Or manually:
```bash
docker run -p 6333:6333 qdrant/qdrant
```

## Data Processing

### Step 1: Process CSV Data

```bash
python -m src.data.enhanced_processor --csv data/raw/CAvideos.csv --country CA
```

This will:
1. Clean and process the data
2. Create SQL database (`youtube_trends_canada.db`)
3. Prepare data for vector indexing

### Step 2: Index Data in Vector Database

```bash
python scripts/index_data.py
```

This will:
1. Load processed data
2. Generate embeddings
3. Index in Qdrant

## Usage

### Interactive Mode (Recommended)

```bash
python -m src.main
```

This starts an interactive CLI where you can ask questions naturally.

### Single Query Mode

```bash
python -m src.main --query "Which category has the most trending videos?"
```

### Python API

```python
from src.main import YouTubeTrendsApp

# Initialize app
app = YouTubeTrendsApp()

# Process query
response = app.query("Find videos about cooking tutorials")

# Print answer
print(response['answer'])

# Access metadata
print(f"Query Type: {response['metadata']['query_type']}")
print(f"Agents Used: {response['metadata']['agents_used']}")
```

## Example Queries

### SQL Queries (Analytical)

```
✅ Which category has the most trending videos?
✅ Top 10 channels by total views
✅ Average likes for Gaming category
✅ Videos trending for more than 5 days
✅ Compare views between Music and Sports
✅ How many videos are in the database?
✅ Channel with highest average views per video
```

### Vector Queries (Semantic)

```
✅ Find videos about cooking tutorials
✅ Videos similar to tech reviews
✅ Content related to fitness and wellness
✅ Search for motivational content
✅ Videos discussing climate change
✅ Gaming content for beginners
```

### Hybrid Queries (Both)

```
✅ Most popular gaming videos about Minecraft
✅ Top educational content about programming
✅ Find trending cooking videos with high engagement
✅ Popular music videos in the last month
```

## Workflow Details

### Query Processing Flow

1. **User submits query** → `app.query(query)`

2. **Router classifies query** → Determines SQL/Vector/Hybrid
   - Uses LLM with structured output
   - Returns confidence score and reasoning

3. **LangGraph orchestrates execution**:
   - **SQL path**: Query → SQL Agent → Natural language response
   - **Vector path**: Query → Embedding → Qdrant search → LLM response
   - **Hybrid path**: Both agents in parallel → Synthesize results

4. **Response synthesis**:
   - Single agent: Direct response
   - Multiple agents: LLM combines insights

5. **Return to user** with metadata

### State Management (LangGraph)

```python
AgentState = {
    'query': str,                    # Original query
    'routing_info': dict,            # Classification results
    'sql_result': dict,              # SQL agent output
    'vector_result': dict,           # Vector agent output
    'final_response': str,           # Synthesized answer
    'error': str,                    # Error if any
    'metadata': dict                 # Additional info
}
```

## OOP Design Principles

### Base Agent Pattern

All agents inherit from `BaseAgent`:

```python
class BaseAgent(ABC):
    @abstractmethod
    def process_query(self, query: str) -> Dict[str, Any]:
        pass
    
    @abstractmethod
    def get_capabilities(self) -> Dict[str, Any]:
        pass
```

### Benefits:
- **Extensibility**: Easy to add new agents (Graph DB, etc.)
- **Consistency**: Standard interface across agents
- **Maintainability**: Clear separation of concerns
- **Testability**: Each agent can be tested independently

## Adding New Agents (e.g., Graph DB)

### Step 1: Create Agent Class

```python
# src/agents/graph_agent.py
from .base_agent import BaseAgent

class GraphAgent(BaseAgent):
    def __init__(self, api_key=None):
        super().__init__(name="GraphAgent")
        # Initialize graph database connection
        
    def process_query(self, query: str) -> Dict[str, Any]:
        # Implement graph query logic
        pass
    
    def get_capabilities(self) -> Dict[str, Any]:
        return {
            'name': self.name,
            'type': 'graph',
            'description': 'Handles relationship and network queries',
            'best_for': [
                'Channel collaboration networks',
                'Video recommendation graphs',
                'Trending cascade patterns'
            ]
        }
```

### Step 2: Update Router

Add graph query classification in `query_router.py`:

```python
class QueryType(str, Enum):
    SQL = "sql"
    VECTOR = "vector"
    GRAPH = "graph"  # New
    HYBRID = "hybrid"
```

### Step 3: Update Orchestrator

Add graph agent to `orchestrator.py`:

```python
if self.enable_graph:
    self.agents['graph'] = GraphAgent(api_key=self.api_key)
```

### Step 4: Update Workflow

Add graph node to LangGraph workflow.

## Configuration

### Settings (`src/config/settings.py`)

All configuration is centralized using Pydantic Settings:

```python
class Settings(BaseSettings):
    # Automatically loads from .env
    openai_api_key: str
    llm_model: str = "anthropic/claude-3-haiku"
    sql_db_path: str = "youtube_trends_canada.db"
    # ... more settings
```

## Troubleshooting

### Issue: "API key not found"
**Solution**: Set `OPENAI_API_KEY` in `.env` file

### Issue: "Database file not found"
**Solution**: Run data processing first:
```bash
python -m src.data.enhanced_processor --csv data/raw/CAvideos.csv
```

### Issue: "Qdrant connection failed"
**Solution**: Start Qdrant:
```bash
docker-compose up -d
```

### Issue: "No results from vector search"
**Solution**: Index data first:
```bash
python scripts/index_data.py
```

## Performance Optimization

### Parallel Execution
- Hybrid queries run SQL and Vector agents in parallel
- LangGraph manages concurrent execution

### Caching
- Embedding cache for repeated queries
- LLM response caching (future)

### Batch Processing
- Vector indexing in batches
- Configurable batch size in settings

## Testing

```bash
# Run all tests
pytest

# Run specific test
pytest tests/test_agents.py

# Run with coverage
pytest --cov=src tests/
```

## Future Enhancements

1. **Graph Database Agent** (Neo4j)
   - Channel networks
   - Video relationships
   - Trending cascades

2. **Caching Layer** (Redis)
   - Query result caching
   - Embedding caching

3. **API Server** (FastAPI)
   - REST endpoints
   - WebSocket for streaming
   - Authentication

4. **Advanced Routing**
   - Multi-hop reasoning
   - Query decomposition
   - Self-correction

5. **Monitoring & Analytics**
   - Query performance metrics
   - Agent usage statistics
   - Error tracking

## References

- **LangChain**: https://python.langchain.com/
- **LangGraph**: https://langchain-ai.github.io/langgraph/
- **Qdrant**: https://qdrant.tech/
- **Pydantic**: https://docs.pydantic.dev/

## License

MIT License - See LICENSE file for details
