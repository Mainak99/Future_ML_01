# src/data_cleaner.py
import pandas as pd
import numpy as np

class DataCleaner:
    def __init__(self, df):
        self.df = df.copy()
    
    def clean_dates(self):
        """Clean date columns"""
        print("📅 Cleaning date columns...")
        date_columns = [col for col in self.df.columns if 'date' in col.lower()]
        
        for col in date_columns:
            self.df[col] = pd.to_datetime(self.df[col], errors='coerce')
            invalid_dates = self.df[col].isnull().sum()
            if invalid_dates > 0:
                print(f"   Fixed {invalid_dates} invalid dates in {col}")
        
        return self
    
    def handle_missing_values(self):
        """Handle missing values"""
        print("🔧 Handling missing values...")
        
        for col in self.df.columns:
            if self.df[col].isnull().sum() > 0:
                if self.df[col].dtype in ['float64', 'int64']:
                    self.df[col].fillna(self.df[col].median(), inplace=True)
                else:
                    self.df[col].fillna('Unknown', inplace=True)
        
        return self
    
    def remove_outliers(self, column='Sales'):
        """Remove outliers using IQR method"""
        print(f"📊 Removing outliers from {column}...")
        
        if column in self.df.columns:
            Q1 = self.df[column].quantile(0.25)
            Q3 = self.df[column].quantile(0.75)
            IQR = Q3 - Q1
            lower_bound = Q1 - 1.5 * IQR
            upper_bound = Q3 + 1.5 * IQR
            
            before = len(self.df)
            self.df = self.df[(self.df[column] >= lower_bound) & (self.df[column] <= upper_bound)]
            after = len(self.df)
            
            print(f"   Removed {before - after} outliers")
        
        return self
    
    def generate_report(self):
        """Generate cleaning report"""
        print("✅ Data cleaning completed!")
        print(f"📊 Final dataset shape: {self.df.shape}")
        return self.df