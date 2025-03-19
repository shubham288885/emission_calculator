from pymilvus import (
    connections,
    utility,
    FieldSchema,
    CollectionSchema,
    DataType,
    Collection,
)

def reset_milvus():
    print("=== Starting Direct Milvus Reset Process ===")
    
    # Hardcoded Milvus credentials from the .env file
    milvus_uri = "https://in03-81207deaf340e29.serverless.gcp-us-west1.cloud.zilliz.com"
    milvus_token = "38aa2f9559a761f826222cb1ba312486fe2a37dc0435e653e8456c7871fe87ef2b9716383a36f799e835d8f26ecb0eac16b6f1d9"
    
    print(f"Connecting to Milvus at: {milvus_uri}")
    
    try:
        # Connect to Milvus Cloud
        connections.connect(
            alias="default",
            uri=milvus_uri,
            token=milvus_token
        )
        print("Connected to Milvus successfully")
        
        collection_name = "vector_db"
        
        # Check if collection exists and drop it
        if utility.has_collection(collection_name):
            print(f"Collection {collection_name} exists - dropping it")
            utility.drop_collection(collection_name)
            print(f"Collection {collection_name} dropped successfully")
        else:
            print(f"Collection {collection_name} does not exist")
        
        # Define fields with correct schema
        fields = [
            FieldSchema(name="id", dtype=DataType.INT64, is_primary=True, auto_id=True),
            FieldSchema(name="doc_id", dtype=DataType.VARCHAR, max_length=256),
            FieldSchema(name="text", dtype=DataType.VARCHAR, max_length=65535),
            FieldSchema(name="embedding", dtype=DataType.FLOAT_VECTOR, dim=1024),
            FieldSchema(name="metadata", dtype=DataType.JSON)
        ]
        
        # Create schema
        schema = CollectionSchema(fields, description="Vector DB for document embeddings")
        
        # Create collection
        collection = Collection(collection_name, schema)
        print(f"Created collection {collection_name} with new schema")
        
        # Create index
        index_params = {
            "metric_type": "L2",
            "index_type": "IVF_FLAT",
            "params": {"nlist": 1024}
        }
        
        collection.create_index("embedding", index_params)
        print(f"Created index on 'embedding' field")
        
        # Load collection
        collection.load()
        
        # Run a simple query to test
        search_params = {"metric_type": "L2", "params": {"nprobe": 10}}
        dummy_vector = [0.0] * 1024
        results = collection.search(
            data=[dummy_vector],
            anns_field="embedding",
            param=search_params,
            limit=1,
            output_fields=["text"]
        )
        print("Test search completed successfully")
        
        print("=== Milvus setup completed successfully ===")
        return True
        
    except Exception as e:
        print(f"Error during Milvus reset: {e}")
        return False

if __name__ == "__main__":
    reset_milvus() 