# src/data_validator.py
import pandas as pd

class DataValidator:
    def __init__(self, df, column_mappings):
        self.df = df
        self.mappings = column_mappings
    
    def validate_data_suitability(self):
        """Validate if data is suitable for forecasting"""
        print("✅ Validating dataset...")
        
        requirements = {
            'has_date_column': False,
            'has_sales_column': False, 
            'sufficient_records': False,
            'sufficient_date_range': False
        }
        
        # Check date column
        date_col = self.mappings.get('date')
        if date_col and date_col in self.df.columns:
            requirements['has_date_column'] = True
            self.df[date_col] = pd.to_datetime(self.df[date_col], errors='coerce')
            date_range = (self.df[date_col].max() - self.df[date_col].min()).days
            requirements['sufficient_date_range'] = date_range >= 180
        
        # Check sales column  
        sales_col = self.mappings.get('sales')
        if sales_col and sales_col in self.df.columns:
            requirements['has_sales_column'] = True
        
        # Check record count
        requirements['sufficient_records'] = len(self.df) >= 100
        
        # Calculate score
        met_requirements = sum(requirements.values())
        suitability_score = (met_requirements / len(requirements)) * 100
        
        print(f"📊 Suitability Score: {suitability_score:.1f}%")
        for req, met in requirements.items():
            print(f"   {'✅' if met else '❌'} {req}")
        
        return requirements, suitability_score