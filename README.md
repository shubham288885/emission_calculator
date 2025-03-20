# Carbon6 Emission Tools

This repository contains two main components for carbon emissions management:

## 1. Emission Calculator

A comprehensive tool for calculating carbon emissions from documents and activities. This tool combines PDF extraction, multimodal analysis, vector search, and emissions calculation capabilities.

### Key Features:
- Document processing and information extraction
- Carbon accounting and emissions calculation
- Semantic search through documents
- Interactive Streamlit interface

### How to Run:
```bash
cd multimodal_pdf_extractor
python run_streamlit.py
```

## 2. Emission Factors API

A FastAPI-based REST API for semantically searching emission factors using vector embeddings with AWS Bedrock.

### Key Features:
- Semantic search for emission factors
- AWS Bedrock integration for high-quality embeddings
- FAISS vector index for efficient similarity search
- FastAPI with automatic documentation

### How to Run:
```bash
cd emission_factors_api
python run.py
```

## System Architecture

The two components are designed to work together in a complete carbon accounting system:

1. **Emission Calculator** extracts and analyzes document content to identify emission-relevant activities
2. **Emission Factors API** provides accurate emission factors based on semantic search
3. Together they enable precise carbon footprint calculations from various documents

## Getting Started

Each tool has its own README.md with detailed setup instructions in their respective directories:
- [Emission Calculator Documentation](multimodal_pdf_extractor/emission_calculator/README.md)
- [Emission Factors API Documentation](emission_factors_api/README.md)

## License

[MIT License](LICENSE)

## Contact

Carbon6 Team  
Email: support@carbon6.ai  
Website: https://carbon6.ai 