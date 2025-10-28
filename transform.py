import json 
import os
import pandas as pd
def transform_properties(raw_folder="data/raw", transformed_folder="data/transformed"):
    
    os.makedirs(transformed_folder, exist_ok=True)

    
    selected_columns = [
        'id', 'formattedAddress', 'city', 'state', 'stateFips',
        'zipCode', 'county', 'countyFips', 'latitude', 'longitude',
        'propertyType', 'bedrooms', 'bathrooms', 'squareFootage', 'yearBuilt'
    ]

    
    rename_map = {
        'formattedAddress': 'address',
        'stateFips': 'state_fips',
        'zipCode': 'zip_code',
        'countyFips': 'county_fips',
        'propertyType': 'property_type',
        'squareFootage': 'square_footage',
        'yearBuilt': 'year_built'
    }

    
    for filename in os.listdir(raw_folder):
        if not filename.endswith(".json"):
            continue

        filepath = os.path.join(raw_folder, filename)
        print(f"Transforming: {filename}")

        
        with open(filepath, "r") as f:
            data = json.load(f)

        
        if isinstance(data, dict) and "properties" in data:
            data = data["properties"]

        
        df = pd.json_normalize(data)

        
        available_cols = [col for col in selected_columns if col in df.columns]
        df = df[available_cols]

        
        df.rename(columns=rename_map, inplace=True)

        
        df.drop_duplicates(inplace=True)
        df.fillna("", inplace=True)

        # Save transformed CSV
        clean_filename = filename.replace(".json", ".csv").replace(" ", "_")
        save_path = os.path.join(transformed_folder, clean_filename)
        df.to_csv(save_path, index=False)

        print(f"Saved transformed file: {save_path} ({len(df)} records)\n")

    print("All property data transformed successfully!")


transform_properties()