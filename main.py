import streamlit as st 
import tensorflow as tf 
import numpy as np 
import pandas as pd
import datetime
import time
import smtplib
from email.mime.text import MIMEText

# --- 1. GLOBAL CONFIGURATION & MODEL LOADING ---
st.set_page_config(page_title="Plant_Scan AI", layout="wide")

@st.cache_resource
def load_my_model():
    """
    Loads the 18M parameter CNN model once and caches it to prevent 
    'non-zero exit code' memory crashes on Streamlit Cloud.
    """
    #
    model = tf.keras.models.load_model('trained_model.keras', compile=False)
    model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])
    return model

# Initialize the model at the start of the app
model = load_my_model()

# --- 2. CORE FUNCTIONS ---

def model_prediction(test_image):
    """Processes image and returns prediction index using the global model."""
    image = tf.keras.preprocessing.image.load_img(test_image, target_size=(128, 128))
    input_arr = tf.keras.preprocessing.image.img_to_array(image)
    input_arr = np.array([input_arr])
    prediction = model.predict(input_arr)
    return np.argmax(prediction)

def send_email(name, email, msg):
    """Handles research feedback transmission via SMTP."""
    sender_email = "shivam.it.2820@gmail.com" 
    receiver_email = "apanashivamsingh@gmail.com" 
    password = "yycy vnwb vrqy peri" # App Password

    body = f"New Feedback from {name} ({email}):\n\n{msg}"
    message = MIMEText(body)
    message["Subject"] = f"Plant AI Feedback: {name}"
    message["From"] = sender_email
    message["To"] = receiver_email

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, message.as_string())
        return True
    except Exception as e:
        st.error(f"Mail System Error: {e}")
        return False

