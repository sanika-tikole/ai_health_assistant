import random
import pandas as pd
import streamlit as st
from sentence_transformers import SentenceTransformer, util
from googletrans import Translator

# Load your data
df = pd.read_csv(r'C:\Users\Admin\Desktop\chatbot\AI-Health-Assistant\dataset - Sheet1.csv')  # Replace with your dataset path

# Initialize the SentenceTransformer model
model = SentenceTransformer('all-MiniLM-L6-v2')

# Define medical keywords for fallback
medical_keywords = {
    "fever": "It sounds like you may have a fever. Stay hydrated and consider seeing a doctor if symptoms persist.",
    "cough": "A persistent cough might be due to an infection or allergy. Try warm fluids and rest.",
    "headache": "Headaches can have many causes, including stress and dehydration. Consider resting and drinking water.",
    "cold": "Common colds usually go away on their own. Stay warm, drink fluids, and get rest.",
}

# List of health tips categorized by keywords
health_tips = {
    "sleep": [
        "Try to get at least 7-8 hours of sleep each night.",
        "Establish a regular sleep routine to improve sleep quality.",
        "Avoid screens before bed to help your mind relax.",
    ],
    "energy": [
        "Make sure you're eating a balanced diet to maintain energy.",
        "Exercise regularly to boost your energy levels.",
        "Stay hydrated throughout the day to avoid fatigue.",
    ],
    "stress": [
        "Take short breaks throughout the day to reduce stress.",
        "Practice mindfulness or meditation to help manage stress.",
        "Engage in physical activity to reduce anxiety and stress.",
    ],
    "general": [
        "Drink plenty of water throughout the day.",
        "Get at least 30 minutes of exercise every day.",
        "Eat a balanced diet rich in fruits and vegetables.",
    ],
}

# Function to get personalized health tip
def get_personalized_health_tip(user_input):
    # Convert input to lowercase for easier matching
    user_input_lower = user_input.lower()

    # Check for specific keywords in the user input
    if "tired" in user_input_lower or "fatigue" in user_input_lower:
        return random.choice(health_tips["energy"])
    elif "sleep" in user_input_lower or "rest" in user_input_lower:
        return random.choice(health_tips["sleep"])
    elif "stress" in user_input_lower or "anxious" in user_input_lower:
        return random.choice(health_tips["stress"])
    else:
        # Default to a general health tip if no specific keywords match
        return random.choice(health_tips["general"])

# Function to find the best cure based on similarity
def find_best_cure(user_input):
    user_input_embedding = model.encode(user_input, convert_to_tensor=True)
    disease_embeddings = model.encode(df['disease'].tolist(), convert_to_tensor=True)

    similarities = util.pytorch_cos_sim(user_input_embedding, disease_embeddings)[0]
    best_match_idx = similarities.argmax().item()
    best_match_score = similarities[best_match_idx].item()

    # Define a similarity threshold for valid matches
    SIMILARITY_THRESHOLD = 0.5  # Adjust as needed

    if best_match_score < SIMILARITY_THRESHOLD:
        # Check for keywords in user input
        for keyword, response in medical_keywords.items():
            if keyword in user_input.lower():
                return response

        # Default fallback response if no keywords match
        return "I'm sorry, I don't have enough information on this. Please consult a healthcare professional."

    return df.iloc[best_match_idx]['cure']

# Function to translate text
def translate_text(text, dest_language='en'):
    return translator.translate(text, dest=dest_language).text

# Initialize translator
translator = Translator()

# Streamlit UI enhancements
st.set_page_config(page_title="Medical Chatbot", page_icon="⚕️", layout="wide")

# Custom CSS for styling
st.markdown(
    """
    <style>
    .reportview-container {
        background: #f0f2f6; /* Light gray background */
    }
    .sidebar .sidebar-content {
        background: #e1f5fe; /* Light blue sidebar */
        border:none;
    }

    h1, h2, h3 {
        color: #007bff; /* Primary blue color for headings */
    }
    .stButton>button {
        color: white !important;
        background-color: #007bff;
        border: none;
        padding: 10px 20px;
        border-radius: 5px;
        cursor: pointer;
    }

    .stTextInput>div>div>input {
        border: 2px solid #007bff;
        border-radius: 5px;
        padding: 10px;
    }


    .stSelectbox>div>div>div {
        border: 2px solid #007bff;
        border-radius: 5px;
        padding: 5px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Sidebar for settings
with st.sidebar:
    st.header("Settings")
    language_choice = st.selectbox(
        "Select Language",
        [
            "English",
            "Hindi",
            "Gujarati",
            "Korean",
            "Turkish",
            "German",
            "French",
            "Arabic",
            "Urdu",
            "Tamil",
            "Telugu",
            "Chinese",
            "Japanese",
        ],
    )

    # Language codes based on the user selection
    language_codes = {
        "English": "en",
        "Hindi": "hi",
        "Gujarati": "gu",
        "Korean": "ko",
        "Turkish": "tr",
        "German": "de",
        "French": "fr",
        "Arabic": "ar",
        "Urdu": "ur",
        "Tamil": "ta",
        "Telugu": "te",
        "Chinese": "zh-CN",  # Simplified Chinese
        "Japanese": "ja",
    }

    st.markdown("---")
    st.write("Disclaimer: This chatbot provides suggestions for informational purposes only and does not constitute medical advice. Always consult with a qualified healthcare professional for any health concerns.")

# Main area
st.title("Medical Chatbot ⚕️")
user_input = st.text_input("Ask a question about your health:", "")

col1, col2 = st.columns(2)

with col1:
    if st.button("Get Response"):
        if user_input:
            response = find_best_cure(user_input)
            translated_response = translate_text(response, dest_language=language_codes[language_choice])
            st.markdown(f"**Suggestion:** {translated_response}")
            st.caption("*Please note, the translation is provided by AI and might not be perfect.*")

with col2:
    if st.button("Get a Personalized Health Tip"):
        if user_input:
            personalized_tip = get_personalized_health_tip(user_input)
            translated_tip = translate_text(personalized_tip, dest_language=language_codes[language_choice])
            st.markdown(f"**Health Tip:** {translated_tip}")
            st.caption("*Please note, the translation is provided by AI and might not be perfect.*")
