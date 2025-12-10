import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score

def train_models():
    print("Loading Processed Data...")
    df = pd.read_csv('processed_data.csv')
    
    # Drop non-feature columns
    # Timestamp is not directly usable unless we convert to numeric, but we have extracted hourly features.
    X = df.drop(columns=['Vehicle_Count', 'Timestamp'])
    y = df['Vehicle_Count']
    
    print(f"Features: {list(X.columns)}")
    
    # Split
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Model 1: Linear Regression (Baseline)
    lr = LinearRegression()
    lr.fit(X_train, y_train)
    y_pred_lr = lr.predict(X_test)
    
    rmse_lr = np.sqrt(mean_squared_error(y_test, y_pred_lr))
    r2_lr = r2_score(y_test, y_pred_lr)
    
    print("\n--- Linear Regression Results ---")
    print(f"RMSE: {rmse_lr:.2f}")
    print(f"R2 : {r2_lr:.2f}")
    
    # Model 2: Random Forest
    rf = RandomForestRegressor(n_estimators=100, random_state=42)
    rf.fit(X_train, y_train)
    y_pred_rf = rf.predict(X_test)
    
    rmse_rf = np.sqrt(mean_squared_error(y_test, y_pred_rf))
    r2_rf = r2_score(y_test, y_pred_rf)
    
    print("\n--- Random Forest Results ---")
    print(f"RMSE: {rmse_rf:.2f}")
    print(f"R2 : {r2_rf:.2f}")
    
    # Feature Importance
    importances = pd.DataFrame({
        'Feature': X.columns,
        'Importance': rf.feature_importances_
    }).sort_values(by='Importance', ascending=False)
    
    print("\n--- Feature Importance (Top 5) ---")
    print(importances.head(5))

if __name__ == "__main__":
    train_models()
