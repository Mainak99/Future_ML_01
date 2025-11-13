# check_files.py
import os
import glob

def check_project_structure():
    print("🔍 CHECKING PROJECT STRUCTURE")
    print("=" * 50)
    
    folders = ['data', 'powerbi', 'reports', 'models', 'src']
    for folder in folders:
        if os.path.exists(folder):
            files = os.listdir(folder)
            print(f"📁 {folder}/: {len(files)} files")
            for file in files:
                print(f"   • {file}")
        else:
            print(f"❌ {folder}/: Folder missing!")
        print()

def check_powerbi_files():
    print("📊 POWER BI FILES CHECK:")
    if os.path.exists('powerbi'):
        csv_files = glob.glob('powerbi/*.csv')
        if csv_files:
            for file in csv_files:
                size = os.path.getsize(file) / 1024  # Size in KB
                print(f"✅ {file} ({size:.1f} KB)")
                # Show first few rows
                try:
                    import pandas as pd
                    df = pd.read_csv(file)
                    print(f"   Shape: {df.shape}, Columns: {list(df.columns)}")
                    if len(df) > 0:
                        print(f"   First date: {df.iloc[0][0] if len(df.columns) > 0 else 'N/A'}")
                except Exception as e:
                    print(f"   Error reading: {e}")
        else:
            print("❌ No CSV files in powerbi/ folder")

if __name__ == "__main__":
    check_project_structure()
    check_powerbi_files()