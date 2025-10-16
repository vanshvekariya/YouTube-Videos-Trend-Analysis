"""Script to ingest YouTube data and create embeddings"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from loguru import logger
from src.config import get_settings
from src.data import DataLoader, DataPreprocessor
from src.embeddings import get_embedding_model
from src.vectordb import QdrantManager, VectorDBOperations


def main():
    """Main ingestion pipeline"""
    
    logger.info("="*80)
    logger.info("YouTube Trends Data Ingestion Pipeline")
    logger.info("="*80)
    
    settings = get_settings()
    
    # Step 1: Load data
    logger.info("\n[Step 1/5] Loading data from CSV files...")
    loader = DataLoader()
    
    try:
        df = loader.load_all_csv_files()
        logger.info(f"✓ Loaded {len(df)} records")
    except FileNotFoundError as e:
        logger.error(f"✗ {e}")
        logger.info("\nPlease download the YouTube dataset from:")
        logger.info("https://www.kaggle.com/datasets/datasnaek/youtube-new/data")
        logger.info(f"And place CSV files in: {settings.raw_data_dir}")
        return
    
    # Step 2: Preprocess data
    logger.info("\n[Step 2/5] Preprocessing data...")
    preprocessor = DataPreprocessor()
    df_processed = preprocessor.preprocess(df)
    logger.info(f"✓ Preprocessed {len(df_processed)} records")
    
    # Step 3: Convert to documents
    logger.info("\n[Step 3/5] Converting to documents...")
    documents = preprocessor.to_documents(df_processed)
    logger.info(f"✓ Created {len(documents)} documents")
    
    # Step 4: Generate embeddings
    logger.info("\n[Step 4/5] Generating embeddings...")
    embedding_model = get_embedding_model()
    
    texts = [doc['text'] for doc in documents]
    embeddings = embedding_model.encode(texts, batch_size=settings.batch_size)
    logger.info(f"✓ Generated {len(embeddings)} embeddings (dimension: {embeddings.shape[1]})")
    
    # Step 5: Index in Qdrant
    logger.info("\n[Step 5/5] Indexing in Qdrant...")
    
    # Initialize Qdrant
    qdrant_manager = QdrantManager()
    
    # Create collection (recreate if exists)
    qdrant_manager.create_collection(
        vector_size=embedding_model.get_dimension(),
        recreate=True
    )
    
    # Index documents
    db_ops = VectorDBOperations(qdrant_manager)
    indexed_count = db_ops.index_documents(documents, embeddings)
    logger.info(f"✓ Indexed {indexed_count} documents")
    
    # Show collection info
    info = qdrant_manager.get_collection_info()
    logger.info("\n" + "="*80)
    logger.info("Ingestion Complete!")
    logger.info("="*80)
    logger.info(f"Collection: {info['name']}")
    logger.info(f"Total documents: {info['points_count']}")
    logger.info(f"Status: {info['status']}")
    logger.info("\nYou can now run semantic search using: python scripts/search_demo.py")
    logger.info("="*80)


if __name__ == "__main__":
    main()
