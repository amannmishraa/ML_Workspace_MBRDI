import streamlit as st
import requests

st.set_page_config(page_title="House Price Predictor", layout="wide")

st.title("🏠 House Price & Quick Sale Prediction")

with st.form("house_form"):
    col1, col2, col3 = st.columns(3)

    Square_Footage = col1.number_input("Square Footage", 500, 10000)
    Bedrooms = col1.number_input("Bedrooms", 1, 10)
    Bathrooms = col1.number_input("Bathrooms", 1.0, 10.0)
    Age = col2.number_input("House Age", 0, 100)
    Garage_Spaces = col2.number_input("Garage Spaces", 0, 5)
    Lot_Size = col2.number_input("Lot Size", 500, 20000)
    Floors = col3.number_input("Floors", 1, 3)
    Neighborhood_Rating = col3.slider("Neighborhood Rating", 1, 10)
    School_Rating = col3.slider("School Rating", 1, 10)

    Condition = st.selectbox("Condition", ["Poor", "Fair", "Good", "Excellent"])
    Location_Type = st.selectbox("Location Type", ["Urban", "Suburban", "Rural"])
    Has_Pool = st.radio("Has Pool", [0, 1])
    Renovated = st.radio("Renovated", [0, 1])
    Distance_To_Center_KM = st.slider("Distance to City Center (KM)", 0.0, 50.0)

    submit = st.form_submit_button("Predict")


if submit:
    payload = {
        "Square_Footage": Square_Footage,
        "Bedrooms": Bedrooms,
        "Bathrooms": Bathrooms,
        "Age": Age,
        "Garage_Spaces": Garage_Spaces,
        "Lot_Size": Lot_Size,
        "Floors": Floors,
        "Neighborhood_Rating": Neighborhood_Rating,
        "Condition": Condition,
        "School_Rating": School_Rating,
        "Has_Pool": Has_Pool,
        "Renovated": Renovated,
        "Location_Type": Location_Type,
        "Distance_To_Center_KM": Distance_To_Center_KM
    }

    res = requests.post(
        "http://localhost:8000/predict",
        json=payload
    ).json()

    # 💰 Price output
    st.success(f"💰 Estimated Price: ${res['predicted_price']:,}")

    # 🧠 Business rule: Poor condition → longer sale time
    if Condition == "Poor":
        st.warning(
            "🐢 Due to poor condition, this house is likely to take longer to sell "
            "regardless of market demand."
        )
    else:
        if res["sold_within_week"]:
            st.info("⚡ Likely to sell within a week")
        else:
            st.info("🐢 May take longer to sell")
