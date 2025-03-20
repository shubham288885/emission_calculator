# Carbon6 Emission Factors Semantic Search API

A high-performance FastAPI-based REST API for semantically searching emission factors using vector embeddings with AWS Bedrock and FAISS.

## 🚀 Features

- **Advanced Semantic Search**: Search emission factors by semantic meaning rather than just keywords
- **AWS Bedrock Integration**: Uses Amazon Titan embedding model for high-quality vector embeddings
- **FAISS Vector Index**: Efficient similarity search using Facebook AI's FAISS library
- **Modern FastAPI Framework**: High-performance API with automatic documentation
- **Comprehensive Error Handling**: Clear error messages and graceful fallbacks
- **Extensive Test Suite**: Utilities to test model connection and API functionality
- **Docker Support**: Containerized deployment for consistent runtime environments

## 📋 Prerequisites

- Python 3.8+
- AWS Account with Bedrock access
- AWS Credentials with Bedrock permissions

## 🔧 Installation

1. Clone the repository:
```bash
git clone https://github.com/carbon6/emission-factors-api.git
cd emission-factors-api
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Create a `.env` file with your AWS Bedrock credentials:
```
# AWS Bedrock Credentials
AWS_ACCESS_KEY_ID=your_access_key
AWS_SECRET_ACCESS_KEY=your_secret_key
AWS_REGION=us-east-1

# Model ID - Use the correct model ID for your Bedrock account
# Common choices:
# - amazon.titan-embed-text-v1
# - anthropic.claude-3-haiku-20240307-v1:0
EMBEDDING_MODEL_ID=amazon.titan-embed-text-v1

# API Configuration
API_V1_STR=/api/v1
PROJECT_NAME=Emission Factors Semantic Search API
```

## 🌐 AWS Bedrock Setup

1. **Enable AWS Bedrock Service**:
   - Go to AWS console and navigate to Amazon Bedrock
   - Request access to the models you want to use (e.g., Titan Embeddings)
   - Verify model access in the AWS console

2. **Create AWS IAM User with Bedrock Access**:
   - Create an IAM user with programmatic access
   - Attach the `AmazonBedrockFullAccess` policy
   - Note the access key and secret key for your `.env` file

3. **Test AWS Bedrock Access**:
   ```bash
   python test_bedrock.py
   ```
   
   You can also list available models:
   ```bash
   python test_bedrock.py --list-models
   ```

## 🏃‍♂️ Usage

1. Start the API server:
   ```bash
   python run.py
   ```

2. Access the API documentation:
   - Swagger UI: http://localhost:8000/docs
   - ReDoc: http://localhost:8000/redoc

3. Test the API with sample queries:
   ```bash
   python test_api.py "Carbon dioxide from electricity"
   ```

## 🔍 API Endpoints

### POST /api/v1/emission-factors/search

Search for emission factors semantically similar to the input query.

**Request Body:**
```json
{
  "query": "Carbon dioxide emissions from electricity generation",
  "top_k": 5
}
```

**Response:**
```json
{
  "results": [
    {
      "ef_id": "EF123456",
      "ipcc_category_2006": "Energy",
      "gas": "CO2",
      "description": "Carbon dioxide emissions from electricity generation",
      "value": 0.5,
      "unit": "kg CO2/kWh",
      "similarity_score": 0.95
    },
    ...
  ],
  "query_vector": [...] // The embedding vector of your query
}
```

## 🧠 How It Works

1. The API loads emission factors with pre-computed vector embeddings from JSON files.
2. It builds a FAISS index for efficient similarity search.
3. When a search query is received, the API:
   - Encodes the query text into a vector using AWS Bedrock's Titan embedding model
   - Performs a similarity search against the FAISS index
   - Returns the most semantically similar emission factors

## 🐳 Docker Deployment

```bash
# Build the Docker image
docker build -t emission-factors-api .

# Run the container
docker run -p 8000:8000 --env-file .env emission-factors-api
```

## 🔧 Troubleshooting

If you encounter issues with AWS Bedrock:

1. **Check AWS Credentials**: Verify your AWS credentials are correct and have Bedrock access
   ```bash
   python test_bedrock.py
   ```

2. **Check Model Availability**: Make sure the model specified in your `.env` file is available
   ```bash
   python test_bedrock.py --list-models
   ```

3. **Check Region**: Ensure Bedrock is available in your specified AWS region

4. **Try Different Model**: Test with a different embedding model
   ```bash
   python test_bedrock.py --model anthropic.claude-3-haiku-20240307-v1:0
   ```

5. **Fallback to SentenceTransformers**: If AWS Bedrock isn't working, edit `app/core/config.py` to set `USE_AWS_BEDROCK = False`

## 🛠️ Development

### Running Tests
```bash
pytest tests/
```

### Code Formatting
```bash
black app/
isort app/
```

## 📄 License

[MIT License](LICENSE)

## 📞 Contact

Carbon6 Team
Email: support@carbon6.ai
Website: https://carbon6.ai 