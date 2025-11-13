# src/powerbi_data_exporter.py
import pandas as pd
import os

class PowerBIDataExporter:
    def __init__(self, original_df, time_series_data, prophet_forecast, train_data, test_data):
        self.original_df = original_df
        self.time_series_data = time_series_data
        self.prophet_forecast = prophet_forecast
        self.train_data = train_data
        self.test_data = test_data
        
        os.makedirs('powerbi', exist_ok=True)
    
    def export_all_datasets(self):
        """Export all datasets for Power BI"""
        print("📊 Preparing Power BI datasets...")
        
        # Main forecast data
        historical = self.time_series_data[['ds', 'y']].copy()
        historical['Type'] = 'Actual'
        
        future = self.prophet_forecast[self.prophet_forecast['ds'] > historical['ds'].max()][['ds', 'yhat']].copy()
        future = future.rename(columns={'yhat': 'y'})
        future['Type'] = 'Forecast'
        
        combined_data = pd.concat([historical, future])
        combined_data.to_csv('powerbi/forecast_data.csv', index=False)
        
        # Category data
        date_col = [col for col in self.original_df.columns if 'date' in col.lower()][0]
        category_data = self.original_df.groupby([pd.Grouper(key=date_col, freq='M'), 'Category'])['Sales'].sum().reset_index()
        category_data.to_csv('powerbi/category_data.csv', index=False)
        
        print("✅ Power BI datasets exported!")
        print("   • powerbi/forecast_data.csv")
        print("   • powerbi/category_data.csv")
        
        return {
            'forecast_data': combined_data,
            'category_data': category_data
        }