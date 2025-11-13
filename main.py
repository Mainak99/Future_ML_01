# main.py - RUN THIS FILE TO START THE PROJECT
import os
import sys
import pandas as pd
from src.data_loader import DataLoader
from src.data_detector import DataColumnDetector
from src.data_validator import DataValidator
from src.data_cleaner import DataCleaner
from src.feature_engineer import FeatureEngineer
from src.time_series_preparer import TimeSeriesPreparer
from src.prophet_model import ProphetForecaster
from src.xgboost_model import MLForecaster
from src.powerbi_data_exporter import PowerBIDataExporter
from src.business_report_generator import BusinessReportGenerator

def main():
    print("🚀 FUTURE INTERNS - AI SALES FORECASTING DASHBOARD")
    print("=" * 60)
    
    # Ensure directories exist
    for folder in ['data', 'notebooks', 'src', 'models', 'powerbi', 'reports', 'docs']:
        os.makedirs(folder, exist_ok=True)
    
    try:
        # PHASE 1: Data Loading & Understanding
        print("\n" + "="*50)
        print("📊 PHASE 1: DATA LOADING & UNDERSTANDING")
        print("="*50)
        
        loader = DataLoader()
        df = loader.load_local_superstore_data()
        
        detector = DataColumnDetector(df)
        detected_columns, auto_mappings = detector.detect_columns()
        final_mappings = detector.manual_column_mapping() if not auto_mappings.get('date') else auto_mappings
        
        validator = DataValidator(df, final_mappings)
        requirements, score = validator.validate_data_suitability()
        
        if score < 60:
            print("Using sample data due to low suitability score...")
            df = loader.create_sample_data()
        
        # PHASE 2: Data Cleaning
        print("\n" + "="*50)
        print("🧹 PHASE 2: DATA CLEANING & PREPROCESSING")
        print("="*50)
        
        cleaner = DataCleaner(df)
        cleaned_df = (cleaner.clean_dates()
                             .handle_missing_values()
                             .remove_outliers('Sales')
                             .generate_report())
        
        # PHASE 3: Feature Engineering
        print("\n" + "="*50)
        print("🔧 PHASE 3: FEATURE ENGINEERING")
        print("="*50)
        
        engineer = FeatureEngineer(cleaned_df)
        featured_df = (engineer.create_time_features()
                              .create_aggregate_features()
                              .generate_feature_report())
        
        # PHASE 4: Time Series Preparation
        print("\n" + "="*50)
        print("📈 PHASE 4: TIME SERIES PREPARATION")
        print("="*50)
        
        ts_preparer = TimeSeriesPreparer(featured_df)
        time_series_data = ts_preparer.create_aggregate_time_series()
        featured_ts_data = ts_preparer.create_features_for_ml()
        train_data, test_data = ts_preparer.split_data(test_size=0.2)
        
        # PHASE 5: Model Building
        print("\n" + "="*50)
        print("🤖 PHASE 5: MODEL BUILDING & FORECASTING")
        print("="*50)
        
        # Prophet Model
        prophet_forecaster = ProphetForecaster()
        prophet_model = prophet_forecaster.build_model(train_data)
        prophet_forecast = prophet_forecaster.make_forecast(train_data, periods=12)
        prophet_metrics = prophet_forecaster.evaluate_model(test_data)
        prophet_forecaster.plot_forecast(train_data, test_data)
        
        # XGBoost Model
        ml_forecaster = MLForecaster()
        xgb_results = ml_forecaster.build_xgboost_model(train_data, test_data)
        rf_results = ml_forecaster.build_random_forest_model(train_data, test_data)
        ml_forecaster.plot_model_comparison(train_data, test_data, xgb_results, rf_results)
        
        # PHASE 6: Power BI Preparation
        print("\n" + "="*50)
        print("📊 PHASE 6: POWER BI DASHBOARD PREPARATION")
        print("="*50)
        
        powerbi_exporter = PowerBIDataExporter(
            featured_df, featured_ts_data, prophet_forecast, train_data, test_data
        )
        datasets = powerbi_exporter.export_all_datasets()
        
        # PHASE 7: Reporting
        print("\n" + "="*50)
        print("📄 PHASE 7: BUSINESS REPORTING & INSIGHTS")
        print("="*50)
        
        report_generator = BusinessReportGenerator(
            featured_df, featured_ts_data, prophet_forecast, prophet_metrics, datasets
        )
        report_generator.export_final_report()
        
        print("\n🎉 PROJECT COMPLETED SUCCESSFULLY!")
        print("📁 Check the following folders for outputs:")
        print("   • powerbi/ - Datasets for Power BI")
        print("   • reports/ - Business reports and insights")
        print("   • models/ - Saved ML models")
        
        return True
        
    except Exception as e:
        print(f"❌ Error in project execution: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = main()
    if success:
        print("\n✅ All phases completed! You can now:")
        print("   1. Build Power BI dashboard using files in 'powerbi/' folder")
        print("   2. Check 'reports/' folder for business insights")
        print("   3. Upload to GitHub using the provided scripts")
    else:
        print("\n❌ Project execution failed. Please check the errors above.")