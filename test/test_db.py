from sqlalchemy import create_engine, inspect
from config.setting import settings
import traceback

def test_database_connection():
    print("Testing database connection...")
    print(f"Database URL: {settings.DATABASE_URL}")
    
    try:
        # Create engine
        engine = create_engine(settings.DATABASE_URL)
        
        # Test connection
        with engine.connect() as conn:
            print("\nSuccessfully connected to database")
            
            # Get inspector
            inspector = inspect(engine)
            
            # List all tables
            print("\nListing all tables:")
            tables = inspector.get_table_names()
            for table in tables:
                print(f"- {table}")
                
                # List columns for each table
                print(f"\nColumns in {table}:")
                columns = inspector.get_columns(table)
                for column in columns:
                    print(f"  - {column['name']}: {column['type']}")
            
    except Exception as e:
        print(f"\nError: {str(e)}")
        print("Full error details:")
        traceback.print_exc()

if __name__ == "__main__":
    test_database_connection() 