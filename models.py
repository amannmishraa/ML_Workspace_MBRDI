from sqlalchemy import Column, Integer, String
from database import Base

class LoanApplication(Base):
    __tablename__ = "loan_applications"

    id = Column(Integer, primary_key=True, index=True)
    applicant_income = Column(Integer)
    coapplicant_income = Column(Integer)
    total_income = Column(Integer)
    loan_amount = Column(Integer)
    loan_term = Column(Integer)
    credit_history = Column(Integer)
    married = Column(String)
    self_employed = Column(String)
    education = Column(String)
    property_area = Column(String)
    loan_status = Column(String)
