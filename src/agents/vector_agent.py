"""Vector Database Agent for semantic search using Qdrant.

This module provides a comprehensive vector search agent that handles:
- Semantic similarity search across video content
- Content-based recommendations
- Filtered search by category, views, and other metadata
- Natural language query understanding
- Multi-modal search capabilities

The agent uses Qdrant as the vector database backend and supports
various embedding models for semantic understanding.

Author: YouTube Trends Analysis Team
Date: 2025-11-12
"""

from typing import Dict, Any, List, Optional, Union
import numpy as np
from loguru import logger

from langchain_openai import ChatOpenAI

from .base_agent import BaseAgent
from ..config.settings import get_settings
from ..vectordb.client import QdrantManager
from ..vectordb.operations import VectorDBOperations
from ..embeddings.factory import get_embedding_model
from ..embeddings.base import BaseEmbedding


class VectorAgent(BaseAgent):
    """
    Vector Database Agent for semantic search and content recommendations.
    
    This agent provides advanced semantic search capabilities over YouTube video
    content using vector embeddings and similarity search. It supports:
    
    Features:
        - Semantic similarity search
        - Content-based recommendations
        - Filtered search (category, views, country)
        - Find similar videos
        - Hybrid search combining semantic and metadata filters
        - Natural language response generation
    
    Architecture:
        - Vector DB: Qdrant for efficient similarity search
        - Embeddings: Sentence transformers or OpenAI embeddings
        - LLM: For natural language response generation
    
    Example:
        >>> agent = VectorAgent()
        >>> result = agent.search_videos("funny cat videos", limit=5)
        >>> similar = agent.find_similar_videos("video_id_123")
    """
    
    def __init__(
        self,
        api_key: Optional[str] = None,
        model: Optional[str] = None,
        default_limit: int = 5,
        min_score_threshold: float = 0.3
    ):
        """
        Initialize Vector Agent with all required components.
        
        Args:
            api_key: OpenAI/OpenRouter API key for LLM response generation
            model: LLM model name (e.g., 'gpt-4', 'claude-3-haiku')
            default_limit: Default number of results to return
            min_score_threshold: Minimum similarity score threshold (0-1)
            
        Raises:
            ConnectionError: If unable to connect to Qdrant
            ValueError: If configuration is invalid
        """
        super().__init__(name="VectorAgent")
        
        # Load settings
        settings = get_settings()
        
        # Configuration
        self.api_key = api_key or settings.openai_api_key
        self.model = model or settings.llm_model
        self.base_url = settings.openai_base_url
        self.default_limit = default_limit
        self.min_score_threshold = min_score_threshold
        
        # Initialize components in order
        self._initialize_vector_db()
        self._initialize_embeddings()
        self._initialize_db_operations()
        
        # Initialize LLM for response generation (optional)
        if self.api_key:
            self._initialize_llm()
        else:
            logger.warning(
                "No API key provided. LLM-based response generation disabled. "
                "Set OPENAI_API_KEY in environment for enhanced responses."
            )
            self.llm = None
        
        logger.info(
            f"Vector Agent initialized successfully "
            f"(limit={default_limit}, threshold={min_score_threshold})"
        )
    
    def _initialize_vector_db(self) -> None:
        """
        Initialize connection to Qdrant vector database.
        
        Raises:
            ConnectionError: If unable to connect to Qdrant
        """
        try:
            self.vector_db = QdrantManager()
            
            # Verify collection exists
            if not self.vector_db.collection_exists():
                logger.warning(
                    f"Collection '{self.vector_db.collection_name}' does not exist. "
                    "Please run data ingestion pipeline first."
                )
            
            logger.info(
                f"Connected to Qdrant at {self.vector_db.host}:{self.vector_db.port}"
            )
            
        except Exception as e:
            logger.error(f"Failed to initialize Qdrant: {e}")
            raise ConnectionError(
                f"Unable to connect to Qdrant vector database: {e}"
            ) from e
    
    def _initialize_embeddings(self) -> None:
        """
        Initialize embedding model for text vectorization.
        
        Raises:
            RuntimeError: If embedding model fails to load
        """
        try:
            self.embedding_model: BaseEmbedding = get_embedding_model()
            self.embedding_dim = self.embedding_model.get_dimension()
            
            logger.info(
                f"Embedding model initialized: {self.embedding_model.__class__.__name__} "
                f"(dimension={self.embedding_dim})"
            )
            
        except Exception as e:
            logger.error(f"Failed to initialize embeddings: {e}")
            raise RuntimeError(
                f"Unable to load embedding model: {e}"
            ) from e
    
    def _initialize_db_operations(self) -> None:
        """
        Initialize vector database operations handler.
        
        Raises:
            RuntimeError: If operations handler fails to initialize
        """
        try:
            self.db_ops = VectorDBOperations(qdrant_manager=self.vector_db)
            logger.info("Vector DB operations initialized")
            
        except Exception as e:
            logger.error(f"Failed to initialize DB operations: {e}")
            raise RuntimeError(
                f"Unable to initialize vector DB operations: {e}"
            ) from e
    
    def _initialize_llm(self) -> None:
        """
        Initialize Large Language Model for natural language response generation.
        
        The LLM is used to generate human-friendly responses based on search results.
        """
        try:
            self.llm = ChatOpenAI(
                model=self.model,
                temperature=0.3,  # Low temperature for consistent, factual responses
                api_key=self.api_key,
                base_url=self.base_url
            )
            logger.info(f"LLM initialized: {self.model}")
            
        except Exception as e:
            logger.error(f"Failed to initialize LLM: {e}")
            logger.warning("Falling back to simple response generation")
            self.llm = None
    
    # ==================== Core Query Processing ====================
    
    def process_query(self, query: str, **kwargs) -> Dict[str, Any]:
        """
        Process a natural language semantic search query.
        
        This is the main entry point for the vector agent. It handles:
        1. Query validation
        2. Embedding generation
        3. Vector similarity search
        4. Result filtering and ranking
        5. Natural language response generation
        
        Args:
            query: Natural language search query (e.g., "funny cat videos")
            **kwargs: Additional parameters:
                - limit (int): Number of results to return
                - score_threshold (float): Minimum similarity score
                - filters (dict): Metadata filters (category, min_views, etc.)
                - include_metadata (bool): Include full metadata in response
            
        Returns:
            Dict containing:
                - success (bool): Whether query was successful
                - data (dict): Search results and answer
                - metadata (dict): Query metadata and statistics
                - error (str): Error message if failed
                
        Example:
            >>> result = agent.process_query(
            ...     "gaming videos",
            ...     limit=10,
            ...     filters={'category': 'Gaming', 'min_views': 100000}
            ... )
        """
        # Validate query
        if not self.validate_query(query):
            return self.format_response(
                success=False,
                error="Invalid query: Query cannot be empty or None"
            )
        
        try:
            logger.info(f"Processing vector search query: '{query}'")
            
            # Extract parameters with defaults
            limit = kwargs.get('limit', kwargs.get('top_k', self.default_limit))
            score_threshold = kwargs.get('score_threshold', self.min_score_threshold)
            filters = kwargs.get('filters', None)
            include_metadata = kwargs.get('include_metadata', False)
            
            # Perform semantic search
            results = self.search_videos(
                query=query,
                limit=limit,
                score_threshold=score_threshold,
                filters=filters
            )
            
            # Handle no results
            if not results:
                logger.info(f"No results found for query: '{query}'")
                return self.format_response(
                    success=True,
                    data={
                        'answer': self._generate_no_results_message(query, filters),
                        'results': [],
                        'query_type': 'vector',
                        'source': 'semantic_search'
                    },
                    metadata={
                        'query': query,
                        'limit': limit,
                        'score_threshold': score_threshold,
                        'num_results': 0
                    }
                )
            
            # Format results for output
            formatted_results = self._format_search_results(
                results,
                include_metadata=include_metadata
            )
            
            # Generate natural language response
            if self.llm:
                answer = self._generate_llm_response(query, results, filters)
            else:
                answer = self._generate_simple_response(query, results)
            
            logger.info(
                f"Vector search completed: {len(results)} results found "
                f"(avg_score={np.mean([r['score'] for r in results]):.3f})"
            )
            
            return self.format_response(
                success=True,
                data={
                    'answer': answer,
                    'results': formatted_results,
                    'query_type': 'vector',
                    'source': 'semantic_search'
                },
                metadata={
                    'query': query,
                    'limit': limit,
                    'score_threshold': score_threshold,
                    'num_results': len(results),
                    'avg_score': float(np.mean([r['score'] for r in results])),
                    'model': self.model if self.llm else 'no_llm',
                    'filters_applied': filters is not None
                }
            )
            
        except Exception as e:
            logger.error(f"Error processing vector query: {e}", exc_info=True)
            return self.format_response(
                success=False,
                error=f"Vector search failed: {str(e)}"
            )
    
    # ==================== Search Methods ====================
    
    def search_videos(
        self,
        query: str,
        limit: int = 10,
        score_threshold: Optional[float] = None,
        filters: Optional[Dict[str, Any]] = None
    ) -> List[Dict[str, Any]]:
        """
        Perform semantic search for videos matching the query.
        
        Args:
            query: Natural language search query
            limit: Maximum number of results to return
            score_threshold: Minimum similarity score (0-1)
            filters: Optional metadata filters (category, min_views, etc.)
            
        Returns:
            List of matching videos with scores and metadata
            
        Example:
            >>> results = agent.search_videos(
            ...     "music videos",
            ...     limit=5,
            ...     filters={'category': 'Music', 'min_views': 1000000}
            ... )
        """
        try:
            logger.debug(f"Searching videos: query='{query}', limit={limit}")
            
            # Generate query embedding
            query_vector = self.embedding_model.encode_single(query)
            
            # Perform vector search
            results = self.db_ops.search(
                query_vector=query_vector,
                limit=limit,
                score_threshold=score_threshold or self.min_score_threshold,
                filters=filters
            )
            
            logger.debug(f"Found {len(results)} results")
            return results
            
        except Exception as e:
            logger.error(f"Error in search_videos: {e}", exc_info=True)
            raise
    
    def find_similar_videos(
        self,
        video_id: str,
        limit: int = 10,
        exclude_self: bool = True
    ) -> Dict[str, Any]:
        """
        Find videos similar to a given video based on content similarity.
        
        Args:
            video_id: ID of the reference video
            limit: Number of similar videos to return
            exclude_self: Whether to exclude the reference video from results
            
        Returns:
            Formatted response with similar videos
            
        Example:
            >>> result = agent.find_similar_videos("abc123", limit=5)
        """
        try:
            logger.info(f"Finding videos similar to: {video_id}")
            
            # Get the reference video
            reference_video = self.db_ops.get_document_by_id(video_id)
            
            if not reference_video:
                return self.format_response(
                    success=False,
                    error=f"Video '{video_id}' not found in database"
                )
            
            # Use the video's text/metadata for similarity search
            video_text = reference_video.get('metadata', {}).get('text', '')
            
            if not video_text:
                # Fallback to title + tags if no text available
                title = reference_video.get('title', '')
                tags = reference_video.get('metadata', {}).get('tags', [])
                video_text = f"{title} {' '.join(tags)}"
            
            # Search for similar videos
            results = self.search_videos(
                query=video_text,
                limit=limit + (1 if exclude_self else 0)
            )
            
            # Remove reference video if requested
            if exclude_self:
                results = [r for r in results if r.get('id') != video_id][:limit]
            
            # Format response
            formatted_results = self._format_search_results(results)
            
            answer = f"Found {len(results)} videos similar to '{reference_video.get('title', video_id)}':"
            
            return self.format_response(
                success=True,
                data={
                    'answer': answer,
                    'reference_video': {
                        'id': video_id,
                        'title': reference_video.get('title', ''),
                        'channel': reference_video.get('channel', '')
                    },
                    'similar_videos': formatted_results,
                    'query_type': 'similarity',
                    'source': 'vector_similarity'
                },
                metadata={
                    'reference_video_id': video_id,
                    'num_results': len(results)
                }
            )
            
        except Exception as e:
            logger.error(f"Error finding similar videos: {e}", exc_info=True)
            return self.format_response(
                success=False,
                error=f"Failed to find similar videos: {str(e)}"
            )
    
    def search_by_category(
        self,
        query: str,
        category: str,
        limit: int = 10
    ) -> Dict[str, Any]:
        """
        Search for videos within a specific category.
        
        Args:
            query: Search query
            category: Category name (e.g., "Gaming", "Music", "Education")
            limit: Maximum number of results
            
        Returns:
            Formatted response with search results
            
        Example:
            >>> result = agent.search_by_category("tutorials", "Education", limit=10)
        """
        logger.info(f"Searching in category '{category}': {query}")
        
        return self.process_query(
            query=query,
            limit=limit,
            filters={'category': category}
        )
    
    def search_popular_videos(
        self,
        query: str,
        min_views: int = 100000,
        limit: int = 10
    ) -> Dict[str, Any]:
        """
        Search for popular videos matching the query.
        
        Args:
            query: Search query
            min_views: Minimum view count threshold
            limit: Maximum number of results
            
        Returns:
            Formatted response with popular videos
            
        Example:
            >>> result = agent.search_popular_videos("gaming", min_views=1000000)
        """
        logger.info(f"Searching popular videos (min_views={min_views}): {query}")
        
        return self.process_query(
            query=query,
            limit=limit,
            filters={'min_views': min_views}
        )
    
    def hybrid_search(
        self,
        query: str,
        category: Optional[str] = None,
        min_views: Optional[int] = None,
        max_views: Optional[int] = None,
        limit: int = 10
    ) -> Dict[str, Any]:
        """
        Perform hybrid search combining semantic search with metadata filters.
        
        Args:
            query: Natural language search query
            category: Filter by category
            min_views: Minimum view count
            max_views: Maximum view count
            limit: Number of results
            
        Returns:
            Formatted response with filtered search results
            
        Example:
            >>> result = agent.hybrid_search(
            ...     "funny videos",
            ...     category="Entertainment",
            ...     min_views=50000,
            ...     max_views=500000
            ... )
        """
        logger.info(f"Hybrid search: {query} (filters: category={category}, views={min_views}-{max_views})")
        
        filters = {}
        if category:
            filters['category'] = category
        if min_views:
            filters['min_views'] = min_views
        if max_views:
            filters['max_views'] = max_views
        
        return self.process_query(
            query=query,
            limit=limit,
            filters=filters if filters else None
        )
    
    # ==================== Response Generation ====================
    
    def _format_search_results(
        self,
        results: List[Dict[str, Any]],
        include_metadata: bool = False
    ) -> List[Dict[str, Any]]:
        """
        Format search results for consistent output.
        
        Args:
            results: Raw search results from vector DB
            include_metadata: Whether to include full metadata
            
        Returns:
            List of formatted result dictionaries
        """
        formatted = []
        
        for i, result in enumerate(results, 1):
            formatted_result = {
                'rank': i,
                'score': round(result.get('score', 0), 4),
                'video_id': result.get('id', 'unknown'),
                'title': result.get('title', 'No title'),
                'channel': result.get('channel', 'Unknown channel'),
                'category': result.get('category', 'Unknown'),
                'views': result.get('views', 0),
                'likes': result.get('likes', 0),
                'tags': result.get('tags', [])[:5]  # First 5 tags only
            }
            
            if include_metadata:
                formatted_result['metadata'] = result.get('metadata', {})
            
            formatted.append(formatted_result)
        
        return formatted
    
    def _generate_simple_response(
        self,
        query: str,
        results: List[Dict[str, Any]]
    ) -> str:
        """
        Generate a simple text response without LLM.
        
        Args:
            query: Original search query
            results: Search results
            
        Returns:
            Formatted response string
        """
        if not results:
            return "No relevant videos found."
        
        response_parts = [f"Found {len(results)} videos matching '{query}':\n"]
        
        for i, result in enumerate(results[:5], 1):
            title = result.get('title', 'Unknown')
            channel = result.get('channel', 'Unknown')
            views = result.get('views', 0)
            score = result.get('score', 0)
            
            response_parts.append(
                f"{i}. {title}\n"
                f"   Channel: {channel} | Views: {views:,} | Relevance: {score:.2%}"
            )
        
        if len(results) > 5:
            response_parts.append(f"\n... and {len(results) - 5} more results")
        
        return "\n".join(response_parts)
    
    def _generate_llm_response(
        self,
        query: str,
        results: List[Dict[str, Any]],
        filters: Optional[Dict[str, Any]] = None
    ) -> str:
        """
        Generate natural language response using LLM.
        
        Args:
            query: Original search query
            results: Search results
            filters: Applied filters (if any)
            
        Returns:
            Natural language response
        """
        try:
            # Prepare context from results
            context_parts = []
            for i, result in enumerate(results[:5], 1):
                context_parts.append(
                    f"{i}. Title: {result.get('title', 'Unknown')}\n"
                    f"   Channel: {result.get('channel', 'Unknown')}\n"
                    f"   Category: {result.get('category', 'Unknown')}\n"
                    f"   Views: {result.get('views', 0):,}\n"
                    f"   Likes: {result.get('likes', 0):,}\n"
                    f"   Relevance Score: {result.get('score', 0):.2%}"
                )
            
            context = "\n\n".join(context_parts)
            
            # Add filter information if present
            filter_info = ""
            if filters:
                filter_desc = []
                if 'category' in filters:
                    filter_desc.append(f"Category: {filters['category']}")
                if 'min_views' in filters:
                    filter_desc.append(f"Min Views: {filters['min_views']:,}")
                if 'max_views' in filters:
                    filter_desc.append(f"Max Views: {filters['max_views']:,}")
                
                if filter_desc:
                    filter_info = f"\n\nFilters Applied: {', '.join(filter_desc)}"
            
            # Create prompt
            prompt = f"""You are a YouTube trends analyst. Based on the semantic search results below, 
provide a helpful and informative answer to the user's query using PROPER MARKDOWN FORMATTING.

User Query: {query}{filter_info}

Search Results:
{context}

IMPORTANT: Format your response using proper markdown:
1. Use a brief introductory sentence
2. List videos using markdown bullet points (- **"Video Title" – Channel Name** (views) – description)
3. Add a "## Patterns & Takeaways" section with markdown bullet points
4. Use **bold** for video titles and channel names
5. Use proper markdown headings (##) for sections
6. Keep the response concise and well-structured

Example format:
Here are the top videos for [topic]:

- **"Video Title" – Channel Name** (≈X.X M views) – Brief description highlighting what makes it relevant.
- **"Another Video" – Channel** (≈XXX k views) – Description.

## Patterns & Takeaways
- **Pattern 1**: Description
- **Pattern 2**: Description

Response:"""
            
            # Generate response
            response = self.llm.invoke(prompt)
            return response.content
            
        except Exception as e:
            logger.error(f"Error generating LLM response: {e}")
            # Fallback to simple response
            return self._generate_simple_response(query, results)
    
    def _generate_no_results_message(
        self,
        query: str,
        filters: Optional[Dict[str, Any]] = None
    ) -> str:
        """
        Generate a helpful message when no results are found.
        
        Args:
            query: Original search query
            filters: Applied filters (if any)
            
        Returns:
            Helpful no-results message
        """
        message = f"No videos found matching '{query}'"
        
        if filters:
            filter_desc = []
            if 'category' in filters:
                filter_desc.append(f"category '{filters['category']}'")
            if 'min_views' in filters:
                filter_desc.append(f"minimum {filters['min_views']:,} views")
            
            if filter_desc:
                message += f" with {' and '.join(filter_desc)}"
        
        message += ".\n\nTry:\n"
        message += "- Using different keywords\n"
        message += "- Removing or relaxing filters\n"
        message += "- Using more general terms"
        
        return message
    
    # ==================== Utility Methods ====================
    
    def get_capabilities(self) -> Dict[str, Any]:
        """
        Get Vector Agent capabilities and features.
        
        Returns:
            Dictionary describing agent capabilities
        """
        return {
            'name': self.name,
            'type': 'vector',
            'description': 'Semantic search and content-based recommendations using vector embeddings',
            'capabilities': [
                'Semantic similarity search',
                'Content-based recommendations',
                'Find similar videos',
                'Natural language understanding',
                'Contextual search across titles, descriptions, tags',
                'Fuzzy matching and concept search',
                'Filtered search by category, views, country',
                'Hybrid search combining semantic + metadata filters'
            ],
            'best_for': [
                'Find videos about [topic]',
                'Videos similar to [description]',
                'Content related to [concept]',
                'Search for videos discussing [theme]',
                'Recommendations based on interests',
                'Exploratory searches',
                'Content discovery'
            ],
            'vector_db': {
                'type': 'Qdrant',
                'host': self.vector_db.host,
                'port': self.vector_db.port,
                'collection': self.vector_db.collection_name
            },
            'embedding_model': {
                'name': self.embedding_model.__class__.__name__,
                'dimension': self.embedding_dim
            },
            'llm': {
                'enabled': self.llm is not None,
                'model': self.model if self.llm else None
            }
        }
    
    def get_stats(self) -> Dict[str, Any]:
        """
        Get statistics about the vector database.
        
        Returns:
            Dictionary with database statistics
        """
        try:
            info = self.vector_db.get_collection_info()
            total_docs = self.db_ops.count_documents()
            
            return {
                'collection_name': info.get('name'),
                'total_videos': total_docs,
                'status': info.get('status'),
                'embedding_dimension': self.embedding_dim,
                'default_limit': self.default_limit,
                'min_score_threshold': self.min_score_threshold
            }
            
        except Exception as e:
            logger.error(f"Error getting stats: {e}")
            return {
                'error': str(e),
                'embedding_dimension': self.embedding_dim
            }
    
    def health_check(self) -> Dict[str, Any]:
        """
        Perform health check on all components.
        
        Returns:
            Health status of all components
        """
        health = {
            'agent': 'healthy',
            'components': {}
        }
        
        # Check vector DB
        try:
            self.vector_db.get_collection_info()
            health['components']['vector_db'] = 'healthy'
        except Exception as e:
            health['components']['vector_db'] = f'unhealthy: {str(e)}'
            health['agent'] = 'degraded'
        
        # Check embedding model
        try:
            test_embedding = self.embedding_model.encode_single("test")
            health['components']['embedding_model'] = 'healthy'
        except Exception as e:
            health['components']['embedding_model'] = f'unhealthy: {str(e)}'
            health['agent'] = 'degraded'
        
        # Check LLM
        if self.llm:
            health['components']['llm'] = 'healthy'
        else:
            health['components']['llm'] = 'disabled'
        
        return health
