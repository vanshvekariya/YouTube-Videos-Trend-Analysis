# Architecture Documentation

## System Overview

The YouTube Trends Explorer POC is built with a modular, scalable architecture designed for semantic search over YouTube trending videos using vector embeddings and Qdrant vector database.

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                        Data Sources                              │
│                  (Kaggle YouTube Dataset)                        │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                     Data Ingestion Layer                         │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐         │
│  │ DataLoader   │─▶│Preprocessor  │─▶│ Documents    │         │
│  └──────────────┘  └──────────────┘  └──────────────┘         │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                    Embedding Layer                               │
│  ┌──────────────────┐         ┌──────────────────┐             │
│  │ Local Embeddings │   OR    │ OpenAI Embeddings│             │
│  │ (sentence-trans) │         │  (API-based)     │             │
│  └──────────────────┘         └──────────────────┘             │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                   Vector Database Layer                          │
│                      (Qdrant)                                    │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐         │
│  │   Storage    │  │   Indexing   │  │   Search     │         │
│  │   (HNSW)     │  │   (Cosine)   │  │   (ANN)      │         │
│  └──────────────┘  └──────────────┘  └──────────────┘         │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                    Search & Query Layer                          │
│  ┌──────────────────┐  ┌──────────────────┐                    │
│  │ Semantic Search  │  │ Metadata Filter  │                    │
│  └──────────────────┘  └──────────────────┘                    │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                    Application Layer                             │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐         │
│  │   Scripts    │  │   Notebooks  │  │  Future API  │         │
│  └──────────────┘  └──────────────┘  └──────────────┘         │
└─────────────────────────────────────────────────────────────────┘
```

## Component Details

### 1. Data Ingestion Layer (`src/data/`)

**Purpose**: Load and preprocess YouTube trending data

**Components**:
- **DataLoader**: Loads CSV files from Kaggle dataset
  - Handles multiple country files
  - Combines data from different sources
  - Provides sampling for testing

- **DataPreprocessor**: Cleans and transforms data
  - Text cleaning and normalization
  - Tag parsing
  - Category mapping
  - Creates searchable text fields
  - Converts to document format

**Key Features**:
- Handles encoding issues
- Removes duplicates
- Validates data quality
- Batch processing support

### 2. Embedding Layer (`src/embeddings/`)

**Purpose**: Convert text to vector embeddings

**Components**:
- **BaseEmbedding**: Abstract interface for embedding models
- **LocalEmbedding**: Sentence-transformers implementation
  - Model: `all-MiniLM-L6-v2` (384 dimensions)
  - No API key required
  - Runs locally
  - Good balance of speed/quality

- **OpenAIEmbedding**: OpenAI API implementation
  - Model: `text-embedding-3-small` (1536 dimensions)
  - Requires API key
  - Higher quality embeddings
  - API rate limits apply

- **Factory**: Automatic model selection based on config

**Design Decisions**:
- Strategy pattern for easy model switching
- Batch processing for efficiency
- Progress tracking for long operations
- Consistent interface across implementations

### 3. Vector Database Layer (`src/vectordb/`)

**Purpose**: Store and search vector embeddings

**Technology**: Qdrant
- **Why Qdrant?**
  - Open source
  - Easy Docker deployment
  - Excellent performance
  - Rich filtering capabilities
  - Good Python client

**Components**:
- **QdrantManager**: Connection and collection management
  - Collection creation/deletion
  - Health checks
  - Configuration management

- **VectorDBOperations**: High-level operations
  - Document indexing
  - Similarity search
  - Metadata filtering
  - Batch operations

**Features**:
- HNSW indexing for fast ANN search
- Cosine similarity metric
- Metadata filtering (category, views, country)
- Batch upload for efficiency

### 4. Search Layer (`src/search/`)

**Purpose**: Provide semantic search functionality

**Components**:
- **SemanticSearch**: Main search interface
  - Natural language queries
  - Category filtering
  - Popularity filtering
  - Similar video discovery
  - Result formatting

**Search Capabilities**:
- Semantic similarity search
- Hybrid filtering (vector + metadata)
- Configurable result limits
- Score thresholds
- Multiple search modes

### 5. Configuration Layer (`src/config/`)

**Purpose**: Centralized configuration management

**Components**:
- **Settings**: Pydantic-based configuration
  - Environment variable loading
  - Type validation
  - Default values
  - Path management

**Configuration Sources**:
1. `.env` file (primary)
2. Environment variables
3. Default values

### 6. Application Layer

**Scripts** (`scripts/`):
- `ingest_data.py`: Full data pipeline
- `search_demo.py`: Interactive search demo
- `create_embeddings.py`: Standalone embedding generation

**Notebooks** (`notebooks/`):
- `exploratory_analysis.ipynb`: Interactive exploration

**Tests** (`tests/`):
- Unit tests for core components
- Integration tests for workflows

## Data Flow

### Ingestion Flow

```
CSV Files → DataLoader → Raw DataFrame
    ↓
