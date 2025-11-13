# src/business_report_generator.py
import matplotlib.pyplot as plt
import pandas as pd
from datetime import datetime

class BusinessReportGenerator:
    def __init__(self, original_df, time_series_data, prophet_forecast, model_metrics, datasets):
        self.original_df = original_df
        self.time_series_data = time_series_data
        self.prophet_forecast = prophet_forecast
        self.model_metrics = model_metrics
        self.datasets = datasets
        
        import os
        os.makedirs('reports', exist_ok=True)
    
    def export_final_report(self):
        """Generate final business report"""
        print("📄 Generating business report...")
        
        # Create summary report
        total_sales = self.original_df['Sales'].sum()
        avg_sales = self.time_series_data['y'].mean()
        
        report = f"""
AI-POWERED SALES FORECASTING DASHBOARD
=======================================
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}

BUSINESS INSIGHTS:
• Total Historical Sales: ${total_sales:,.2f}
• Average Monthly Sales: ${avg_sales:,.2f}
• Forecast Accuracy (MAE): ${self.model_metrics.get('MAE', 0):,.2f}
• Dataset Size: {len(self.original_df):,} records

RECOMMENDATIONS:
1. Use the Power BI dashboard for ongoing sales monitoring
2. Focus inventory planning based on forecasted trends  
3. Allocate marketing budget using seasonal insights
4. Monitor actual vs forecasted sales monthly

NEXT STEPS:
• Build Power BI dashboard using exported datasets
• Retrain model quarterly with new data
• Expand analysis to product-level forecasting
"""
        
        with open('reports/business_report.txt', 'w') as f:
            f.write(report)
        
        # Create visualization
        plt.figure(figsize=(10, 6))
        plt.plot(self.time_series_data['ds'], self.time_series_data['y'], 'b-', label='Historical', linewidth=2)
        
        future_data = self.prophet_forecast[self.prophet_forecast['ds'] > self.time_series_data['ds'].max()]
        plt.plot(future_data['ds'], future_data['yhat'], 'r--', label='Forecast', linewidth=2)
        
        plt.title('Sales Forecast - Business Overview', fontsize=14, fontweight='bold')
        plt.ylabel('Sales ($)', fontsize=12)
        plt.legend()
        plt.grid(True, alpha=0.3)
        plt.xticks(rotation=45)
        plt.tight_layout()
        
        plt.savefig('reports/business_overview.png', dpi=300, bbox_inches='tight')
        plt.show()
        
        print("✅ Business report generated!")
        print("   • reports/business_report.txt")
        print("   • reports/business_overview.png")