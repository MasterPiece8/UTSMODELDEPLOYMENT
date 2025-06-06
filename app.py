# -*- coding: utf-8 -*-
"""app

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1hTCBwhd0nkD-0YII82CGkHD9vUHAGKKd
"""


import streamlit as st
import joblib

def load_model(filename):
    return joblib.load(filename)

def make_prediction(model, user_input):
    prediction = model.predict([user_input])
    return prediction[0]

def main():
    st.title("Loan Approval Prediction App")

    model = load_model("xgboost_best_model.pkl")

    # Input
    person_age = st.number_input("Age", min_value=18, max_value=100, value=30)
    person_gender = st.selectbox("Gender", ["male", "female"])
    person_education = st.selectbox("Education Level", ["High School", "Bachelor", "Master", "Doctorate"])
    person_income = st.number_input("Income", min_value=0.0, value=50000.0)
    person_emp_exp = st.number_input("Employment Experience (Years)", min_value=0, max_value=50, value=5)
    loan_amnt = st.number_input("Loan Amount", min_value=1000, max_value=1000000, value=10000)
    loan_int_rate = st.number_input("Loan Interest Rate (%)", min_value=0.0, max_value=100.0, value=10.5)
    cb_person_cred_hist_length = st.number_input("Credit History Length (Years)", min_value=0, value=5)
    credit_score = st.number_input("Credit Score", min_value=300, max_value=850, value=700)
    previous_loan_defaults_on_file = st.selectbox("Previous Loan Defaults on File", ["No", "Yes"])
    loan_intent = st.selectbox("Loan Intent", ["EDUCATION", "PERSONAL", "HOMEIMPROVEMENT", "MEDICAL", "VENTURE"])
    home_ownership = st.selectbox("Home Ownership", ["RENT", "OWN", "OTHER"])

    # Feature engineering
    loan_percent_income = loan_amnt / (person_income + 1e-5)
    income_per_year_exp = person_income / (person_emp_exp + 1e-5)
    is_young = 1 if person_age < 25 else 0

    # One-hot encoding input (27 features)
    input_data = [
        person_age,
        person_income,
        person_emp_exp,
        loan_amnt,
        loan_int_rate,
        loan_percent_income,
        cb_person_cred_hist_length,
        credit_score,

        # Gender one-hot
        1 if person_gender == "male" else 0,
        1 if person_gender == "female" else 0,

        # Education one-hot (5 fitur)
        1 if person_education == "Associate" else 0,
        1 if person_education == "Bachelor" else 0,
        1 if person_education == "Doctorate" else 0,
        1 if person_education == "High School" else 0,
        1 if person_education == "Master" else 0,

        # Home ownership one-hot
        1 if home_ownership == "OTHER" else 0,
        1 if home_ownership == "OWN" else 0,
        1 if home_ownership == "RENT" else 0,

        # Loan intent one-hot
        1 if loan_intent == "EDUCATION" else 0,
        1 if loan_intent == "HOMEIMPROVEMENT" else 0,
        1 if loan_intent == "MEDICAL" else 0,
        1 if loan_intent == "PERSONAL" else 0,
        1 if loan_intent == "VENTURE" else 0,

        # Previous loan default
        1 if previous_loan_defaults_on_file == "Yes" else 0,

        # Engineered features
        loan_percent_income,
        income_per_year_exp,
        is_young
    ]


    # Prediksi
    if st.button("Predict"):
        prediction = make_prediction(model, input_data)
        st.success(f"The prediction is: {'Approved' if prediction == 1 else 'Not Approved'}")

if __name__ == "__main__":
    main()



