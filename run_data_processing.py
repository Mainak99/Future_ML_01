# run_data_processing.py
import pandas as pd
import json
from src.data_loader import DataLoader
from src.data_detector import DataColumnDetector
from src.data_validator import DataValidator
from src.data_cleaner import DataCleaner
from src.feature_engineer import FeatureEngineer

def process_data_only():
    print("🔄 RUNNING DATA PROCESSING PIPELINE")
    print("=" * 50)
    
    # Load data
    loader = DataLoader()
    df = loader.load_local_superstore_data()
    
    # Detect columns
    detector = DataColumnDetector(df)
    detected, mappings = detector.detect_columns()
    
    # Validate
    validator = DataValidator(df, mappings)
    requirements, score = validator.validate_data_suitability()
    
    # Clean data
    cleaner = DataCleaner(df)
    cleaned_df = cleaner.clean_dates().handle_missing_values()
    if mappings.get('sales'):
        cleaned_df = cleaner.remove_outliers(mappings['sales'])
    cleaned_df = cleaner.generate_report()
    
    # Feature engineering
    engineer = FeatureEngineer(cleaned_df)
    featured_df = engineer.create_time_features().create_aggregate_features().generate_feature_report()
    
    # Save processed data
    featured_df.to_csv('data/processed_data.csv', index=False)
    
    # Save mappings
    with open('data/column_mappings.json', 'w') as f:
        json.dump(mappings, f, indent=2)
    
    print("✅ Data processing completed!")
    print(f"📁 Files created:")
    print(f"   • data/column_mappings.json")
    print(f"   • data/processed_data.csv")
    
    return featured_df, mappings

if __name__ == "__main__":
    process_data_only()