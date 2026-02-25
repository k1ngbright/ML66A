# -*- coding: utf-8 -*-
import pickle
import streamlit as st
from streamlit_option_menu import option_menu

# Load models
riding_model = pickle.load(open("Riding_model.sav",'rb'))
loan_model = pickle.load(open("loan_model.sav",'rb'))
bmi_model = pickle.load(open("bmi_model.sav",'rb'))

with st.sidebar:
    selected = option_menu(
        'Classification', ['Loan', 'Riding', 'BMI']
    )

# Mapping data
gender_map = {'Male':1, 'Female':0}
education_map = {'Associate': 0, 'Bachelor': 1, 'Doctorate': 2, 'High School': 3, 'Master': 4}
home_map = {'MORTGAGE': 0, 'OTHER': 1, 'OWN': 2, 'RENT': 3}
intent_map = {'DEBTCONSOLIDATION': 0, 'EDUCATION': 1, 'HOMEIMPROVEMENT': 2, 'MEDICAL': 3, 'PERSONAL': 4, 'VENTURE': 5}
default_map = {'No': 0, 'Yes': 1}

# --- 1. BMI Section (3 กล่องข้อความตามคำขอ) ---
if(selected == 'BMI'):
    st.title('BMI Calculation')
    
    name = st.text_input('Gender')
    weight = st.text_input('Height')
    height = st.text_input('Weight')
    
    if st.button('Predict BMI'):
        if weight and height:
            # คำนวณ BMI แบบคณิตศาสตร์ (ไม่ต้องเปลี่ยน Model)
            w = float(weight)
            h = float(height) / 100
            bmi_value = w / (h * h)
            
            # ใช้ model ทำนาย (ถ้า bmi_model ของคุณต้องการค่า bmi_value ไปทำนายต่อ)
            # หรือถ้าจะแสดงผลเลยก็ใช้ if-else ด้านล่างนี้ครับ
            if bmi_value < 18.5:
                res = "น้ำหนักน้อย (Underweight)"
            elif 18.5 <= bmi_value < 25:
                res = "น้ำหนักปกติ (Normal)"
            else:
                res = "น้ำหนักเกิน (Overweight)"
                
            st.success(f"คุณ {name} ค่า BMI คือ {bmi_value:.2f} ผลทำนาย: {res}")
        else:
            st.warning("กรุณากรอกข้อมูลให้ครบ")

# --- 2. Loan Section ---
if(selected == 'Loan'):
    st.title('Loan Classification')
    
    person_age = st.text_input('person_age')
    person_gender = st.selectbox('person_gender', gender_map)
    person_education = st.selectbox('person_education', education_map)
    person_income = st.text_input('person_income') 
    person_emp_exp = st.text_input('person_emp_exp')
    person_home_ownership = st.selectbox('person_home_ownership', home_map)
    loan_amnt = st.text_input('loan_amnt')
    loan_intent = st.selectbox('loan_intent', intent_map)
    loan_int_rate = st.text_input('loan_int_rate')
    loan_percent_income = st.text_input('loan_percent_income')
    cb_person_cred_hist_length = st.text_input('cb_person_cred_hist_length')
    credit_score = st.text_input('credit_score')
    previous_loan_defaults_on_file = st.selectbox('previous_loan_defaults_on_file', default_map)
    
    if st.button('Predict Loan'):
        input_data = [
            float(person_age), gender_map[person_gender], education_map[person_education],
            float(person_income), float(person_emp_exp), home_map[person_home_ownership],
            float(loan_amnt), intent_map[loan_intent], float(loan_int_rate),
            float(loan_percent_income), float(cb_person_cred_hist_length),
            float(credit_score), default_map[previous_loan_defaults_on_file]
        ]
        loan_prediction = loan_model.predict([input_data])
        
        result = 'Accept' if loan_prediction[0] == 1 else 'Not Accept'
        st.success(f'Loan Status: {result}')

# --- 3. Riding Section ---
if(selected == 'Riding'):
    st.title('Riding Mower Classification')
    
    Income = st.text_input('รายได้')
    LotSize = st.text_input('พื้นที่บ้าน')
    
    if st.button('Predict Riding'):
        riding_prediction = riding_model.predict([[float(Income), float(LotSize)]])
        result = 'Owner' if riding_prediction[0] == 1 else 'Non Owner'
        st.success(f'Result: {result}')

