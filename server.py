# Python
from flask import Flask, request, jsonify
import pandas as pd
import joblib
import os
import traceback

app = Flask(__name__)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "loan_model.joblib")
CSV_PATH = os.path.join(BASE_DIR, "Loan dataset_classification.csv")  # Path to your CSV

# Load pipeline (preprocessing included)
if os.path.exists(MODEL_PATH):
    model = joblib.load(MODEL_PATH)
else:
    raise RuntimeError(f"Model not found at {MODEL_PATH}")

# exact input columns expected by the pipeline (match the notebook)
INPUT_COLS = ['ApplicantIncome','CoapplicantIncome','LoanAmount','Loan_Amount_Term',
              'Credit_History','Gender','Married','Dependents','Education',
              'Self_Employed','Property_Area']

@app.route("/predict", methods=["POST"])
def predict():
    try:
        data = request.get_json()
        if data is None:
            return jsonify({"error": "Invalid or missing JSON body"}), 400

        records = [data] if isinstance(data, dict) else (data if isinstance(data, list) else None)
        if records is None:
            return jsonify({"error": "JSON must be an object or list of objects"}), 400

        df = pd.DataFrame(records)

        # Ensure all required raw columns exist; supply sensible defaults if missing
        for col in INPUT_COLS:
            if col not in df.columns:
                # numeric defaults 0, categorical default 'missing'
                if col in ['ApplicantIncome','CoapplicantIncome','LoanAmount','Loan_Amount_Term','Credit_History']:
                    df[col] = 0
                else:
                    df[col] = 'missing'

        # Reorder/limit to exactly the columns used for training
        df = df[INPUT_COLS]

        # Cast numeric columns
        for c in ['ApplicantIncome','CoapplicantIncome','LoanAmount','Loan_Amount_Term','Credit_History']:
            df[c] = pd.to_numeric(df[c], errors='coerce').fillna(0)

        # Now pass raw df into the pipeline — pipeline will do impute/encode/scale
        preds = model.predict(df).tolist()
        response = {"predictions": preds}

        if hasattr(model, "predict_proba"):
            response["probabilities"] = model.predict_proba(df).tolist()

        return jsonify(response)
    except Exception as e:
        tb = traceback.format_exc()
        return jsonify({"error": str(e), "trace": tb}), 500

# New GET route to fetch CSV details
@app.route("/data", methods=["GET"])
def get_data():
    try:
        if not os.path.exists(CSV_PATH):
            return jsonify({"error": f"CSV file not found at {CSV_PATH}"}), 404
        
        df = pd.read_csv(CSV_PATH)
        # Optionally, return first N rows to avoid huge JSON
        return jsonify({
            "columns": df.columns.tolist(),
            "num_rows": len(df),
            "preview": df.head(1000).to_dict(orient="records")
        })
    except Exception as e:
        tb = traceback.format_exc()
        return jsonify({"error": str(e), "trace": tb}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
