"""Script to ingest YouTube data and create embeddings using enhanced processor"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from loguru import logger
from src.config import get_settings
from src.data.enhanced_processor import EnhancedYouTubeDataProcessor
from src.embeddings import get_embedding_model
from src.vectordb import QdrantManager, VectorDBOperations


def main():
    """Main ingestion pipeline using enhanced processor"""
    
    logger.info("="*80)
    logger.info("YouTube Trends Data Ingestion Pipeline (Enhanced)")
    logger.info("="*80)
    
    settings = get_settings()
    
    # Step 1: Initialize embedding model
    logger.info("\n[Step 1/5] Initializing embedding model...")
    embedding_model = get_embedding_model()
    logger.info(f"✓ Loaded embedding model (dimension: {embedding_model.get_dimension()})")
    
    # Step 2: Initialize enhanced processor with embedding model
    logger.info("\n[Step 2/5] Initializing enhanced data processor...")
    processor = EnhancedYouTubeDataProcessor(
        db_path=settings.sql_db_path,
        embedding_model=embedding_model
    )
    logger.info("✓ Processor initialized")
    
    # Step 3: Find CSV files to process
    logger.info("\n[Step 3/5] Finding CSV files...")
    csv_files = list(settings.raw_data_dir.glob("*.csv"))
    
    if not csv_files:
        logger.error(f"✗ No CSV files found in {settings.raw_data_dir}")
        logger.info("\nPlease download the YouTube dataset from:")
        logger.info("https://www.kaggle.com/datasets/datasnaek/youtube-new/data")
        logger.info(f"And place CSV files in: {settings.raw_data_dir}")
        return
    
    logger.info(f"✓ Found {len(csv_files)} CSV file(s)")
    
    # Process first CSV file (or combine multiple if needed)
    csv_path = csv_files[0]
    logger.info(f"Processing: {csv_path.name}")
    
    # Extract country code from filename (e.g., CAvideos.csv -> CA)
    country = csv_path.stem[:2].upper() if len(csv_path.stem) >= 2 else 'CA'
    
    # Step 4: Process data with SQL and vector preparation
    logger.info("\n[Step 4/5] Processing data (SQL + Vector DB preparation)...")
    sql_df, vector_documents, embeddings = processor.process_csv_file(
        csv_path=str(csv_path),
        country=country,
        create_sql=True,
        prepare_vector=True,
        generate_embeddings=True
    )
    
    logger.info(f"✓ SQL database created: {settings.sql_db_path}")
    logger.info(f"✓ Vector documents prepared: {len(vector_documents)}")
    logger.info(f"✓ Embeddings generated: {embeddings.shape}")
    
    # Step 5: Index in Qdrant
    logger.info("\n[Step 5/5] Indexing in Qdrant...")
    
    # Initialize Qdrant
    qdrant_manager = QdrantManager()
    
    # Create collection (recreate if exists)
    qdrant_manager.create_collection(
        vector_size=embedding_model.get_dimension(),
        recreate=True
    )
    
    # Index documents with enhanced metadata
    db_ops = VectorDBOperations(qdrant_manager)
    indexed_count = db_ops.index_documents(vector_documents, embeddings)
    logger.info(f"✓ Indexed {indexed_count} documents with full metadata")
    
    # Show collection info
    info = qdrant_manager.get_collection_info()
    logger.info("\n" + "="*80)
    logger.info("Ingestion Complete!")
    logger.info("="*80)
    logger.info(f"SQL Database: {settings.sql_db_path}")
    logger.info(f"  - Table: {settings.sql_table_name}")
    logger.info(f"  - Records: {len(sql_df)}")
    logger.info(f"\nVector Database: {info['name']}")
    logger.info(f"  - Documents: {info['points_count']}")
    logger.info(f"  - Status: {info['status']}")
    logger.info(f"  - Metadata fields: video_id, title, channel, category, country, language, tags, views, likes, etc.")
    logger.info("\nYou can now run semantic search using: python scripts/search_demo.py")
    logger.info("="*80)


if __name__ == "__main__":
    main()
