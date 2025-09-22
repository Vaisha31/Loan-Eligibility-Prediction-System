import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.ensemble import RandomForestClassifier
import joblib

class LoanPredictor:
    def __init__(self):
        self.model = None
        self.scaler = StandardScaler()
        self.label_encoders = {}
        self.feature_columns = [
            'no_of_dependents', 'education', 'self_employed', 'income_annum',
            'loan_amount', 'loan_term', 'cibil_score', 'residential_assets_value',
            'commercial_assets_value', 'luxury_assets_value', 'bank_asset_value'
        ]

    def train(self, csv_path):

        df = pd.read_csv(csv_path)

        categorical_columns = ['education', 'self_employed']
        for column in categorical_columns:
            self.label_encoders[column] = LabelEncoder()
            df[column] = self.label_encoders[column].fit_transform(df[column])

        X = df[self.feature_columns]
        y = df['loan_status']

        X_scaled = self.scaler.fit_transform(X)

        self.model = RandomForestClassifier(n_estimators=100, random_state=42)
        self.model.fit(X_scaled, y)

    def predict(self, loan_data):
        input_df = pd.DataFrame([loan_data])
        
        for column in self.label_encoders:
            input_df[column] = self.label_encoders[column].transform(input_df[column])

        input_scaled = self.scaler.transform(input_df[self.feature_columns])

        prediction = self.model.predict(input_scaled)[0]
        probability = self.model.predict_proba(input_scaled)[0]

        return {
            'prediction': prediction,
            'confidence': max(probability) * 100,
            'features_importance': dict(zip(
                self.feature_columns,
                self.model.feature_importances_
            ))
        }
    pass

    def save_model(self, path='loan_model.joblib'):
        joblib.dump({
            'model': self.model,
            'scaler': self.scaler,
            'label_encoders': self.label_encoders
        }, path)

    def load_model(self, path='loan_model.joblib'):
        saved_model = joblib.load(path)
        self.model = saved_model['model']
        self.scaler = saved_model['scaler']
        self.label_encoders = saved_model['label_encoders']