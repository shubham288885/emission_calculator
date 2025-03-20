from pymilvus import connections, utility
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

print("=== Starting Milvus collection cleanup ===")

# Connect to Milvus Cloud
try:
    connections.connect(
        alias="default",
        uri=os.getenv('MILVUS_URI'),
        token=os.getenv('MILVUS_TOKEN')
    )
    print("Connected to Milvus successfully")
    
    # Check if collection exists
    collection_name = "vector_db"
    exists = utility.has_collection(collection_name)
    print(f"Collection {collection_name} exists: {exists}")
    
    # Force drop the collection if it exists
    if exists:
        utility.drop_collection(collection_name)
        print(f"Collection {collection_name} dropped successfully")
    
    print("Cleanup completed. Now you can run the setup_milvus.py script")
    
except Exception as e:
    print(f"Error during Milvus cleanup: {e}") 