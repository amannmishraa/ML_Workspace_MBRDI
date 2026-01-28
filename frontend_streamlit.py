import streamlit as st
import requests

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Loan Approval System",
    page_icon="🏦",
    layout="wide"
)

# ---------------- BACKEND API URL ----------------
API_URL = "http://127.0.0.1:8000/submit-loan"

# ---------------- TITLE ----------------
st.title("🏦 Loan Approval System")
st.markdown(
    "Fill in the applicant details below to check **loan eligibility**."
)
st.divider()

# ---------------- INPUT SECTION ----------------
st.header("📄 Applicant Details")

col1, col2, col3 = st.columns(3)

with col1:
    applicant_income = st.number_input("Applicant Income (₹)", min_value=0, step=1000)
    married = st.selectbox("Marital Status", ["Yes", "No"])
    education = st.selectbox("Education", ["Graduate", "Not Graduate"])

with col2:
    coapplicant_income = st.number_input("Co-applicant Income (₹)", min_value=0, step=1000)
    self_employed = st.selectbox("Self Employed", ["Yes", "No"])
    property_area = st.selectbox("Property Area", ["Urban", "Semiurban", "Rural"])

with col3:
    loan_amount = st.number_input("Loan Amount (in thousands ₹)", min_value=0, step=10)
    loan_amount_term = st.number_input("Loan Term (months)", min_value=0, step=12)
    credit_history = st.selectbox(
        "Credit History",
        [1, 0],
        format_func=lambda x: "Good (1)" if x == 1 else "Bad (0)"
    )

# ---------------- SUBMIT BUTTON ----------------
if st.button("🔍 Check Loan Status"):

    total_income = applicant_income + coapplicant_income

    # ---------------- SUMMARY DATA ----------------
    summary_data = {
        "Applicant Income": f"₹{applicant_income:,.0f}",
        "Co-applicant Income": f"₹{coapplicant_income:,.0f}",
        "Total Income": f"₹{total_income:,.0f}",
        "Loan Amount": f"₹{loan_amount * 1000:,.0f}",
        "Loan Term": f"{int(loan_amount_term)} months",
        "Credit History": "Good" if credit_history == 1 else "Bad",
        "Married": married,
        "Self Employed": self_employed,
        "Education": education,
        "Property Area": property_area
    }

    st.divider()
    st.header("📊 Application Summary")

    col4, col5 = st.columns(2)

    with col4:
        for key, value in summary_data.items():
            st.write(f"**{key}:** {value}")

    with col5:
        st.metric("Total Income", f"₹{total_income:,.0f}")
        st.metric("Loan Amount", f"₹{loan_amount * 1000:,.0f}")

    st.divider()

    # ---------------- SEND DATA TO BACKEND API ----------------
    payload = {
        "applicant_income": applicant_income,
        "coapplicant_income": coapplicant_income,
        "total_income": total_income,
        "loan_amount": loan_amount * 1000,
        "loan_term": loan_amount_term,
        "credit_history": credit_history,
        "married": married,
        "self_employed": self_employed,
        "education": education,
        "property_area": property_area
    }

    try:
        response = requests.post(API_URL, json=payload)

        if response.status_code == 200:
            result = response.json()

            st.header("✅ Loan Decision")

            if result["loan_status"] == "Approved":
                st.success("🎉 **Loan Approved!**")
                st.markdown(
                    """
                    ✔ Good credit history  
                    ✔ Income details verified  
                    ✔ Data saved to database  
                    """
                )
            else:
                st.error("❌ **Loan Rejected**")
                st.markdown(
                    """
                    ❌ Poor credit history  
                    ❌ Data saved to database  
                    """
                )
        else:
            st.error("⚠️ Failed to connect to backend")

    except Exception as e:
        st.error(f"🚨 Backend not running: {e}")

# ---------------- FOOTER ----------------
st.divider()
st.caption("💼 Loan Approval System | Streamlit + FastAPI + SQL")
