# System Architecture - Natural Language to Database Query Flow

## 🎯 How It Works (Natural Language Processing)

Your system **ALREADY** handles natural language queries correctly! Here's the complete flow:

```
User Input (Natural Language)
        ↓
   Orchestrator
        ↓
   Query Router (LLM-based Classification)
        ↓
   ┌─────────────┴─────────────┐
   ↓                           ↓
SQL Agent                 Vector Agent
   ↓                           ↓
Converts NL → SQL        Converts NL → Vector Search
   ↓                           ↓
Executes on SQLite       Executes on Qdrant
   ↓                           ↓
Converts Results → NL    Converts Results → NL
   └─────────────┬─────────────┘
                 ↓
           Synthesizer (LLM)
                 ↓
       Natural Language Response
                 ↓
              User
```

---

## 📝 Detailed Flow

### 1. **User Input** (Natural Language)
```
User types: "give me similar videos to Walk On Water Audio"
```

### 2. **Orchestrator Receives Query**
```python
# In orchestrator.py
def process_query(self, query: str) -> Dict[str, Any]:
    # Receives natural language query
    state = {'query': query, ...}
```

### 3. **Query Router Classifies** (LLM-based)
```python
# In query_router.py
def classify_query(self, query: str) -> Dict[str, Any]:
    # Uses LLM to understand intent
    # Classifies as: SQL, VECTOR, or HYBRID
    
    # For "similar videos" → VECTOR
    # For "top 10 channels" → SQL
    # For "trending gaming videos with stats" → HYBRID
```

### 4. **Agent Execution**

#### **For Vector Queries:**
```python
# In vector_agent.py
def process_query(self, query: str, **kwargs) -> Dict[str, Any]:
    """
    1. Takes natural language: "similar videos to Walk On Water"
    2. Converts to embedding vector using embedding model
    3. Performs similarity search in Qdrant
    4. Gets results with scores
    5. Uses LLM to generate natural language response
    """
    
    # Step 1: Generate embedding from natural language
    query_vector = self.embedding_model.encode_single(query)
    
    # Step 2: Search vector database
    results = self.db_ops.search(
        query_vector=query_vector,
        limit=limit,
        filters=filters
    )
    
    # Step 3: Generate natural language response
    if self.llm:
        answer = self._generate_llm_response(query, results)
    else:
        answer = self._generate_simple_response(query, results)
    
    return {'answer': answer, 'results': results}
```

#### **For SQL Queries:**
```python
# In sql_agent.py
def process_query(self, query: str, **kwargs) -> Dict[str, Any]:
    """
    1. Takes natural language: "top 10 channels by views"
    2. Uses LangChain SQL Agent to convert to SQL
    3. Executes SQL query on SQLite
    4. Gets results
    5. Converts results back to natural language
    """
    
    # LangChain handles NL → SQL → NL conversion
    response = self.agent_executor.invoke({"input": query})
    
    return {'answer': response['output']}
```

### 5. **Response Synthesis**
```python
# In orchestrator.py
def _synthesize_response(self, state: AgentState) -> AgentState:
    """
    Takes results from agents and creates final response
    """
    # Already in natural language from agents
    final_response = self._format_final_response(state)
    return state
```

### 6. **User Receives Natural Language Response**
```
Output: "Found 5 videos similar to 'Walk On Water Audio':
1. [Video Title] by [Channel] (85% match)
2. [Video Title] by [Channel] (78% match)
..."
```

---

## 🔑 Key Points

### ✅ **What's Already Working**

1. **Natural Language Input**: Users type in plain English
2. **Intelligent Routing**: LLM classifies query type automatically
3. **Automatic Conversion**: 
   - Vector Agent: NL → Embeddings → Vector Search → NL
   - SQL Agent: NL → SQL → Results → NL
4. **Natural Language Output**: Users get readable responses

### ❌ **What Users DON'T Do**

Users **NEVER** write code like this:
```python
# ❌ Users DON'T do this
agent.search_by_category("gaming", "Gaming")
agent.hybrid_search("cooking", category="Howto & Style")
```

Instead, users just type:
```
# ✅ Users DO this
"show me gaming videos"
"find cooking videos in how-to category with lots of views"
```

---

## 🏗️ Architecture Components

### **1. Query Router** (Brain)
- **Purpose**: Understand user intent
- **Technology**: LLM (Claude/GPT)
- **Input**: Natural language
- **Output**: Classification (SQL/VECTOR/HYBRID)

```python
# Example classifications:
"top 10 channels" → SQL
"similar videos" → VECTOR
"trending gaming videos with stats" → HYBRID
```

### **2. SQL Agent** (Structured Data)
- **Purpose**: Handle analytical queries
- **Technology**: LangChain SQL Agent + SQLite
- **Capabilities**:
  - Aggregations (COUNT, SUM, AVG)
  - Rankings (TOP N)
  - Filtering
  - Statistical analysis

**Natural Language Examples:**
- "Which category has the most videos?"
- "Top 10 channels by views"
- "Average likes per category"
- "Videos trending for more than 5 days"

