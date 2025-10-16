"""Interactive demo for semantic search"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from loguru import logger
from src.search import SemanticSearch


def run_demo_queries(search: SemanticSearch):
    """Run predefined demo queries"""
    
    demo_queries = [
        {
            "query": "funny cat videos",
            "description": "Finding funny cat videos"
        },
        {
            "query": "gaming tutorials and walkthroughs",
            "description": "Gaming content"
        },
        {
            "query": "cooking recipes and food",
            "description": "Cooking and food videos"
        },
        {
            "query": "music concerts and performances",
            "description": "Music performances"
        },
        {
            "query": "technology reviews and unboxing",
            "description": "Tech reviews"
        }
    ]
    
    print("\n" + "="*80)
    print("DEMO QUERIES")
    print("="*80)
    
    for demo in demo_queries:
        print(f"\n🔍 {demo['description']}: '{demo['query']}'")
        print("-"*80)
        
        results = search.search(demo['query'], limit=5)
        
        if results:
            for i, result in enumerate(results, 1):
                print(f"\n{i}. {result['title']}")
                print(f"   Channel: {result['channel']}")
                print(f"   Category: {result['category']}")
                print(f"   Views: {result['views']:,} | Likes: {result['likes']:,}")
                print(f"   Score: {result['score']:.4f}")
        else:
            print("No results found.")
        
        print()


def interactive_search(search: SemanticSearch):
    """Interactive search mode"""
    
    print("\n" + "="*80)
    print("INTERACTIVE SEARCH MODE")
    print("="*80)
    print("Enter your search queries (or 'quit' to exit)")
    print("Commands:")
    print("  - Type a query to search")
    print("  - 'stats' - Show collection statistics")
    print("  - 'quit' or 'exit' - Exit the program")
    print("="*80 + "\n")
    
    while True:
        try:
            query = input("\n🔍 Search: ").strip()
            
            if not query:
                continue
            
            if query.lower() in ['quit', 'exit', 'q']:
                print("Goodbye!")
                break
            
            if query.lower() == 'stats':
                stats = search.get_stats()
                print("\n📊 Collection Statistics:")
                for key, value in stats.items():
                    print(f"   {key}: {value}")
                continue
            
            # Perform search
            print(f"\nSearching for: '{query}'...")
            results = search.search(query, limit=10)
            
            if results:
                print(f"\nFound {len(results)} results:\n")
                for i, result in enumerate(results, 1):
                    print(f"{i}. {result['title']}")
                    print(f"   Channel: {result['channel']} | Category: {result['category']}")
                    print(f"   Views: {result['views']:,} | Score: {result['score']:.4f}")
                    if result.get('tags'):
                        tags_str = ', '.join(result['tags'][:5])
                        print(f"   Tags: {tags_str}")
                    print()
            else:
                print("No results found.")
        
        except KeyboardInterrupt:
            print("\n\nGoodbye!")
            break
        except Exception as e:
            logger.error(f"Error during search: {e}")
            print(f"Error: {e}")


def main():
    """Main demo function"""
    
    print("\n" + "="*80)
    print("YouTube Trends Semantic Search - Demo")
    print("="*80)
    
    # Initialize search
    try:
        print("\nInitializing semantic search...")
        search = SemanticSearch()
        
        # Show stats
        stats = search.get_stats()
        print("\n📊 Collection Statistics:")
        print(f"   Total videos: {stats.get('total_videos', 0):,}")
        print(f"   Embedding dimension: {stats.get('embedding_dimension', 0)}")
        print(f"   Status: {stats.get('status', 'unknown')}")
        
    except Exception as e:
        logger.error(f"Failed to initialize search: {e}")
        print("\n❌ Error: Could not connect to Qdrant or collection not found.")
        print("Please make sure:")
        print("1. Qdrant is running (docker-compose up -d)")
        print("2. Data has been ingested (python scripts/ingest_data.py)")
        return
    
    # Ask user for mode
    print("\n" + "="*80)
    print("Select mode:")
    print("1. Run demo queries")
    print("2. Interactive search")
    print("="*80)
    
    choice = input("\nEnter choice (1 or 2): ").strip()
    
    if choice == "1":
        run_demo_queries(search)
    elif choice == "2":
        interactive_search(search)
    else:
        print("Invalid choice. Running demo queries...")
        run_demo_queries(search)


if __name__ == "__main__":
    main()
