# Quick Start Guide - Multi-Agent System

## 🚀 Get Started in 5 Minutes

### Prerequisites

1. **Python 3.8+** installed
2. **Docker** installed (for Qdrant)
3. **OpenRouter/OpenAI API Key**

### Step 1: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 2: Set Up Environment

Create `.env` file in project root:

```env
OPENAI_API_KEY=your_api_key_here
```

Get your API key from:
- OpenRouter: https://openrouter.ai/
- OpenAI: https://platform.openai.com/

### Step 3: Start Qdrant (Vector Database)

```bash
docker-compose up -d
```

Verify it's running:
```bash
curl http://localhost:6333
```

### Step 4: Process Your Data

Place your CSV file in `data/raw/` folder, then run:

```bash
python scripts/process_and_index.py --csv data/raw/CAvideos.csv
```

This will:
- ✅ Clean and process data
- ✅ Create SQL database
- ✅ Index in vector database
- ⏱️ Takes ~2-5 minutes depending on data size

### Step 5: Run the System!

**Interactive Mode:**
```bash
python -m src.main
```

**Single Query:**
```bash
python -m src.main --query "Which category has the most videos?"
```

## 📝 Example Usage

### Interactive Session

```
$ python -m src.main

======================================================================
  YouTube Trends Multi-Agent Analysis System
======================================================================

Welcome! Ask questions about YouTube trending videos.
Type 'help' for examples, 'info' for system info, or 'quit' to exit.

🔍 Your question: Which category has the most trending videos?

⏳ Processing your query...

----------------------------------------------------------------------
📊 ANSWER:
----------------------------------------------------------------------
Based on the analysis of the database, the Gaming category has the 
most trending videos with 2,456 videos, followed by Entertainment 
with 1,823 videos and Music with 1,654 videos.

📌 Query Type: sql
🤖 Agents Used: sql
✅ Confidence: 95.00%
----------------------------------------------------------------------

🔍 Your question: Find videos about cooking tutorials

⏳ Processing your query...

----------------------------------------------------------------------
📊 ANSWER:
----------------------------------------------------------------------
I found several relevant cooking videos:

1. "Easy 5-Minute Recipes" by Tasty (12.5M views)
   A collection of quick and simple recipes perfect for beginners.

2. "Gordon Ramsay's Ultimate Cooking Course" by Gordon Ramsay (8.2M views)
   Professional cooking techniques explained step-by-step.

3. "Binging with Babish: Basics" by Babish Culinary Universe (6.8M views)
   Fundamental cooking skills and techniques.

These videos are highly popular in the Howto & Style category and 
focus on practical cooking instruction.

📌 Query Type: vector
🤖 Agents Used: vector
✅ Confidence: 92.00%
----------------------------------------------------------------------
```

## 🎯 Query Examples

### SQL Queries (Analytics)

```python
# Statistical queries
"How many videos are in the database?"
"Average views per category"
"Top 10 channels by total likes"

# Filtering queries
"Videos with more than 1 million views"
"Gaming videos trending for more than 5 days"
"Channels in the Music category"

# Comparison queries
"Compare views between Gaming and Sports"
"Which has more engagement: Music or Comedy?"

# Temporal queries
"Videos published in the last month"
"Longest trending streak"
```

### Vector Queries (Semantic Search)

```python
# Topic-based search
"Find videos about machine learning"
"Content related to fitness and health"
"Videos discussing climate change"

# Similarity search
"Videos similar to tech reviews"
"Content like cooking tutorials"
"Gaming videos for beginners"

# Exploratory search
"Motivational content"
"Educational videos about science"
"Funny animal videos"
```

### Hybrid Queries (Both)

```python
# Combines analytics + semantic search
"Most popular gaming videos about Minecraft"
"Top educational content about programming"
"Trending cooking videos with high engagement"
"Popular music videos in the last month"
```

## 🔧 Configuration

### Basic Configuration (.env)

```env
# Required
OPENAI_API_KEY=sk-or-v1-xxxxx

# Optional - LLM Settings
LLM_MODEL=anthropic/claude-3-haiku
LLM_TEMPERATURE=0.0

# Optional - Database Settings
SQL_DB_PATH=youtube_trends_canada.db
QDRANT_HOST=localhost
QDRANT_PORT=6333
```

