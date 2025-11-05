"""Enhanced data processing for YouTube videos with SQL database creation"""

import os
import pandas as pd
import numpy as np
import sqlite3
import re
import string
import langid
import pycountry
from typing import Optional
from pathlib import Path
from loguru import logger


class EnhancedYouTubeDataProcessor:
    """
    Enhanced data processor that creates both SQL database and prepares data for vector DB.
    Based on the comprehensive data processing pipeline from the notebook.
    """
    
    # Category mapping from YouTube
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
        30: "Movies",
        43: "Shows"
    }
    
    def __init__(self, db_path: str = "youtube_trends_canada.db"):
        """
        Initialize the processor.
        
        Args:
            db_path: Path to SQLite database file
        """
        self.db_path = db_path
        
    def detect_language(self, text: str) -> str:
        """
        Detects language from a combined text string.
        
        Args:
            text: Text to detect language from
            
        Returns:
            Language code
        """
        if pd.isna(text) or len(str(text).strip()) == 0:
            return "unknown"
        try:
            lang, _ = langid.classify(str(text))
            return lang
        except Exception as e:
            logger.warning(f"Language detection error: {e}")
            return "error"
    
    def code_to_name(self, code: str) -> str:
        """
        Converts 2-letter lang code to full name.
        
        Args:
            code: Language code
            
        Returns:
            Language name
        """
        if code in ["unknown", "error", ""]:
            return code
        try:
            return pycountry.languages.get(alpha_2=code).name
        except (AttributeError, KeyError):
            return code
    
    def clean_text(self, text: str) -> str:
        """
        General text cleaning for titles and descriptions.
        
        Args:
            text: Raw text
            
        Returns:
            Cleaned text
        """
        if not isinstance(text, str):
            text = str(text)
        
        text = text.lower()
        text = text.encode('ascii', 'ignore').decode()  # Remove unicode
        text = re.sub(r'https?://\S+|www\.\S+', '', text)  # Remove URLs
        text = re.sub(r'<.*?>', '', text)  # Remove HTML
        text = re.sub(f'[{re.escape(string.punctuation)}]', '', text)  # Remove punctuation
        text = re.sub(r'\n', ' ', text)  # Remove newlines
        return text.strip()
    
    def split_and_clean_tags(self, tags_string: str) -> list:
        """
        Splits and cleans the pipe-delimited tags column.
        
        Args:
            tags_string: Raw tags string
            
        Returns:
            List of cleaned tags
        """
        if not isinstance(tags_string, str) or tags_string == '[none]':
            return []
        
        tags_list = tags_string.split('|')
        cleaned_list = [tag.lower().strip().replace('"', '') for tag in tags_list]
        return cleaned_list
    
    def process_dataframe(self, df: pd.DataFrame, country: str = 'CA') -> pd.DataFrame:
        """
        Process the raw dataframe with all transformations.
        
        Args:
            df: Raw DataFrame
            country: Country code
            
        Returns:
            Processed DataFrame
        """
        logger.info(f"Starting data processing for {len(df)} records...")
        
        # Handle NaNs
        df['description'] = df['description'].fillna('[no description]')
        df['tags'] = df['tags'].fillna('[none]')
        
        # Language detection
        logger.info("Detecting languages...")
        df['text_for_lang'] = df['title'].fillna('') + ' ' + df['description'].fillna('')
        df['lang_code'] = df['text_for_lang'].apply(self.detect_language)
        df['language'] = df['lang_code'].apply(self.code_to_name)
        
        # Category mapping
        df['category_name'] = df['category_id'].map(self.CATEGORY_MAPPING).fillna('Other')
        
        # Text cleaning
        logger.info("Cleaning text fields...")
        df['title_cleaned'] = df['title'].apply(self.clean_text)
        df['description_cleaned'] = df['description'].apply(self.clean_text)
        
        # Tags processing
        df['tags_list'] = df['tags'].apply(self.split_and_clean_tags)
        df['tags_cleaned'] = df['tags_list'].apply(lambda x: ' '.join(x))
        df['num_tags'] = df['tags_list'].apply(len)
        
        # Date conversions
        df['publish_time'] = pd.to_datetime(df['publish_time'])
        df['trending_date'] = pd.to_datetime(df['trending_date'], format='%y.%d.%m')
        
        # Add country code
        df['country'] = country
        
        return df
    
    def calculate_temporal_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Calculate temporal (trending) features.
        
        Args:
            df: Processed DataFrame
            
        Returns:
            DataFrame with temporal features
        """
        logger.info("Calculating temporal features...")
        
        # Sort by video_id and trending_date
        df_sorted = df.sort_values(by=['video_id', 'trending_date'])
        
        # Calculate longest consecutive streak
        df_sorted['date_diff'] = df_sorted.groupby('video_id')['trending_date'].diff().dt.days
        df_sorted['new_streak'] = (df_sorted['date_diff'] > 1).cumsum()
        streak_lengths = df_sorted.groupby(['video_id', 'new_streak']).size()
        longest_streaks = streak_lengths.groupby('video_id').max().rename('longest_consecutive_streak_days')
        
        # Aggregate temporal features
        agg_df = df.groupby('video_id').agg(
            first_trend_date=('trending_date', 'min'),
            last_trend_date=('trending_date', 'max'),
            days_trending_unique=('trending_date', 'nunique')
        )
        
        # Join streak data
        final_agg_df = agg_df.join(longest_streaks)
        final_agg_df['longest_consecutive_streak_days'] = (
            final_agg_df['longest_consecutive_streak_days'].fillna(1).astype(int)
        )
        
        return final_agg_df
    
    def create_final_dataframe(self, df: pd.DataFrame, temporal_df: pd.DataFrame) -> pd.DataFrame:
        """
        Create final de-duplicated DataFrame for database.
        
        Args:
            df: Processed DataFrame
            temporal_df: Temporal features DataFrame
            
        Returns:
            Final DataFrame ready for database
        """
        logger.info("Creating final de-duplicated table...")
        
        # Sort by trending_date to get the latest stats for each video
        df_latest_stats = df.sort_values('trending_date').drop_duplicates('video_id', keep='last')
        
        # Merge aggregated temporal features
        final_db_df = df_latest_stats.merge(temporal_df, on='video_id', how='left')
        
        # Select and order columns for SQL schema
        schema_columns = [
            'video_id', 'title', 'description_cleaned', 'tags_cleaned', 'category_id',
            'category_name', 'channel_title', 'country', 'language', 'publish_time',
            'first_trend_date', 'last_trend_date', 'days_trending_unique',
            'longest_consecutive_streak_days', 'views', 'likes', 'comment_count'
        ]
        
        # Rename columns for the database
        final_db_df = final_db_df[schema_columns].rename(columns={
            'description_cleaned': 'description',
            'tags_cleaned': 'tags'
        })
        
        logger.info(f"Final dataset contains {len(final_db_df)} unique videos")
        return final_db_df
    
    def create_sql_database(self, df: pd.DataFrame, table_name: str = 'videos') -> None:
        """
        Create and populate SQLite database.
        
        Args:
            df: Final processed DataFrame
            table_name: Name of the table to create
        """
        logger.info(f"Creating SQLite database: {self.db_path}")
        
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        
        # Drop table if it exists
        c.execute(f"DROP TABLE IF EXISTS {table_name}")
        
        # Create table with schema
        c.execute(f"""
        CREATE TABLE {table_name} (
            video_id TEXT PRIMARY KEY,
            title TEXT,
            description TEXT,
            tags TEXT,
            category_id INTEGER,
            category_name TEXT,
            channel_title TEXT,
            country TEXT,
            language TEXT,
            publish_time TIMESTAMP,
            first_trend_date DATE,
            last_trend_date DATE,
            days_trending_unique INTEGER,
            longest_consecutive_streak_days INTEGER,
            views INTEGER,
            likes INTEGER,
            comment_count INTEGER
        );
        """)
        
        logger.info(f"Populating '{table_name}' table with {len(df)} unique videos...")
        
        # Populate the table
        df.to_sql(table_name, conn, if_exists='append', index=False)
        
        conn.commit()
        conn.close()
        
        logger.info(f"✅ Database creation complete! File: {self.db_path}")
    
    def prepare_for_vector_db(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Prepare data for vector database indexing.
        
        Args:
            df: Final processed DataFrame
            
        Returns:
            DataFrame with searchable text for embeddings
        """
        logger.info("Preparing data for vector database...")
        
        df_vector = df.copy()
        
        # Create searchable text combining multiple fields
        def create_searchable_text(row):
            parts = []
            parts.append(f"Title: {row['title']}")
            parts.append(f"Channel: {row['channel_title']}")
            parts.append(f"Category: {row['category_name']}")
            
            if row['tags'] and row['tags'] != '':
                parts.append(f"Tags: {row['tags']}")
            
            if row['description'] and row['description'] != '[no description]':
                desc = row['description'][:300]  # Limit description
                parts.append(f"Description: {desc}")
            
            return " | ".join(parts)
        
        df_vector['searchable_text'] = df_vector.apply(create_searchable_text, axis=1)
        
        logger.info(f"Prepared {len(df_vector)} documents for vector database")
        return df_vector
    
    def process_csv_file(
        self,
        csv_path: str,
        country: str = 'CA',
        create_sql: bool = True,
        prepare_vector: bool = True
    ) -> tuple[Optional[pd.DataFrame], Optional[pd.DataFrame]]:
        """
        Complete processing pipeline from CSV to databases.
        
        Args:
            csv_path: Path to CSV file
            country: Country code
            create_sql: Whether to create SQL database
            prepare_vector: Whether to prepare vector database data
            
        Returns:
            Tuple of (sql_df, vector_df)
        """
        logger.info(f"Loading data from {csv_path}...")
        
        try:
            df = pd.read_csv(csv_path)
        except FileNotFoundError:
            logger.error(f"CSV file not found: {csv_path}")
            raise
        
        # Process dataframe
        df_processed = self.process_dataframe(df, country)
        
        # Calculate temporal features
        temporal_features = self.calculate_temporal_features(df_processed)
        
        # Create final dataframe
        final_df = self.create_final_dataframe(df_processed, temporal_features)
        
        sql_df = None
        vector_df = None
        
        # Create SQL database
        if create_sql:
            self.create_sql_database(final_df)
            sql_df = final_df
        
        # Prepare for vector database
        if prepare_vector:
            vector_df = self.prepare_for_vector_db(final_df)
        
        logger.info("✅ Data processing pipeline complete!")
        return sql_df, vector_df


def main():
    """Main function for standalone execution"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Process YouTube trending data')
    parser.add_argument('--csv', type=str, required=True, help='Path to CSV file')
    parser.add_argument('--country', type=str, default='CA', help='Country code')
    parser.add_argument('--db-path', type=str, default='youtube_trends_canada.db', 
                       help='SQLite database path')
    
    args = parser.parse_args()
    
    processor = EnhancedYouTubeDataProcessor(db_path=args.db_path)
    processor.process_csv_file(args.csv, country=args.country)


if __name__ == "__main__":
    main()
