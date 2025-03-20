# Carbon6 Emission Calculator

## 🌍 System Architecture Overview

This system is a comprehensive document processing, retrieval, and carbon accounting solution. It combines document ingestion, vector search, and AI-powered question answering with greenhouse gas emissions calculation capabilities.

### 🧩 Key Components

#### 1. Retrieval Pipeline
- **User Query Processing**: Takes user questions and processes them through the system
- **Vector Embedding**: Converts queries to vector embeddings using advanced embedding models
- **Vector Database**: Stores document embeddings in Milvus for efficient similarity search
- **Reranking**: Refines search results using state-of-the-art reranking models
- **LLM Integration**: Generates comprehensive answers using DeepSeek-R1 model

#### 2. Ingestion Pipeline
- **Document Processing**: Extracts text and visual elements from documents
- **Object Detection**: Identifies charts, tables, and other visual elements using YOLOX
- **Chart Extraction**: Processes charts using DeePlot and CACHED models
- **Table Extraction**: Extracts tabular data using PaddleOCR
- **Post-Processing**: Filters and chunks extracted data for efficient storage
- **Vector Storage**: Embeds and stores document content in Milvus

#### 3. Carbon Accounting
- **Activity Extraction**: Identifies emission-relevant activities from documents
- **Emission Factor Lookup**: Finds appropriate emission factors through semantic search
- **Emissions Calculation**: Calculates Scope 1, 2, and 3 emissions using advanced models
- **Structured Output**: Generates detailed JSON reports with emissions breakdowns
- **Visualization**: Displays emissions results in an interactive UI

## 🚀 Setup Instructions

### Prerequisites
- Python 3.8+
- API keys for various AI models
- Milvus Cloud account
- Access to Carbon6 Emission Factors API

### Environment Setup

1. Clone the repository:
```bash
git clone https://github.com/carbon6/emission-calculator.git
cd emission-calculator
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Configure your `.env` file with your API keys and endpoints:
```
# API Keys for Models
MODEL_YOLOX_KEY=your-key-here
MODEL_DEPLOT_KEY=your-key-here
# ... other API keys

# API Endpoints
MODEL_YOLOX_ENDPOINT=https://api.model-provider.com/v1/yolox
# ... other endpoints

# Milvus Cloud Configuration
MILVUS_URI=your-milvus-uri
MILVUS_TOKEN=your-milvus-token

# Emission Factors API
EMISSION_FACTORS_API_URL=http://localhost:8000/api/v1/emission-factors/search
```

### Setting Up Milvus

Initialize Milvus collections:
```bash
python setup_milvus.py
```

If you encounter issues with Milvus:
```bash
python fix_milvus.py
```

To drop a specific collection:
```bash
python drop_collection.py collection_name
```

### Running the System

Launch the Streamlit App:
```bash
python run_streamlit.py
```

Or directly with streamlit:
```bash
streamlit run emission_calculator/app/frontend/streamlit_app.py
```

## 📋 Features and Usage

### Document Search

1. Upload PDF documents through the Streamlit interface
2. Enter natural language queries about the documents
3. View AI-generated answers based on document content
4. Explore extracted charts, tables, and text in a unified interface

### Carbon Emissions Calculation

1. Upload bills or documents with emission-relevant activities
2. The system automatically extracts activities that could generate emissions
3. View detailed emissions breakdown by source and scope
4. Download results in structured JSON format for reporting

## 🔬 Emissions Calculation Methodology

The system follows these steps to calculate emissions:

1. **Document Analysis**: Extracts text and visual elements from documents
2. **Activity Identification**: Uses AI to identify emission-relevant activities
3. **Emission Factor Selection**: Finds appropriate emission factors via semantic search
4. **Calculation**: Computes emissions following GHG Protocol and IPCC guidelines
5. **Structured Output**: Provides detailed breakdown of emissions by source and process

### Emission Result Format

```json
{
  "activity_description": "Purchase of 20 kg plastic bags (20 km transport)",
  "emission_sources": [
    {
      "source": "production",
      "processes": [
        {
          "name": "polyethylene_production",
          "description": "Crude oil refining, polymerization, and bag manufacturing",
          "parameters": {
            "quantity": "20 kg",
            "emission_factor": "1.5 kg CO2e/kg (IPCC 2023, Plastics Manufacturing)",
            "calculation": "20 kg × 1.5 kg CO2e/kg = 30 kg CO2e",
            "total_emissions": 30.0
          }
        }
      ],
      "total_emissions": 32.3
    }
  ],
  "total_scope_3_emissions": 43.1,
  "assumptions": [
    "Defaulted to landfill disposal (emission factor: 0.1 kg CO2e/kg)."
  ],
  "data_sources": [
    "IPCC 2023: Plastics Production Emission Factors"
  ]
}
```

## 🧰 Troubleshooting

- **API Connection Issues**: Verify your API keys and endpoints in the .env file
- **Milvus Connection Problems**: 
  ```bash
  python fix_milvus.py
  ```
- **Document Processing Errors**: Ensure documents are in supported formats (PDF)
- **PyMuPDF Errors**: The system will try to fix PyMuPDF issues automatically, but you can manually reinstall:
  ```bash
  pip uninstall -y PyMuPDF && pip install pymupdf==1.25.1
  ```

## 🔄 Integration with Emission Factors API

This system integrates with the Carbon6 Emission Factors API for retrieving accurate emission factors. Make sure the Emission Factors API is running and accessible according to your `.env` configuration.

## 📄 License

[MIT License](LICENSE)

## 📞 Contact

Carbon6 Team
Email: support@carbon6.ai
Website: https://carbon6.ai 