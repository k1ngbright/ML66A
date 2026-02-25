if selected == 'BMI':

    st.title('BMI Classification')

    # รับค่า Input 3 ตัว

    # หมายเหตุ: ต้องแน่ใจว่ามีการประกาศ gender_map ไว้ก่อนหน้า เช่น gender_map = {'Male': 0, 'Female': 1}

    person_gender = st.selectbox('Gender', gender_map.keys())

    person_height = st.text_input('Height (cm)')

    person_weight = st.text_input('Weight (kg)')

    bmi_result = ''

    if st.button('Predict'):

        try:

            # นำค่าทั้ง 3 ไปเข้าโมเดล (เปลี่ยนชื่อจาก loan_model เป็น bmi_model)

            # ลำดับของ Input ต้องตรงกับตอนที่คุณเทรนโมเดลมา

            prediction = bmi_model.predict([

                [

                    gender_map[person_gender],

                    float(person_height),

                    float(person_weight)

                ]

            ])

            # แปลงผลลัพธ์การทำนาย (ปรับแก้ตัวเลขและข้อความให้ตรงกับคลาสที่คุณเทรนมา)

            if prediction[0] == 0:

                bmi_result = 'Underweight (น้ำหนักต่ำกว่าเกณฑ์)'

            elif prediction[0] == 1:

                bmi_result = 'Normal (น้ำหนักปกติ)'

            elif prediction[0] == 2:

                bmi_result = 'Overweight (ท้วม)'

            else:

                bmi_result = 'Obese (อ้วน)'

            st.success(bmi_result)

        except ValueError:

            # ป้องกันกรณีผู้ใช้งานกรอกตัวหนังสือลงในช่องน้ำหนัก/ส่วนสูง

            st.error("กรุณากรอกข้อมูล Height และ Weight เป็นตัวเลข")
 
