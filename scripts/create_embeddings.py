"""Script to create embeddings for existing data (alternative to full ingestion)"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent))

import pandas as pd
from loguru import logger
from src.config import get_settings
from src.data import DataPreprocessor
from src.embeddings import get_embedding_model


def main():
    """Create embeddings from preprocessed data"""
    
    logger.info("Creating embeddings for YouTube data")
    
    settings = get_settings()
    
    # Check for preprocessed data
    processed_file = settings.processed_data_dir / "youtube_processed.parquet"
    
    if not processed_file.exists():
        logger.error(f"Preprocessed data not found at {processed_file}")
        logger.info("Please run ingest_data.py first")
        return
    
    # Load preprocessed data
    logger.info(f"Loading preprocessed data from {processed_file}")
    df = pd.read_parquet(processed_file)
    logger.info(f"Loaded {len(df)} records")
    
    # Convert to documents
    preprocessor = DataPreprocessor()
    documents = preprocessor.to_documents(df)
    
    # Generate embeddings
    logger.info("Generating embeddings...")
    embedding_model = get_embedding_model()
    
    texts = [doc['text'] for doc in documents]
    embeddings = embedding_model.encode(texts, batch_size=settings.batch_size)
    
    logger.info(f"Generated {len(embeddings)} embeddings")
    logger.info(f"Embedding dimension: {embeddings.shape[1]}")
    
    # Save embeddings
    import numpy as np
    embeddings_file = settings.processed_data_dir / "embeddings.npy"
    np.save(embeddings_file, embeddings)
    logger.info(f"Saved embeddings to {embeddings_file}")


if __name__ == "__main__":
    main()
