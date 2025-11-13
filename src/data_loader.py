# src/data_loader.py
import pandas as pd
import numpy as np
import os

class DataLoader:
    def __init__(self):
        self.data_path = "data/"
        os.makedirs(self.data_path, exist_ok=True)
    
    def load_local_superstore_data(self):
        """Load Superstore dataset from local file"""
        print("🔍 Searching for Superstore dataset...")
        
        possible_paths = [
            "superstore.csv", "Superstore.csv", "Sample - Superstore.csv",
            "data/superstore.csv", "data/Superstore.csv", 
            "superstore_sales.csv", "data/superstore_sales.csv"
        ]
        
        for path in possible_paths:
            if os.path.exists(path):
                try:
                    print(f"📁 Found: {path}")
                    df = pd.read_csv(path, encoding='utf-8')
                    print(f"✅ Loaded successfully! Shape: {df.shape}")
                    return df
                except Exception as e:
                    print(f"❌ Error loading {path}: {e}")
                    continue
        
        print("❌ No Superstore file found. Creating sample data...")
        return self.create_sample_data()
    
    def create_sample_data(self):
        """Create sample data if no file found"""
        print("📊 Creating sample retail data...")
        
        dates = pd.date_range('2018-01-01', '2023-12-31', freq='D')
        categories = ['Furniture', 'Office Supplies', 'Technology']
        regions = ['West', 'East', 'Central', 'South']
        
        data = []
        for date in dates:
            if np.random.random() > 0.3:  # 70% chance of having data each day
                for _ in range(np.random.randint(1, 5)):
                    data.append({
                        'Order Date': date,
                        'Category': np.random.choice(categories),
                        'Region': np.random.choice(regions),
                        'Sales': np.random.normal(500, 150),
                        'Quantity': np.random.randint(1, 5)
                    })
        
        df = pd.DataFrame(data)
        df.to_csv("data/sample_superstore.csv", index=False)
        print(f"✅ Sample data created with {len(df)} records")
        return df