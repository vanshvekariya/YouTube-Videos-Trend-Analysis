"""
Example script demonstrating the Multi-Agent System usage.

This script shows how to:
1. Initialize the multi-agent system
2. Process different types of queries
3. Access detailed results
4. Handle errors
"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.main import YouTubeTrendsApp
from loguru import logger


def example_sql_queries(app: YouTubeTrendsApp):
    """Example SQL/analytical queries"""
    print("\n" + "="*70)
    print("SQL AGENT EXAMPLES (Analytical Queries)")
    print("="*70)
    
    sql_queries = [
        "Which category has the most trending videos?",
        "Top 5 channels by total views",
        "Average likes for Gaming category",
        "How many videos are in the database?",
    ]
    
    for query in sql_queries:
        print(f"\n📊 Query: {query}")
        print("-" * 70)
        
        response = app.query(query)
        
        if response['success']:
            print(f"Answer: {response['answer']}")
            print(f"Agent: {response['metadata'].get('agents_used', [])}")
            print(f"Type: {response['metadata'].get('query_type', 'unknown')}")
        else:
            print(f"Error: {response.get('error', 'Unknown error')}")


def example_vector_queries(app: YouTubeTrendsApp):
    """Example Vector/semantic queries"""
    print("\n" + "="*70)
    print("VECTOR AGENT EXAMPLES (Semantic Search)")
    print("="*70)
    
    vector_queries = [
        "Find videos about cooking tutorials",
        "Videos related to gaming and esports",
        "Content about fitness and health",
        "Search for educational science videos",
    ]
    
    for query in vector_queries:
        print(f"\n🔍 Query: {query}")
        print("-" * 70)
        
        response = app.query(query)
        
        if response['success']:
            print(f"Answer: {response['answer'][:300]}...")  # Truncate for display
            print(f"Agent: {response['metadata'].get('agents_used', [])}")
            print(f"Type: {response['metadata'].get('query_type', 'unknown')}")
            
            # Show top results if available
            if 'vector_result' in response:
                vector_data = response['vector_result'].get('data', {})
                results = vector_data.get('results', [])
                if results:
                    print(f"\nTop {min(3, len(results))} Results:")
                    for i, result in enumerate(results[:3], 1):
                        print(f"  {i}. {result.get('title', 'N/A')} "
                              f"(Score: {result.get('score', 0):.3f})")
        else:
            print(f"Error: {response.get('error', 'Unknown error')}")


def example_hybrid_queries(app: YouTubeTrendsApp):
    """Example Hybrid queries (both SQL and Vector)"""
    print("\n" + "="*70)
    print("HYBRID EXAMPLES (Both Analytical + Semantic)")
    print("="*70)
    
    hybrid_queries = [
        "Most popular gaming videos about Minecraft",
        "Top educational content about programming",
        "Find trending cooking videos with high engagement",
    ]
    
    for query in hybrid_queries:
        print(f"\n🔄 Query: {query}")
        print("-" * 70)
        
        response = app.query(query)
        
        if response['success']:
            print(f"Answer: {response['answer'][:400]}...")  # Truncate
            print(f"Agents: {response['metadata'].get('agents_used', [])}")
            print(f"Type: {response['metadata'].get('query_type', 'unknown')}")
        else:
            print(f"Error: {response.get('error', 'Unknown error')}")


def example_detailed_access(app: YouTubeTrendsApp):
    """Example of accessing detailed response data"""
    print("\n" + "="*70)
    print("DETAILED RESPONSE ACCESS")
    print("="*70)
    
    query = "Top 3 channels by views"
    print(f"\n📊 Query: {query}")
    print("-" * 70)
    
    response = app.query(query)
    
    print("\n🔍 Full Response Structure:")
    print(f"  Success: {response['success']}")
    print(f"  Query: {response['query']}")
    print(f"  Answer: {response['answer'][:200]}...")
    
    print("\n📋 Metadata:")
    metadata = response.get('metadata', {})
    for key, value in metadata.items():
        print(f"  {key}: {value}")
    
    print("\n🤖 Routing Information:")
    routing = response.get('routing', {})
    if routing:
        classification = routing.get('classification', {})
        print(f"  Type: {classification.get('type', 'N/A')}")
        print(f"  Confidence: {classification.get('confidence', 0):.2%}")
        print(f"  Reasoning: {classification.get('reasoning', 'N/A')}")
    
    print("\n📊 Agent Results:")
    if 'sql_result' in response:
        sql_result = response['sql_result']
        print(f"  SQL Agent Success: {sql_result.get('success', False)}")
        if sql_result.get('metadata'):
            print(f"  SQL Metadata: {sql_result['metadata']}")
    
    if 'vector_result' in response:
        vector_result = response['vector_result']
        print(f"  Vector Agent Success: {vector_result.get('success', False)}")
        if vector_result.get('metadata'):
            print(f"  Vector Metadata: {vector_result['metadata']}")


def example_error_handling(app: YouTubeTrendsApp):
    """Example of error handling"""
    print("\n" + "="*70)
    print("ERROR HANDLING EXAMPLES")
    print("="*70)
    
    # Empty query
    print("\n❌ Test: Empty query")
    response = app.query("")
    print(f"  Success: {response['success']}")
    print(f"  Error: {response.get('error', 'N/A')}")
    
    # Ambiguous query
    print("\n❓ Test: Ambiguous query")
    response = app.query("asdfghjkl")
    print(f"  Success: {response['success']}")
    print(f"  Answer: {response['answer'][:100]}...")


def example_system_info(app: YouTubeTrendsApp):
    """Example of getting system information"""
    print("\n" + "="*70)
    print("SYSTEM INFORMATION")
    print("="*70)
    
    info = app.get_system_info()
    
    print(f"\n🤖 Orchestrator: {info.get('orchestrator', 'Unknown')}")
    
    print("\n📦 Available Agents:")
    for agent_name, agent_info in info.get('agents', {}).items():
        print(f"\n  {agent_info.get('name', agent_name)}:")
        print(f"    Type: {agent_info.get('type', 'unknown')}")
        print(f"    Description: {agent_info.get('description', 'N/A')}")
        
        capabilities = agent_info.get('capabilities', [])
        if capabilities:
            print(f"    Capabilities:")
            for cap in capabilities[:3]:  # Show first 3
                print(f"      • {cap}")


def main():
    """Main example runner"""
    print("\n" + "="*70)
    print("  YOUTUBE TRENDS MULTI-AGENT SYSTEM - EXAMPLES")
    print("="*70)
    
    try:
        # Initialize app
        print("\n🚀 Initializing Multi-Agent System...")
        app = YouTubeTrendsApp()
        print("✅ System initialized successfully!")
        
        # Run examples
        example_system_info(app)
        example_sql_queries(app)
        example_vector_queries(app)
        example_hybrid_queries(app)
        example_detailed_access(app)
        example_error_handling(app)
        
        print("\n" + "="*70)
        print("✅ ALL EXAMPLES COMPLETED!")
        print("="*70)
        
    except Exception as e:
        logger.error(f"Error running examples: {e}")
        print(f"\n❌ Error: {str(e)}")
        print("\nMake sure you have:")
        print("  1. Set OPENAI_API_KEY in .env file")
        print("  2. Processed data: python scripts/process_and_index.py --csv data/raw/CAvideos.csv")
        print("  3. Started Qdrant: docker-compose up -d")
        sys.exit(1)


if __name__ == "__main__":
    main()
