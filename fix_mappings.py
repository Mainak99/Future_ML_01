# fix_mappings.py
import pandas as pd
import json
import os

def detect_superstore_columns():
    """Auto-detect columns from Superstore dataset"""
    print("🔍 Auto-detecting columns from Superstore file...")
    
    # Find the Superstore file
    possible_files = [
        'superstore_sales.csv', 'Superstore.csv', 'Sample - Superstore.csv',
        'data/superstore_sales.csv', 'data/Superstore.csv'
    ]
    
    df = None
    used_file = None
    
    for file in possible_files:
        if os.path.exists(file):
            try:
                df = pd.read_csv(file)
                used_file = file
                print(f"✅ Loaded: {file} (Shape: {df.shape})")
                break
            except Exception as e:
                print(f"❌ Error loading {file}: {e}")
    
    if df is None:
        print("❌ Could not find Superstore file")
        return None
    
    # Auto-detect columns
    mappings = {}
    
    # Date column
    date_candidates = [col for col in df.columns if 'date' in col.lower() or 'time' in col.lower()]
    if date_candidates:
        mappings['date'] = date_candidates[0]
        print(f"📅 Date column: {date_candidates[0]}")
    
    # Sales column
    sales_candidates = [col for col in df.columns if 'sales' in col.lower() or 'amount' in col.lower() or 'revenue' in col.lower()]
    if sales_candidates:
        mappings['sales'] = sales_candidates[0]
        print(f"💰 Sales column: {sales_candidates[0]}")
    
    # Category column
    category_candidates = [col for col in df.columns if 'category' in col.lower() or 'type' in col.lower() or 'segment' in col.lower()]
    if category_candidates:
        mappings['category'] = category_candidates[0]
        print(f"🏷️ Category column: {category_candidates[0]}")
    
    # Region column
    region_candidates = [col for col in df.columns if 'region' in col.lower() or 'state' in col.lower() or 'city' in col.lower()]
    if region_candidates:
        mappings['region'] = region_candidates[0]
        print(f"🌍 Region column: {region_candidates[0]}")
    
    # Save mappings
    os.makedirs('data', exist_ok=True)
    with open('data/column_mappings.json', 'w') as f:
        json.dump(mappings, f, indent=2)
    
    print(f"✅ Column mappings saved to data/column_mappings.json")
    print(f"📋 Mappings: {mappings}")
    
    return mappings

def manual_column_mapping():
    """Manual column mapping if auto-detection fails"""
    print("\n🎯 Manual Column Mapping")
    
    # Find available CSV files
    csv_files = [f for f in os.listdir('.') if f.endswith('.csv')]
    if csv_files:
        print(f"Available CSV files: {csv_files}")
        
        file_choice = input("Enter filename (or press Enter for superstore_sales.csv): ").strip()
        if not file_choice:
            file_choice = 'superstore_sales.csv'
        
        if os.path.exists(file_choice):
            df = pd.read_csv(file_choice)
            print(f"Columns in {file_choice}: {list(df.columns)}")
            
            mappings = {}
            mappings['date'] = input("Enter DATE column name: ").strip()
            mappings['sales'] = input("Enter SALES column name: ").strip()
            mappings['category'] = input("Enter CATEGORY column name: ").strip()
            mappings['region'] = input("Enter REGION column name: ").strip()
            
            # Save mappings
            os.makedirs('data', exist_ok=True)
            with open('data/column_mappings.json', 'w') as f:
                json.dump(mappings, f, indent=2)
            
            print("✅ Manual mappings saved!")
            return mappings
        else:
            print("❌ File not found")
    else:
        print("❌ No CSV files found in current directory")
    
    return None

if __name__ == "__main__":
    print("🛠 FIXING COLUMN MAPPINGS")
    print("=" * 40)
    
    # Try auto-detection first
    mappings = detect_superstore_columns()
    
    if not mappings or len(mappings) < 2:  # Need at least date and sales
        print("\n⚠️ Auto-detection failed or incomplete")
        mappings = manual_column_mapping()
    
    if mappings:
        print(f"\n🎉 Success! Using mappings: {mappings}")
    else:
        print("\n❌ Failed to create column mappings")