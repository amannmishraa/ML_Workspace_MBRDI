from fastapi import FastAPI
from database import engine, SessionLocal
from models import Base, LoanApplication

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Loan Approval Backend")

# ---------------- CREATE LOAN (POST) ----------------
@app.post("/submit-loan")
def submit_loan(data: dict):
    db = SessionLocal()

    loan_status = "Approved" if data["credit_history"] == 1 else "Rejected"

    loan = LoanApplication(
        applicant_income=data["applicant_income"],
        coapplicant_income=data["coapplicant_income"],
        total_income=data["total_income"],
        loan_amount=data["loan_amount"],
        loan_term=data["loan_term"],
        credit_history=data["credit_history"],
        married=data["married"],
        self_employed=data["self_employed"],
        education=data["education"],
        property_area=data["property_area"],
        loan_status=loan_status
    )

    db.add(loan)
    db.commit()
    db.refresh(loan)
    db.close()

    return {
        "message": "Loan stored successfully",
        "loan_status": loan_status
    }

# ---------------- READ ALL LOANS (GET) ----------------
@app.get("/loans")
def get_all_loans():
    db = SessionLocal()
    loans = db.query(LoanApplication).all()
    db.close()

    return [
        {
            "id": loan.id,
            "applicant_income": loan.applicant_income,
            "coapplicant_income": loan.coapplicant_income,
            "total_income": loan.total_income,
            "loan_amount": loan.loan_amount,
            "loan_term": loan.loan_term,
            "credit_history": loan.credit_history,
            "married": loan.married,
            "self_employed": loan.self_employed,
            "education": loan.education,
            "property_area": loan.property_area,
            "loan_status": loan.loan_status
        }
        for loan in loans
    ]

# ---------------- READ SINGLE LOAN (GET) ----------------
@app.get("/loans/{loan_id}")
def get_loan_by_id(loan_id: int):
    db = SessionLocal()
    loan = db.query(LoanApplication).filter(LoanApplication.id == loan_id).first()
    db.close()

    if not loan:
        return {"error": "Loan not found"}

    return {
        "id": loan.id,
        "applicant_income": loan.applicant_income,
        "coapplicant_income": loan.coapplicant_income,
        "total_income": loan.total_income,
        "loan_amount": loan.loan_amount,
        "loan_term": loan.loan_term,
        "credit_history": loan.credit_history,
        "married": loan.married,
        "self_employed": loan.self_employed,
        "education": loan.education,
        "property_area": loan.property_area,
        "loan_status": loan.loan_status
    }