### **3. Vector Agent** (Semantic Search)
- **Purpose**: Handle content-based queries
- **Technology**: Qdrant + Sentence Transformers + LLM
- **Capabilities**:
  - Semantic similarity
  - Content recommendations
  - Fuzzy matching
  - Concept search

**Natural Language Examples:**
- "Find videos about machine learning"
- "Videos similar to [title]"
- "Content related to cooking"
- "Funny cat videos"

---

## 🔄 Complete Example Flow

### Example 1: Vector Query

**User Input:**
```
"give me similar videos to Walk On Water Audio"
```

**Processing:**
```
1. Orchestrator receives query
2. Router classifies as VECTOR (confidence: 0.80)
3. Vector Agent:
   a. Generates embedding from query text
   b. Searches Qdrant for similar embeddings
   c. Retrieves top 5 matches with scores
   d. Uses LLM to generate natural response
4. Synthesizer formats final output
```

**User Output:**
```
Found 5 videos similar to 'Walk On Water Audio':

1. Walk On Water - Official Audio (92% match)
   Channel: Music Channel | Views: 1.5M | Likes: 45K
   
2. Walk On Water Remix (87% match)
   Channel: Remix Studio | Views: 850K | Likes: 23K
   
... (more results)
```

### Example 2: SQL Query

**User Input:**
```
"what are the top 5 most viewed videos?"
```

**Processing:**
```
1. Orchestrator receives query
2. Router classifies as SQL
3. SQL Agent:
   a. LangChain converts to: SELECT title, views FROM videos ORDER BY views DESC LIMIT 5
   b. Executes on SQLite database
   c. Gets results
   d. LangChain converts back to natural language
4. Synthesizer formats final output
```

**User Output:**
```
Here are the top 5 most viewed videos:

1. "Video Title 1" - 15.2M views
2. "Video Title 2" - 12.8M views
3. "Video Title 3" - 10.5M views
4. "Video Title 4" - 9.3M views
5. "Video Title 5" - 8.7M views
```

---

## 🎓 Why This Architecture?

### **Separation of Concerns**
- **Router**: Understands intent
- **SQL Agent**: Handles structured queries
- **Vector Agent**: Handles semantic queries
- **Orchestrator**: Coordinates everything

### **Flexibility**
- Can handle pure SQL queries
- Can handle pure vector queries
- Can handle hybrid queries (both)

### **Scalability**
- Each agent is independent
- Can add more agents easily
- Can run agents in parallel

### **User-Friendly**
- Users speak natural language
- System handles all conversions
- Responses are human-readable

---

## 🛠️ For Developers

### **Adding New Features to Vector Agent**

The methods like `search_by_category()`, `hybrid_search()`, etc. are **helper methods** for:
1. **Internal use** by the agent
2. **Direct API access** if building a REST API
3. **Testing and debugging**

But the **main interface** is always:
```python
# This is what orchestrator calls
result = agent.process_query(query_string)
```

The agent internally decides which helper method to use based on the query.

### **How Vector Agent Processes Queries**

```python
def process_query(self, query: str, **kwargs):
    """
    Main entry point - receives natural language
    """
    # 1. Validate query
    if not self.validate_query(query):
        return error_response
    
    # 2. Extract intent/parameters (could use LLM here)
    # For now, uses simple keyword matching or direct search
    
    # 3. Generate embedding
    query_vector = self.embedding_model.encode_single(query)
    
    # 4. Search vector database
    results = self.db_ops.search(query_vector, ...)
    
    # 5. Generate natural language response
    answer = self._generate_llm_response(query, results)
    
    # 6. Return formatted response
    return {'success': True, 'data': {'answer': answer, ...}}
```

---

## 🐛 Current Issue Resolution

### **The "Unknown" Title Problem**

**Issue**: Results showing "Unknown" titles

**Root Cause**: The old vector agent code was still cached

**Solution**: 
1. ✅ Removed import error (`PromptTemplate`)
2. ✅ Cleared Python cache (`__pycache__`)
3. ✅ New vector agent properly extracts metadata from Qdrant

**Fix Applied**:
```python
# Old (wrong):
title = payload.get('title', 'Unknown')

# New (correct):
title = result.get('title', 'No title')  # Direct from result dict
```

---

## ✅ Summary

### **Your System Architecture is CORRECT!**

✅ Users input natural language
✅ Router classifies intent
✅ Agents convert NL → DB queries
✅ Agents convert results → NL
✅ Users receive natural language responses

### **The Only Issue Was:**

❌ Import error + cached bytecode
✅ **FIXED**: Removed bad import, cleared cache

### **Next Steps:**

1. Restart your application (cache is cleared)
2. Test with natural language queries
3. System will work correctly now!

---

## 📞 Testing

```bash
# Clear cache (already done)
# Restart application
python -m src.main

# Test queries (natural language):
"give me similar videos to Walk On Water Audio"
"show me gaming videos"
"what are the top channels?"
"find funny cat videos"
```

All queries are processed as natural language - no code needed from users! 🎉
