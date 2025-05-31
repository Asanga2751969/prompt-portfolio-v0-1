import streamlit as st
import openai
import os

# Set OpenAI API key from Streamlit secrets
openai.api_key = st.secrets["OPENAI_API_KEY"]

# App title
st.title("🎓 A-Level Study Assistant")

# Subject and level selectors
subject = st.selectbox("Choose a subject:", ["Physics", "Biology", "Chemistry", "Math", "Economics"])
level = st.selectbox("Choose exam level:", ["AS", "A2", "Full A-Level"])

# User question
question = st.text_input("Ask a question related to your selected subject and level:")

# Create a dynamic system prompt
system_prompt = (
    f"You are an expert A-Level tutor helping a student prepare for the {level} exam in {subject}. "
    "Give concise explanations with examples where appropriate. Prioritize what is needed to score high marks in exams. "
    "Make concepts beginner-friendly but academically accurate."
)

# Process question
if st.button("Get Answer") and question:
    try:
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": question}
            ]
        )
        answer = response.choices[0].message.content
        st.markdown("### 📘 Answer:")
        st.write(answer)
    except Exception as e:
        st.error(f"Error: {e}")

