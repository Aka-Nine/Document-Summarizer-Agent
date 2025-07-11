from minio import Minio
from config.setting import settings
import traceback

def test_minio_connection():
    print("Testing MinIO connection...")
    print(f"Endpoint: {settings.MINIO_ENDPOINT}")
    print(f"Access Key: {settings.MINIO_ACCESS_KEY}")
    print(f"Secret Key: {settings.MINIO_SECRET_KEY}")
    
    try:
        # Initialize MinIO client
        client = Minio(
            settings.MINIO_ENDPOINT,
            access_key=settings.MINIO_ACCESS_KEY,
            secret_key=settings.MINIO_SECRET_KEY,
            secure=False
        )
        
        # List buckets
        print("\nListing buckets:")
        buckets = client.list_buckets()
        for bucket in buckets:
            print(f"- {bucket.name}")
        
        # Check if our bucket exists
        bucket_name = settings.BUCKET_NAME
        print(f"\nChecking if bucket '{bucket_name}' exists...")
        if client.bucket_exists(bucket_name):
            print(f"Bucket '{bucket_name}' exists")
            
            # List objects in bucket
            print(f"\nListing objects in bucket '{bucket_name}':")
            objects = client.list_objects(bucket_name)
            for obj in objects:
                print(f"- {obj.object_name}")
        else:
            print(f"Bucket '{bucket_name}' does not exist")
            print("Creating bucket...")
            client.make_bucket(bucket_name)
            print(f"Bucket '{bucket_name}' created successfully")
            
    except Exception as e:
        print(f"\nError: {str(e)}")
        print("Full error details:")
        traceback.print_exc()

if __name__ == "__main__":
    test_minio_connection() 