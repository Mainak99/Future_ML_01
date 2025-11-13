# src/prophet_model.py
from prophet import Prophet
import matplotlib.pyplot as plt
import numpy as np
from sklearn.metrics import mean_absolute_error, mean_squared_error

class ProphetForecaster:
    def __init__(self):
        self.model = None
        self.forecast = None
    
    def build_model(self, train_data):
        """Build and train Prophet model"""
        print("🔮 Building Prophet model...")
        
        prophet_train = train_data[['ds', 'y']].copy()
        
        self.model = Prophet(
            yearly_seasonality=True,
            weekly_seasonality=False,
            daily_seasonality=False,
            changepoint_prior_scale=0.05
        )
        
        self.model.fit(prophet_train)
        print("✅ Prophet model trained!")
        return self.model
    
    def make_forecast(self, train_data, periods=12):
        """Generate forecasts"""
        future = self.model.make_future_dataframe(periods=periods, freq='M')
        self.forecast = self.model.predict(future)
        print(f"✅ Forecast generated for {periods} periods")
        return self.forecast
    
    def evaluate_model(self, test_data):
        """Evaluate model performance"""
        evaluation_data = test_data[['ds', 'y']].merge(
            self.forecast[['ds', 'yhat']], on='ds'
        )
        
        mae = mean_absolute_error(evaluation_data['y'], evaluation_data['yhat'])
        rmse = np.sqrt(mean_squared_error(evaluation_data['y'], evaluation_data['yhat']))
        
        metrics = {'MAE': mae, 'RMSE': rmse}
        print(f"📊 Model Performance - MAE: ${mae:,.2f}, RMSE: ${rmse:,.2f}")
        return metrics
    
    def plot_forecast(self, train_data, test_data):
        """Plot forecast results"""
        plt.figure(figsize=(12, 6))
        
        # Plot historical data
        plt.plot(train_data['ds'], train_data['y'], 'b-', label='Historical', linewidth=2)
        plt.plot(test_data['ds'], test_data['y'], 'g-', label='Actual Test', linewidth=2)
        
        # Plot forecast
        future_forecast = self.forecast[self.forecast['ds'] > train_data['ds'].max()]
        plt.plot(future_forecast['ds'], future_forecast['yhat'], 'r--', label='Forecast', linewidth=2)
        
        plt.title('Sales Forecast with Prophet', fontsize=14, fontweight='bold')
        plt.ylabel('Sales ($)', fontsize=12)
        plt.legend()
        plt.grid(True, alpha=0.3)
        plt.xticks(rotation=45)
        
        plt.tight_layout()
        plt.savefig('reports/prophet_forecast.png', dpi=300, bbox_inches='tight')
        plt.show()