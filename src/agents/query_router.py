"""Query Router for classifying and routing queries to appropriate agents"""

from typing import Dict, Any, Literal, Optional
from enum import Enum

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
# from langchain.output_parsers import PydanticOutputParser
from langchain_core.output_parsers import PydanticOutputParser

from pydantic import BaseModel, Field
from loguru import logger

from ..config.settings import get_settings


class QueryType(str, Enum):
    """Enum for query types"""
    SQL = "sql"
    VECTOR = "vector"
    HYBRID = "hybrid"
    UNKNOWN = "unknown"


class QueryClassification(BaseModel):
    """Structured output for query classification"""
    query_type: QueryType = Field(
        description="Type of query: 'sql' for structured/analytical, 'vector' for semantic/content-based, 'hybrid' for both"
    )
    confidence: float = Field(
        description="Confidence score between 0 and 1",
        ge=0.0,
        le=1.0
    )
    reasoning: str = Field(
        description="Brief explanation of why this classification was chosen"
    )
    suggested_agent: str = Field(
        description="Which agent(s) should handle this query"
    )


class QueryRouter:
    """
    Intelligent query router that classifies queries and routes them to appropriate agents.
    Uses LLM-based classification with structured output.
    """
    
    def __init__(
        self,
        api_key: Optional[str] = None,
        model: Optional[str] = None
    ):
        """
        Initialize Query Router.
        
        Args:
            api_key: OpenAI/OpenRouter API key
            model: LLM model to use
        """
        settings = get_settings()
        
        self.api_key = api_key or settings.openai_api_key
        self.model = model or settings.llm_model
        self.base_url = settings.openai_base_url
        
        if not self.api_key:
            raise ValueError(
                "API key is required for Query Router. "
                "Set OPENAI_API_KEY in environment or .env file"
            )
        
        self._initialize_llm()
        self._initialize_chain()
        
        logger.info("Query Router initialized")
    
    def _initialize_llm(self) -> None:
        """Initialize LLM for classification"""
        self.llm = ChatOpenAI(
            model=self.model,
            temperature=0,
            api_key=self.api_key,
            base_url=self.base_url
        )
        logger.info(f"Router LLM initialized: {self.model}")
    
    def _initialize_chain(self) -> None:
        """Initialize classification chain"""
        # Create output parser
        self.parser = PydanticOutputParser(pydantic_object=QueryClassification)
        
        # Create prompt template
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", """You are an intelligent query router for a YouTube trends analysis system.
You must classify user queries into one of these types:

1. **SQL** - For structured, analytical queries requiring:
   - Aggregations (count, sum, average, max, min)
   - Filtering by specific attributes (category, channel, date ranges)
   - Sorting and ranking (top N, bottom N)
   - Statistical analysis
   - Comparisons between groups
   - Temporal analysis (trends over time)
   
   Examples:
   - "Which category has the most videos?"
   - "Top 10 channels by views"
   - "Average likes for Gaming category"
   - "Videos trending for more than 5 days"
   - "Compare views between Music and Sports"

2. **VECTOR** - For semantic, content-based queries requiring:
   - Similarity search
   - Content recommendations
   - Topic-based search
   - Conceptual queries
   - Natural language understanding
   - Exploratory searches
   
   Examples:
   - "Find videos about cooking tutorials"
   - "Videos similar to tech reviews"
   - "Content related to fitness and wellness"
   - "Search for motivational content"
   - "Videos discussing climate change"

3. **HYBRID** - For queries requiring both:
   - Semantic search with statistical filters
   - Content-based search with aggregations
   - Complex multi-step analysis
   
   Examples:
   - "Find popular gaming videos about Minecraft"
   - "Most viewed videos about cooking in the last month"
   - "Top educational content about programming"

4. **UNKNOWN** - For unclear or out-of-scope queries

Analyze the query and provide a classification with reasoning.

