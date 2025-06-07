import streamlit as st
import openai
import os

# Set page config
st.set_page_config(page_title="A-Level Study Assistant", page_icon="🎓")

# Load API key
openai.api_key = st.secrets["OPENAI_API_KEY"]
client = openai

# Sidebar configuration
st.sidebar.title("🛠️ Settings Panel")
subject = st.sidebar.selectbox("Select Subject", ["Physics", "Mathematics", "Biology", "Chemistry", "Economics"])
level = st.sidebar.selectbox("Select Study Level", ["AS Level", "A Level (Full)"])

# Dynamic system prompt
system_prompt = (
    f"You are an expert A-Level tutor helping a student prepare for the {level} exam in {subject}. "
    "Give concise explanations with examples where appropriate. Prioritize what is needed to score high marks in exams. "
    "Make concepts beginner-friendly but academically accurate."
)

# Initialize memory
if "history" not in st.session_state:
    st.session_state["history"] = [{"role": "system", "content": system_prompt}]

# Main interface
st.title("🎓 A-Level Study Assistant")
st.markdown("Ask your subject questions below and get exam-focused, beginner-friendly answers.")

user_question = st.text_input("📘 Enter your question")

# Reset conversation
if st.button("🧹 Start New Topic"):
    st.session_state["history"] = [{"role": "system", "content": system_prompt}]
    st.success("Memory cleared. Start a new topic!")

if user_question:
    # Add user question to memory
    st.session_state["history"].append({"role": "user", "content": user_question})

    # Get response
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=st.session_state["history"]
        )
        assistant_reply = response.choices[0].message.content

        # Add assistant reply to memory
        st.session_state["history"].append({"role": "assistant", "content": assistant_reply})

        # Display answer
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
        st.error(f"⚠️ Error generating response: {str(e)}")



     
