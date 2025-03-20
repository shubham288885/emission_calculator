import requests
import json
import sys

def test_api(query, top_k=5):
    """Test the emission factors search API with a query"""
    url = "http://localhost:8000/api/v1/emission-factors/search"
    
    payload = {
        "query": query,
        "top_k": top_k
    }
    
    headers = {
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.post(url, json=payload, headers=headers)
        
        # Check if successful
        response.raise_for_status()
        
        # Get the results
        results = response.json()
        
        # Print the results
        print(f"\nSearch Query: '{query}'")
        print(f"Found {len(results['results'])} results:")
        print("-" * 60)
        
        for i, result in enumerate(results['results']):
            print(f"Result {i+1}:")
            print(f"  EF ID: {result.get('ef_id')}")
            print(f"  Category: {result.get('ipcc_category_2006')}")
            print(f"  Gas: {result.get('gas')}")
            print(f"  Description: {result.get('description')}")
            print(f"  Value: {result.get('value')} {result.get('unit')}")
            print(f"  Similarity Score: {result.get('similarity_score'):.4f}")
            print("-" * 60)
            
        return True
        
    except requests.exceptions.RequestException as e:
        print(f"Error calling API: {e}")
        return False

if __name__ == "__main__":
    # Default query if none provided
    query = "Carbon dioxide emissions from electricity generation"
    
    # Check if query was provided as command line argument
    if len(sys.argv) > 1:
        query = sys.argv[1]
    
    # Test the API
    test_api(query) 