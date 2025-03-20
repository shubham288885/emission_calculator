import json
import os
import numpy as np
import faiss
from sentence_transformers import SentenceTransformer
from typing import List, Dict, Any, Tuple
import glob
import logging
import traceback
import hashlib

from app.core.config import settings
from app.models.emission_factor import EmissionFactor

# Import the Bedrock client
from app.core.bedrock_client import bedrock_client

logger = logging.getLogger(__name__)

class VectorSearchService:
    def __init__(self, model_name: str = None):
        self.model_name = model_name or settings.EMBEDDING_MODEL
        
        # Use AWS Bedrock for embeddings
        if settings.USE_AWS_BEDROCK:
            logger.info(f"Using AWS Bedrock for embeddings with model: {settings.AWS_BEDROCK_MODEL_ID}")
            
            # Check if Bedrock client is initialized
            if hasattr(bedrock_client, 'initialized') and bedrock_client.initialized:
                self.model = bedrock_client
                logger.info("AWS Bedrock client successfully initialized")
            else:
                logger.error("AWS Bedrock client failed to initialize. Search results will be random.")
                # Still set the model to bedrock_client to maintain API compatibility
                self.model = bedrock_client
        else:
            logger.error("AWS_BEDROCK must be set to True for this application. Search results will be random.")
            self.model = bedrock_client
            
        self.data_dir = settings.DATA_DIR
        self.emission_factors = []
        self.index = None
        self.dimension = None
        self.expected_dimension = None
        
    def load_data(self):
        """Load emission factors from JSON files"""
        self.emission_factors = []
        logger.info(f"Loading emission factors from {self.data_dir}")

        # Path to the data files
        ef_files_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "efdb_embeddings", "*.json")
        logger.info(f"Looking for files at: {ef_files_path}")
        ef_files = glob.glob(ef_files_path)
        
        if not ef_files:
            logger.warning(f"No emission factor files found at path: {ef_files_path}")
            return False
            
        logger.info(f"Found {len(ef_files)} files to process")
        valid_items = 0
        invalid_items = 0
            
        for file_path in ef_files:
            try:
                logger.info(f"Processing file: {file_path}")
                with open(file_path, 'r', encoding='utf-8') as f:
                    try:
                        file_data = json.load(f)
                        if not isinstance(file_data, list):
                            logger.warning(f"File {file_path} does not contain a list of emission factors")
                            continue
                            
                        logger.info(f"File {file_path} contains {len(file_data)} emission factors")
                        
                        for item in file_data:
                            try:
                                # Check if item has required fields
                                if 'ef_id' not in item or 'vector' not in item:
                                    logger.warning(f"Item missing required fields: {item.get('ef_id', 'unknown')}")
                                    invalid_items += 1
                                    continue
                                
                                # Check vector dimension
                                if not isinstance(item['vector'], list):
                                    logger.warning(f"Vector is not a list for item: {item.get('ef_id', 'unknown')}")
                                    invalid_items += 1
                                    continue
                                    
                                # If this is the first valid vector, determine expected dimension
                                if self.expected_dimension is None and len(item['vector']) > 0:
                                    self.expected_dimension = len(item['vector'])
                                    logger.info(f"Determined expected vector dimension: {self.expected_dimension}")
                                
                                # Skip items with incorrect vector dimension
                                if len(item['vector']) != self.expected_dimension:
                                    logger.warning(f"Vector dimension mismatch for item {item.get('ef_id', 'unknown')}: expected {self.expected_dimension}, got {len(item['vector'])}")
                                    invalid_items += 1
                                    continue
                                    
                                # Convert to EmissionFactor model and add to list
                                ef = EmissionFactor(**item)
                                self.emission_factors.append(ef)
                                valid_items += 1
                            except Exception as item_e:
                                logger.error(f"Error processing item {item.get('ef_id', 'unknown')}: {str(item_e)}")
                                invalid_items += 1
                    except json.JSONDecodeError as json_e:
                        logger.error(f"JSON decode error in file {file_path}: {str(json_e)}")
            except Exception as e:
                logger.error(f"Error loading file {file_path}: {str(e)}")
                logger.error(traceback.format_exc())
                
        logger.info(f"Loaded {len(self.emission_factors)} emission factors (valid: {valid_items}, invalid: {invalid_items})")
        return len(self.emission_factors) > 0
    
    def build_index(self):
        """Build FAISS index from loaded emission factors"""
        if not self.emission_factors:
            logger.warning("No emission factors loaded, cannot build index")
            return False
            
        # Get vectors from emission factors
        vectors = [ef.vector for ef in self.emission_factors]
        
        if not vectors:
            logger.warning("No vectors found in emission factors")
            return False
            
        try:
            logger.info(f"Building index with vectors of dimension {self.expected_dimension}")
            vectors_np = np.array(vectors, dtype=np.float32)
            
            # Get dimension from the first vector
            self.dimension = vectors_np.shape[1]
            
            # Create FAISS index - using L2 distance
            self.index = faiss.IndexFlatL2(self.dimension)
            self.index.add(vectors_np)
            
            logger.info(f"Successfully built index with {len(vectors)} vectors of dimension {self.dimension}")
            return True
        except Exception as e:
            logger.error(f"Error building index: {str(e)}")
            logger.error(traceback.format_exc())
            return False
    
    def encode_query(self, query_text: str) -> np.ndarray:
        """Encode query text into a vector using AWS Bedrock embeddings"""
        try:
            logger.info(f"ENCODE DEBUG: Encoding query with AWS Bedrock: '{query_text}'")
            
            # Clean the query text for more consistent results
            clean_query = query_text.strip()
            logger.info(f"ENCODE DEBUG: Cleaned query: '{clean_query}'")
            
            # Call AWS Bedrock to generate embeddings
            if not hasattr(self.model, 'generate_embedding'):
                logger.error("AWS Bedrock client doesn't have generate_embedding method")
                raise AttributeError("AWS Bedrock client doesn't have generate_embedding method")
                
            # Log the AWS Bedrock client configuration
            if hasattr(self.model, 'initialized'):
                logger.info(f"ENCODE DEBUG: AWS Bedrock client initialized: {self.model.initialized}")
            
            if hasattr(self.model, 'model_id'):
                logger.info(f"ENCODE DEBUG: AWS Bedrock model ID: {self.model.model_id}")
            
            # Call AWS Bedrock to get embeddings
            logger.info(f"ENCODE DEBUG: Calling AWS Bedrock generate_embedding for query: '{clean_query}'")
            embedding_result = self.model.generate_embedding(clean_query)
            
            # Log the raw embedding result for debugging
            logger.info(f"ENCODE DEBUG: AWS Bedrock embedding result type: {type(embedding_result)}")
            logger.info(f"ENCODE DEBUG: AWS Bedrock embedding result: {embedding_result[:100] if isinstance(embedding_result, list) else embedding_result}")
            
            # Check if embedding result is None (API call failed)
            if embedding_result is None:
                logger.error("AWS Bedrock returned None for embedding result")
                raise ValueError("AWS Bedrock embedding generation failed and returned None")
            
            # Convert to numpy array
            if isinstance(embedding_result, list):
                query_vector = np.array(embedding_result, dtype=np.float32)
            else:
                logger.error(f"Unexpected embedding result type: {type(embedding_result)}")
                raise ValueError(f"Unexpected embedding result type: {type(embedding_result)}")
            
            # Verify the vector is not all zeros
            vector_norm = np.linalg.norm(query_vector)
            non_zero_count = np.count_nonzero(query_vector)
            
            logger.info(f"ENCODE DEBUG: AWS Bedrock vector with dimension: {len(query_vector)}, norm: {vector_norm}")
            logger.info(f"ENCODE DEBUG: Vector has {non_zero_count} non-zero elements out of {len(query_vector)}")
            logger.info(f"ENCODE DEBUG: First 5 values: {query_vector[:5]}")
            
            # If vector is all zeros or very small norm, this is a serious issue
            if vector_norm < 1e-6:
                logger.error(f"ENCODE DEBUG: AWS Bedrock returned a zero or near-zero vector (norm: {vector_norm})")
                logger.error(f"ENCODE DEBUG: Raw embedding result: {embedding_result[:100] if isinstance(embedding_result, list) else embedding_result}")
                raise ValueError("AWS Bedrock returned a zero vector. Check credentials and API access.")
                
            return query_vector
            
        except Exception as e:
            logger.error(f"Error getting embeddings from AWS Bedrock: {str(e)}")
            logger.error(traceback.format_exc())
            
            # IMPORTANT: The user specifically wants AWS Bedrock, so we'll raise the error
            # instead of falling back to a random vector
            logger.error("AWS Bedrock embedding generation failed and no fallback is allowed.")
            raise
    
    def search(self, query_text: str, top_k: int = 5) -> Tuple[List[Dict[str, Any]], List[float]]:
        """Search for similar emission factors based on query text"""
        if not self.index:
            logger.warning("Index not built yet, attempting to load data and build index")
            if not self.load_data() or not self.build_index():
                logger.error("Failed to load data or build index")
                raise ValueError("Vector search index not initialized. Failed to load data or build index.")
                
        # Encode the query
        logger.info(f"SEARCH DEBUG: Starting query encoding for '{query_text}'")
        query_vector = self.encode_query(query_text)
        
        # Print the entire query vector for debugging
        if isinstance(query_vector, np.ndarray):
            logger.info(f"SEARCH DEBUG: Full query vector (numpy): first 10 elements {query_vector.tolist()[:10]}...")
        else:
            logger.info(f"SEARCH DEBUG: Full query vector: first 10 elements {query_vector[:10]}...")
        
        # Check if query vector contains all zeros or has a very small norm
        vector_norm = np.linalg.norm(query_vector)
        logger.info(f"SEARCH DEBUG: Query vector norm: {vector_norm}")
        
        # Check if the vector has any non-zero values
        non_zero_count = np.count_nonzero(query_vector)
        logger.info(f"SEARCH DEBUG: Vector has {non_zero_count} non-zero elements out of {len(query_vector)}")
        
        if vector_norm < 1e-6:  # Essentially zero
            logger.error(f"Query vector for '{query_text}' has norm close to zero ({vector_norm}). Cannot proceed.")
            raise ValueError(f"AWS Bedrock returned a zero vector for query: '{query_text}'")
        
        # Reshape for FAISS
        query_vector_np = np.array([query_vector]).astype('float32')
        
        logger.info(f"SEARCH DEBUG: Executing search with query vector norm: {vector_norm}")
        
        # Search the index
        distances, indices = self.index.search(query_vector_np, min(top_k, len(self.emission_factors)))
        
        logger.info(f"SEARCH DEBUG: Search results - indices: {indices[0]}, distances: {distances[0]}")
        
        # Get results
        results = []
        for idx, distance in zip(indices[0], distances[0]):
            if idx != -1 and idx < len(self.emission_factors):  # Valid index
                ef = self.emission_factors[idx]
                result = ef.dict(exclude={'vector'})
                similarity_score = float(1.0 / (1.0 + distance))
                result['similarity_score'] = similarity_score
                results.append(result)
                logger.info(f"SEARCH DEBUG: Result {idx}: {ef.ef_id} - {ef.description[:30]}... (score: {similarity_score:.4f})")
        
        logger.info(f"SEARCH DEBUG: Search for '{query_text}' returned {len(results)} results")
        
        return results, query_vector.tolist() if isinstance(query_vector, np.ndarray) else query_vector


# Create singleton instance
vector_search_service = VectorSearchService() 