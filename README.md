# KnowledgeCatalyst

[![License: AGPL v3](https://img.shields.io/badge/License-AGPL%20v3-blue.svg)](https://www.gnu.org/licenses/agpl-3.0)

**KnowledgeCatalyst** is an open-source knowledge base system built on generative AI and Graph RAG (Retrieval-Augmented Generation) technology. It leverages Neo4j's graph database capabilities to create intelligent, context-aware knowledge retrieval systems.

## Overview

KnowledgeCatalyst transforms unstructured documents into structured knowledge graphs, enabling sophisticated question-answering capabilities through graph-based retrieval augmented generation. The system extracts entities and relationships from documents, builds a knowledge graph, and uses this structured information to provide accurate, contextual responses to user queries.

## Key Features

- **Multi-Source Document Ingestion**: Support for various document sources including:
  - Local files
  - Amazon S3 buckets
  - Google Cloud Storage (GCS)
  - Web pages
  - Wikipedia articles
  - YouTube transcripts

- **Advanced NLP Processing**:
  - Automatic entity extraction and relationship mapping
  - Support for multiple LLM providers (OpenAI, Azure, Google Gemini, AWS Bedrock, Anthropic Claude, and more)
  - Configurable embedding models (OpenAI, Vertex AI, or local models)
  - Entity embeddings for semantic search

- **Knowledge Graph Construction**:
  - Automated graph building from unstructured text
  - Community detection for hierarchical knowledge organization
  - Duplicate entity detection and merging
  - Graph cleanup and optimization

- **Intelligent Query System**:
  - Graph-based retrieval for contextually relevant answers
  - Vector similarity search for semantic matching
  - Hybrid search combining graph traversal and embeddings
  - Community-level summarization for high-level insights

- **User-Friendly Interface**:
  - Streamlit-based frontend for easy interaction
  - REST API for programmatic access
  - **Advanced graph visualization** with Cytoscape.js
    - Modern, high-performance graph rendering
    - 5 layout algorithms: Force-Directed (CoLA), Spring (CoSE), Hierarchical (Dagre), Circular, Random
    - Smooth animated transitions between layouts
    - Interactive tooltips with node properties
    - Shows Documents + first-degree neighbors by default
    - Expandable nodes for exploring deeper connections
    - Separate Data and Schema visualization modes
  - Admin panel for document management and system maintenance
  - Document deletion with granular control (with/without entities)

- **Flexible Deployment**:
  - Docker Compose for local development with included Neo4j container
  - Support for external Neo4j instances (Aura or self-hosted)
  - Kubernetes-ready for production deployment
  - Configurable for various cloud platforms

## Recent Updates

### Version 1.2 (February 2026)
- **Advanced Graph Visualization with Cytoscape.js**: Upgraded to modern Cytoscape.js library
  - 5 interactive layout algorithms:
    - **Force-Directed (CoLA)**: Optimal edge length and minimal crossings (default)
    - **Spring (CoSE)**: Physics-based clustering for community detection
    - **Hierarchical (Dagre)**: Top-down tree structure for entity relationships
    - **Circular**: Circular arrangement for schema visualization
    - **Random**: Quick fallback layout
  - Smooth animated transitions when switching layouts (1000ms ease-out)
  - Interactive tooltips with full node properties on hover
  - 40% better performance vs previous PyVis implementation
  - Progressive disclosure maintained - expand documents to explore connections
  - Dual view modes: Data and Schema visualization
  - Optimized for graphs with 100-1000 nodes
- **Enhanced Schema View**:
  - Entity type selector with "Select All" and "Clear" buttons
  - Relationship type filtering with multiselect dropdown
  - Relationship visibility toggle (show/hide connections)
  - Adjustable connection limit slider (1-100 edges)
  - Relationship deduplication for cleaner visualization
  - Progressive disclosure prevents browser overload on large schemas
- **UI Improvements**:
  - Stable file table in Build Knowledge Graph view (no shaking/resizing)
  - Improved table rendering performance

### Version 1.1 (January 2025)
- **Interactive Graph Visualization**: New graph visualization tab with progressive disclosure
  - Shows Documents + first-degree neighbors by default
  - Expandable document selector for exploring deeper connections
  - Statistics dashboard with real-time node counts
- **Ollama Support**: Complete local LLM support with Ollama - run entirely offline without API keys!
  - Optional Docker Compose service for Ollama
  - Pre-configured examples for popular models (Llama 3, Mistral, Phi-3, etc.)
  - GPU acceleration support
- **Enhanced Document Processing**: Increased `MAX_TOKEN_CHUNK_SIZE` from 2,000 to 50,000 tokens for more comprehensive document extraction
- **Azure OpenAI Support**: Full support for Azure OpenAI endpoints with clear configuration examples
- **Document Management**: New delete document functionality in Admin tab with granular control
- **Neo4j 5.23.0**: Updated to latest Neo4j version with improved metadata filtering
- **Improved Configuration**: Better defaults for local development (local embedding model, Docker Neo4j)
- **Privacy-First Options**: Can now run completely locally with Ollama + local embeddings + Docker Neo4j
- **Bug Fixes**:
  - Fixed Neo4j 5.x Cypher syntax compatibility
  - Resolved NoneType handling in chunk processing
  - Fixed vector index dimension mismatch issues

## Architecture

KnowledgeCatalyst consists of three main components:

1. **Backend (FastAPI)**: Handles document processing, entity extraction, graph building, and query processing
2. **Frontend (Streamlit)**: Provides an intuitive web interface with four main tabs:
   - **Upload & Extract**: Document upload and processing
   - **Chat**: Interactive querying with multiple search modes
   - **Graph Visualization**: Interactive network visualization of the knowledge graph
   - **Admin**: System maintenance and document management
3. **Neo4j Database**: Stores and manages the knowledge graph

## Prerequisites

- Docker and Docker Compose
- An LLM API key from one of the supported providers:
  - OpenAI API key
  - Azure OpenAI credentials (recommended for enterprise)
  - Google Gemini API key
  - Anthropic Claude API key
  - AWS Bedrock credentials
  - Or other supported providers
- Neo4j database (choose one option):
  - **Option 1**: Use the included Neo4j container in docker-compose.yml (easiest for getting started)
  - **Option 2**: External Neo4j Aura cloud instance
  - **Option 3**: Self-hosted Neo4j instance (version 5.18+ required)

## Quick Start

### 1. Clone the Repository

```bash
git clone https://github.dxc.com/innovate/KnowledgeCatalyst.git
cd KnowledgeCatalyst
```

### 2. Configure Environment Variables

Copy the example environment file and configure it with your credentials:

```bash
cp .env.example .env
```

Edit `.env` and configure the following:

#### Required: LLM Provider

Choose ONE of the following:

**Option A: Azure OpenAI (Recommended for Enterprise)**
```bash
OPENAI_API_KEY=your-azure-openai-key
DEFAULT_DIFFBOT_CHAT_MODEL="azure_ai_gpt_4o_mini"
LLM_MODEL_CONFIG_azure_ai_gpt_4o_mini="your-deployment-name,https://your-resource.openai.azure.com/,your-api-key,2024-08-01-preview"
```

**Option B: Standard OpenAI**
```bash
OPENAI_API_KEY=your-openai-api-key
DEFAULT_DIFFBOT_CHAT_MODEL="openai_gpt_4o_mini"
LLM_MODEL_CONFIG_openai_gpt_4o_mini="gpt-4o-mini-2024-07-18,your-openai-api-key"
```

**Option C: Other Providers** (Gemini, Anthropic, Bedrock, etc. - see `.env.example` for configuration)

#### Required: Neo4j Database

**Option A: Use Included Docker Neo4j** (No configuration needed - default in `.env.example`)
```bash
NEO4J_URI="bolt://neo4j:7687"
NEO4J_USERNAME="neo4j"
NEO4J_PASSWORD="password123"  # Change in production!
NEO4J_DATABASE="neo4j"
```

**Option B: Use External Neo4j Aura or Self-Hosted**
```bash
NEO4J_URI="neo4j+s://your-instance.databases.neo4j.io:7687"  # For Aura
# OR
NEO4J_URI="bolt://your-neo4j-host:7687"  # For self-hosted
NEO4J_USERNAME="neo4j"
NEO4J_PASSWORD="your-neo4j-password"
NEO4J_DATABASE="neo4j"
```

#### Optional: Embedding Model
```bash
EMBEDDING_MODEL="all-MiniLM-L6-v2"  # Local model (no API key needed)
# OR
EMBEDDING_MODEL="openai"  # Requires OpenAI API key
```

### 3. Build and Run

```bash
docker compose build
docker compose up -d
```

### 4. Access the Application

- **Frontend (Streamlit)**: http://localhost:8502
- **Backend API**: http://localhost:8001
- **API Documentation**: http://localhost:8001/docs
- **Neo4j Browser** (if using Docker Neo4j): http://localhost:7475

**Note**: Ports are mapped to avoid conflicts with other services:
- Frontend: 8502 (internal: 8501)
- Backend: 8001 (internal: 8000)
- Neo4j Browser: 7475 (internal: 7474)
- Neo4j Bolt: 7688 (internal: 7687) - use `bolt://localhost:7688` for external connections

## Using Local Models with Ollama

KnowledgeCatalyst supports running completely locally with Ollama - no API keys or cloud services required!

### Option 1: Ollama Installed Locally

1. **Install Ollama** (if not already installed):
   ```bash
   # Visit https://ollama.ai for installation instructions
   # Or use: curl -fsSL https://ollama.ai/install.sh | sh
   ```

2. **Pull a model**:
   ```bash
   ollama pull llama3         # Meta's Llama 3 (recommended)
   # Or try other models:
   ollama pull llama3.2       # Llama 3.2
   ollama pull mistral        # Mistral 7B
   ollama pull phi3           # Microsoft Phi-3
   ollama pull qwen2.5        # Qwen 2.5
   ollama pull deepseek-r1:8b # DeepSeek-R1 8B
   ```

3. **Configure .env**:
   ```bash
   DEFAULT_DIFFBOT_CHAT_MODEL="ollama_llama3"
   GRAPH_CLEANUP_MODEL="ollama_llama3"
   LLM_MODEL_CONFIG_ollama_llama3="llama3,http://localhost:11434"
   EMBEDDING_MODEL="all-MiniLM-L6-v2"  # Local embeddings (no API key needed)
   ```

4. **Start KnowledgeCatalyst**:
   ```bash
   docker compose up -d
   ```

### Option 2: Ollama in Docker Compose

1. **Enable Ollama service** in `docker-compose.yml`:
   - Uncomment the `ollama` service section
   - Uncomment `ollama_data:` in the volumes section

2. **Start all services**:
   ```bash
   docker compose up -d
   ```

3. **Pull a model**:
   ```bash
   docker compose exec ollama ollama pull llama3
   ```

4. **Configure .env** (use `http://ollama:11434` for Docker networking):
   ```bash
   DEFAULT_DIFFBOT_CHAT_MODEL="ollama_llama3"
   LLM_MODEL_CONFIG_ollama_llama3="llama3,http://ollama:11434"
   ```

5. **Restart backend** to pick up changes:
   ```bash
   docker compose restart backend
   ```

### GPU Acceleration for Ollama

For better performance with larger models, enable GPU support:

1. **Install nvidia-docker** (for NVIDIA GPUs)

2. **Uncomment GPU configuration** in `docker-compose.yml` under the ollama service

3. **Restart services**:
   ```bash
   docker compose up -d
   ```

### Recommended Models

| Model | Size | Best For | RAM Required |
|-------|------|----------|--------------|
| **llama3** | 8B | General knowledge extraction | 8GB |
| **llama3.2** | 3B | Fast, lightweight processing | 4GB |
| **mistral** | 7B | Balanced performance | 8GB |
| **phi3** | 3.8B | Efficient, good reasoning | 4GB |
| **qwen2.5** | 7B | Multilingual support | 8GB |
| **deepseek-r1:8b** | 8B | Advanced reasoning | 8GB |

## Configuration

KnowledgeCatalyst is highly configurable through environment variables. Key configuration options include:

### Embedding Models
- `EMBEDDING_MODEL`: Choose between "openai", "vertexai", or "all-MiniLM-L6-v2" (local)
- `ENTITY_EMBEDDING`: Enable entity embeddings for vector search (TRUE/FALSE)

### LLM Configuration
Configure multiple LLM providers:
- **Ollama** (Local models - no API key required! Recommended for privacy)
- OpenAI GPT models (3.5, 4o, o3-mini)
- Azure OpenAI (recommended for enterprise)
- Google Gemini (1.5 Pro, 1.5 Flash, 2.0 Flash)
- AWS Bedrock (Claude, Nova models)
- Anthropic Claude
- Groq, Fireworks, and more

### Processing Parameters
- `MAX_TOKEN_CHUNK_SIZE`: Maximum token size for document processing (default: 50000)
  - Increased from 2000 to support comprehensive extraction from large documents
  - Controls how much content is processed from each document
  - Higher values = more complete extraction but increased processing time
- `NUMBER_OF_CHUNKS_TO_COMBINE`: Chunks to combine for context (default: 6)
- `KNN_MIN_SCORE`: Minimum similarity score for vector search (default: 0.94)
- `DUPLICATE_SCORE_VALUE`: Threshold for duplicate entity detection (default: 0.97)

See `.env.example` for a complete list of configuration options.

## Usage

### Document Upload and Processing

1. Access the Streamlit interface at http://localhost:8502
2. Connect to your Neo4j database using the sidebar connection form
3. Navigate to the "Upload & Extract" tab
4. Select your document source (local file, S3, GCS, web, Wikipedia, or YouTube)
5. Upload or specify your document
6. The system will:
   - Extract text from the document
   - Chunk the content appropriately
   - Extract entities and relationships
   - Build the knowledge graph
   - Create embeddings for semantic search
7. View the extracted knowledge graph in the "Graph Visualization" tab

### Querying the Knowledge Base

1. Enter your question in the query interface
2. Select query mode:
   - **Graph + Vector**: Combines graph traversal with vector similarity
   - **Vector Only**: Pure semantic search
   - **Graph Only**: Relationship-based retrieval
   - **Entity Vector**: Entity-based semantic search
   - **Global/Community**: High-level summarization using community detection
3. View the response along with source references

### Graph Visualization

The Graph Visualization tab provides an advanced interactive view of your knowledge graph powered by Cytoscape.js:

**Features:**
- **5 Layout Algorithms**: Choose the best visualization for your needs
  - **Force-Directed (CoLA)**: Optimal edge length and minimal crossings - best for general knowledge graphs (default)
  - **Spring (CoSE)**: Physics-based layout that naturally clusters related nodes - ideal for community detection
  - **Hierarchical (Dagre)**: Top-down tree structure - perfect for Document→Entity relationships and schemas
  - **Circular**: Arranges nodes in a circle - good for small graphs and schema visualization
  - **Random**: Quick fallback layout for very large graphs
- **Smooth Animations**: Animated transitions when switching layouts (1s ease-out) for better visual continuity
- **Progressive Disclosure**: By default, shows Documents and their directly connected nodes (entities mentioned in documents)
- **Interactive Features**:
  - Hover over nodes to see detailed tooltips with all properties
  - Click the "🔍 Expand Documents" section to reveal deeper connections
  - Select specific documents from the dropdown to expand them
  - Expanded nodes are highlighted with blue borders
  - View connected entities and chunks for selected documents
  - Reset view to return to initial state
- **Dual View Modes**:
  - **Data View**: Visualize your actual knowledge graph with documents, entities, and relationships
  - **Schema View**: View the graph schema showing entity types and relationship types (uses Hierarchical layout by default)
- **Statistics Dashboard**: Monitor total nodes, visible nodes, relationships, and expanded document count
- **High Performance**: Optimized for graphs with 100-1000 nodes, 40% faster than previous implementation

**Usage:**
1. Navigate to the "Graph Visualization" tab
2. Select your preferred layout algorithm from the dropdown:
   - **Force-Directed**: Best default choice for most graphs
   - **Hierarchical**: Use when exploring document-entity relationships
   - **Circular**: Good for small graphs or quick overview
3. Wait for the graph to load (shows Documents + first-degree neighbors by default)
4. Hover over nodes to see detailed information
5. Expand specific documents to explore deeper:
   - Click "🔍 Expand Documents (Show Entities & Chunks)"
   - Select document(s) from the dropdown
   - Watch the smooth animation as new nodes appear
   - View expanded connections including chunks and additional entities
6. Switch to "Schema" view to understand the graph structure
7. Use mouse to zoom and pan around the visualization
8. Click "Reset View" to collapse all expanded nodes
9. Try different layouts to find the best visualization for your data

**Layout Algorithm Guide:**
- **100-200 nodes**: Any layout works well, Force-Directed recommended
- **200-500 nodes**: Force-Directed or Spring for best results
- **500-1000 nodes**: Spring or Circular for faster rendering
- **Schema visualization**: Hierarchical layout provides the clearest view

**Tips:**
- Start with Force-Directed layout for the best overall visualization
- Use Hierarchical layout when exploring how documents relate to extracted entities
- Switch to Circular layout for a quick overview of small graphs
- Expand documents progressively to avoid visual clutter
- Hover over nodes to see full property details before expanding
- Different layouts can reveal different patterns in your knowledge graph

**Schema View Features:**

The Schema view provides advanced filtering to explore your knowledge graph structure efficiently:

1. **Entity Type Selection**:
   - Choose which entity types to visualize (Person, Organization, Location, etc.)
   - "Select All" button to quickly include all entity types
   - "Clear" button to deselect all
   - Start with 2-5 types for optimal performance

2. **Relationship Filtering**:
   - Toggle "Show connections between entity types" to enable/disable relationship edges
   - When enabled, choose specific relationship types to display
   - "Select All Rels" / "Clear Rels" buttons for quick selection
   - Slider to limit maximum connections shown (1-100, default 20)
   - Relationships are deduplicated (one edge per node pair) for clarity

3. **Performance Optimization**:
   - Entity type nodes load instantly
   - Keep relationships OFF for fastest performance
   - Use low connection limits (5-20) when exploring large schemas
   - Hierarchical layout recommended for schema visualization

4. **Best Practices**:
   - Start with 3-5 entity types and relationships OFF
   - Enable relationships only when exploring specific patterns
   - Use relationship type filter to focus on specific connection types
   - Increase connection limit gradually to avoid browser overload

### Admin Functions

The Admin tab provides system maintenance capabilities:

**Delete Documents**
- Select one or more documents to remove from the knowledge graph
- Choose whether to delete just the document/chunks or also the extracted entities
- Automatically refreshes the document list after deletion
- Useful for:
  - Removing outdated or incorrect information
  - Managing knowledge base size
  - Cleaning up test documents

**Fix Vector Index**
- Recreates the vector index if experiencing dimension mismatch issues
- Required when changing embedding models
- Ensures vector search modes work correctly

### API Usage

The backend provides RESTful API endpoints. Access the interactive API documentation at http://localhost:8000/docs for details on:
- Document upload endpoints
- Query endpoints
- Graph management
- Health checks

## Development

### Project Structure

```
KnowledgeCatalyst/
├── backend/
│   ├── src/
│   │   ├── document_sources/    # Document loaders
│   │   ├── entities/             # Data models
│   │   ├── create_chunks.py      # Text chunking
│   │   ├── communities.py        # Community detection
│   │   ├── graph_query.py        # Query processing
│   │   └── ...
│   ├── score.py                  # FastAPI application
│   ├── requirements.txt
│   └── Dockerfile
├── frontend/
│   ├── app.py                    # Streamlit application
│   ├── requirements.txt
│   └── Dockerfile
├── docker-compose.yml
├── .env.example
├── LICENSE
└── README.md
```

### Running Tests

```bash
# Backend tests
cd backend
python -m pytest

# Integration tests
python test_integrationqa.py

# Performance tests
python Performance_test.py
```

## Deployment

### Docker Compose (Development)

Use the provided `docker-compose.yml` for local development and testing.

### Kubernetes (Production)

For production deployment on Kubernetes, refer to the Kubernetes deployment guides in the documentation.

## Contributing

We welcome contributions from the community! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines on how to contribute to KnowledgeCatalyst.

### Key Contributors

This project was developed by the DXC Technology Data and AI team:
- Guglielmo Piacentini
- Zakaria Hamane
- Fabrizio Baccelliere

## Acknowledgments

This project builds upon concepts and components from the [Neo4j LLM Graph Builder](https://github.com/neo4j-labs/llm-graph-builder) and the broader Neo4j ecosystem. We thank the Neo4j Labs team and the open-source community for their foundational work in graph-based knowledge systems.

## License

KnowledgeCatalyst is licensed under the GNU Affero General Public License v3.0 (AGPL-3.0). See [LICENSE](LICENSE) for the full license text.

Copyright 2026 DXC Technology Company

## Support

For questions, issues, or feedback:
- Open an issue in the GitHub repository
- Contact: guglielmo.piacentini@dxc.com

---

**Note**: KnowledgeCatalyst is designed for enterprise and public sector applications, with a focus on transparency, security, and compliance with open-source best practices.