### Advanced Configuration

Edit `src/config/settings.py` for more options:
- Embedding model selection
- Batch sizes
- Vector dimensions
- Collection names

## 🐍 Python API Usage

```python
from src.main import YouTubeTrendsApp

# Initialize
app = YouTubeTrendsApp()

# Simple query
response = app.query("Top 10 channels by views")
print(response['answer'])

# Access detailed results
print(f"Query Type: {response['metadata']['query_type']}")
print(f"Agents Used: {response['metadata']['agents_used']}")
print(f"Confidence: {response['metadata']['confidence']:.2%}")

# Get system info
info = app.get_system_info()
print(info)
```

## 🔍 Understanding Query Routing

The system automatically classifies your query:

### SQL Agent Triggers
- Keywords: "how many", "count", "average", "top", "compare"
- Numerical analysis
- Aggregations
- Rankings

### Vector Agent Triggers
- Keywords: "find", "search", "similar", "about", "related"
- Content-based queries
- Topic exploration
- Semantic similarity

### Hybrid Triggers
- Combines both types
- Example: "popular videos about X"
- Runs both agents in parallel

## 📊 System Architecture

```
┌─────────────────────────────────────────────────┐
│           User Query                            │
└────────────────┬────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────┐
│     Query Router (LLM Classifier)               │
│     - Analyzes query intent                     │
│     - Returns: SQL/Vector/Hybrid                │
└────────────────┬────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────┐
│     LangGraph Orchestrator                      │
│     - Manages workflow                          │
│     - Coordinates agents                        │
└─────┬───────────────────────┬───────────────────┘
      │                       │
      ▼                       ▼
┌─────────────┐         ┌─────────────┐
│  SQL Agent  │         │Vector Agent │
│  (SQLite)   │         │  (Qdrant)   │
└─────┬───────┘         └─────┬───────┘
      │                       │
      └───────────┬───────────┘
                  ▼
      ┌───────────────────────┐
      │ Response Synthesizer  │
      │      (LLM)            │
      └───────────┬───────────┘
                  │
                  ▼
      ┌───────────────────────┐
      │   Final Answer        │
      └───────────────────────┘
```

## 🛠️ Troubleshooting

### "API key not found"
```bash
# Check .env file exists
ls -la .env

# Verify key is set
cat .env | grep OPENAI_API_KEY
```

### "Database not found"
```bash
# Run data processing
python scripts/process_and_index.py --csv data/raw/CAvideos.csv
```

### "Qdrant connection failed"
```bash
# Check if Qdrant is running
docker ps | grep qdrant

# Restart Qdrant
docker-compose restart
```

### "No results from vector search"
```bash
# Re-index data
python scripts/process_and_index.py --csv data/raw/CAvideos.csv --skip-sql
```

## 📚 Next Steps

1. **Explore the system**
   - Try different query types
   - Check system info: `python -m src.main --info`

2. **Customize configuration**
   - Edit `.env` for different models
   - Adjust settings in `src/config/settings.py`

3. **Add more data**
   - Process additional CSV files
   - Different countries/regions

4. **Extend functionality**
   - Add new agents (see MULTI_AGENT_SETUP.md)
   - Customize routing logic
   - Add new query types

## 🎓 Learning Resources

- **LangChain Docs**: https://python.langchain.com/
- **LangGraph Tutorial**: https://langchain-ai.github.io/langgraph/
- **Qdrant Guide**: https://qdrant.tech/documentation/
- **Project Architecture**: See `MULTI_AGENT_SETUP.md`

## 💡 Tips

1. **Start simple**: Try basic queries first
2. **Use help**: Type `help` in interactive mode
3. **Check logs**: Look in `logs/` folder for details
4. **Experiment**: Try different phrasings to see routing changes
5. **Monitor**: Watch which agents are used for each query

## 🤝 Support

- **Issues**: Check `MULTI_AGENT_SETUP.md` for detailed docs
- **Examples**: See `examples/` folder
- **Logs**: Check `logs/` for debugging

---

**Ready to analyze YouTube trends with AI! 🚀**
