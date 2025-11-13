# src/xgboost_model.py
import xgboost as xgb
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error
import numpy as np
import matplotlib.pyplot as plt

class MLForecaster:
    def __init__(self):
        self.xgb_model = None
        self.rf_model = None
    
    def build_xgboost_model(self, train_data, test_data):
        """Build XGBoost model"""
        print("🌳 Building XGBoost model...")
        
        features = ['lag_1', 'lag_3', 'lag_6', 'rolling_mean_3', 'month']
        X_train = train_data[features]
        y_train = train_data['y']
        X_test = test_data[features]
        y_test = test_data['y']
        
        self.xgb_model = xgb.XGBRegressor(n_estimators=100, random_state=42)
        self.xgb_model.fit(X_train, y_train)
        
        y_pred = self.xgb_model.predict(X_test)
        mae = mean_absolute_error(y_test, y_pred)
        rmse = np.sqrt(mean_squared_error(y_test, y_pred))
        
        print(f"✅ XGBoost - MAE: ${mae:,.2f}, RMSE: ${rmse:,.2f}")
        
        return {
            'test_predictions': y_pred,
            'test_metrics': {'MAE': mae, 'RMSE': rmse}
        }
    
    def build_random_forest_model(self, train_data, test_data):
        """Build Random Forest model"""
        print("🌲 Building Random Forest model...")
        
        features = ['lag_1', 'lag_3', 'lag_6', 'rolling_mean_3', 'month']
        X_train = train_data[features]
        y_train = train_data['y']
        X_test = test_data[features]
        y_test = test_data['y']
        
        self.rf_model = RandomForestRegressor(n_estimators=100, random_state=42)
        self.rf_model.fit(X_train, y_train)
        
        y_pred = self.rf_model.predict(X_test)
        mae = mean_absolute_error(y_test, y_pred)
        rmse = np.sqrt(mean_squared_error(y_test, y_pred))
        
        print(f"✅ Random Forest - MAE: ${mae:,.2f}, RMSE: ${rmse:,.2f}")
        
        return {
            'test_predictions': y_pred,
            'test_metrics': {'MAE': mae, 'RMSE': rmse}
        }
    
    def plot_model_comparison(self, train_data, test_data, xgb_results, rf_results):
        """Compare model performances"""
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 5))
        
        # Test set comparison
        ax1.plot(test_data['ds'], test_data['y'], 'k-', label='Actual', linewidth=2)
        ax1.plot(test_data['ds'], xgb_results['test_predictions'], 'r--', label='XGBoost')
        ax1.plot(test_data['ds'], rf_results['test_predictions'], 'b--', label='Random Forest')
        ax1.set_title('Model Comparison: Test Set', fontweight='bold')
        ax1.legend()
        ax1.grid(True, alpha=0.3)
        
        # Performance comparison
        models = ['XGBoost', 'Random Forest']
        mae_scores = [xgb_results['test_metrics']['MAE'], rf_results['test_metrics']['MAE']]
        
        ax2.bar(models, mae_scores, color=['red', 'blue'], alpha=0.7)
        ax2.set_title('Model Performance (MAE)', fontweight='bold')
        ax2.set_ylabel('MAE ($)')
        
        for i, v in enumerate(mae_scores):
            ax2.text(i, v, f'${v:,.0f}', ha='center', va='bottom', fontweight='bold')
        
        plt.tight_layout()
        plt.savefig('reports/model_comparison.png', dpi=300, bbox_inches='tight')
        plt.show()