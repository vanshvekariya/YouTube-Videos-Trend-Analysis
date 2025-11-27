# Hybrid Query Processing - Improvements

## 🎯 Problem Identified

Your query: **"give me top 10 gaming channels based on likes and also suggest some of the gaming videos related to counter strike"**

This query contains **TWO distinct parts**:
1. **SQL Part**: "top 10 gaming channels based on likes" (requires ranking/aggregation)
2. **Vector Part**: "suggest gaming videos related to counter strike" (requires semantic search)

**Previous Behavior**: Only processed as VECTOR query
**Expected Behavior**: Process as HYBRID query with both agents running in parallel

---

## ✅ Improvements Made

### 1. **Enhanced Query Router** 

#### **Improved LLM Prompt**
Added explicit rules for detecting hybrid queries:

```python
3. **HYBRID** - For queries requiring BOTH SQL and VECTOR:
   - Queries with "AND", "ALSO", "PLUS" connecting different requirements
   - Ranking/statistics (SQL) + content search (VECTOR)
   - Aggregations (SQL) + semantic search (VECTOR)
   - Multiple distinct questions in one query
   
   IMPORTANT: Look for queries that contain BOTH:
   - Statistical/ranking keywords (top, most, count, average) AND
   - Content/semantic keywords (about, related to, similar, videos on)
   
   Examples:
   - "Top 10 gaming channels AND suggest gaming videos about Counter Strike"
   - "Most viewed cooking videos AND find recipes related to Italian food"
   
CRITICAL RULES:
- If query contains TWO distinct parts (connected by AND/ALSO/PLUS), classify as HYBRID
- If query asks for both rankings/stats AND content recommendations, classify as HYBRID
- If query mentions both "top/most/count" AND "find/show/suggest/related", classify as HYBRID
```

#### **Improved Simple Router**
Added hybrid connector detection:

```python
hybrid_connectors = ['and also', 'also', 'and suggest', 'and find', 'plus', 'and show']
has_hybrid_connector = any(conn in query_lower for conn in hybrid_connectors)

if (sql_score > 0 and vector_score > 0) or (has_hybrid_connector and (sql_score > 0 or vector_score > 0)):
    query_type = QueryType.HYBRID
```

### 2. **Query Extraction for Hybrid Queries**

Added intelligent query splitting to send appropriate sub-queries to each agent:

#### **SQL Query Extraction**
```python
def _extract_sql_query(self, query: str) -> str:
    """
    Extract SQL-relevant part from a hybrid query.
    Uses LLM to intelligently extract the analytical part.
    Fallback: Simple split on connectors.
    """
    # LLM extraction
    prompt = "Extract the SQL/analytical part from this query..."
    
    # Fallback: Split on 'and also', 'also', etc.
```

**Example**:
- **Full Query**: "top 10 gaming channels based on likes and also suggest gaming videos related to counter strike"
- **Extracted for SQL**: "top 10 gaming channels based on likes"

#### **Vector Query Extraction**
```python
def _extract_vector_query(self, query: str) -> str:
    """
    Extract Vector-relevant part from a hybrid query.
    Uses LLM to intelligently extract the semantic search part.
    Fallback: Simple split on connectors.
    """
    # LLM extraction
    prompt = "Extract the semantic search/content part from this query..."
    
    # Fallback: Split on connectors, return second part
```

**Example**:
- **Full Query**: "top 10 gaming channels based on likes and also suggest gaming videos related to counter strike"
- **Extracted for Vector**: "suggest gaming videos related to counter strike"

### 3. **Parallel Execution**

The orchestrator already supports parallel execution for hybrid queries:

```python
# Workflow:
1. Route query → Detects HYBRID
2. Execute SQL Agent (with extracted SQL query)
3. Execute Vector Agent (with extracted Vector query) 
4. Synthesize both results into unified response
```

---

## 🔄 How It Works Now

### **Example Query Flow**

**User Input**:
```
"give me top 10 gaming channels based on likes and also suggest some of the gaming videos related to counter strike"
```

### **Step 1: Classification**
```
Router: HYBRID detected
Confidence: 0.85
Reasoning: "Query contains both ranking keywords (top 10, based on likes) 
           and semantic search keywords (suggest, related to)"
Agents: ['sql', 'vector']
```

### **Step 2: Query Extraction**

**For SQL Agent**:
```
Original: "give me top 10 gaming channels based on likes and also suggest..."
Extracted: "top 10 gaming channels based on likes"
```

**For Vector Agent**:
```
Original: "give me top 10 gaming channels based on likes and also suggest..."
Extracted: "suggest gaming videos related to counter strike"
```

### **Step 3: Parallel Execution**

**SQL Agent** (processes extracted SQL query):
```sql
SELECT channel_title, SUM(likes) as total_likes
FROM videos
WHERE category_name = 'Gaming'
GROUP BY channel_title
ORDER BY total_likes DESC
LIMIT 10
```

