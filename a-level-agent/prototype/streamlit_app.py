import streamlit as st
import openai
import os

# Page config
st.set_page_config(page_title="A-Level Study Assistant", layout="wide")

# Sidebar settings
st.sidebar.markdown("### 🛠️ Settings Panel")
subject = st.sidebar.selectbox("Select Subject", ["Physics", "Biology", "Chemistry", "Mathematics", "Economics"])
level = st.sidebar.selectbox("Select Study Level", ["AS Level", "A2 Level", "Full A Level"])

# Input field
st.markdown("# 📚 A-Level AI Study Assistant")
prompt = st.text_input("Ask a question related to your subject:")

# Initialize memory
if "history" not in st.session_state:
    st.session_state["history"] = []

# Create dynamic system prompt
system_prompt = (
    f"You are an expert A-Level tutor helping a student prepare for the {level} exam in {subject}. "
    "Give concise explanations with examples where appropriate. Prioritize what is needed to score high marks in exams. "
    "Make concepts beginner-friendly but academically accurate."
)

# Build full message history
messages = [{"role": "system", "content": system_prompt}]
for entry in st.session_state["history"]:
    messages.append({"role": "user", "content": entry["user"]})
    messages.append({"role": "assistant", "content": entry["assistant"]})

# Add latest user message
if prompt:
    messages.append({"role": "user", "content": prompt})

    try:
        # Load API key securely
        openai.api_key = st.secrets["OPENAI_API_KEY"]

        # Get model response
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=messages
        )

        assistant_reply = response.choices[0].message.content

        # Save current exchange to history
        st.session_state["history"].append({"user": prompt, "assistant": assistant_reply})

        # Display AI response
        st.markdown("### 📘 AI Tutor Response")
        st.markdown(
            f"""
            <div style='background-color:#f9f9f9; padding:15px; border-radius:10px; border:1px solid #ddd; overflow-x:auto'>
                {assistant_reply}
            </div>
            """,
            unsafe_allow_html=True
        )

    except Exception as e:
        st.error(f"⚠️ An error occurred: {str(e)}")





     