{format_instructions}
"""),
            ("user", "Query: {query}")
        ])
        
        # Create chain
        self.chain = self.prompt | self.llm | self.parser
        
        logger.info("Classification chain initialized")
    
    def classify_query(self, query: str) -> QueryClassification:
        """
        Classify a query into appropriate type.
        
        Args:
            query: User query string
            
        Returns:
            QueryClassification object
        """
        try:
            logger.info(f"Classifying query: {query}")
            
            # Invoke chain
            result = self.chain.invoke({
                "query": query,
                "format_instructions": self.parser.get_format_instructions()
            })
            
            logger.info(
                f"Query classified as: {result.query_type} "
                f"(confidence: {result.confidence:.2f})"
            )
            
            return result
            
        except Exception as e:
            logger.error(f"Error classifying query: {e}")
            # Return default classification
            return QueryClassification(
                query_type=QueryType.UNKNOWN,
                confidence=0.0,
                reasoning=f"Classification failed: {str(e)}",
                suggested_agent="none"
            )
    
    def route_query(self, query: str) -> Dict[str, Any]:
        """
        Classify and route a query.
        
        Args:
            query: User query string
            
        Returns:
            Routing information dictionary
        """
        classification = self.classify_query(query)
        
        # Determine which agents to use
        agents_to_use = []
        
        if classification.query_type == QueryType.SQL:
            agents_to_use = ["sql"]
        elif classification.query_type == QueryType.VECTOR:
            agents_to_use = ["vector"]
        elif classification.query_type == QueryType.HYBRID:
            agents_to_use = ["sql", "vector"]
        else:
            agents_to_use = []
        
        routing_info = {
            'query': query,
            'classification': {
                'type': classification.query_type.value,
                'confidence': classification.confidence,
                'reasoning': classification.reasoning,
                'suggested_agent': classification.suggested_agent
            },
            'agents': agents_to_use,
            'execution_strategy': self._determine_execution_strategy(
                classification.query_type
            )
        }
        
        logger.info(f"Query routed to agents: {agents_to_use}")
        
        return routing_info
    
    def _determine_execution_strategy(self, query_type: QueryType) -> str:
        """
        Determine execution strategy based on query type.
        
        Args:
            query_type: Classified query type
            
        Returns:
            Execution strategy string
        """
        strategies = {
            QueryType.SQL: "single_agent",
            QueryType.VECTOR: "single_agent",
            QueryType.HYBRID: "multi_agent_parallel",
            QueryType.UNKNOWN: "fallback"
        }
        
        return strategies.get(query_type, "fallback")
    
    def get_routing_stats(self) -> Dict[str, Any]:
        """
        Get routing statistics (placeholder for future implementation).
        
        Returns:
            Statistics dictionary
        """
        return {
            'total_queries': 0,
            'sql_queries': 0,
            'vector_queries': 0,
            'hybrid_queries': 0,
            'unknown_queries': 0
        }


class SimpleQueryRouter:
    """
    Simplified rule-based query router (fallback when LLM is unavailable).
    Uses keyword matching for classification.
    """
    
    SQL_KEYWORDS = [
        'how many', 'count', 'total', 'average', 'sum', 'top', 'bottom',
        'most', 'least', 'highest', 'lowest', 'compare', 'comparison',
        'statistics', 'stat', 'number of', 'percentage', 'ratio'
    ]
    
    VECTOR_KEYWORDS = [
        'find', 'search', 'similar', 'like', 'about', 'related to',
        'videos on', 'content about', 'show me', 'recommend', 'suggestion'
    ]
    
    def __init__(self):
        """Initialize simple router"""
        logger.info("Simple Query Router initialized (rule-based)")
    
    def classify_query(self, query: str) -> QueryClassification:
        """
        Classify query using simple keyword matching.
        
        Args:
            query: User query
            
        Returns:
            QueryClassification
        """
        query_lower = query.lower()
        
        sql_score = sum(1 for kw in self.SQL_KEYWORDS if kw in query_lower)
        vector_score = sum(1 for kw in self.VECTOR_KEYWORDS if kw in query_lower)
        
        if sql_score > vector_score:
            query_type = QueryType.SQL
            confidence = min(0.7, 0.5 + sql_score * 0.1)
            reasoning = "Query contains analytical keywords"
        elif vector_score > sql_score:
            query_type = QueryType.VECTOR
            confidence = min(0.7, 0.5 + vector_score * 0.1)
            reasoning = "Query contains semantic search keywords"
        elif sql_score > 0 and vector_score > 0:
            query_type = QueryType.HYBRID
            confidence = 0.6
            reasoning = "Query contains both analytical and semantic keywords"
        else:
            query_type = QueryType.VECTOR  # Default to vector search
            confidence = 0.5
            reasoning = "No clear indicators, defaulting to semantic search"
        
        return QueryClassification(
            query_type=query_type,
            confidence=confidence,
            reasoning=reasoning,
            suggested_agent=query_type.value
        )
    
    def route_query(self, query: str) -> Dict[str, Any]:
        """
        Route query using simple classification.
        
        Args:
            query: User query
            
        Returns:
            Routing information
        """
        classification = self.classify_query(query)
        
        agents_to_use = []
        if classification.query_type == QueryType.SQL:
            agents_to_use = ["sql"]
        elif classification.query_type == QueryType.VECTOR:
            agents_to_use = ["vector"]
        elif classification.query_type == QueryType.HYBRID:
            agents_to_use = ["sql", "vector"]
        
        return {
            'query': query,
            'classification': {
                'type': classification.query_type.value,
                'confidence': classification.confidence,
                'reasoning': classification.reasoning,
                'suggested_agent': classification.suggested_agent
            },
            'agents': agents_to_use,
            'execution_strategy': 'single_agent' if len(agents_to_use) == 1 else 'multi_agent_parallel'
        }
