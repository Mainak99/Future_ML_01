# src/feature_engineer.py
import pandas as pd
import numpy as np

class FeatureEngineer:
    def __init__(self, df):
        self.df = df.copy()
    
    def create_time_features(self):
        """Create time-based features"""
        print("⏰ Creating time features...")
        
        date_col = [col for col in self.df.columns if 'date' in col.lower()][0]
        
        self.df['year'] = self.df[date_col].dt.year
        self.df['month'] = self.df[date_col].dt.month
        self.df['quarter'] = self.df[date_col].dt.quarter
        self.df['day_of_week'] = self.df[date_col].dt.dayofweek
        self.df['is_weekend'] = (self.df['day_of_week'] >= 5).astype(int)
        self.df['is_holiday_season'] = self.df['month'].isin([11, 12]).astype(int)
        
        return self
    
    def create_aggregate_features(self):
        """Create aggregate features"""
        print("📈 Creating aggregate features...")
        
        # Monthly aggregates
        monthly_agg = self.df.groupby(['year', 'month']).agg({
            'Sales': ['mean', 'std', 'count']
        }).reset_index()
        monthly_agg.columns = ['year', 'month', 'avg_monthly_sales', 'sales_std', 'transaction_count']
        
        self.df = self.df.merge(monthly_agg, on=['year', 'month'], how='left')
        
        return self
    
    def generate_feature_report(self):
        """Generate feature engineering report"""
        print("✅ Feature engineering completed!")
        print(f"📊 Total features: {len(self.df.columns)}")
        return self.df