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
        self.agent_executor = create_sql_agent(
            llm=self.llm,
            db=self.db,
            agent_type="openai-tools",
            verbose=True,
            handle_parsing_errors=True,
            extra_prompt_messages=[
                f"""You are an expert YouTube trends analyst with access to a SQLite database.
                
                Database: {self.db_path}
                Table: {self.table_name}
                
                The 'videos' table contains the following columns:
                - video_id: Unique identifier
                - title: Video title
                - description: Video description
                - tags: Space-separated tags
                - category_id: Numeric category ID
                - category_name: Category name (Music, Gaming, Education, etc.)
                - channel_title: Channel name
                - country: Country code (CA for Canada)
                - language: Detected language
                - publish_time: When video was published
                - first_trend_date: First date video trended
                - last_trend_date: Last date video trended
                - days_trending_unique: Number of unique days trending
                - longest_consecutive_streak_days: Longest consecutive trending streak
                - views: View count
                - likes: Like count
                - comment_count: Comment count
                
                Your goal is to:
                1. Understand the user's question
                2. Generate appropriate SQL queries
                3. Execute them against the database
                4. Return results in clear, natural language
                
                Focus on providing insights about trending patterns, popular categories,
                top channels, engagement metrics, and temporal trends.
                """
            ]
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
