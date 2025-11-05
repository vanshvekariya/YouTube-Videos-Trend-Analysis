# YouTube Trends Multi-Agent Analysis System 🚀

A production-ready, intelligent multi-agent system for analyzing YouTube trending videos using **LangChain** and **LangGraph**.

## 🌟 Key Features

- **🤖 Intelligent Query Routing**: LLM automatically classifies queries and routes to appropriate agents
- **📊 SQL Agent**: Handles analytical queries (aggregations, statistics, rankings)
- **🔍 Vector Agent**: Handles semantic search (content-based, similarity)
- **🔄 Hybrid Queries**: Combines both agents for complex questions
- **🎯 LangGraph Orchestration**: Sophisticated workflow management with state tracking
- **🏗️ OOP Design**: Extensible architecture ready for Graph DB and more
- **⚡ Production-Ready**: Comprehensive error handling, logging, and configuration

## 🏛️ Architecture

```
User Query → Query Router (LLM) → LangGraph Orchestrator
                                          ↓
                        ┌─────────────────┴─────────────────┐
                        ▼                                   ▼
                   SQL Agent                          Vector Agent
                   (SQLite)                           (Qdrant)
                        │                                   │
                        └─────────────────┬─────────────────┘
                                          ▼
                              Response Synthesizer (LLM)
                                          ▼
                                   Final Answer
```

## 📋 Table of Contents

