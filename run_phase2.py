# run_phase2.py (MAIN CONTROLLER - Run this first)
import sys
import os

# Add src directory to Python path
sys.path.append('src')

def main():
    print("🚀 STARTING FUTURE INTERNS TASK 1 - PHASE 2")
    print("=" * 60)
    
    try:
        # Step 1: Import and load data
        print("\n📁 STEP 1: Loading Local Superstore Dataset")
        from data_loader import DataLoader
        
        loader = DataLoader()
        df = loader.load_local_superstore_data()
        
        if df is None:
            print("❌ Failed to load dataset. Exiting.")
            return
        
        print(f"✅ Dataset loaded successfully! Shape: {df.shape}")
        
        # Step 2: Detect columns
        print("\n🔍 STEP 2: Detecting Column Types")
        from data_detector import DataColumnDetector
        
        detector = DataColumnDetector(df)
        detected_columns, auto_mappings = detector.detect_columns()
        
        # Use automatic mappings or get manual input
        if auto_mappings.get('date') and auto_mappings.get('sales'):
            final_mappings = auto_mappings
            print("✅ Using automatic column mappings")
        else:
            final_mappings = detector.manual_column_mapping()
        
        # Step 3: Validate dataset
        print("\n✅ STEP 3: Validating Dataset")
        from data_validator import DataValidator
        
        validator = DataValidator(df, final_mappings)
        requirements, score = validator.validate_data_suitability()
        
        if score < 60:
            print("❌ Dataset doesn't meet minimum requirements.")
            use_sample = input("Use sample data instead? (y/n): ").lower().strip()
            if use_sample == 'y':
                df = loader.create_sample_data()
                print("✅ Using sample dataset for the project")
            else:
                print("💡 Please check your dataset and try again.")
                return
        
        # Step 4: Comprehensive analysis
        print("\n📊 STEP 4: Comprehensive Data Analysis")
        
        # Import the analysis function
        analysis_code = """
import pandas as pd
import numpy as np

def comprehensive_data_analysis_local(df, column_mappings):
    print("=" * 70)
    print("📊 COMPREHENSIVE DATA ANALYSIS - LOCAL SUPERSTORE DATASET")
    print("=" * 70)
    
    # Extract mapped columns
    date_col = column_mappings.get('date')
    sales_col = column_mappings.get('sales')
    category_col = column_mappings.get('category')
    region_col = column_mappings.get('region')
    
    # Basic Information
    print("\\\\n1. 📐 DATASET OVERVIEW:")
    print(f"   • Shape: {df.shape}")
    print(f"   • Memory Usage: {df.memory_usage(deep=True).sum() / 1024**2:.2f} MB")
    
    # Convert date column if exists
    if date_col and date_col in df.columns:
        df[date_col] = pd.to_datetime(df[date_col], errors='coerce')
        date_min = df[date_col].min()
        date_max = df[date_col].max()
        print(f"   • Date Range: {date_min} to {date_max}")
    
    print("\\\\n✅ Phase 2 Analysis Completed Successfully!")
    return df

# Run analysis
df_analyzed = comprehensive_data_analysis_local(df, final_mappings)
"""
        
        # Execute the analysis
        exec(analysis_code)
        
        # Save the column mappings for later use
        import json
        os.makedirs('data', exist_ok=True)
        with open('data/column_mappings.json', 'w') as f:
            json.dump(final_mappings, f, indent=2)
        print("💾 Column mappings saved to 'data/column_mappings.json'")
        
        print("\n🎉 PHASE 2 COMPLETED SUCCESSFULLY!")
        print("📁 Next: Proceed to Phase 3 - Data Cleaning & Preprocessing")
        
        return df, final_mappings
        
    except Exception as e:
        print(f"❌ Error during execution: {e}")
        print("💡 Make sure all required files are in the 'src' folder")
        return None, None

if __name__ == "__main__":
    df, mappings = main()
    
    if df is not None:
        print(f"\\\\n✅ Ready to continue! Dataset shape: {df.shape}")
        print(f"🎯 Using column mappings: {mappings}")
        
        # Save the processed dataframe for next phases
        df.to_csv('data/loaded_superstore_data.csv', index=False)
        print("💾 Dataset saved to 'data/loaded_superstore_data.csv'")
    else:
        print("\\\\n❌ Failed to complete Phase 2.")