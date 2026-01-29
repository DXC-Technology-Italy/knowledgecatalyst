# Running KnowledgeCatalyst with Ollama (Fully Local Setup)

This guide shows you how to run KnowledgeCatalyst completely locally using Ollama for LLM inference - no API keys or cloud services required!

## Why Use Ollama?

- **Complete Privacy**: All data stays on your machine
- **No API Costs**: Free to use, no per-token charges
- **Offline Capable**: Works without internet connection
- **Fast**: Local inference can be faster than API calls
- **Full Control**: Choose and customize your own models

## Quick Start

### Prerequisites

- Docker and Docker Compose installed
- At least 8GB RAM (16GB recommended for larger models)
- Optional: NVIDIA GPU for faster inference

### Setup Steps

#### 1. Install Ollama

**Option A: Install Ollama on your host machine**
```bash
# Linux/Mac
curl -fsSL https://ollama.ai/install.sh | sh

# Windows
# Download from https://ollama.ai
```

**Option B: Use Ollama in Docker Compose** (recommended)
- Edit `docker-compose.yml` and uncomment the `ollama` service
- Uncomment `ollama_data:` in the volumes section

#### 2. Pull a Model

**If using host Ollama:**
```bash
ollama pull llama3
```

**If using Docker Ollama:**
```bash
docker compose up -d ollama
docker compose exec ollama ollama pull llama3
```

#### 3. Configure Environment

Edit your `.env` file:

```bash
# Use Ollama for LLM
DEFAULT_DIFFBOT_CHAT_MODEL="ollama_llama3"
GRAPH_CLEANUP_MODEL="ollama_llama3"

# Configure Ollama endpoint
# For host Ollama:
LLM_MODEL_CONFIG_ollama_llama3="llama3,http://localhost:11434"

# For Docker Ollama (use service name):
# LLM_MODEL_CONFIG_ollama_llama3="llama3,http://ollama:11434"

# Use local embeddings (no API key needed)
EMBEDDING_MODEL="all-MiniLM-L6-v2"
RAGAS_EMBEDDING_MODEL=""

# Remove or comment out API keys (not needed)
# OPENAI_API_KEY=

# Neo4j (use included Docker service)
NEO4J_URI="bolt://neo4j:7687"
NEO4J_USERNAME="neo4j"
NEO4J_PASSWORD="password123"
NEO4J_DATABASE="neo4j"
```

#### 4. Start KnowledgeCatalyst

```bash
docker compose up -d
```

Access the application at http://localhost:8502

## Model Recommendations

### For 8GB RAM Systems

**Llama 3.2 3B** - Fast and efficient
```bash
ollama pull llama3.2
```
```bash
LLM_MODEL_CONFIG_ollama_llama3_2="llama3.2,http://localhost:11434"
DEFAULT_DIFFBOT_CHAT_MODEL="ollama_llama3_2"
```

**Phi-3 Mini** - Microsoft's efficient model
```bash
ollama pull phi3
```
```bash
LLM_MODEL_CONFIG_ollama_phi3="phi3,http://localhost:11434"
DEFAULT_DIFFBOT_CHAT_MODEL="ollama_phi3"
```

### For 16GB+ RAM Systems

**Llama 3 8B** - Best all-around performance (recommended)
```bash
ollama pull llama3
```
```bash
LLM_MODEL_CONFIG_ollama_llama3="llama3,http://localhost:11434"
DEFAULT_DIFFBOT_CHAT_MODEL="ollama_llama3"
```

**Mistral 7B** - Excellent for knowledge extraction
```bash
ollama pull mistral
```
```bash
LLM_MODEL_CONFIG_ollama_mistral="mistral,http://localhost:11434"
DEFAULT_DIFFBOT_CHAT_MODEL="ollama_mistral"
```

**DeepSeek-R1 8B** - Advanced reasoning capabilities
```bash
ollama pull deepseek-r1:8b
```
```bash
LLM_MODEL_CONFIG_ollama_deepseek_r1="deepseek-r1:8b,http://localhost:11434"
DEFAULT_DIFFBOT_CHAT_MODEL="ollama_deepseek_r1"
```

### For 32GB+ RAM or GPU Systems

**Qwen 2.5 14B** - Excellent multilingual support
```bash
ollama pull qwen2.5:14b
```

**Llama 3 70B** - Highest quality (requires GPU)
```bash
ollama pull llama3:70b
```

## GPU Acceleration

### NVIDIA GPU Setup

1. **Install NVIDIA Container Toolkit**:
```bash
# Ubuntu/Debian
distribution=$(. /etc/os-release;echo $ID$VERSION_ID)
curl -s -L https://nvidia.github.io/nvidia-docker/gpgkey | sudo apt-key add -
curl -s -L https://nvidia.github.io/nvidia-docker/$distribution/nvidia-docker.list | \
  sudo tee /etc/apt/sources.list.d/nvidia-docker.list
sudo apt-get update && sudo apt-get install -y nvidia-container-toolkit
sudo systemctl restart docker
```

