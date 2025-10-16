"""Data loading utilities for YouTube dataset"""

import pandas as pd
from pathlib import Path
from typing import List, Optional
from loguru import logger

from src.config import get_settings


class DataLoader:
    """Load and manage YouTube trending data from CSV files"""
    
    def __init__(self):
        self.settings = get_settings()
        
    def load_csv(self, file_path: Path) -> pd.DataFrame:
        """
        Load a single CSV file
        
        Args:
            file_path: Path to CSV file
            
        Returns:
            DataFrame with loaded data
        """
        try:
            logger.info(f"Loading data from {file_path}")
            df = pd.read_csv(file_path, encoding='utf-8', on_bad_lines='skip')
            logger.info(f"Loaded {len(df)} records from {file_path.name}")
            return df
        except Exception as e:
            logger.error(f"Error loading {file_path}: {e}")
            raise
    
    def load_all_csv_files(self, directory: Optional[Path] = None) -> pd.DataFrame:
        """
        Load all CSV files from a directory and combine them
        
        Args:
            directory: Directory containing CSV files (default: raw_data_dir)
            
        Returns:
            Combined DataFrame
        """
        if directory is None:
            directory = self.settings.raw_data_dir
            
        csv_files = list(directory.glob("*.csv"))
        
        if not csv_files:
            raise FileNotFoundError(f"No CSV files found in {directory}")
        
        logger.info(f"Found {len(csv_files)} CSV files")
        
        dataframes = []
        for csv_file in csv_files:
            try:
                df = self.load_csv(csv_file)
                # Add source file as metadata
                df['source_file'] = csv_file.name
                dataframes.append(df)
            except Exception as e:
                logger.warning(f"Skipping {csv_file.name}: {e}")
                continue
        
        if not dataframes:
            raise ValueError("No data could be loaded from CSV files")
        
        combined_df = pd.concat(dataframes, ignore_index=True)
        logger.info(f"Combined dataset: {len(combined_df)} total records")
        
        return combined_df
    
    def get_sample_data(self, n: int = 1000) -> pd.DataFrame:
        """
        Load a sample of data for testing
        
        Args:
            n: Number of samples to load
            
        Returns:
            Sample DataFrame
        """
        df = self.load_all_csv_files()
        sample = df.sample(n=min(n, len(df)), random_state=42)
        logger.info(f"Created sample dataset with {len(sample)} records")
        return sample
