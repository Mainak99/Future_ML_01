# src/data_detector.py
class DataColumnDetector:
    def __init__(self, df):
        self.df = df
        self.column_mapping = {}
    
    def detect_columns(self):
        """Automatically detect column types"""
        print("🔍 Detecting column types...")
        
        detected_columns = {'date_columns': [], 'sales_columns': [], 'category_columns': [], 'region_columns': []}
        
        for col in self.df.columns:
            col_lower = col.lower()
            
            if any(x in col_lower for x in ['date', 'time', 'year', 'month']):
                detected_columns['date_columns'].append(col)
                print(f"📅 Date column: {col}")
            elif any(x in col_lower for x in ['sales', 'amount', 'revenue']):
                detected_columns['sales_columns'].append(col)
                print(f"💰 Sales column: {col}")
            elif any(x in col_lower for x in ['category', 'type', 'segment']):
                detected_columns['category_columns'].append(col)
                print(f"🏷️ Category column: {col}")
            elif any(x in col_lower for x in ['region', 'state', 'city', 'area']):
                detected_columns['region_columns'].append(col)
                print(f"🌍 Region column: {col}")
        
        # Set default mappings
        self.column_mapping['date'] = detected_columns['date_columns'][0] if detected_columns['date_columns'] else None
        self.column_mapping['sales'] = detected_columns['sales_columns'][0] if detected_columns['sales_columns'] else None
        self.column_mapping['category'] = detected_columns['category_columns'][0] if detected_columns['category_columns'] else None
        self.column_mapping['region'] = detected_columns['region_columns'][0] if detected_columns['region_columns'] else None
        
        return detected_columns, self.column_mapping
    
    def manual_column_mapping(self):
        """Manual column mapping if auto-detection fails"""
        print("\n🎯 Manual Column Mapping Required")
        print(f"Available columns: {list(self.df.columns)}")
        
        if not self.column_mapping.get('date'):
            date_col = input("Enter DATE column name: ").strip()
            if date_col in self.df.columns:
                self.column_mapping['date'] = date_col
        
        if not self.column_mapping.get('sales'):
            sales_col = input("Enter SALES column name: ").strip()
            if sales_col in self.df.columns:
                self.column_mapping['sales'] = sales_col
        
        print(f"✅ Final mappings: {self.column_mapping}")
        return self.column_mapping