2. **Enable GPU in docker-compose.yml**:
Uncomment the GPU configuration under the ollama service:
```yaml
deploy:
  resources:
    reservations:
      devices:
        - driver: nvidia
          count: 1
          capabilities: [gpu]
```

3. **Restart services**:
```bash
docker compose down
docker compose up -d
```

4. **Verify GPU is being used**:
```bash
docker compose exec ollama nvidia-smi
```

## Using Multiple Models

You can configure multiple Ollama models and switch between them:

```bash
# In .env
LLM_MODEL_CONFIG_ollama_llama3="llama3,http://localhost:11434"
LLM_MODEL_CONFIG_ollama_mistral="mistral,http://localhost:11434"
LLM_MODEL_CONFIG_ollama_phi3="phi3,http://localhost:11434"

# Use different models for different tasks
DEFAULT_DIFFBOT_CHAT_MODEL="ollama_llama3"      # For chat
GRAPH_CLEANUP_MODEL="ollama_phi3"                # Lighter model for cleanup
```

Then in the Streamlit UI, you can select which model to use for each query.

## Performance Tips

### 1. Keep Model Loaded
Models stay loaded in memory after first use, making subsequent queries much faster.

### 2. Adjust Context Window
For longer documents, you may want to use models with larger context windows:
```bash
ollama pull llama3:32k  # 32k context window version
```

### 3. Model Quantization
Ollama models are pre-quantized for efficiency. For even smaller models:
```bash
ollama pull llama3:8b-q4_0  # 4-bit quantized (smaller, faster)
```

### 4. Concurrent Requests
Ollama can handle multiple concurrent requests. Adjust based on your RAM:
```bash
# Set in .env if using Docker Ollama
OLLAMA_NUM_PARALLEL=2
```

## Troubleshooting

### Model Not Found
```bash
# List available models
ollama list

# Pull the model if missing
ollama pull llama3
```

### Connection Refused
```bash
# Check if Ollama is running
curl http://localhost:11434/api/tags

# Restart Ollama
docker compose restart ollama  # If using Docker
# OR
systemctl restart ollama  # If installed on host
```

### Out of Memory
- Use a smaller model (e.g., llama3.2 instead of llama3)
- Reduce `MAX_TOKEN_CHUNK_SIZE` in .env
- Close other applications
- Enable GPU acceleration if available

### Slow Performance
- Use GPU acceleration
- Try a smaller/quantized model
- Ensure model is loaded (first query is always slower)
- Check system resources: `docker stats`

## Complete Local Setup Example

Here's a complete `.env` configuration for running fully locally:

```bash
# ============================================================================
# FULLY LOCAL CONFIGURATION - NO API KEYS REQUIRED
# ============================================================================

# Ollama LLM (Local)
DEFAULT_DIFFBOT_CHAT_MODEL="ollama_llama3"
GRAPH_CLEANUP_MODEL="ollama_llama3"
LLM_MODEL_CONFIG_ollama_llama3="llama3,http://ollama:11434"

# Local Embeddings (No API key needed)
EMBEDDING_MODEL="all-MiniLM-L6-v2"
RAGAS_EMBEDDING_MODEL=""
IS_EMBEDDING="TRUE"
ENTITY_EMBEDDING="TRUE"

# Search Configuration
KNN_MIN_SCORE="0.94"
EFFECTIVE_SEARCH_RATIO=5
DUPLICATE_SCORE_VALUE=0.97
DUPLICATE_TEXT_DISTANCE=3

# Processing Configuration
NUMBER_OF_CHUNKS_TO_COMBINE=6
UPDATE_GRAPH_CHUNKS_PROCESSED=20
MAX_TOKEN_CHUNK_SIZE=50000

# Neo4j Database (Docker)
NEO4J_URI="bolt://neo4j:7687"
NEO4J_USERNAME="neo4j"
NEO4J_PASSWORD="password123"
NEO4J_DATABASE="neo4j"

# Backend Configuration
BACKEND_URL="http://backend:8000"

# Optional Features (disabled for local use)
GEMINI_ENABLED=False
GCP_LOG_METRICS_ENABLED=False
GCS_FILE_CACHE=""
```

## Next Steps

1. **Upload documents** via the Streamlit UI
2. **Extract knowledge graph** - this uses your local Ollama model
3. **Query your knowledge base** - all processing happens locally
4. **Experiment with different models** to find the best balance of speed and quality

## Support

For Ollama-specific issues:
- Ollama Documentation: https://ollama.ai/docs
- Ollama GitHub: https://github.com/ollama/ollama

For KnowledgeCatalyst issues:
- Open an issue in the GitHub repository
- Contact: guglielmo.piacentini@dxc.com
