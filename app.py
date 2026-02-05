from fastapi import FastAPI
import pickle
import pandas as pd

app = FastAPI()

# Load saved objects
kmeans = pickle.load(open("kmeans_model.pkl", "rb"))
scaler = pickle.load(open("scaler.pkl", "rb"))
label_encoders = pickle.load(open("label_encoders.pkl", "rb"))

cluster_labels = {
    0: "High-Value Loyal Customers",
    1: "Value-Seeking Regular Customers",
    2: "Price-Sensitive Occasional Customers"
}

offers = {
    0: "Exclusive early access + Premium membership",
    1: "Festival discounts (10–15%) + Reward points",
    2: "Flash sales + Coupons + Free shipping"
}

@app.post("/predict")
def predict_cluster(customer: dict):

    df = pd.DataFrame([customer])

    # Encode categorical columns
    for col, encoder in label_encoders.items():
        df[col] = encoder.transform(df[col])

    # Scale
    X_scaled = scaler.transform(df)

    # Predict
    cluster = int(kmeans.predict(X_scaled)[0])

    return {
        "Cluster": cluster,
        "Customer Segment": cluster_labels[cluster],
        "Recommended Offer": offers[cluster]
    }
