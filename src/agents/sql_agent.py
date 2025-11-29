"""SQL Agent for structured database queries using LangChain"""

import os
from typing import Dict, Any, Optional
from pathlib import Path

from langchain_community.utilities import SQLDatabase
from langchain_openai import ChatOpenAI
from langchain_community.agent_toolkits import create_sql_agent
from loguru import logger

from .base_agent import BaseAgent
from ..config.settings import get_settings


class SQLAgent(BaseAgent):
    """
    SQL Agent that converts natural language queries to SQL and executes them.
    Uses LangChain's SQL agent toolkit for intelligent query generation.
    """
    
    def __init__(
        self,
        db_path: Optional[str] = None,
        api_key: Optional[str] = None,
        model: Optional[str] = None
    ):
        """
        Initialize SQL Agent.
        
        Args:
            db_path: Path to SQLite database
            api_key: OpenAI/OpenRouter API key
            model: LLM model to use
        """
        super().__init__(name="SQLAgent")
        
        settings = get_settings()
        
        # Database configuration
        self.db_path = db_path or settings.sql_db_path
        self.table_name = settings.sql_table_name
        
        # LLM configuration
        self.api_key = api_key or settings.openai_api_key
        self.model = model or settings.llm_model
        self.base_url = settings.openai_base_url
        
        if not self.api_key:
            raise ValueError(
                "API key is required. Set OPENAI_API_KEY in environment or .env file"
            )
        
        # Initialize components
        self._initialize_database()
        self._initialize_llm()
        self._initialize_agent()
        
        logger.info(f"SQL Agent initialized with database: {self.db_path}")
    
    def _initialize_database(self) -> None:
        """Initialize database connection"""
        if not os.path.exists(self.db_path):
            raise FileNotFoundError(
                f"Database file not found: {self.db_path}. "
                f"Please run the data processing pipeline first."
            )
        
        self.db = SQLDatabase.from_uri(f"sqlite:///{self.db_path}")
        logger.info(f"Connected to database: {self.db_path}")
    
    def _initialize_llm(self) -> None:
        """Initialize LLM for SQL generation"""
        self.llm = ChatOpenAI(
            model=self.model,
            temperature=0,
            api_key=self.api_key,
            base_url=self.base_url
        )
        logger.info(f"Initialized LLM: {self.model}")
    
    def _initialize_agent(self) -> None:
        """Initialize LangChain SQL agent"""
        
        # Create a detailed prefix with exact column names
        prefix = f"""You are an expert YouTube trends analyst with access to a SQLite database.

Database: {self.db_path}
Table: {self.table_name}

IMPORTANT - EXACT COLUMN NAMES (use these exactly as shown):
┌─────────────────────────────────┬──────────────────────────────────────┐
│ Column Name                     │ Description                          │
├─────────────────────────────────┼──────────────────────────────────────┤
│ video_id                        │ Unique identifier (TEXT)             │
│ title                           │ Video title (TEXT)                   │
│ description                     │ Video description (TEXT)             │
│ tags                            │ Space-separated tags (TEXT)          │
│ category_id                     │ Numeric category ID (INTEGER)        │
│ category_name                   │ Category name (TEXT)                 │
│ channel_title                   │ Channel name (TEXT)                  │
│ country                         │ Country code (TEXT)                  │
│ language                        │ Detected language (TEXT)             │
│ publish_time                    │ Publication timestamp (TIMESTAMP)    │
│ first_trend_date                │ First trending date (DATE)           │
│ last_trend_date                 │ Last trending date (DATE)            │
│ days_trending_unique            │ Unique days trending (INTEGER)       │
│ longest_consecutive_streak_days │ Longest streak (INTEGER)             │
│ views                           │ View count (INTEGER) ⚠️              │
│ likes                           │ Like count (INTEGER) ⚠️              │
│ comment_count                   │ Comment count (INTEGER) ⚠️           │
└─────────────────────────────────┴──────────────────────────────────────┘

⚠️ CRITICAL COLUMN NAME MAPPINGS:
- For VIEW COUNT: Use "views" NOT "view_count" or "view_counts"
- For LIKE COUNT: Use "likes" NOT "like_count" or "like_counts"
- For COMMENTS: Use "comment_count" NOT "comments" or "comment_counts"
- For CHANNEL: Use "channel_title" NOT "channel" or "channel_name"

COMMON QUERY PATTERNS:
1. Top channels by views: SELECT channel_title, SUM(views) AS total_views FROM videos GROUP BY channel_title ORDER BY total_views DESC LIMIT N;
2. Top videos by likes: SELECT title, likes, views FROM videos ORDER BY likes DESC LIMIT N;
3. Category analysis: SELECT category_name, COUNT(*) as count, AVG(views) as avg_views FROM videos GROUP BY category_name;
4. Trending analysis: SELECT title, days_trending_unique, longest_consecutive_streak_days FROM videos ORDER BY days_trending_unique DESC;

Your goal is to:
1. Understand the user's question
2. Generate SQL queries using the EXACT column names above
3. Execute them against the database
4. Return results in clear, natural language with PROPER MARKDOWN FORMATTING

RESPONSE FORMATTING REQUIREMENTS:
- Use markdown bullet points (- **Item**: Description) for lists
- Use **bold** for video titles, channel names, and important metrics
- Use proper markdown headings (##) for sections like "## Key Insights" or "## Summary"
- Format numbers with appropriate units (e.g., ≈X.X M views, XXX k likes)
- Structure responses with clear sections when appropriate

Example format:
Here are the top channels by views:

- **Channel Name 1** – ≈X.X M total views across Y videos
- **Channel Name 2** – ≈X.X M total views across Y videos

## Key Insights
- **Insight 1**: Description
- **Insight 2**: Description

If you encounter a "no such column" error, check the column names table above and use the exact names shown.
"""
        
        self.agent_executor = create_sql_agent(
            llm=self.llm,
            db=self.db,
            agent_type="openai-tools",
            verbose=True,
            handle_parsing_errors=True,
            prefix=prefix,
            max_iterations=15,
            agent_executor_kwargs={
                "handle_parsing_errors": True
            }
        )
        logger.info("SQL Agent executor initialized")
    
    def process_query(self, query: str, **kwargs) -> Dict[str, Any]:
        """
        Process a natural language query using SQL.
        
        Args:
            query: Natural language query
            **kwargs: Additional parameters
            
        Returns:
            Formatted response with results
        """
        if not self.validate_query(query):
            return self.format_response(
                success=False,
                error="Invalid query: Query cannot be empty"
            )
        
        try:
            logger.info(f"Processing SQL query: {query}")
            
            # Invoke the agent
            response = self.agent_executor.invoke({"input": query})
            
            # Extract output
            output = response.get("output", "I'm sorry, I couldn't find an answer.")
            
            logger.info("SQL query processed successfully")
            
            return self.format_response(
                success=True,
                data={
                    'answer': output,
                    'query_type': 'sql',
                    'source': 'structured_database'
                },
                metadata={
                    'database': self.db_path,
                    'table': self.table_name,
                    'model': self.model
                }
            )
            
        except Exception as e:
            logger.error(f"Error processing SQL query: {e}")
            return self.format_response(
                success=False,
                error=f"SQL Agent error: {str(e)}"
            )
    
    def get_capabilities(self) -> Dict[str, Any]:
        """
        Get SQL Agent capabilities.
        
        Returns:
            Dictionary describing capabilities
        """
        return {
            'name': self.name,
            'type': 'sql',
            'description': 'Handles structured queries requiring aggregations, filtering, and statistical analysis',
            'capabilities': [
                'Aggregation queries (COUNT, SUM, AVG, MAX, MIN)',
                'Filtering by categories, channels, dates',
                'Sorting and ranking (TOP N queries)',
                'Statistical analysis (trends over time)',
                'Complex joins and grouping',
                'Temporal analysis (date ranges, trending periods)'
            ],
            'best_for': [
                'Which category has the most videos?',
                'Top 10 channels by views',
                'Average likes per category',
                'Videos trending for more than X days',
                'Comparison between categories',
                'Statistical summaries'
            ],
            'database': self.db_path,
            'table': self.table_name
        }
    
    def get_schema_info(self) -> str:
        """
        Get database schema information.
        
        Returns:
            Schema description string
        """
        try:
            return self.db.get_table_info()
        except Exception as e:
            logger.error(f"Error getting schema info: {e}")
            return "Schema information unavailable"
    
    def execute_raw_sql(self, sql_query: str) -> Dict[str, Any]:
        """
        Execute a raw SQL query (for advanced users).
        
        Args:
            sql_query: Raw SQL query string
            
        Returns:
            Query results
        """
        try:
            logger.info(f"Executing raw SQL: {sql_query}")
            result = self.db.run(sql_query)
            
            return self.format_response(
                success=True,
                data={'result': result},
                metadata={'query': sql_query}
            )
            
        except Exception as e:
            logger.error(f"Error executing raw SQL: {e}")
            return self.format_response(
                success=False,
                error=f"SQL execution error: {str(e)}"
            )
