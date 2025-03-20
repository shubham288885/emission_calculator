import os
from dotenv import load_dotenv
from pydantic_settings import BaseSettings

# Load environment variables from .env file
load_dotenv()

class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "Emission Factors Semantic Search API"
    
    # For compatibility with both SentenceTransformer and AWS Bedrock
    EMBEDDING_MODEL: str = "all-MiniLM-L6-v2"  # Default SentenceTransformer model
    USE_AWS_BEDROCK: bool = True  # Set to True to use AWS Bedrock instead
    
    # AWS Bedrock settings
    AWS_ACCESS_KEY_ID: str = os.getenv("AWS_ACCESS_KEY_ID", "")
    AWS_SECRET_ACCESS_KEY: str = os.getenv("AWS_SECRET_ACCESS_KEY", "")
    AWS_REGION: str = os.getenv("AWS_REGION", "us-east-1")
    EMBEDDING_MODEL_ID: str = os.getenv("EMBEDDING_MODEL_ID", "amazon.titan-embed-text-v1")
    AWS_BEDROCK_MODEL_ID: str = os.getenv("EMBEDDING_MODEL_ID", "amazon.titan-embed-text-v1")
    
    # Data and index settings
    INDEX_NAME: str = "emission_factors"
    DATA_DIR: str = "app/data"
    
    model_config = {
        "env_file": ".env",
        "case_sensitive": True,
        "extra": "ignore"  # Important: allow extra fields from env vars
    }

    def model_post_init(self, __context):
        """Run after initialization to sync EMBEDDING_MODEL_ID with AWS_BEDROCK_MODEL_ID"""
        if hasattr(self, 'EMBEDDING_MODEL_ID'):
            self.AWS_BEDROCK_MODEL_ID = self.EMBEDDING_MODEL_ID

settings = Settings()

# This is no longer needed since we handle it in model_post_init
# if os.getenv("EMBEDDING_MODEL_ID"):
#     settings.AWS_BEDROCK_MODEL_ID = os.getenv("EMBEDDING_MODEL_ID") 