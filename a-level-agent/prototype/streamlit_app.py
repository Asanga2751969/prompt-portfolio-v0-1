import streamlit as st
import openai
import os

# Set page configuration
st.set_page_config(page_title="📘 A-Level Study Assistant", layout="centered")

# Sidebar: Subject and Level selection
st.sidebar.markdown("### 🛠️ Settings")
subject = st.sidebar.selectbox("Select Subject", ["Physics", "Biology", "Chemistry", "Mathematics", "Economics"])
level = st.sidebar.radio("Study Level", ["AS Level", "A Level"])

# Input field for question
st.title("🎓 A-Level Study Assistant")
st.markdown("Ask any subject-related question and get a study-friendly response.")
user_question = st.text_input("✏️ Enter your question here:")

# Only proceed if a question is entered
if user_question:
    # Build dynamic system prompt
    system_prompt = (
        f"You are an expert A-Level tutor helping a student prepare for the {level} exam in {subject}. "
        "Give concise explanations with examples where appropriate. Prioritize what is needed to score high marks in exams. "
        "Make concepts beginner-friendly but academically accurate."
    )

    # Authenticate via secrets
    openai.api_key = os.getenv("OPENAI_API_KEY")

    # Call OpenAI API
    try:
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_question}
            ]
        )

        # Styled display of AI response
        st.markdown("### 📘 AI Tutor Response")
        st.markdown(
            f"""
            <div style='background-color:#f9f9f9; padding:15px; border-radius:10px; border:1px solid #ddd; overflow-x:auto'>
                {response.choices[0].message.content}
            </div>
            """,
            unsafe_allow_html=True
        )

    except Exception as e:
        st.error(f"⚠️ Something went wrong: {e}")


     
