"""Script to process CSV data and index in both SQL and Vector databases"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from loguru import logger
from src.data.enhanced_processor import EnhancedYouTubeDataProcessor
from src.vectordb.operations import VectorDBOperations
from src.config.settings import get_settings


def main():
    """Main processing pipeline"""
    import argparse
    
    parser = argparse.ArgumentParser(
        description='Process YouTube data and index in databases'
    )
    parser.add_argument(
        '--csv',
        type=str,
        required=True,
        help='Path to CSV file (e.g., data/raw/CAvideos.csv)'
    )
    parser.add_argument(
        '--country',
        type=str,
        default='CA',
        help='Country code (default: CA)'
    )
    parser.add_argument(
        '--skip-sql',
        action='store_true',
        help='Skip SQL database creation'
    )
    parser.add_argument(
        '--skip-vector',
        action='store_true',
        help='Skip vector database indexing'
    )
    
    args = parser.parse_args()
    
    settings = get_settings()
    
    logger.info("="*70)
    logger.info("YouTube Trends Data Processing Pipeline")
    logger.info("="*70)
    
    # Step 1: Process CSV data
    logger.info("\n📊 Step 1: Processing CSV data...")
    
    processor = EnhancedYouTubeDataProcessor(db_path=settings.sql_db_path)
    
    try:
        sql_df, vector_df = processor.process_csv_file(
            csv_path=args.csv,
            country=args.country,
            create_sql=not args.skip_sql,
            prepare_vector=not args.skip_vector
        )
        
        logger.info("✅ Data processing complete!")
        
    except Exception as e:
        logger.error(f"❌ Data processing failed: {e}")
        sys.exit(1)
    
    # Step 2: Index in vector database
    if not args.skip_vector and vector_df is not None:
        logger.info("\n🔍 Step 2: Indexing in vector database...")
        
        try:
            vector_ops = VectorDBOperations()
            
            # Prepare documents
            documents = []
            for _, row in vector_df.iterrows():
                doc = {
                    'id': row['video_id'],
                    'text': row['searchable_text'],
                    'metadata': {
                        'video_id': row['video_id'],
                        'title': row['title'],
                        'channel': row['channel_title'],
                        'category': row['category_name'],
                        'category_id': int(row['category_id']),
                        'views': int(row['views']),
                        'likes': int(row['likes']),
                        'comment_count': int(row['comment_count']),
                        'tags': row['tags'].split()[:10] if row['tags'] else [],
                        'country': row['country'],
                        'language': row['language']
                    }
                }
                documents.append(doc)
            
            # Index documents
            logger.info(f"Indexing {len(documents)} documents...")
            vector_ops.index_documents(documents)
            
            logger.info("✅ Vector indexing complete!")
            
        except Exception as e:
            logger.error(f"❌ Vector indexing failed: {e}")
            logger.warning("SQL database was created successfully, but vector indexing failed.")
    
    # Summary
    logger.info("\n" + "="*70)
    logger.info("✅ PROCESSING COMPLETE!")
    logger.info("="*70)
    
    if not args.skip_sql:
        logger.info(f"📊 SQL Database: {settings.sql_db_path}")
        logger.info(f"   Records: {len(sql_df) if sql_df is not None else 0}")
    
    if not args.skip_vector:
        logger.info(f"🔍 Vector Database: Qdrant at {settings.qdrant_host}:{settings.qdrant_port}")
        logger.info(f"   Collection: {settings.qdrant_collection_name}")
        logger.info(f"   Records: {len(vector_df) if vector_df is not None else 0}")
    
    logger.info("\n🚀 You can now run the multi-agent system:")
    logger.info("   python -m src.main")
    logger.info("="*70)


if __name__ == "__main__":
    main()