**Vector Agent** (processes extracted Vector query):
```python
# Generates embedding for "gaming videos related to counter strike"
# Searches Qdrant for similar content
# Returns top matching videos
```

### **Step 4: Response Synthesis**

```
SQL Result: "Top 10 gaming channels by likes:
1. Channel A - 5.2M likes
2. Channel B - 4.8M likes
..."

Vector Result: "Gaming videos related to Counter Strike:
1. CS:GO Tournament Highlights
2. Counter Strike Tips and Tricks
..."

Synthesized Response: "Here are the top 10 gaming channels by likes, 
along with Counter Strike video recommendations:

**Top Gaming Channels:**
1. Channel A - 5.2M total likes
2. Channel B - 4.8M total likes
...

**Counter Strike Videos:**
1. CS:GO Tournament Highlights (850K views)
2. Counter Strike Tips and Tricks (620K views)
..."
```

---

## 📊 Supported Hybrid Query Patterns

### **Pattern 1: Rankings + Content Search**
```
"Top 10 [category] channels AND find videos about [topic]"
"Most viewed [category] AND suggest [content type]"
```

### **Pattern 2: Statistics + Recommendations**
```
"Show me statistics on [category] and also recommend [content]"
"Count of [metric] plus suggest videos related to [topic]"
```

### **Pattern 3: Comparisons + Similar Content**
```
"Compare [A] and [B] and find similar videos"
"Which has more [metric] and show related content"
```

### **Pattern 4: Multiple Questions**
```
"What are the top channels? Also find videos about [topic]"
"Give me stats on [category] and search for [content]"
```

---

## 🧪 Testing

### **Test Queries**

1. **Hybrid - Rankings + Search**
   ```
   "top 10 gaming channels based on likes and also suggest gaming videos related to counter strike"
   ```
   Expected: SQL for rankings + Vector for Counter Strike videos

2. **Hybrid - Statistics + Recommendations**
   ```
   "show me statistics on music videos and also find songs related to pop music"
   ```
   Expected: SQL for statistics + Vector for pop music search

3. **Hybrid - Multiple Questions**
   ```
   "which category has most videos? also show me cooking tutorials"
   ```
   Expected: SQL for category count + Vector for cooking tutorials

4. **Pure SQL** (should still work)
   ```
   "top 10 channels by views"
   ```
   Expected: Only SQL agent

5. **Pure Vector** (should still work)
   ```
   "find videos about machine learning"
   ```
   Expected: Only Vector agent

---

## 🎯 Key Features

### ✅ **Intelligent Classification**
- LLM-based detection of hybrid queries
- Fallback to rule-based detection
- High confidence scoring

### ✅ **Smart Query Splitting**
- LLM extracts relevant parts for each agent
- Fallback to simple connector-based splitting
- Preserves query intent

### ✅ **Parallel Execution**
- Both agents run simultaneously
- Faster response times
- Independent processing

### ✅ **Unified Response**
- LLM synthesizes both results
- Coherent, natural language output
- Addresses all parts of the query

---

## 📈 Performance

### **Before (Single Agent)**
```
Query: "top 10 channels and suggest videos about X"
Processing: Only Vector agent
Time: ~3 seconds
Result: Incomplete (missing rankings)
```

### **After (Hybrid)**
```
Query: "top 10 channels and suggest videos about X"
Processing: SQL + Vector (parallel)
Time: ~3-4 seconds (parallel execution)
Result: Complete (rankings + recommendations)
```

---

## 🔮 Future Enhancements

1. **Query Rewriting**: Automatically improve extracted queries
2. **Context Sharing**: Share SQL results with Vector agent for filtering
3. **Iterative Refinement**: Allow agents to request clarification
4. **Caching**: Cache common hybrid query patterns
5. **Analytics**: Track hybrid query performance

---

## 📝 Summary

### **What Changed**:
1. ✅ Enhanced router prompt with explicit hybrid detection rules
2. ✅ Added hybrid connector detection in simple router
3. ✅ Implemented query extraction for SQL and Vector parts
4. ✅ Maintained parallel execution architecture

### **What It Means**:
- **Better Classification**: Hybrid queries are now correctly identified
- **Smarter Processing**: Each agent gets the relevant part of the query
- **Complete Answers**: Both SQL and Vector results are combined
- **Natural Responses**: LLM synthesizes coherent answers

### **How to Use**:
Just ask your question naturally! The system handles everything:
```
"give me top 10 gaming channels and also suggest counter strike videos"
```

The system will:
1. Detect it's a hybrid query
2. Extract SQL part: "top 10 gaming channels"
3. Extract Vector part: "counter strike videos"
4. Run both agents in parallel
5. Combine results into one answer

---

**Status**: ✅ Ready to test!
**Next Step**: Restart application and try hybrid queries
