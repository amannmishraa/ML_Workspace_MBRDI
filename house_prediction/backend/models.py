import joblib
import pandas as pd

price_model = joblib.load("price_model.pkl")
sale_model = joblib.load("sale_model.pkl")

def predict_price(data: dict):
    df = pd.DataFrame([data])
    return price_model.predict(df)[0]

def predict_sale(data: dict, price: float):
    df = pd.DataFrame([data])
    df["Price"] = price
    return int(sale_model.predict(df)[0])
