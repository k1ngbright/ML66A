# -*- coding: utf-8 -*-
import pickle
import streamlit as st
from streamlit_option_menu import option_menu

# 1. Load models (ย้ายมาไว้ด้านบนสุดเพื่อให้เรียกใช้ได้ทุกส่วน)
riding_model = pickle.load(open("Riding_model.sav",'rb'))
loan_model = pickle.load(open("loan_model.sav",'rb'))
bmi_model = pickle.load(open("bmi_model.sav",'rb'))

# 2. Sidebar Menu (สร้างตัวแปร selected ก่อนเริ่มเงื่อนไข if)
with st.sidebar:
    selected = option_menu(
        'Classification', ['Loan', 'Riding', 'BMI'],
        icons=['cash-stack', 'bicycle', 'person-bounding-box'],
        default_index=0
    )

# 3. Mapping data สำหรับ Loan (ประกาศไว้ส่วนกลาง)
gender_map = {'Male': 1, 'Female': 0}
education_map = {'Associate': 0, 'Bachelor': 1, 'Doctorate': 2, 'High School': 3, 'Master': 4}
home_map = {'MORTGAGE': 0, 'OTHER': 1, 'OWN': 2, 'RENT': 3}
intent_map = {'DEBTCONSOLIDATION': 0, 'EDUCATION': 1, 'HOMEIMPROVEMENT': 2, 'MEDICAL': 3, 'PERSONAL': 4, 'VENTURE': 5}
default_map = {'No': 0, 'Yes': 1}

# --- ส่วนที่ 1: BMI (3 กล่องข้อความ และคำนวณค่า) ---
if selected == 'BMI':
    st.title('BMI Calculation & Prediction')
    
    # รับค่า 3 กล่องตามที่ต้องการ
    name = st.text_input('ชื่อ-นามสกุล')
    weight = st.text_input('น้ำหนัก (กิโลกรัม)')
    height = st.text_input('ส่วนสูง (เซนติเมตร)')
    
    if st.button('Predict BMI'):
        if name and weight and height:
            try:
                w_val = float(weight)
                h_val = float(height) / 100 # แปลงเป็นเมตร
                bmi_calc = w_val / (h_val ** 2)
                
                # แสดงผลการคำนวณเบื้องต้น
                st.write(f"คุณ {name} มีค่า BMI คือ: **{bmi_calc:.2f}**")
                
                # แปลผลเกณฑ์ BMI มาตรฐาน
                if bmi_calc < 18.5:
                    st.warning("เกณฑ์: น้ำหนักน้อยกว่ามาตรฐาน")
                elif 18.5 <= bmi_calc < 23:
                    st.success("เกณฑ์: น้ำหนักปกติ")
                elif 23 <= bmi_calc < 25:
                    st.info("เกณฑ์: น้ำหนักเกิน (เริ่มอ้วน)")
                else:
                    st.error("เกณฑ์: อ้วน")
            except ValueError:
                st.error("กรุณากรอกเฉพาะตัวเลขในช่องน้ำหนักและส่วนสูง")
        else:
            st.warning("กรุณากรอกข้อมูลให้ครบทั้ง 3 ช่อง")

# --- ส่วนที่ 2: Loan ---
elif selected == 'Loan':
    st.title('Loan Classification')
    
    col1, col2 = st.columns(2)
    with col1:
        person_age = st.text_input('Age')
        person_gender = st.selectbox('Gender', list(gender_map.keys()))
        person_education = st.selectbox('Education', list(education_map.keys()))
        person_income = st.text_input('Annual Income')
        person_emp_exp = st.text_input('Employment Experience (Years)')
        person_home_ownership = st.selectbox('Home Ownership', list(home_map.keys()))
    
    with col2:
        loan_amnt = st.text_input('Loan Amount')
        loan_intent = st.selectbox('Loan Intent', list(intent_map.keys()))
        loan_int_rate = st.text_input('Interest Rate')
        loan_percent_income = st.text_input('Percent Income')
        cb_person_cred_hist_length = st.text_input('Credit History Length')
        credit_score = st.text_input('Credit Score')
        previous_loan_defaults_on_file = st.selectbox('Previous Default', list(default_map.keys()))
    
    if st.button('Predict Loan'):
        features = [
            float(person_age), gender_map[person_gender], education_map[person_education],
            float(person_income), float(person_emp_exp), home_map[person_home_ownership],
            float(loan_amnt), intent_map[loan_intent], float(loan_int_rate),
            float(loan_percent_income), float(cb_person_cred_hist_length),
            float(credit_score), default_map[previous_loan_defaults_on_file]
        ]
        pred = loan_model.predict([features])
        st.success(f"Loan Result: {'Accept' if pred[0] == 1 else 'Not Accept'}")

# --- ส่วนที่ 3: Riding ---
elif selected == 'Riding':
    st.title('Riding Mower Classification')
    income_val = st.text_input('รายได้ (Income)')
    lotsize_val = st.text_input('พื้นที่บ้าน (Lot Size)')
    
    if st.button('Predict Riding'):
        try:
            pred = riding_model.predict([[float(income_val), float(lotsize_val)]])
            st.success(f"Result: {'Owner' if pred[0] == 1 else 'Non Owner'}")
        except:
            st.error("กรุณากรอกข้อมูลเป็นตัวเลข")
