import streamlit as st
import pickle
import os
from streamlit_option_menu import option_menu

# ----------------- Streamlit Page Setup --------------------
st.set_page_config(page_title="Disease Prediction System", page_icon="⚕️", layout="centered")

# Background Image URL
background_image_url = "https://d2jx2rerrg6sh3.cloudfront.net/images/news/ImageForNews_776422_17123165547518811.jpg"

# Light Theme with Background Image
st.markdown(f"""
    <style>
    #MainMenu {{visibility: hidden;}}
    footer {{visibility: hidden;}}
    header {{visibility: hidden;}}

    [data-testid="stAppViewContainer"] {{
        background-image: url("{background_image_url}");
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
        background-attachment: fixed;
    }}

    .stApp {{
        color: #222;
        font-family: "Segoe UI", sans-serif;
    }}

    .css-1d391kg, .css-ffhzg2 {{
        color: #222 !important;
    }}

    h1, h2, h3, h4, h5, h6, p, label {{
        color: #111 !important;
    }}

    
/* 🟢 Ensure all inner text inside tooltip is white */
    div[role="tooltip"] * {{
        color: white !important;
}}

    .stButton>button {{
        background-color: #4CAF50;
        color: white;
        border: none;
        padding: 0.5rem 1rem;
        border-radius: 8px;
    }}
    
    </style>
""", unsafe_allow_html=True)


# ---------------- Load Models ----------------


# Define base path to current file location
base_path = os.path.dirname(__file__)
model_dir = os.path.join(base_path, 'Models')

models = {
    'diabetes': pickle.load(open(os.path.join(model_dir, 'diabetes_model_selected.sav'), 'rb')),
    'heart_disease': pickle.load(open(os.path.join(model_dir, 'heart_disease_model.sav'), 'rb')),
    'parkinsons': pickle.load(open(os.path.join(model_dir, 'parkinson_rf_model.sav'), 'rb')),
    'lung_cancer': pickle.load(open(os.path.join(model_dir, 'lungs_disease_model.sav'), 'rb')),
}


# ---------------- Sidebar Menu ----------------
with st.sidebar:
    selected = option_menu(
        menu_title="Main Menu",
        options=["Home", "Diabetes Prediction", "Heart Disease Prediction", "Parkinsons Prediction", "Lung Cancer Prediction"],
        icons=["house", "activity", "heart", "cpu", "lungs"],
        default_index=0,
    )

# ---------------- Reusable Input Function ----------------
def display_input(label, tooltip, key, type="text"):
    if type == "text":
        return st.text_input(label, key=key, help=tooltip)
    elif type == "number":
        return st.number_input(label, key=key, help=tooltip, step=1)

# ---------------- Pages ----------------

# ---------------- Home Page ----------------
if selected == "Home":
    st.title("⚕️ Welcome to Disease Prediction System")
    st.markdown("""
    <div style="background-color:rgba(255,255,255,0.1); padding:20px; border-radius:15px;">
        <h3>📌 About</h3>
        <p>This AI-powered system helps in the early detection of multiple diseases using machine learning models trained on real medical data.</p>
        <p>✅ Diseases Covered:</p>
        <ul>
            <li>Diabetes</li>
            <li>Heart Disease</li>
            <li>Parkinson's Disease</li>
            <li>Lung Cancer</li>
        </ul>
        <h3>🩺 How to Use</h3>
        <ol>
            <li>Select a disease from the sidebar.</li>
            <li>Enter your medical details.</li>
            <li>Click the prediction button to see the result.</li>
        </ol>
        <p style="margin-top:20px;">⚠️ <b>Disclaimer:</b> This tool is for probabilistic predictions of initial consultation only and not a substitute for professional medical advice.</p>
    </div>
    """, unsafe_allow_html=True)

# ---------------- Diabetes Page ----------------
if selected == 'Diabetes Prediction':
    st.title('🩸 Diabetes Prediction')
    st.write("Enter the following details to predict diabetes:")
    
    Glucose = display_input('Glucose Level', 'Enter glucose level', 'Glucose', 'number')
    BloodPressure = display_input('Blood Pressure value', 'Enter blood pressure value', 'BloodPressure', 'number')
    BMI = display_input('BMI value', 'Enter Body Mass Index value', 'BMI', 'number')
    Age = display_input('Age of the Person', 'Enter age of the person', 'Age', 'number')

    diab_diagnosis = ''
    if st.button('Predict Diabetes'):
        prediction = models['diabetes'].predict([[Glucose, BloodPressure, BMI, Age]])
        result = '✅ The person is diabetic' if prediction[0] == 1 else '❌ The person is not diabetic'
        st.success(result)

