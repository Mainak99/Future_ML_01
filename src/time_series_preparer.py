# src/time_series_preparer.py
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split

class TimeSeriesPreparer:
    def __init__(self, df):
        self.df = df.copy()
        self.time_series_data = None
    
    def create_aggregate_time_series(self, frequency='M'):
        """Create aggregated time series"""
        print("📈 Creating time series data...")
        
        date_col = [col for col in self.df.columns if 'date' in col.lower()][0]
        
        self.time_series_data = self.df.groupby(pd.Grouper(key=date_col, freq=frequency)).agg({
            'Sales': 'sum'
        }).reset_index()
        
        self.time_series_data.columns = ['ds', 'y']
        print(f"✅ Time series created with {len(self.time_series_data)} periods")
        return self.time_series_data
    
    def create_features_for_ml(self):
        """Create features for ML models"""
        print("🔧 Creating ML features...")
        
        # Lag features
        self.time_series_data['lag_1'] = self.time_series_data['y'].shift(1)
        self.time_series_data['lag_3'] = self.time_series_data['y'].shift(3)
        self.time_series_data['lag_6'] = self.time_series_data['y'].shift(6)
        
        # Rolling statistics
        self.time_series_data['rolling_mean_3'] = self.time_series_data['y'].rolling(3).mean()
        self.time_series_data['rolling_std_3'] = self.time_series_data['y'].rolling(3).std()
        
        # Time features
        self.time_series_data['month'] = self.time_series_data['ds'].dt.month
        self.time_series_data['year'] = self.time_series_data['ds'].dt.year
        
        # Remove NaN
        self.time_series_data = self.time_series_data.dropna()
        
        return self.time_series_data
    
    def split_data(self, test_size=0.2):
        """Split data into train and test sets"""
        self.time_series_data = self.time_series_data.sort_values('ds')
        split_idx = int(len(self.time_series_data) * (1 - test_size))
        
        train_data = self.time_series_data.iloc[:split_idx]
        test_data = self.time_series_data.iloc[split_idx:]
        
        print(f"📊 Data split - Train: {len(train_data)}, Test: {len(test_data)}")
        return train_data, test_data