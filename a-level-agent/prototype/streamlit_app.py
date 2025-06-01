import streamlit as st
import openai
import os

# Set page config
st.set_page_config(page_title="📘 A-Level Study Assistant", layout="centered")

# App title and intro
st.title("📘 A-Level Study Assistant")
st.markdown(
    "Ask any A-Level subject question and get clear, exam-focused explanations. "
    "Choose your subject and level from the sidebar to get started!"
)

# Sidebar inputs
st.sidebar.header("🛠️ Settings")
subject = st.sidebar.selectbox("Select Subject", ["Physics", "Biology", "Math", "Economics"])
level = st.sidebar.radio("Exam Level", ["AS", "A Level"])

# OpenAI API key from secrets
openai.api_key = st.secrets["OPENAI_API_KEY"]

# Get user question
user_question = st.text_input("❓ Enter your study question:")

# Dynamic system prompt based on subject and level
system_prompt = (
    f"You are an expert A-Level tutor helping a student prepare for the {level} exam in {subject}. "
    "Give concise explanations with examples where appropriate. Prioritize what is needed to score high marks in exams. "
    "Make concepts beginner-friendly but academically accurate."
)

# Generate AI response
if user_question:
    with st.spinner("Thinking..."):
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_question}
            ]
        )
        answer = response.choices[0].message.content

    st.markdown("### 📘 Answer")
    st.markdown(
        f"<div style='background-color:#f8f9fa; padding: 15px; border-radius: 8px; "
        f"border: 1px solid #ddd; overflow-y: auto; max-height: 400px;'>"
        f"{answer}</div>",
        unsafe_allow_html=True
    )

# Footer
st.markdown("---")
st.markdown("Made with ❤️ using OpenAI + Streamlit")

     