# --- 3. SIDEBAR NAVIGATION & STYLING ---
st.sidebar.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&display=swap');
    [data-testid="stSidebar"] { background: linear-gradient(180deg, #0f0f0f 0%, #1a1a1a 100%); border-right: 1px solid #333; }
    .sidebar-title { font-family: 'Orbitron', sans-serif; color: #00e676; text-align: center; font-size: 24px; padding: 20px 0; border-bottom: 2px solid #00e676; margin-bottom: 30px; }
    @keyframes heartbeat { 0% { transform: scale(1); opacity: 1; } 50% { transform: scale(1.2); opacity: 0.7; } 100% { transform: scale(1); opacity: 1; } }
    .heartbeat-icon { display: inline-block; color: #ff1744; animation: heartbeat 1.5s infinite; margin-right: 10px; }
    </style>
    <div class="sidebar-title">Plant_Scan AI</div>
""", unsafe_allow_html=True)

app_mode = st.sidebar.selectbox(
    "💠 SYSTEM MODULE", 
    ["🏠 DASHBOARD", "📚 PROJECT INFO", "🎯 NEURAL DIAGNOSIS"]
)

with st.sidebar.expander("🛠️ HARDWARE STATUS", expanded=True):
    st.markdown("""
        <div style='font-size: 14px;'>
            <span class="heartbeat-icon">●</span> <b>IoT NODE:</b> RKGIT_GHZ_01 <br>
            📟 <b>FIRMWARE:</b> v2.4.1 (Stable)
        </div>
    """, unsafe_allow_html=True)
    st.progress(88)

st.sidebar.markdown("---")
st.sidebar.markdown("""
    <div style='color: #888; font-size: 12px;'>
        <b>Affiliation:</b> RKGIT Ghaziabad<br>
        <b>Guide:</b> Dr. P.K. Sagar
    </div>
""", unsafe_allow_html=True)

# --- 4. MODULE: DASHBOARD ---
if app_mode == "🏠 DASHBOARD":
    st.markdown("<h1 style='text-align: center; color: #2E7D32;'>🌿 Intelligent Pesticide Sprinkling System</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; font-style: italic;'>AI-Powered Diagnosis for Sustainable Agriculture</p>", unsafe_allow_html=True)
    
    try:
        st.image("home image.jpeg", use_container_width=True)
    except:
        st.warning("Dashboard image 'home image.jpeg' not found in repository.")

    col1, col2 = st.columns(2)
    with col1:
        with st.container(border=True):
            st.markdown("#### 🎯 Precision Spraying")
            st.write("Calculates Infection Level to determine exact pesticide dosage.")
    with col2:
        with st.container(border=True):
            st.markdown("#### 📊 Real-time Analytics")
            st.write("Monitor crop health trends over the season.")

# --- 5. MODULE: PROJECT INFO ---
elif app_mode == "📚 PROJECT INFO":
    st.title("📄 Research & Documentation")
    st.info("Conference: GTSS 2026 | Venue: MMMUT Gorakhpur") #
    
    with st.container(border=True):
        st.markdown("### 👥 The Development Team")
        st.write("**Guide:** Dr. Pramod Kumar Sagar (Associate Professor, RKGIT)")
        cols = st.columns(4)
        members = ["Bhawana (TL)", "Shivam (AI/IoT)", "Naman (Data)", "Husain (Backend)"]
        for col, member in zip(cols, members):
            col.button(member, disabled=True, use_container_width=True)

    st.markdown("### 📧 Feedback")
    with st.form("feedback_form"):
        u_name = st.text_input("Name")
        u_email = st.text_input("Email")
        u_msg = st.text_area("Message")
        if st.form_submit_button("🚀 SUBMIT"):
            if send_email(u_name, u_email, u_msg):
                st.success("Feedback sent!")

# --- 6. MODULE: NEURAL DIAGNOSIS ---
elif app_mode == "🎯 NEURAL DIAGNOSIS":
    st.title("🛡️ Neural Health Diagnostic")
    test_image = st.file_uploader("Upload leaf sample", type=["jpg", "png", "jpeg"])
    
    if test_image:
        st.image(test_image, width=300)
        if st.button("🚀 INITIATE SCAN"):
            with st.spinner("Analyzing Biological Markers..."):
                idx = model_prediction(test_image)
                
                class_names = ['Apple___Apple_scab', 'Apple___Black_rot', 'Apple___Cedar_apple_rust', 'Apple___healthy',
                            'Blueberry___healthy', 'Cherry_(including_sour)___Powdery_mildew', 
                            'Cherry_(including_sour)___healthy', 'Corn_(maize)___Cercospora_leaf_spot Gray_leaf_spot', 
                            'Corn_(maize)___Common_rust_', 'Corn_(maize)___Northern_Leaf_Blight', 'Corn_(maize)___healthy', 
                            'Grape___Black_rot', 'Grape___Esca_(Black_Measles)', 'Grape___Leaf_blight_(Isariopsis_Leaf_Spot)', 
                            'Grape___healthy', 'Orange___Haunglongbing_(Citrus_greening)', 'Peach___Bacterial_spot',
                            'Peach___healthy', 'Pepper,_bell___Bacterial_spot', 'Pepper,_bell___healthy', 
                            'Potato___Early_blight', 'Potato___Late_blight', 'Potato___healthy', 
                            'Raspberry___healthy', 'Soybean___healthy', 'Squash___Powdery_mildew', 
                            'Strawberry___Leaf_scorch', 'Strawberry___healthy', 'Tomato___Bacterial_spot', 
                            'Tomato___Early_blight', 'Tomato___Late_blight', 'Tomato___Leaf_Mold', 
                            'Tomato___Septoria_leaf_spot', 'Tomato___Spider_mites Two-spotted_spider_mite', 
                            'Tomato___Target_Spot', 'Tomato___Tomato_Yellow_Leaf_Curl_Virus', 'Tomato___Tomato_mosaic_virus',
                            'Tomato___healthy']
                
                result = class_names[idx]
                plant, status = result.split("___")
                
                st.success(f"**Diagnosis:** {status.replace('_', ' ')} found in {plant.replace('_', ' ')}")
                
                if "healthy" not in status.lower():
                    st.error("🚨 Action Required: Initiating IoT Sprinkler Protocol")
                else:
                    st.balloons()
                    st.info("✅ Crop is healthy. No treatment needed.")
