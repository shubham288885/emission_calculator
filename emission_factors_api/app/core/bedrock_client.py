import json
import boto3
import logging
import numpy as np
import os
import traceback
from typing import List, Optional
from app.core.config import settings

logger = logging.getLogger(__name__)

class BedrockEmbeddingClient:
    """
    Client for generating embeddings using AWS Bedrock.
    """
    def __init__(self):
        """Initialize the Bedrock client using credentials from settings."""
        self.initialized = False
        # Try to get model ID from AWS_BEDROCK_MODEL_ID or fall back to EMBEDDING_MODEL_ID
        self.model_id = settings.AWS_BEDROCK_MODEL_ID or settings.EMBEDDING_MODEL_ID
        
        logger.info(f"Selected Bedrock model ID: {self.model_id}")
        
        # Get AWS credentials directly from environment variables (loaded via python-dotenv)
        aws_access_key = os.getenv("AWS_ACCESS_KEY_ID")
        aws_secret_key = os.getenv("AWS_SECRET_ACCESS_KEY")
        aws_region = os.getenv("AWS_REGION", "us-east-1")
        
        logger.info(f"AWS credentials from env: Access Key ID available: {bool(aws_access_key)}")
        logger.info(f"AWS Region from env: {aws_region}")
            
        try:
            # Initialize AWS session and Bedrock client
            logger.info(f"Initializing AWS Bedrock client with model: {self.model_id}")
            
            self.session = boto3.Session(
                aws_access_key_id=aws_access_key,
                aws_secret_access_key=aws_secret_key,
                region_name=aws_region
            )
            
            self.bedrock_runtime = self.session.client(
                service_name="bedrock-runtime",
                region_name=aws_region
            )
            
            self.initialized = True
            logger.info(f"Successfully initialized AWS Bedrock client with model: {self.model_id}")
            
            # Test connection
            self._test_connection()
            
        except Exception as e:
            logger.error(f"Failed to initialize AWS Bedrock client: {str(e)}")
            logger.error(traceback.format_exc())
            logger.error("Will fall back to SentenceTransformer for embeddings if needed")
    
    def _test_connection(self):
        """Test the connection to AWS Bedrock with a simple embedding request."""
        try:
            # Simple test to see if the connection works
            test_result = self.generate_embedding("test")
            if test_result:
                logger.info(f"AWS Bedrock connection test successful. Vector dimension: {len(test_result)}")
            else:
                logger.warning("AWS Bedrock connection test failed to return embeddings")
        except Exception as e:
            logger.error(f"AWS Bedrock connection test failed: {str(e)}")
    
    def generate_embedding(self, text: str) -> Optional[List[float]]:
        """
        Generate an embedding for the given text using AWS Bedrock.
        
        Args:
            text: The input text to embed
            
        Returns:
            A list of floats representing the embedding vector, or None if embedding failed
        """
        if not self.initialized:
            logger.warning("AWS Bedrock client not initialized. Cannot generate embeddings.")
            return None
            
        try:
            # Log the input text to help with debugging
            logger.info(f"Generating embedding for text: '{text}'")
            
            # Prepare the request body according to Titan model requirements
            if "titan" in self.model_id.lower():
                # For Amazon Titan models
                request_body = json.dumps({
                    "inputText": text
                })
            else:
                # For other models (e.g., Claude)
                request_body = json.dumps({
                    "text": text
                })
            
            # Log the exact request being sent to Bedrock
            logger.info(f"Bedrock request: modelId={self.model_id}")
            logger.debug(f"Request body: {request_body}")
            
            # Call Bedrock API
            try:
                response = self.bedrock_runtime.invoke_model(
                    modelId=self.model_id,
                    contentType="application/json",
                    accept="application/json",
                    body=request_body
                )
                logger.info("Successfully got response from Bedrock API")
            except Exception as api_error:
                logger.error(f"AWS Bedrock API call failed: {str(api_error)}")
                logger.error(traceback.format_exc())
                return None
            
            # Parse the response
            try:
                response_body = json.loads(response.get("body").read())
                logger.info(f"Response keys: {list(response_body.keys())}")
                
                # Extract embedding - handle different model responses
                embedding = None
                
                # Try different possible response formats
                if "embedding" in response_body:
                    embedding = response_body["embedding"]
                elif "embeddings" in response_body:
                    embedding = response_body["embeddings"][0]
                elif "data" in response_body and isinstance(response_body["data"], list):
                    embedding = response_body["data"]
                elif "vector" in response_body:
                    embedding = response_body["vector"]
                
                # Log full response for debugging if embedding not found
                if not embedding:
                    logger.error(f"Bedrock response didn't contain embedding. Full response: {response_body}")
                    return None
                    
                # Log more detailed information about the embedding
                embedding_array = np.array(embedding)
                logger.info(f"Successfully generated embedding: dimension={len(embedding)}, norm={np.linalg.norm(embedding_array)}")
                logger.info(f"First 5 values: {embedding[:5]}")
                
                return embedding
            except Exception as parse_error:
                logger.error(f"Error parsing Bedrock API response: {str(parse_error)}")
                logger.error(f"Raw response: {response}")
                logger.error(traceback.format_exc())
                return None
                
        except Exception as e:
            logger.error(f"Error generating embedding with AWS Bedrock: {str(e)}")
            logger.error(traceback.format_exc())
            return None
    
    def encode(self, texts: List[str]) -> np.ndarray:
        """
        SentenceTransformer-compatible method for generating embeddings.
        This allows the client to be used as a drop-in replacement.
        
        Args:
            texts: A list of input texts to embed
            
        Returns:
            A numpy array of embeddings
        """
        if not self.initialized:
            # Return zero vector if not initialized
            logger.warning("AWS Bedrock client not initialized. Returning zero vectors.")
            if isinstance(texts, str):
                return np.zeros(1536, dtype=np.float32)
            else:
                return np.array([[0.0] * 1536 for _ in range(len(texts))], dtype=np.float32)
                
        if isinstance(texts, str):
            # Single text case
            embedding = self.generate_embedding(texts)
            if embedding:
                return np.array(embedding, dtype=np.float32)
            else:
                # Return a zero vector of the expected dimension (1536 for Titan model)
                logger.warning("Returning zero vector as fallback for failed embedding")
                return np.zeros(1536, dtype=np.float32)
        else:
            # Multiple texts case
            embeddings = []
            for text in texts:
                embedding = self.generate_embedding(text)
                if embedding:
                    embeddings.append(embedding)
                else:
                    # Zero vector as fallback
                    embeddings.append([0.0] * 1536)
            return np.array(embeddings, dtype=np.float32)

# Create singleton instance
bedrock_client = BedrockEmbeddingClient() 