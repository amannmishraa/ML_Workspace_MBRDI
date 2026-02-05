import streamlit as st
import requests

st.set_page_config(page_title="Customer Clustering Prediction", layout="centered")

st.title("Customer Clustering Prediction")

# Input fields
age = st.number_input("Age", min_value=0, max_value=120, value=30)
gender = st.selectbox("Gender", ["M", "F"])
city = st.text_input("City", "Bangalore")
annual_income = st.number_input("Annual Income", min_value=0, value=500000)
total_spent = st.number_input("Total Amount Spent", min_value=0, value=50000)
monthly_purchases = st.number_input("Number of Purchases per Month", min_value=0, value=5)
avg_order_value = st.number_input("Average Order Value", min_value=0, value=2000)
app_time = st.number_input("Time Spent on App (minutes per day)", min_value=0, value=60)
discount_usage = st.selectbox("Discount Usage Frequency", ["Low", "Medium", "High"])
shopping_time = st.selectbox("Preferred Shopping Time", ["Day", "Night"])

# Button to predict
if st.button("Predict Cluster"):

    # Create customer dict
    customer = {
        "Age": age,
        "Gender": gender,
        "City": city,
        "AnnualIncome": annual_income,
        "TotalSpent": total_spent,
        "MonthlyPurchases": monthly_purchases,
        "AvgOrderValue": avg_order_value,
        "AppTimeMinutes": app_time,
        "DiscountUsage": discount_usage,
        "PreferredShoppingTime": shopping_time
    }

    # Call FastAPI endpoint
    try:
        response = requests.post("http://127.0.0.1:8000/predict", json=customer)
        data = response.json()

        st.success("Prediction Complete!")
        st.write(f"**Cluster:** {data['Cluster']}")
        st.write(f"**Customer Segment:** {data['Customer Segment']}")
        st.write(f"**Recommended Offer:** {data['Recommended Offer']}")

    except Exception as e:
        st.error(f"Error calling API: {e}")
