"""Quick start script to verify setup and run a simple demo"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from loguru import logger
import time


def check_dependencies():
    """Check if all required packages are installed"""
    logger.info("Checking dependencies...")
    
    required_packages = [
        'qdrant_client',
        'sentence_transformers',
        'pandas',
        'numpy',
        'pydantic',
        'loguru',
        'tqdm'
    ]
    
    missing = []
    for package in required_packages:
        try:
            __import__(package)
            logger.info(f"  ✓ {package}")
        except ImportError:
            logger.error(f"  ✗ {package}")
            missing.append(package)
    
    if missing:
        logger.error(f"\nMissing packages: {', '.join(missing)}")
        logger.info("Run: pip install -r requirements.txt")
        return False
    
    logger.info("✓ All dependencies installed\n")
    return True


def check_qdrant():
    """Check if Qdrant is running"""
    logger.info("Checking Qdrant connection...")
    
    try:
        from src.vectordb import QdrantManager
        
        manager = QdrantManager()
        logger.info("  ✓ Connected to Qdrant")
        logger.info(f"  Host: {manager.host}:{manager.port}\n")
        return True
        
    except Exception as e:
        logger.error(f"  ✗ Cannot connect to Qdrant: {e}")
        logger.info("\nPlease start Qdrant:")
        logger.info("  docker-compose up -d")
        logger.info("\nThen verify at: http://localhost:6333/dashboard\n")
        return False


def check_data():
    """Check if data files exist"""
    logger.info("Checking for data files...")
    
    from src.config import get_settings
    settings = get_settings()
    
    csv_files = list(settings.raw_data_dir.glob("*.csv"))
    
    if csv_files:
        logger.info(f"  ✓ Found {len(csv_files)} CSV files")
        for f in csv_files[:3]:
            logger.info(f"    - {f.name}")
        if len(csv_files) > 3:
            logger.info(f"    ... and {len(csv_files) - 3} more")
        logger.info("")
        return True
    else:
        logger.warning(f"  ⚠ No CSV files found in {settings.raw_data_dir}")
        logger.info("\nPlease download YouTube dataset from:")
        logger.info("  https://www.kaggle.com/datasets/datasnaek/youtube-new/data")
        logger.info(f"\nAnd place CSV files in: {settings.raw_data_dir}\n")
        return False


def test_embedding():
    """Test embedding generation"""
    logger.info("Testing embedding generation...")
    
    try:
        from src.embeddings import get_embedding_model
        
        model = get_embedding_model()
        logger.info(f"  ✓ Loaded embedding model")
        logger.info(f"  Dimension: {model.get_dimension()}")
        
        # Test encoding
        test_text = "This is a test video about cats"
        embedding = model.encode_single(test_text)
        logger.info(f"  ✓ Generated test embedding (shape: {embedding.shape})\n")
        return True
        
    except Exception as e:
        logger.error(f"  ✗ Error testing embeddings: {e}\n")
        return False


def run_mini_demo():
    """Run a minimal demo with sample data"""
    logger.info("Running mini demo with sample data...")
    
    try:
        from src.data import DataPreprocessor
        from src.embeddings import get_embedding_model
        import pandas as pd
        
        # Create sample data
        sample_data = pd.DataFrame({
            'video_id': ['v1', 'v2', 'v3'],
            'title': [
                'Funny Cat Compilation 2024',
                'How to Cook Pasta - Italian Recipe',
                'Gaming Tutorial - Minecraft Tips'
            ],
            'channel_title': ['Cat Videos', 'Cooking Channel', 'Gaming Pro'],
            'category_id': [23, 26, 20],
            'tags': ['cats|funny|pets', 'cooking|recipe|pasta', 'gaming|minecraft|tutorial'],
            'views': [1000000, 500000, 750000],
            'likes': [50000, 25000, 40000],
            'dislikes': [1000, 500, 800],
            'comment_count': [10000, 5000, 8000]
        })
        
        # Preprocess
        preprocessor = DataPreprocessor()
        df_processed = preprocessor.preprocess(sample_data)
        logger.info(f"  ✓ Preprocessed {len(df_processed)} sample videos")
        
        # Generate embeddings
        embedding_model = get_embedding_model()
        texts = df_processed['searchable_text'].tolist()
        embeddings = embedding_model.encode(texts, show_progress=False)
        logger.info(f"  ✓ Generated embeddings for sample data")
        
        # Show sample
        logger.info("\n  Sample processed data:")
        for idx, row in df_processed.iterrows():
            logger.info(f"    {idx + 1}. {row['title']}")
            logger.info(f"       Category: {row['category_name']}")
            logger.info(f"       Tags: {', '.join(row['tags_list'][:3])}")
        
        logger.info("\n✓ Mini demo completed successfully!\n")
        return True
        
    except Exception as e:
        logger.error(f"  ✗ Error in mini demo: {e}\n")
        return False


def main():
    """Main quick start function"""
    
    print("\n" + "="*80)
    print("YouTube Trends Explorer - Quick Start")
    print("="*80 + "\n")
    
    # Run checks
    checks = {
        "Dependencies": check_dependencies(),
        "Qdrant": check_qdrant(),
        "Data Files": check_data(),
        "Embeddings": test_embedding(),
        "Mini Demo": run_mini_demo()
    }
    
    # Summary
    print("="*80)
    print("Setup Summary")
    print("="*80)
    
    for check_name, passed in checks.items():
        status = "✓ PASS" if passed else "✗ FAIL"
        print(f"  {status} - {check_name}")
    
    print("="*80)
    
    all_passed = all(checks.values())
    
    if all_passed:
        print("\n🎉 All checks passed! Your setup is ready.")
        print("\nNext steps:")
        print("  1. Ingest data: python scripts/ingest_data.py")
        print("  2. Run search demo: python scripts/search_demo.py")
        print("  3. Explore notebook: notebooks/exploratory_analysis.ipynb")
    else:
        print("\n⚠ Some checks failed. Please fix the issues above.")
        
        if not checks["Qdrant"]:
            print("\nQuick fix for Qdrant:")
            print("  docker-compose up -d")
        
        if not checks["Data Files"]:
            print("\nNote: You can still test with sample data,")
            print("but you'll need real data for the full demo.")
    
    print("\n" + "="*80 + "\n")


if __name__ == "__main__":
    main()
