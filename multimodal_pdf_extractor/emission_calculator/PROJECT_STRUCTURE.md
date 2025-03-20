# Carbon6 Emission Calculator - Project Structure

## 📋 Overview

This project implements a comprehensive document processing and carbon accounting system. It combines PDF extraction, multimodal analysis, vector search, and emissions calculation capabilities into an integrated application with a Streamlit frontend.

## 📁 Directory Structure

```
emission-calculator/
├── emission_calculator/         # Main application package
│   ├── app/                      # Application core
│   │   ├── frontend/             # UI components
│   │   │   ├── pages/            # Streamlit pages
│   │   │   └── streamlit_app.py  # Main Streamlit application
│   │   └── utils/                # Frontend utilities
│   ├── core/                     # Core functionality
│   │   ├── document_processor/   # Document processing
│   │   │   ├── __init__.py
│   │   │   ├── extractor.py      # Content extraction
│   │   │   ├── ocr.py            # OCR capabilities
│   │   │   └── parser.py         # Document parsing
│   │   ├── embedding/            # Vector embedding
│   │   │   ├── __init__.py
│   │   │   └── embedder.py       # Vector embedding logic
│   │   ├── vector_store/         # Vector database
│   │   │   ├── __init__.py
│   │   │   └── store.py          # Milvus integration
│   │   ├── carbon_accounting/    # Carbon accounting
│   │   │   ├── __init__.py
│   │   │   ├── activities.py     # Activity extraction
│   │   │   ├── calculator.py     # Emissions calculator
│   │   │   └── factors.py        # Emission factor lookup
│   │   ├── models/               # Model integrations
│   │   │   ├── __init__.py
│   │   │   ├── yolox.py          # Object detection
│   │   │   ├── deplot.py         # Chart extraction
│   │   │   └── deepseek.py       # LLM integration
│   │   └── utils/                # Utilities
│   │       ├── __init__.py
│   │       └── helpers.py        # Helper functions
│   ├── __init__.py
│   └── config.py                 # Configuration settings
├── tools/                        # Utility scripts
│   ├── drop_collection.py        # Milvus collection management
│   ├── fix_milvus.py             # Milvus troubleshooting
│   └── setup_milvus.py           # Milvus initialization
├── tests/                        # Test suite
│   ├── __init__.py
│   ├── test_document_processor.py
│   ├── test_carbon_accounting.py
│   └── test_vector_store.py
├── requirements.txt              # Project dependencies
├── run_streamlit.py              # Script to run the application
├── PROJECT_STRUCTURE.md          # This file
├── Dockerfile                    # Docker configuration
├── docker-compose.yml            # Docker Compose configuration
└── README.md                     # Project documentation
```

## 🧩 Key Components

### 1. Document Processing (`core/document_processor/`)

- **Purpose**: Extract and process content from PDF documents
- **Key Files**:
  - `extractor.py`: Extracts text, charts, and tables
  - `ocr.py`: Performs OCR on document images
  - `parser.py`: Parses document structure
- **Features**:
  - Text extraction with layout preservation
  - Chart and graph detection and extraction
  - Table structure recognition
  - Multi-page document handling

### 2. Vector Embedding and Storage (`core/embedding/` and `core/vector_store/`)

- **Purpose**: Convert document content to vector embeddings and store in Milvus
- **Key Files**:
  - `embedder.py`: Generates vector embeddings
  - `store.py`: Manages Milvus collections and operations
- **Features**:
  - High-quality vector embeddings
  - Efficient similarity search
  - Document chunking for better retrieval
  - Collection management

### 3. Carbon Accounting (`core/carbon_accounting/`)

- **Purpose**: Extract activities and calculate emissions
- **Key Files**:
  - `activities.py`: Extract emission-relevant activities
  - `calculator.py`: Calculate emissions based on activities
  - `factors.py`: Retrieve appropriate emission factors
- **Features**:
  - Activity extraction from text
  - Emission factor selection via semantic search
  - Scope 1, 2, and 3 emissions calculation
  - Structured emissions reporting

### 4. Model Integrations (`core/models/`)

- **Purpose**: Integrate with various AI models
- **Key Files**:
  - `yolox.py`: Object detection for document elements
  - `deplot.py`: Chart analysis and data extraction
  - `deepseek.py`: LLM for QA and analysis
- **Features**:
  - Consistent API interfaces
  - Error handling and retries
  - Caching for performance
  - Fallback mechanisms

### 5. Frontend (`app/frontend/`)

- **Purpose**: User interface for the application
- **Key Files**:
  - `streamlit_app.py`: Main application entry point
  - `pages/`: Additional UI pages
- **Features**:
  - Document upload and processing
  - Search interface
  - Results visualization
  - Emissions reporting

### 6. Utility Scripts (`tools/`)

- **Purpose**: Maintenance and setup tasks
- **Key Files**:
  - `setup_milvus.py`: Initialize Milvus collections
  - `fix_milvus.py`: Troubleshoot Milvus issues
  - `drop_collection.py`: Manage Milvus collections
- **Features**:
  - Database administration
  - System maintenance
  - Troubleshooting

## 🔄 Data Flow

1. **Document Ingestion Flow**:
   - User uploads document via Streamlit interface
   - Document is processed to extract text, tables, and charts
   - Content is chunked and embedded as vectors
   - Vectors and metadata are stored in Milvus

2. **Search and Retrieval Flow**:
   - User submits natural language query
   - Query is converted to vector embedding
   - Similarity search is performed in Milvus
   - Results are reranked and formatted
   - LLM generates comprehensive answer

3. **Carbon Accounting Flow**:
   - Document is analyzed for emission-relevant activities
   - Activities are matched with appropriate emission factors
   - Emissions are calculated according to GHG Protocol
   - Results are organized into structured report
   - User is presented with visualization and download options

## 🛠️ Design Principles

1. **Modularity**: Components are designed to be interchangeable
2. **Extensibility**: New capabilities can be added without changing existing code
3. **Robustness**: Error handling at all levels with graceful degradation
4. **Performance**: Optimized for handling large documents
5. **User Experience**: Intuitive interface with clear results presentation

## 🔍 Extending the Project

- **Adding New Models**: Create new files in `core/models/`
- **Adding New Extractors**: Extend functionality in `core/document_processor/`
- **Adding New Frontend Pages**: Create new files in `app/frontend/pages/`
- **Adding New Emission Sources**: Update logic in `core/carbon_accounting/`
- **Adding Tests**: Create test files in the `tests/` directory 