Preprocessor → Cleaned DataFrame
    ↓
Document Converter → Document List
    ↓
Embedding Model → Vector Embeddings
    ↓
Qdrant Operations → Indexed Collection
```

### Search Flow

```
User Query → Embedding Model → Query Vector
    ↓
Qdrant Search (with filters) → Similar Vectors
    ↓
Result Formatter → Ranked Results
    ↓
User Interface
```

## Technology Stack

### Core Technologies
- **Python 3.9+**: Main language
- **Qdrant**: Vector database
- **Sentence-Transformers**: Local embeddings
- **Docker**: Containerization

### Key Libraries
- **qdrant-client**: Vector DB client
- **sentence-transformers**: Embedding models
- **pandas**: Data processing
- **pydantic**: Configuration & validation
- **loguru**: Logging
- **tqdm**: Progress bars

### Development Tools
- **pytest**: Testing
- **black**: Code formatting
- **flake8**: Linting
- **jupyter**: Notebooks

## Design Patterns

### 1. Strategy Pattern
- Used for embedding models
- Easy to switch between local/API embeddings
- Consistent interface

### 2. Factory Pattern
- Embedding model creation
- Automatic selection based on config

### 3. Repository Pattern
- VectorDBOperations abstracts Qdrant details
- Clean separation of concerns

### 4. Configuration Pattern
- Centralized settings
- Environment-based configuration
- Type-safe with Pydantic

## Scalability Considerations

### Current Scale
- Handles 10K-100K videos efficiently
- Single machine deployment
- Local embeddings

### Future Scaling Options

**Horizontal Scaling**:
- Qdrant cluster mode
- Distributed embedding generation
- Load balancing

**Vertical Scaling**:
- GPU acceleration for embeddings
- Larger embedding models
- More RAM for batch processing

**Optimization**:
- Caching frequently accessed embeddings
- Incremental indexing
- Async operations

## Security Considerations

### Current Implementation
- API keys in `.env` (not committed)
- Local-first approach (no external calls by default)
- Docker network isolation

### Production Recommendations
- Use secrets management (Azure Key Vault, AWS Secrets Manager)
- API rate limiting
- Authentication/authorization
- HTTPS for API endpoints
- Input validation and sanitization

## Performance Metrics

### Embedding Generation
- **Local Model**: ~100-500 texts/second (CPU)
- **OpenAI API**: ~100 texts/second (rate limited)

### Search Performance
- **Query Time**: <100ms for 10K vectors
- **Indexing**: ~1000 vectors/second
- **Memory**: ~1GB for 10K vectors (384 dim)

### Bottlenecks
1. Embedding generation (CPU-bound)
2. CSV parsing (I/O-bound)
3. Network latency (for OpenAI)

## Future Architecture Enhancements

### Phase 2: RAG Integration
```
Search Results → LLM Context → Generated Response
```

### Phase 3: Graph Database
```
Qdrant (vectors) ↔ Neo4j (relationships)
```

### Phase 4: API & UI
```
FastAPI Backend ↔ React Frontend
```

### Phase 5: Real-time Updates
```
YouTube API → Stream Processing → Live Updates
```

## Error Handling Strategy

### Levels
1. **Data Level**: Skip malformed records, log warnings
2. **Processing Level**: Retry with backoff, fallback options
3. **System Level**: Graceful degradation, health checks

### Logging
- Structured logging with loguru
- Different levels: DEBUG, INFO, WARNING, ERROR
- Contextual information in logs

## Testing Strategy

### Unit Tests
- Individual component testing
- Mock external dependencies
- Fast execution

### Integration Tests
- End-to-end workflows
- Real Qdrant instance
- Sample data

### Performance Tests
- Load testing
- Benchmark embedding speed
- Search latency measurement

## Deployment Options

### Development
- Local Python environment
- Docker Compose for Qdrant
- `.env` configuration

### Production Options

**Option 1: Single Server**
- Docker Compose
- Nginx reverse proxy
- Systemd services

**Option 2: Cloud Native**
- Kubernetes deployment
- Managed Qdrant (Qdrant Cloud)
- Cloud functions for processing

**Option 3: Serverless**
- AWS Lambda for API
- Qdrant Cloud for vectors
- S3 for data storage

## Monitoring & Observability

### Metrics to Track
- Search latency
- Embedding generation time
- Qdrant memory usage
- Query success rate
- Error rates

### Tools
- Prometheus for metrics
- Grafana for visualization
- Qdrant built-in metrics
- Application logs

## Conclusion

This architecture provides:
- ✅ **Modularity**: Easy to extend and modify
- ✅ **Scalability**: Can grow with data volume
- ✅ **Maintainability**: Clean separation of concerns
- ✅ **Testability**: Well-defined interfaces
- ✅ **Flexibility**: Multiple embedding options
- ✅ **Performance**: Optimized for speed

The POC validates the core concept and provides a solid foundation for future enhancements including RAG, graph analytics, and production deployment.
