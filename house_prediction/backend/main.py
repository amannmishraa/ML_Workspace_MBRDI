from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

from schemas import HouseInput
from models import predict_price, predict_sale
from database import SessionLocal, engine
from db_models import Prediction, Base

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="House Price Prediction API")

# DB dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# 🔮 Predict + Save to DB
@app.post("/predict")
def predict(input: HouseInput, db: Session = Depends(get_db)):
    data = input.dict()

    price = predict_price(data)
    sold = predict_sale(data, price)

    record = Prediction(
        predicted_price=price,
        sold_within_week=sold,
        condition=data["Condition"],
        location_type=data["Location_Type"]
    )

    db.add(record)
    db.commit()
    db.refresh(record)

    return {
        "id": record.id,
        "predicted_price": round(price, 2),
        "sold_within_week": bool(sold)
    }


# 📜 Fetch prediction history
@app.get("/get")
def get_predictions(db: Session = Depends(get_db)):
    records = db.query(Prediction).order_by(Prediction.created_at.desc()).all()

    return [
        {
            "id": r.id,
            "predicted_price": r.predicted_price,
            "sold_within_week": bool(r.sold_within_week),
            "condition": r.condition,
            "location_type": r.location_type,
            "created_at": r.created_at
        }
        for r in records
    ]
