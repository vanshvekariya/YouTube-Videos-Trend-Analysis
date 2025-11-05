"""Vector DB Agent for semantic search using Qdrant"""

from typing import Dict, Any, List, Optional
from loguru import logger

from langchain_openai import ChatOpenAI

from .base_agent import BaseAgent
from ..config.settings import get_settings
from ..vectordb.client import QdrantManager
from ..embeddings.factory import get_embedding_model
from ..search.semantic_search import SemanticSearch


class VectorAgent(BaseAgent):
    """
    Vector DB Agent that performs semantic search on video embeddings.
    Uses Qdrant for vector storage and retrieval.
    """
    
    def __init__(
        self,
        api_key: Optional[str] = None,
        model: Optional[str] = None,
        top_k: int = 5
    ):
        """
        Initialize Vector Agent.
        
        Args:
            api_key: OpenAI/OpenRouter API key for LLM
            model: LLM model to use for response generation
            top_k: Number of results to retrieve
        """
        super().__init__(name="VectorAgent")
        
        settings = get_settings()
        
        # LLM configuration
        self.api_key = api_key or settings.openai_api_key
        self.model = model or settings.llm_model
        self.base_url = settings.openai_base_url
        self.top_k = top_k
        
        # Initialize components
        self._initialize_vector_db()
        self._initialize_embeddings()
        self._initialize_search()
        
        if self.api_key:
            self._initialize_llm()
        else:
            logger.warning("No API key provided, LLM-based response generation disabled")
            self.llm = None
        
        logger.info("Vector Agent initialized successfully")
    
    def _initialize_vector_db(self) -> None:
        """Initialize Qdrant vector database connection"""
        try:
            self.vector_db = QdrantManager()
            logger.info("Connected to Qdrant vector database")
        except Exception as e:
            logger.error(f"Failed to initialize Qdrant: {e}")
            raise
    
    def _initialize_embeddings(self) -> None:
        """Initialize embedding model"""
        try:
            self.embedding_model = get_embedding_model()
            logger.info("Embedding model initialized")
        except Exception as e:
            logger.error(f"Failed to initialize embeddings: {e}")
            raise
    
    def _initialize_search(self) -> None:
        """Initialize semantic search"""
        try:
            self.search_engine = SemanticSearch(
                vector_db=self.vector_db,
                embedding_model=self.embedding_model
            )
            logger.info("Semantic search engine initialized")
        except Exception as e:
            logger.error(f"Failed to initialize search: {e}")
            raise
    
    def _initialize_llm(self) -> None:
        """Initialize LLM for response generation"""
        try:
            self.llm = ChatOpenAI(
                model=self.model,
                temperature=0.3,
                api_key=self.api_key,
                base_url=self.base_url
            )
            logger.info(f"Initialized LLM: {self.model}")
        except Exception as e:
            logger.error(f"Failed to initialize LLM: {e}")
            self.llm = None
    
    def process_query(self, query: str, **kwargs) -> Dict[str, Any]:
        """
        Process a semantic search query.
        
        Args:
            query: Natural language search query
            **kwargs: Additional parameters (top_k, filters, etc.)
            
        Returns:
            Formatted response with search results
        """
        if not self.validate_query(query):
            return self.format_response(
                success=False,
                error="Invalid query: Query cannot be empty"
            )
        
        try:
            logger.info(f"Processing vector search query: {query}")
            
            # Get parameters
            top_k = kwargs.get('top_k', self.top_k)
            filters = kwargs.get('filters', None)
            
            # Perform semantic search
            results = self.search_engine.search(
                query=query,
                top_k=top_k,
                filters=filters
            )
            
            if not results:
                return self.format_response(
                    success=True,
                    data={
                        'answer': "No relevant videos found for your query.",
                        'results': [],
                        'query_type': 'vector',
                        'source': 'semantic_search'
                    },
                    metadata={'top_k': top_k}
                )
            
            # Format results
            formatted_results = self._format_search_results(results)
            
            # Generate natural language response if LLM is available
            if self.llm:
                answer = self._generate_llm_response(query, results)
            else:
                answer = self._generate_simple_response(results)
            
            logger.info(f"Vector search completed: {len(results)} results found")
            
            return self.format_response(
                success=True,
                data={
                    'answer': answer,
                    'results': formatted_results,
                    'query_type': 'vector',
                    'source': 'semantic_search'
                },
                metadata={
                    'top_k': top_k,
                    'num_results': len(results),
                    'model': self.model if self.llm else 'no_llm'
                }
            )
            
        except Exception as e:
            logger.error(f"Error processing vector query: {e}")
            return self.format_response(
                success=False,
                error=f"Vector Agent error: {str(e)}"
            )
    
    def _format_search_results(self, results: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Format search results for output.
        
        Args:
            results: Raw search results
            
        Returns:
            Formatted results
        """
        formatted = []
        
        for i, result in enumerate(results, 1):
            payload = result.get('payload', {})
            
            formatted_result = {
                'rank': i,
                'score': round(result.get('score', 0), 4),
                'video_id': payload.get('video_id', 'unknown'),
                'title': payload.get('title', 'No title'),
                'channel': payload.get('channel', 'Unknown channel'),
                'category': payload.get('category', 'Unknown'),
                'views': payload.get('views', 0),
                'likes': payload.get('likes', 0),
                'tags': payload.get('tags', [])[:5]  # First 5 tags
            }
            
            formatted.append(formatted_result)
        
        return formatted
    
    def _generate_simple_response(self, results: List[Dict[str, Any]]) -> str:
        """
        Generate a simple text response without LLM.
        
        Args:
            results: Search results
            
        Returns:
            Response string
        """
        if not results:
            return "No relevant videos found."
        
        response_parts = [f"Found {len(results)} relevant videos:\n"]
        
        for i, result in enumerate(results[:5], 1):
            payload = result.get('payload', {})
            title = payload.get('title', 'Unknown')
            channel = payload.get('channel', 'Unknown')
            views = payload.get('views', 0)
            
            response_parts.append(
                f"{i}. {title} by {channel} ({views:,} views)"
            )
        
        return "\n".join(response_parts)
    
    def _generate_llm_response(self, query: str, results: List[Dict[str, Any]]) -> str:
        """
        Generate natural language response using LLM.
        
        Args:
            query: Original query
            results: Search results
            
        Returns:
            Natural language response
        """
        try:
            # Prepare context from results
            context_parts = []
            for i, result in enumerate(results[:5], 1):
                payload = result.get('payload', {})
                context_parts.append(
                    f"{i}. Title: {payload.get('title', 'Unknown')}\n"
                    f"   Channel: {payload.get('channel', 'Unknown')}\n"
                    f"   Category: {payload.get('category', 'Unknown')}\n"
                    f"   Views: {payload.get('views', 0):,}\n"
                    f"   Likes: {payload.get('likes', 0):,}\n"
                )
            
            context = "\n".join(context_parts)
            
            # Create prompt
            prompt = f"""You are a YouTube trends analyst. Based on the semantic search results below, 
provide a helpful and informative answer to the user's query.

User Query: {query}

Search Results:
{context}

Provide a natural, conversational response that:
1. Directly answers the user's question
2. Highlights the most relevant videos
3. Mentions interesting patterns or insights
4. Keeps the response concise (2-3 paragraphs max)

Response:"""
            
            # Generate response
            response = self.llm.invoke(prompt)
            return response.content
            
        except Exception as e:
            logger.error(f"Error generating LLM response: {e}")
            return self._generate_simple_response(results)
    
    def get_capabilities(self) -> Dict[str, Any]:
        """
        Get Vector Agent capabilities.
        
        Returns:
            Dictionary describing capabilities
        """
        return {
            'name': self.name,
            'type': 'vector',
            'description': 'Handles semantic search queries based on content similarity',
            'capabilities': [
                'Semantic similarity search',
                'Content-based recommendations',
                'Find videos similar to a topic',
                'Natural language understanding',
                'Contextual search across titles, descriptions, tags',
                'Fuzzy matching and concept search'
            ],
            'best_for': [
                'Find videos about [topic]',
                'Videos similar to [description]',
                'Content related to [concept]',
                'Search for videos discussing [theme]',
                'Recommendations based on interests',
                'Exploratory searches'
            ],
            'vector_db': 'Qdrant',
            'embedding_model': self.embedding_model.__class__.__name__
        }
    
    def search_with_filters(
        self,
        query: str,
        category: Optional[str] = None,
        min_views: Optional[int] = None,
        top_k: int = 5
    ) -> Dict[str, Any]:
        """
        Perform filtered semantic search.
        
        Args:
            query: Search query
            category: Filter by category
            min_views: Minimum view count
            top_k: Number of results
            
        Returns:
            Search results
        """
        filters = {}
        
        if category:
            filters['category'] = category
        
        if min_views:
            filters['views'] = {'gte': min_views}
        
        return self.process_query(query, top_k=top_k, filters=filters)
    
    def get_similar_videos(self, video_id: str, top_k: int = 5) -> Dict[str, Any]:
        """
        Find videos similar to a given video.
        
        Args:
            video_id: Video ID to find similar videos for
            top_k: Number of similar videos to return
            
        Returns:
            Similar videos
        """
        try:
            # This would require implementing a method to get video by ID
            # and then search for similar ones
            logger.info(f"Finding videos similar to: {video_id}")
            
            # Placeholder implementation
            return self.format_response(
                success=False,
                error="Similar video search not yet implemented"
            )
            
        except Exception as e:
            logger.error(f"Error finding similar videos: {e}")
            return self.format_response(
                success=False,
                error=f"Error: {str(e)}"
            )
