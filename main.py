from extract import extract_properties
from transform import transform_properties
from load import load_all_properties


def run_pipeline():
    print("Starting Property Data ETL Pipeline...\n")
    extract_properties()
    transform_properties()
    load_all_properties()
    print("ETL Pipeline completed successfully!")


if __name__ == "__main__":
    run_pipeline()