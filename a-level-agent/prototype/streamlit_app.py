import os
import streamlit as st
import openai

# Load API key from Streamlit secrets
openai.api_key = st.secrets["OPENAI_API_KEY"]

# Set up page
st.set_page_config(page_title="📚 A-Level Study Assistant", layout="wide")
st.title("🎓 A-Level Study Assistant")
st.markdown("Ask any A-Level subject question and get a concise, exam-focused explanation!")

# Sidebar for settings
st.sidebar.markdown("### 🛠️ Settings Panel")
subject = st.sidebar.selectbox("Select Subject", ["Physics", "Math", "Biology", "Economics", "Chemistry"])
level = st.sidebar.radio("Exam Level", ["AS", "A2", "Full A-Level"])

# Input field
user_input = st.text_input("🔍 Enter your study question:")

# Dynamic system prompt based on settings
system_prompt = (
    f"You are an expert A-Level tutor helping a student prepare for the {level} exam in {subject}. "
    "Give concise explanations with examples where appropriate. Prioritize what is needed to score high marks in exams. "
    "Make concepts beginner-friendly but academically accurate."
)

# If user submits question
if user_input:
    try:
        # Call OpenAI API
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_input}
            ]
        )

        # Display response
        st.markdown("### 📘 AI Tutor Response")
        try:
            st.markdown(response.choices[0].message.content)
        except Exception as e:
            st.error(f"❌ Error displaying response: {e}")

    except Exception as e:
        st.error(f"❌ API error: {e}")



     
