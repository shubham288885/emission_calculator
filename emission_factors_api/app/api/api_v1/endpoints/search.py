from fastapi import APIRouter, Depends, HTTPException, status
from typing import List, Dict, Any
import logging
import traceback
import numpy as np

from app.models.emission_factor import EmissionFactorQuery, EmissionFactorResponse
from app.core.vector_search import vector_search_service

router = APIRouter()
logger = logging.getLogger(__name__)

@router.post("/search", response_model=EmissionFactorResponse, status_code=status.HTTP_200_OK)
async def search_emission_factors(query: EmissionFactorQuery):
    """
    Search for emission factors semantically similar to the input query.
    
    The API uses vector embeddings to find the most relevant emission factors
    by computing similarity between the query text and the stored emission factors.
    """
    try:
        logger.info(f"API DEBUG: Received search request: {query.query}, top_k={query.top_k}")
        
        # Check if search service is initialized
        if not vector_search_service.index:
            logger.warning("Vector search index not initialized, attempting to initialize now")
            data_loaded = vector_search_service.load_data()
            if not data_loaded:
                logger.error("Failed to load emission factor data")
                raise HTTPException(
                    status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                    detail="Failed to load emission factor data. The service is not ready. Check server logs for more information."
                )
            
            index_built = vector_search_service.build_index()
            if not index_built:
                logger.error("Failed to build search index")
                if vector_search_service.expected_dimension is not None:
                    error_detail = f"Failed to build search index. Vector dimension issues detected: expected dimension {vector_search_service.expected_dimension}. Check server logs for more information."
                else:
                    error_detail = "Failed to build search index. The service is not ready. Check server logs for more information."
                    
                raise HTTPException(
                    status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                    detail=error_detail
                )
                
        # Perform the search
        try:
            logger.info(f"API DEBUG: Starting search for query: '{query.query}'")
            results, query_vector = vector_search_service.search(query.query, query.top_k)
            
            # Check if query_vector is valid
            vector_norm = np.linalg.norm(query_vector) if isinstance(query_vector, np.ndarray) else sum(x*x for x in query_vector)**0.5
            logger.info(f"API DEBUG: Query vector norm: {vector_norm}")
            
            # Ensure query_vector is not all zeros
            if vector_norm < 1e-6:  # Near zero
                logger.error("API DEBUG: AWS Bedrock returned a zero or near-zero vector. Cannot proceed with random vectors.")
                logger.error(f"API DEBUG: Vector norm: {vector_norm}")
                # We don't want to fall back to random vectors, so raise an error
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="AWS Bedrock generated a zero vector. Please check AWS credentials and API access."
                )
                
        except Exception as search_error:
            if isinstance(search_error, HTTPException):
                # Re-raise HTTP exceptions
                raise
                
            logger.error(f"API DEBUG: Error during search operation: {str(search_error)}")
            logger.error(traceback.format_exc())
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error during search operation with AWS Bedrock: {str(search_error)}"
            )
        
        if not results:
            logger.warning(f"API DEBUG: No results found for query: {query.query}")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No results found for your query. Try a different search term or check if the vector index was properly built."
            )
            
        logger.info(f"API DEBUG: Found {len(results)} results for query: {query.query}")
        logger.info(f"API DEBUG: Query vector has {sum(1 for v in query_vector if v != 0)} non-zero elements out of {len(query_vector)}")
        
        return {
            "results": results,
            "query_vector": query_vector
        }
    except HTTPException:
        # Re-raise HTTP exceptions
        raise 