# ---------------- Heart Disease Page ----------------
if selected == 'Heart Disease Prediction':
    st.title('❤️ Heart Disease Prediction')
    st.write("Enter the following details to predict heart disease:")

    age = st.number_input('Age', min_value=18, max_value=100, step=1)
    sex = st.selectbox('Sex', ['Female', 'Male'])
    cp = st.selectbox(
    'Chest Pain Type',
    (
        'Typical Angina (Pressure or squeezing in the chest(chest pain on exertion))',
        'Atypical Angina (Unusual chest pain not related to exertion)',
        'Non-anginal Pain (Chest pain not related to the heart)',
        'Asymptomatic (No chest pain)'
    )
)
    # Convert to numerical value for model
    cp_mapping = {
    'Typical Angina (Pressure or squeezing in the chest(chest pain on exertion))': 0,
    'Atypical Angina (Unusual chest pain not related to exertion)': 1,
    'Non-anginal Pain (Chest pain not related to the heart)': 2,
    'Asymptomatic (No chest pain)': 3
}
    cp = cp_mapping[cp]
    
    trestbps = st.number_input('Resting Blood Pressure (mm Hg)', min_value=50, max_value=300)
    chol = st.number_input('Serum Cholesterol (mg/dL)', min_value=100, max_value=600)
    thalach = st.number_input('Max Heart Rate Achieved', min_value=60, max_value=220)
    exang = st.selectbox('Exercise Induced Angina(chest pain)', ('No', 'Yes'))

    # Convert categorical inputs
    sex = 1 if sex == 'Male' else 0
    exang = 1 if exang == 'Yes' else 0

    heart_diagnosis = ''
    if st.button('Predict Heart Disease'):
        prediction = models['heart_disease'].predict([[age, sex, cp, trestbps, chol, thalach, exang]])
        result = '✅ The person has heart disease' if prediction[0] == 1 else '❌ The person does not have heart disease'
        st.success(result)

# ---------------- Parkinson's Disease Page ----------------
if selected == "Parkinsons Prediction":
    st.title("🧠 Parkinson's Disease Prediction")
    st.write("Enter the following details to predict Parkinson's disease:")

     # User Input Fields (0 = No, 1 = Yes)
    tremors = st.selectbox('Tremors (shaking or trembling)', ('No', 'Yes'),
    help = "Involuntary shaking of hands, arms, legs, or other body parts — often noticed at rest.")
    tremors = 1 if tremors == 'Yes' else 0

    bradykinesia = st.selectbox('Bradykinesia (slowness of movement)', ('No', 'Yes'),
    help = "Slowed movements or difficulty initiating movement, common in Parkinson’s Disease.")
    bradykinesia = 1 if bradykinesia == 'Yes' else 0

    muscle_stiffness = st.selectbox('Muscle Stiffness (rigidity)', ('No', 'Yes'),
    help = "Feeling of tight or rigid muscles, especially in arms or legs.")
    muscle_stiffness = 1 if muscle_stiffness == 'Yes' else 0

    balance_issues = st.selectbox('Balance Issues', ('No', 'Yes'),
    help = "Unsteady gait or frequent loss of balance while standing or walking.")
    balance_issues = 1 if balance_issues == 'Yes' else 0

    voice_changes = st.selectbox('Voice Changes', ('No', 'Yes'),
    help = "Changes in voice such as becoming softer, hoarse, or monotone.")
    voice_changes = 1 if voice_changes == 'Yes' else 0

    facial_expression_changes = st.selectbox('Facial Expression Changes', ('No', 'Yes'),
    help = "Reduced facial expressions or a 'masked' look — often noticed by others.")
    facial_expression_changes = 1 if facial_expression_changes == 'Yes' else 0

# Prediction Button
    parkinsons_diagnosis = ''
    if st.button("Parkinson's Test Result"):
        parkinsons_prediction = models['parkinsons'].predict([[tremors, bradykinesia, muscle_stiffness, balance_issues, voice_changes, facial_expression_changes]])
        parkinsons_diagnosis = '✅The person is likely to have Parkinson\'s Disease' if parkinsons_prediction[0] == 1 else '❌ The person is not likely to have Parkinson\'s Disease'
        st.success(parkinsons_diagnosis)

# ---------------- Lung Cancer Page ----------------
if selected == "Lung Cancer Prediction":
    st.title("🫁 Lung Cancer Prediction")
    st.write("Enter the following details to predict lung cancer:")

    
# Gender (still a select box because it's mutually exclusive)
    gender = st.selectbox('Gender', ('Female', 'Male'),help="Select your gender")
    gender = 1 if gender == 'Male' else 0

# Age input
    age = st.slider("Age", 1, 100, 30, help="Enter your age in years")

# Binary inputs as checkboxes
    smoking = st.checkbox("Smoking", help="Check if you are a regular smoker")
    fatigue = st.checkbox("Fatigue", help="Check if you often feel tired or low on energy")
    wheezing = st.checkbox("Wheezing", help="Check if you experience a whistling sound when breathing")
    coughing = st.checkbox("Coughing", help="Check if you have frequent or chronic cough")
    short_breath = st.checkbox("Shortness of Breath", help="Check if you experience difficulty breathing or feel breathless")
    chest_pain = st.checkbox("Chest Pain", help="Check if you feel pain or discomfort in your chest")

# Convert checkbox values to 0 or 1
    smoking = 1 if smoking else 0
    fatigue = 1 if fatigue else 0
    wheezing = 1 if wheezing else 0
    coughing = 1 if coughing else 0
    short_breath = 1 if short_breath else 0
    chest_pain = 1 if chest_pain else 0
    
   
    lungs_diagnosis = ''
    if st.button("Lung Cancer Test Result"):
        lungs_prediction = models['lung_cancer'].predict([[gender, age, smoking, fatigue, wheezing, coughing, short_breath, chest_pain]])
        lungs_diagnosis = "✅The person is likely to have Lung Cancer." if lungs_prediction[0] == 1 else "❌ The person is not likely to have Lung Cancer."
        st.success(lungs_diagnosis)