- [Quick Start](#-quick-start)
- [Installation](#-installation)
- [Usage](#-usage)
- [Query Examples](#-query-examples)
- [Architecture Details](#-architecture-details)
- [Extending the System](#-extending-the-system)
- [API Reference](#-api-reference)
- [Troubleshooting](#-troubleshooting)

## 🚀 Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure Environment

Create `.env` file:

```env
OPENAI_API_KEY=your_api_key_here
```

### 3. Start Vector Database

```bash
docker-compose up -d
```

### 4. Process Data

```bash
python scripts/process_and_index.py --csv data/raw/CAvideos.csv
```

### 5. Run the System

**Interactive Mode:**
```bash
python -m src.main
```

**Single Query:**
```bash
python -m src.main --query "Which category has the most videos?"
```

**Python API:**
```python
from src.main import YouTubeTrendsApp

app = YouTubeTrendsApp()
response = app.query("Top 10 channels by views")
print(response['answer'])
```

## 📦 Installation

### Prerequisites

- Python 3.8+
- Docker (for Qdrant)
- OpenRouter or OpenAI API key

### Step-by-Step

1. **Clone the repository**
   ```bash
   cd YouTube-Videos-Trend-Analysis
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Edit .env and add your API key
   ```

5. **Start Qdrant**
   ```bash
   docker-compose up -d
   ```

6. **Verify installation**
   ```bash
   python -m src.main --info
   ```

## 💻 Usage

### Interactive CLI

The easiest way to use the system:

```bash
python -m src.main
```

```
======================================================================
  YouTube Trends Multi-Agent Analysis System
======================================================================

🔍 Your question: Which category has the most trending videos?

⏳ Processing your query...

----------------------------------------------------------------------
📊 ANSWER:
----------------------------------------------------------------------
Based on the analysis, Gaming has the most trending videos with 2,456
videos, followed by Entertainment (1,823) and Music (1,654).

📌 Query Type: sql
🤖 Agents Used: sql
✅ Confidence: 95.00%
----------------------------------------------------------------------
```

### Python API

```python
from src.main import YouTubeTrendsApp

# Initialize
app = YouTubeTrendsApp()

# Simple query
response = app.query("Find videos about cooking")
print(response['answer'])

# Access metadata
print(f"Type: {response['metadata']['query_type']}")
print(f"Agents: {response['metadata']['agents_used']}")
print(f"Confidence: {response['metadata']['confidence']:.2%}")

# Get system info
info = app.get_system_info()
print(info)
```

### Command Line Options

```bash
# Single query
python -m src.main --query "Your question here"

# Custom API key
python -m src.main --api-key "sk-..."

# Custom model
python -m src.main --model "anthropic/claude-3-sonnet"

# Disable specific agents
python -m src.main --no-sql    # Disable SQL agent
python -m src.main --no-vector # Disable Vector agent

# Show system info
python -m src.main --info
```

## 📝 Query Examples

### SQL Queries (Analytical)

Perfect for:
- Aggregations and statistics
- Filtering and sorting
- Rankings and comparisons
- Numerical analysis

```
✅ "Which category has the most trending videos?"
✅ "Top 10 channels by total views"
✅ "Average likes for Gaming category"
✅ "Videos trending for more than 5 days"
✅ "Compare views between Music and Sports"
✅ "How many videos have over 1 million views?"
✅ "Channel with highest average engagement"
```

### Vector Queries (Semantic Search)

Perfect for:
- Content-based search
- Topic exploration
- Similarity matching
- Natural language understanding

```
✅ "Find videos about cooking tutorials"
✅ "Videos similar to tech reviews"
✅ "Content related to fitness and wellness"
✅ "Search for motivational content"
✅ "Videos discussing climate change"
✅ "Gaming content for beginners"
✅ "Educational science videos"
```

### Hybrid Queries (Both Agents)

Combines analytical and semantic capabilities:

```
✅ "Most popular gaming videos about Minecraft"
✅ "Top educational content about programming"
✅ "Find trending cooking videos with high engagement"
✅ "Popular music videos in the last month"
✅ "Best performing fitness channels"
```

## 🏗️ Architecture Details

### Components

#### 1. **Query Router** (`src/agents/query_router.py`)
- **Purpose**: Classifies incoming queries using LLM
- **Output**: SQL, Vector, Hybrid, or Unknown
- **Features**: Confidence scoring, reasoning, fallback classifier

#### 2. **SQL Agent** (`src/agents/sql_agent.py`)
- **Technology**: LangChain SQL Agent + SQLite
- **Capabilities**: Aggregations, filtering, sorting, statistics
- **Process**: Natural Language → SQL → Execution → Natural Language

#### 3. **Vector Agent** (`src/agents/vector_agent.py`)
- **Technology**: Qdrant + Sentence Transformers + LLM
- **Capabilities**: Semantic search, similarity, recommendations
- **Process**: Query → Embedding → Vector Search → LLM Response

#### 4. **LangGraph Orchestrator** (`src/agents/orchestrator.py`)
- **Purpose**: Manages multi-agent workflow
- **Features**: State management, parallel execution, response synthesis
- **Workflow**: Route → Execute → Synthesize → Return

#### 5. **Data Processor** (`src/data/enhanced_processor.py`)
- **Purpose**: Processes raw CSV data
- **Features**: Language detection, cleaning, temporal features
- **Output**: SQL database + Vector-ready data

### Workflow

```python
# 1. User submits query
query = "Most popular gaming videos about Minecraft"

# 2. Router classifies (Hybrid)
classification = {
    'type': 'hybrid',
    'confidence': 0.92,
    'reasoning': 'Combines analytical (most popular) and semantic (about Minecraft)'
}

# 3. LangGraph orchestrates
state = {
    'query': query,
    'routing_info': classification,
    'sql_result': None,
    'vector_result': None
}

# 4. Execute agents in parallel
sql_result = sql_agent.process_query(query)      # Get popular gaming videos
vector_result = vector_agent.process_query(query) # Find Minecraft content

# 5. Synthesize results
final_answer = synthesizer.combine(sql_result, vector_result)

# 6. Return to user
return {
    'answer': final_answer,
    'metadata': {...}
}
```

## 🔧 Extending the System

### Adding a Graph Database Agent

The system is designed for easy extension. Here's how to add a Graph DB agent:

#### Step 1: Create Agent Class

```python
# src/agents/graph_agent.py
from .base_agent import BaseAgent

class GraphAgent(BaseAgent):
    def __init__(self, api_key=None):
        super().__init__(name="GraphAgent")
        # Initialize Neo4j connection
        self.graph_db = Neo4jClient()
    
    def process_query(self, query: str) -> Dict[str, Any]:
        # Convert query to Cypher
        # Execute on graph
        # Return results
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

#### Step 2: Update Router

```python
# src/agents/query_router.py
class QueryType(str, Enum):
    SQL = "sql"
    VECTOR = "vector"
    GRAPH = "graph"  # Add this
    HYBRID = "hybrid"
```

#### Step 3: Update Orchestrator

```python
# src/agents/orchestrator.py
if self.enable_graph:
    self.agents['graph'] = GraphAgent(api_key=self.api_key)
```

That's it! The system will automatically route graph queries to your new agent.

## 📚 API Reference

### YouTubeTrendsApp

```python
class YouTubeTrendsApp:
    def __init__(
        self,
        api_key: Optional[str] = None,
        model: Optional[str] = None,
        enable_sql: bool = True,
        enable_vector: bool = True
    )
    
    def query(self, query: str) -> dict:
        """Process a query and return results"""
    
    def get_system_info(self) -> dict:
        """Get system and agent information"""
    
    def interactive_mode(self) -> None:
        """Run interactive CLI"""
```

### Response Format

```python
{
    'query': str,              # Original query
    'answer': str,             # Natural language answer
    'success': bool,           # Whether query succeeded
    'metadata': {
        'query_type': str,     # sql, vector, or hybrid
        'agents_used': list,   # Which agents processed it
        'confidence': float    # Classification confidence
    },
    'routing': {               # Routing details
        'classification': {...},
        'agents': [...],
        'execution_strategy': str
    },
    'sql_result': dict,        # SQL agent result (if used)
    'vector_result': dict      # Vector agent result (if used)
}
```

## 🐛 Troubleshooting

### Common Issues

#### "API key not found"
```bash
# Solution: Set in .env file
echo "OPENAI_API_KEY=your_key" > .env
```

#### "Database file not found"
```bash
# Solution: Process data first
python scripts/process_and_index.py --csv data/raw/CAvideos.csv
```

#### "Qdrant connection failed"
```bash
# Solution: Start Qdrant
docker-compose up -d

# Verify it's running
curl http://localhost:6333
```

#### "No results from vector search"
```bash
# Solution: Re-index data
python scripts/process_and_index.py --csv data/raw/CAvideos.csv --skip-sql
```

#### Import errors
```bash
# Solution: Reinstall dependencies
pip install -r requirements.txt --force-reinstall
```

### Debug Mode

Enable verbose logging:

```python
from src.main import YouTubeTrendsApp
import logging

logging.basicConfig(level=logging.DEBUG)
app = YouTubeTrendsApp()
```

Check logs:
```bash
tail -f logs/youtube_trends_*.log
```

## 📖 Documentation

- **[QUICKSTART_MULTI_AGENT.md](QUICKSTART_MULTI_AGENT.md)**: 5-minute quick start guide
- **[MULTI_AGENT_SETUP.md](MULTI_AGENT_SETUP.md)**: Comprehensive setup and architecture
- **[IMPLEMENTATION_SUMMARY.md](IMPLEMENTATION_SUMMARY.md)**: Implementation details
- **[examples/multi_agent_example.py](examples/multi_agent_example.py)**: Code examples

## 🧪 Testing

Run tests:
```bash
pytest tests/test_multi_agent_system.py -v
```

Run with coverage:
```bash
pytest --cov=src tests/
```

## 🔐 Security

- API keys stored in `.env` (gitignored)
- No hardcoded credentials
- Input validation on all queries
- SQL injection protection (via LangChain)

## 🚀 Performance

- **Parallel execution** for hybrid queries
- **Batch processing** for data indexing
- **Caching** (embedding cache)
- **Configurable batch sizes**

## 📊 Tech Stack

- **LangChain**: LLM orchestration
- **LangGraph**: Workflow management
- **Qdrant**: Vector database
- **SQLite**: Structured database
- **Sentence Transformers**: Embeddings
- **Pydantic**: Data validation
- **FastAPI**: Ready for API deployment
- **Loguru**: Advanced logging

## 🤝 Contributing

Contributions welcome! Areas for improvement:
- Additional agents (Graph DB, Time Series)
- Advanced routing strategies
- Caching layer
- API server
- Monitoring dashboard

## 📄 License

MIT License - See LICENSE file

## 🙏 Acknowledgments

- LangChain team for the framework
- Qdrant for vector database
- OpenRouter for LLM access

---

**Built with ❤️ using LangChain and LangGraph**

For questions or issues, check the documentation or create an issue.
