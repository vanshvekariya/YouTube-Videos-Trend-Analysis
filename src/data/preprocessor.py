"""Data preprocessing for YouTube videos"""

import pandas as pd
import re
from typing import Dict, Any, List
from loguru import logger


class DataPreprocessor:
    """Preprocess YouTube video data for embedding and indexing"""
    
    # Expected columns in the dataset
    EXPECTED_COLUMNS = [
        'video_id', 'title', 'channel_title', 'category_id',
        'tags', 'views', 'likes', 'dislikes', 'comment_count'
    ]
    
    # Category mapping (YouTube category IDs)
    CATEGORY_MAPPING = {
        1: "Film & Animation",
        2: "Autos & Vehicles",
        10: "Music",
        15: "Pets & Animals",
        17: "Sports",
        19: "Travel & Events",
        20: "Gaming",
        22: "People & Blogs",
        23: "Comedy",
        24: "Entertainment",
        25: "News & Politics",
        26: "Howto & Style",
        27: "Education",
        28: "Science & Technology",
        29: "Nonprofits & Activism",
    }
    
    def __init__(self):
        pass
    
    def clean_text(self, text: str) -> str:
        """
        Clean and normalize text
        
        Args:
            text: Raw text
            
        Returns:
            Cleaned text
        """
        if pd.isna(text) or text == "":
            return ""
        
        # Convert to string
        text = str(text)
        
        # Remove URLs
        text = re.sub(r'http\S+|www.\S+', '', text)
        
        # Remove special characters but keep spaces and basic punctuation
        text = re.sub(r'[^\w\s\-.,!?]', ' ', text)
        
        # Remove extra whitespace
        text = ' '.join(text.split())
        
        return text.strip()
    
    def parse_tags(self, tags: str) -> List[str]:
        """
        Parse tags string into list
        
        Args:
            tags: Tags string (pipe-separated or quoted)
            
        Returns:
            List of tags
        """
        if pd.isna(tags) or tags == "" or tags == "[none]":
            return []
        
        # Handle pipe-separated tags
        if '|' in tags:
            tag_list = tags.split('|')
        # Handle quoted tags
        elif '"' in tags:
            tag_list = re.findall(r'"([^"]*)"', tags)
        else:
            tag_list = [tags]
        
        # Clean and filter tags
        cleaned_tags = [self.clean_text(tag) for tag in tag_list]
        return [tag for tag in cleaned_tags if tag]
    
    def get_category_name(self, category_id: int) -> str:
        """
        Get category name from ID
        
        Args:
            category_id: YouTube category ID
            
        Returns:
            Category name
        """
        return self.CATEGORY_MAPPING.get(int(category_id), "Unknown")
    
    def create_searchable_text(self, row: pd.Series) -> str:
        """
        Create a combined text field for embedding
        
        Args:
            row: DataFrame row
            
        Returns:
            Combined searchable text
        """
        parts = []
        
        # Title (most important)
        if 'title' in row and pd.notna(row['title']):
            parts.append(f"Title: {row['title']}")
        
        # Channel
        if 'channel_title' in row and pd.notna(row['channel_title']):
            parts.append(f"Channel: {row['channel_title']}")
        
        # Category
        if 'category_name' in row and pd.notna(row['category_name']):
            parts.append(f"Category: {row['category_name']}")
        
        # Tags
        if 'tags_list' in row and row['tags_list']:
            tags_str = ', '.join(row['tags_list'][:10])  # Limit to first 10 tags
            parts.append(f"Tags: {tags_str}")
        
        # Description (if available)
        if 'description' in row and pd.notna(row['description']):
            desc = row['description'][:200]  # Limit description length
            parts.append(f"Description: {desc}")
        
        return " | ".join(parts)
    
    def preprocess(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Preprocess the entire dataset
        
        Args:
            df: Raw DataFrame
            
        Returns:
            Preprocessed DataFrame
        """
        logger.info(f"Starting preprocessing of {len(df)} records")
        
        # Create a copy
        df_processed = df.copy()
        
        # Remove duplicates based on video_id
        if 'video_id' in df_processed.columns:
            initial_count = len(df_processed)
            df_processed = df_processed.drop_duplicates(subset=['video_id'], keep='first')
            logger.info(f"Removed {initial_count - len(df_processed)} duplicate videos")
        
        # Clean text fields
        if 'title' in df_processed.columns:
            df_processed['title'] = df_processed['title'].apply(self.clean_text)
        
        if 'channel_title' in df_processed.columns:
            df_processed['channel_title'] = df_processed['channel_title'].apply(self.clean_text)
        
        # Parse tags
        if 'tags' in df_processed.columns:
            df_processed['tags_list'] = df_processed['tags'].apply(self.parse_tags)
        else:
            df_processed['tags_list'] = [[] for _ in range(len(df_processed))]
        
        # Add category names
        if 'category_id' in df_processed.columns:
            df_processed['category_name'] = df_processed['category_id'].apply(
                lambda x: self.get_category_name(x) if pd.notna(x) else "Unknown"
            )
        
        # Convert numeric fields
        numeric_fields = ['views', 'likes', 'dislikes', 'comment_count']
        for field in numeric_fields:
            if field in df_processed.columns:
                df_processed[field] = pd.to_numeric(df_processed[field], errors='coerce').fillna(0).astype(int)
        
        # Create searchable text
        df_processed['searchable_text'] = df_processed.apply(self.create_searchable_text, axis=1)
        
        # Remove rows with empty searchable text
        df_processed = df_processed[df_processed['searchable_text'].str.len() > 0]
        
        logger.info(f"Preprocessing complete: {len(df_processed)} records ready")
        
        return df_processed
    
    def to_documents(self, df: pd.DataFrame) -> List[Dict[str, Any]]:
        """
        Convert DataFrame to list of documents for indexing
        
        Args:
            df: Preprocessed DataFrame
            
        Returns:
            List of document dictionaries
        """
        documents = []
        
        for idx, row in df.iterrows():
            doc = {
                'id': row.get('video_id', str(idx)),
                'text': row['searchable_text'],
                'metadata': {
                    'title': row.get('title', ''),
                    'channel': row.get('channel_title', ''),
                    'category': row.get('category_name', 'Unknown'),
                    'category_id': int(row.get('category_id', 0)),
                    'tags': row.get('tags_list', []),
                    'views': int(row.get('views', 0)),
                    'likes': int(row.get('likes', 0)),
                    'dislikes': int(row.get('dislikes', 0)),
                    'comment_count': int(row.get('comment_count', 0)),
                }
            }
            
            # Add optional fields if available
            if 'trending_date' in row:
                doc['metadata']['trending_date'] = str(row['trending_date'])
            
            if 'publish_time' in row:
                doc['metadata']['publish_time'] = str(row['publish_time'])
            
            if 'country' in row:
                doc['metadata']['country'] = str(row['country'])
            
            documents.append(doc)
        
        logger.info(f"Created {len(documents)} documents")
        return documents
