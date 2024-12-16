import streamlit as st
import pandas as pd
import joblib
import warnings

# Suppress warnings
warnings.filterwarnings("ignore")

# App Header
st.header("📚 Dropout Risk Prediction 📉")

st.write("📊 *Predictive Model Built on Student Data*")

# Load the dataset for display and range extraction
try:
    df = pd.read_csv("simulated_dropout_prediction_dataset.csv")
    st.dataframe(df.head())  # Display the first few rows of the dataset
except FileNotFoundError:
    st.error("❌ Dataset file 'simulated_dropout_prediction_dataset.csv' not found. Please upload the file.")
    st.stop()

# Input fields for user data
st.write("🌟 *Enter the following student data for prediction:*")

# Layout input fields using columns
col1, col2 = st.columns(2)

with col1:
    student_ID = st.number_input(f"Enter Student ID (Min: {df.Student_ID.min()} to Max: {df.Student_ID.max()})", min_value=int(df.Student_ID.min()), max_value=int(df.Student_ID.max()))

with col2:
    Gender = st.selectbox("Enter Gender (0 = Female, 1 = Male)", options=[0, 1])

col3, col4 = st.columns(2)

with col3:
    Parental_Education = st.selectbox("Enter Parental Education Level (0=Some High School, 1=High School Graduate, 2=Some College, 3=Bachelor's Degree)", options=[0, 1, 2, 3])

with col4:
    Attendance_Rate = st.slider("Enter Attendance Rate (%)", min_value=0, max_value=100, step=1)

col5, col6 = st.columns(2)

with col5:
    SocioEconomic_Status = st.selectbox("Enter Socioeconomic Status (0=Low, 1=Medium, 2=High)", options=[0, 1, 2])

with col6:
    Engagement_Score = st.number_input("Enter Engagement Score (0 to 100)", min_value=0, max_value=100, step=1)

Test_Score_Median = st.number_input("Enter Test Score Median (0 to 100)", min_value=0, max_value=100, step=1)

# Prepare input data for prediction
input_data = [[student_ID, Gender, Parental_Education, Attendance_Rate, SocioEconomic_Status, Engagement_Score, Test_Score_Median]]

###################### Prediction Logic ######################

# Load the trained model
try:
    model = joblib.load('Dropout_pred.pkl')
except FileNotFoundError:
    st.error("❌ Model file 'Dropout_pred.pkl' not found. Please upload the model.")
    st.stop()
except Exception as e:
    st.error(f"❌ Error loading model: {e}")
    st.stop()

# Predict and display result when button is clicked
if st.button("🔍 Predict Dropout Risk"):
    try:
        prediction = model.predict(input_data)
        
        # Display result with a message
        if prediction == 1:
            st.markdown("<h3 style='color: red;'>The student is at risk of dropping out. 🚨</h3>", unsafe_allow_html=True)
        else:
            st.markdown("<h3 style='color: green;'>The student is not at risk of dropping out. ✅</h3>", unsafe_allow_html=True)
        
        # Optionally, show the input data
        st.write("💾 *Given Input:*")
        input_df = pd.DataFrame(input_data, columns=["Student ID", "Gender", "Parental Education", "Attendance Rate", "Socioeconomic Status", "Engagement Score", "Test Score Median"])
        st.dataframe(input_df)
    except Exception as e:
        st.error(f"❌ Error making prediction: {e}")
