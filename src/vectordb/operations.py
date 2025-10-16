"""Vector database operations for indexing and searching"""

from typing import List, Dict, Any, Optional
import numpy as np
from qdrant_client.models import PointStruct, Filter, FieldCondition, MatchValue
from loguru import logger
from tqdm import tqdm

from .client import QdrantManager
from src.config import get_settings


class VectorDBOperations:
    """High-level operations for vector database"""
    
    def __init__(self, qdrant_manager: Optional[QdrantManager] = None):
        """
        Initialize vector DB operations
        
        Args:
            qdrant_manager: QdrantManager instance (creates new if None)
        """
        self.manager = qdrant_manager or QdrantManager()
        self.client = self.manager.get_client()
        self.collection_name = self.manager.collection_name
        self.settings = get_settings()
    
    def index_documents(
        self,
        documents: List[Dict[str, Any]],
        embeddings: np.ndarray,
        batch_size: Optional[int] = None
    ) -> int:
        """
        Index documents with their embeddings
        
        Args:
            documents: List of document dictionaries with 'id', 'text', and 'metadata'
            embeddings: Array of embeddings corresponding to documents
            batch_size: Batch size for uploading (default: from settings)
            
        Returns:
            Number of documents indexed
        """
        if len(documents) != len(embeddings):
            raise ValueError(f"Mismatch: {len(documents)} documents but {len(embeddings)} embeddings")
        
        batch_size = batch_size or self.settings.batch_size
        
        logger.info(f"Indexing {len(documents)} documents in batches of {batch_size}")
        
        # Prepare points
        points = []
        for i, (doc, embedding) in enumerate(zip(documents, embeddings)):
            point = PointStruct(
                id=i,  # Use sequential ID for Qdrant
                vector=embedding.tolist(),
                payload={
                    'video_id': doc['id'],
                    'text': doc['text'],
                    **doc['metadata']
                }
            )
            points.append(point)
        
        # Upload in batches
        total_indexed = 0
        for i in tqdm(range(0, len(points), batch_size), desc="Uploading batches"):
            batch = points[i:i + batch_size]
            
            try:
                self.client.upsert(
                    collection_name=self.collection_name,
                    points=batch
                )
                total_indexed += len(batch)
                
            except Exception as e:
                logger.error(f"Error uploading batch {i // batch_size}: {e}")
                raise
        
        logger.info(f"Successfully indexed {total_indexed} documents")
        return total_indexed
    
    def search(
        self,
        query_vector: np.ndarray,
        limit: int = 10,
        score_threshold: Optional[float] = None,
        filters: Optional[Dict[str, Any]] = None
    ) -> List[Dict[str, Any]]:
        """
        Search for similar vectors
        
        Args:
            query_vector: Query embedding vector
            limit: Maximum number of results
            score_threshold: Minimum similarity score
            filters: Optional metadata filters
            
        Returns:
            List of search results with scores and metadata
        """
        try:
            # Build filter if provided
            qdrant_filter = None
            if filters:
                qdrant_filter = self._build_filter(filters)
            
            # Perform search
            results = self.client.search(
                collection_name=self.collection_name,
                query_vector=query_vector.tolist(),
                limit=limit,
                score_threshold=score_threshold,
                query_filter=qdrant_filter
            )
            
            # Format results
            formatted_results = []
            for result in results:
                formatted_results.append({
                    'id': result.payload.get('video_id'),
                    'score': result.score,
                    'title': result.payload.get('title', ''),
                    'channel': result.payload.get('channel', ''),
                    'category': result.payload.get('category', ''),
                    'views': result.payload.get('views', 0),
                    'likes': result.payload.get('likes', 0),
                    'tags': result.payload.get('tags', []),
                    'text': result.payload.get('text', ''),
                    'metadata': result.payload
                })
            
            return formatted_results
            
        except Exception as e:
            logger.error(f"Error during search: {e}")
            raise
    
    def _build_filter(self, filters: Dict[str, Any]) -> Filter:
        """
        Build Qdrant filter from dictionary
        
        Args:
            filters: Filter dictionary
            
        Returns:
            Qdrant Filter object
        """
        conditions = []
        
        # Category filter
        if 'category' in filters:
            conditions.append(
                FieldCondition(
                    key='category',
                    match=MatchValue(value=filters['category'])
                )
            )
        
        # Country filter
        if 'country' in filters:
            conditions.append(
                FieldCondition(
                    key='country',
                    match=MatchValue(value=filters['country'])
                )
            )
        
        # Minimum views filter
        if 'min_views' in filters:
            conditions.append(
                FieldCondition(
                    key='views',
                    range={'gte': filters['min_views']}
                )
            )
        
        # Maximum views filter
        if 'max_views' in filters:
            conditions.append(
                FieldCondition(
                    key='views',
                    range={'lte': filters['max_views']}
                )
            )
        
        if conditions:
            return Filter(must=conditions)
        
        return None
    
    def get_document_by_id(self, video_id: str) -> Optional[Dict[str, Any]]:
        """
        Retrieve a document by its video ID
        
        Args:
            video_id: Video ID
            
        Returns:
            Document data or None if not found
        """
        try:
            # Search by video_id in payload
            results = self.client.scroll(
                collection_name=self.collection_name,
                scroll_filter=Filter(
                    must=[
                        FieldCondition(
                            key='video_id',
                            match=MatchValue(value=video_id)
                        )
                    ]
                ),
                limit=1
            )
            
            if results[0]:
                point = results[0][0]
                return {
                    'id': point.payload.get('video_id'),
                    'title': point.payload.get('title', ''),
                    'channel': point.payload.get('channel', ''),
                    'metadata': point.payload
                }
            
            return None
            
        except Exception as e:
            logger.error(f"Error retrieving document: {e}")
            return None
    
    def count_documents(self) -> int:
        """
        Count total documents in collection
        
        Returns:
            Number of documents
        """
        try:
            info = self.manager.get_collection_info()
            return info['points_count']
        except Exception as e:
            logger.error(f"Error counting documents: {e}")
            return 0
