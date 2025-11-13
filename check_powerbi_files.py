# check_powerbi_files.py
import pandas as pd
import os

def check_powerbi_data():
    print("📊 CHECKING POWER BI FILES")
    print("=" * 40)
    
    if not os.path.exists('powerbi'):
        print("❌ powerbi/ folder doesn't exist")
        return False
    
    csv_files = [f for f in os.listdir('powerbi') if f.endswith('.csv')]
    
    if not csv_files:
        print("❌ No CSV files in powerbi/ folder")
        return False
    
    print(f"✅ Found {len(csv_files)} CSV files:")
    
    for file in csv_files:
        filepath = os.path.join('powerbi', file)
        try:
            df = pd.read_csv(filepath)
            print(f"\n📁 {file}:")
            print(f"   Shape: {df.shape}")
            print(f"   Columns: {list(df.columns)}")
            print(f"   First few rows:")
            print(df.head(3).to_string(index=False))
            print("-" * 30)
        except Exception as e:
            print(f"❌ Error reading {file}: {e}")
    
    return True

if __name__ == "__main__":
    check_powerbi_data()