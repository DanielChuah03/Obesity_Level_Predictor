import streamlit as st
import pandas as pd
import joblib

model1 = joblib.load('obesity_Level_prediction.pkl')


st.title("Obesity Level Predictor")
    
# Define input fields
gender = st.selectbox('What is your gender?', ['Select', 'Male', 'Female'])
family_history = st.selectbox('Has a family member suffered or suffers from overweight?', ['Select', 'no', 'yes'])
smoke = st.selectbox('Do you smoke?', ['Select', 'no', 'yes'])
scc = st.selectbox('Do you monitor the calories you eat daily?', ['Select', 'no', 'yes'])
favc = st.selectbox('Do you eat high caloric food frequently?', ['Select', 'no', 'yes'])
calc = st.selectbox('How often do you drink alcohol?', ['Select', 'no', 'Sometimes', 'Frequently', 'Always'])
caec = st.selectbox('Do you eat any food between meals?', ['Select', 'no', 'Sometimes', 'Frequently', 'Always'])
mtrans = st.selectbox('Which transportation do you usually use?', ['Select', 'Automobile', 'Motorbike', 'Bike', 'Public Transportation', 'Walking'])
    
age = st.slider('What is your age?', 1, 100, 25, format="%d years old")
height = st.slider('What is your height?', 100, 250, 150, format="%d cm")
height_meters = height / 100.0
weight = st.slider('What is your weight?', 20, 200, 70, format="%d kg")
    
    #mapping
fcvc_labels = ['Never', 'Sometimes', 'Always']
fcvc_map = {'Never': 1, 'Sometimes': 2, 'Always': 3}
fcvc = st.select_slider('Do you usually eat vegetables in your meals?', options=fcvc_labels)
fcvc_numeric = fcvc_map[fcvc]
    
ncp_options = ['Select', 'Between 1 and 2', 'Three', 'More than three']
ncp_map = {'Between 1 and 2': 1, 'Three': 2, 'More than three': 3}
ncp = st.selectbox('How many main meals do you have daily?', options=ncp_options, index=0 if ncp_options[0] == 'Select' else None)
ncp_numeric = ncp_map.get(ncp, None)
    
ch2o_options = ['Select', 'Less than a liter', 'Between 1 and 2 L', 'More than 2 L']
ch2o_map = {'Less than a liter': 1, 'Between 1 and 2 L': 2, 'More than 2 L': 3}
ch2o = st.selectbox('How much water do you drink daily?', options=ch2o_options, index=0 if ch2o_options[0] == 'Select' else None)
ch2o_numeric = ch2o_map.get(ch2o, None)
    
faf_options = ['Select', 'I do not have', '1 or 2 days', '2 or 4 days', '4 or 5 days']
faf_map = {'Select': None, 'I do not have': 0, '1 or 2 days': 1, '2 or 4 days': 2, '4 or 5 days': 3}
faf = st.selectbox('How often do you have physical activity?', options=faf_options, index=0 if faf_options[0] == 'Select' else None)
faf_numeric = faf_map.get(faf, None)

tue_options = ['Select', '0-2 hours', '3-5 hours', 'More than 5 hours']
tue_map = {'Select': None, '0-2 hours': 0, '3-5 hours': 1, 'More than 5 hours': 2}
tue = st.selectbox('Tech device usage?', options=tue_options, index=0 if tue_options[0] == 'Select' else None)
tue_numeric = tue_map.get(tue, None)
    
    # Check for missing selections
if (family_history == 'Select' or smoke == 'Select' or scc == 'Select' or 
        favc == 'Select' or caec == 'Select' or mtrans == 'Select' or
        ncp == 'Select' or ch2o == 'Select' or faf == 'Select' or tue == 'Select'):
        st.warning('Please answer all questions before predicting.')
else:
        # Create input dataframe
        input_df = pd.DataFrame({
            'Gender': [gender],
            'family_history_with_overweight': [family_history],
            'SMOKE': [smoke],
            'SCC': [scc],
            'FAVC': [favc],
            'CALC': [calc],
            'CAEC': [caec],
            'MTRANS': [mtrans],
            'Age': [age],
            'Height': [height_meters],
            'Weight': [weight],
            'FCVC': [fcvc_numeric],
            'NCP': [ncp_numeric],    
            'CH2O': [ch2o_numeric],  
            'FAF': [faf_numeric],
            'TUE': [tue_numeric]  
        })
        
        # Handle unknown categories
        try:
            # Make prediction
            if st.button('Predict Obesity Level'):
                prediction = model1.predict(input_df)
                prediction_label = ['Insufficient_Weight', 'Normal_Weight', 'Overweight_Level_I',
                                    'Overweight_Level_II', 'Obesity_Type_I', 'Obesity_Type_II', 'Obesity_Type_III']
                st.write(f"Predicted Obesity Level: {prediction_label[int(prediction)]}")
        except ValueError as ve:
            st.error(f"Error predicting: {ve}")
