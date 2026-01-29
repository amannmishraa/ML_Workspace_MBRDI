from fastapi import FastAPI
from schemas import HouseInput
from models import predict_price, predict_sale

app = FastAPI(title="House Price Prediction API")

@app.post("/predict")
def predict(input: HouseInput):
    data = input.dict()
    
    price = predict_price(data)
    sold = predict_sale(data, price)

    return {
        "predicted_price": round(price, 2),
        "sold_within_week": bool(sold)
    }
