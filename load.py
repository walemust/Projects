import os
import pandas as pd
from sqlalchemy import create_engine, text
from dotenv import load_dotenv
from sqlalchemy.exc import SQLAlchemyError

def load_all_properties(transformed_folder="data/transformed", table_name="properties"):
    
    load_dotenv()

    db_host = os.getenv('host')
    db_name = os.getenv('database_name')
    db_user = os.getenv('username')
    db_port = os.getenv('port')
    db_password = os.getenv('password')

    
    connection_string = f"postgresql+psycopg2://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
    print(f"Connecting to database: {db_name} on {db_host}:{db_port}")

    engine = create_engine(connection_string)

    try:
        
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        print("Database connection successful.\n")

        
        csv_files = [f for f in os.listdir(transformed_folder) if f.endswith(".csv")]

        if not csv_files:
            print("No CSV files found in transformed folder.")
            return

        
        all_dataframes = []
        for file in csv_files:
            filepath = os.path.join(transformed_folder, file)
            print(f"Reading {file}...")
            df = pd.read_csv(filepath)

            if df.empty:
                print(f"Skipping {file} (empty).")
                continue

            all_dataframes.append(df)

        if not all_dataframes:
            print("No valid data found to load.")
            return

        merged_df = pd.concat(all_dataframes, ignore_index=True)
        print(f"Combined total records: {len(merged_df)}")

        
        merged_df.columns = [col.strip().lower().replace(" ", "_") for col in merged_df.columns]

        
        merged_df.drop_duplicates(inplace=True)

        
        print(f"Loading merged dataset into '{table_name}' table...")
        merged_df.to_sql(table_name, engine, if_exists="replace", index=False)
        print(f"Successfully loaded {len(merged_df)} records into '{table_name}' table.\n")

    except SQLAlchemyError as e:
        print(f"Database error: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")
    finally:
        engine.dispose()
        print("Database connection closed.")


load_all_properties()