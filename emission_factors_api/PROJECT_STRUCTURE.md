# Carbon6 Emission Factors API - Project Structure 

## 📋 Overview

This project implements a semantic search API for emission factors using vector embeddings with AWS Bedrock. The architecture follows modern API development practices with separation of concerns and a clean organization.

## 📁 Directory Structure

```
emission-factors-api/
├── app/                          # Main application package
│   ├── api/                      # API layer
│   │   ├── api_v1/               # API version 1
│   │   │   ├── endpoints/        # API endpoints
│   │   │   │   ├── __init__.py   
│   │   │   │   └── search.py     # Search endpoint
│   │   │   ├── __init__.py
│   │   │   └── api.py            # API router collection
│   │   └── __init__.py
│   ├── core/                     # Core functionality
│   │   ├── __init__.py
│   │   ├── config.py             # Application settings
│   │   └── vector_search.py      # Vector search service
│   ├── data/                     # Data directory (for caching)
│   ├── models/                   # Pydantic models
│   │   ├── __init__.py
│   │   └── emission_factor.py    # Emission factor models
│   ├── __init__.py
│   └── main.py                   # FastAPI application
├── efdb_embeddings/              # Emission factor databases with embeddings
│   └── *.json                    # JSON files with emission factors and vectors
├── tests/                        # Test suite
│   ├── __init__.py
│   ├── test_api.py               # API endpoint tests
│   └── test_vector_search.py     # Vector search tests
├── .env                          # Environment variables (git-ignored)
├── requirements.txt              # Project dependencies
├── run.py                        # Script to run the application
├── test_api.py                   # Script to test the API
├── PROJECT_STRUCTURE.md          # This file
├── Dockerfile                    # Docker configuration
├── docker-compose.yml            # Docker Compose configuration
└── README.md                     # Project documentation
```

## 🧩 Key Components

### 1. API Layer (`app/api/`)

- **Purpose**: Handles HTTP requests and responses
- **Key Files**:
  - `api_v1/api.py`: Collects and organizes all API routers
  - `api_v1/endpoints/search.py`: Implements the search endpoint
- **Features**:
  - Clean routing with API versioning
  - Automatic request validation
  - Structured error responses

### 2. Core Layer (`app/core/`)

- **Purpose**: Contains core business logic and services
- **Key Files**:
  - `config.py`: Application configuration settings
  - `vector_search.py`: Implements the vector search functionality using FAISS
- **Features**:
  - AWS Bedrock integration for embeddings
  - FAISS vector index for similarity search
  - Fallback to local models when needed

### 3. Models (`app/models/`)

- **Purpose**: Data models and validation
- **Key Files**:
  - `emission_factor.py`: Contains Pydantic models for emission factors and search requests/responses
- **Features**:
  - Automatic request/response validation
  - Clear documentation via Pydantic schemas
  - Consistent typing for all data

### 4. Application Entry Point (`app/main.py`)

- **Purpose**: Sets up the FastAPI application, middleware, and event handlers
- **Features**:
  - Configures CORS middleware
  - Sets up API routes
  - Initializes the vector search service on startup
  - Implements error handling
  - Swagger documentation setup

### 5. Data Store (`efdb_embeddings/`)

- **Purpose**: Contains the emission factor data with vector embeddings
- **Format**: JSON files containing emission factor details and their vector representations
- **Features**:
  - Pre-computed vectors for performance
  - Consistent vector dimensions
  - Organized categorization

### 6. Auxiliary Files

- `run.py`: Simple script to start the application with Uvicorn
- `test_api.py`: Script to test the API functionality
- `requirements.txt`: Lists all Python package dependencies
- `Dockerfile`: Container configuration for deployment
- `docker-compose.yml`: Multi-container application setup

## 🔄 Data Flow

1. **Startup Flow**:
   - Application loads configuration from environment variables
   - Emission factor data is read from JSON files
   - FAISS index is built from vector embeddings
   - FastAPI application is initialized with routes

2. **Search Request Flow**:
   - User submits search query via API
   - Request is validated using Pydantic models
   - Query text is converted to vector embedding using AWS Bedrock
   - FAISS performs similarity search against the index
   - Results are ranked, formatted, and returned to the client

3. **Error Handling Flow**:
   - Exceptions are caught at appropriate levels
   - Structured error responses are returned
   - Fallback mechanisms are employed when possible

## 🛠️ Design Principles

1. **Separation of Concerns**: Different aspects of the application are separated into different modules
2. **Single Responsibility**: Each module has a clear, single responsibility
3. **Dependency Injection**: Services are initialized and injected when needed
4. **Configuration Management**: Settings are centralized in the config module
5. **API Versioning**: Clear API versioning for future compatibility

## 🔍 Extending the Project

- **Adding New Endpoints**: Create new files in `app/api/api_v1/endpoints/` and register them in `api.py`
- **Adding New Services**: Create new service files in `app/core/`
- **Adding New Models**: Define new Pydantic models in `app/models/`
- **Adding Data**: Place additional JSON files in the `efdb_embeddings/` directory
- **Adding Tests**: Create test files in the `tests/` directory 