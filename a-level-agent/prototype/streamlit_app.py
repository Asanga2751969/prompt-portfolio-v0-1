import streamlit as st
import openai
import os

# Load OpenAI API key from Streamlit secrets
openai.api_key = st.secrets["OPENAI_API_KEY"]

# Load the system prompt
with open("a-level-agent/prototype/system-prompt.txt", "r") as file:
    system_prompt = file.read()

# Streamlit page setup
st.set_page_config(page_title="A-Level Study Assistant", page_icon="🎓")
st.title("🎓 A-Level Study Assistant")
st.write("Ask a question related to your A-Level subjects.")

# User input
user_question = st.text_input("Enter your question here:", placeholder="e.g., Explain Newton's third law")

# Button to trigger response
if st.button("Get Answer") and user_question:
    with st.spinner("Thinking..."):
        try:
            response = openai.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_question}
                ]
            )
            answer = response.choices[0].message.content
            st.success("✅ Answer Ready:")
            st.write(answer)
        except Exception as e:
            st.error("❌ Something went wrong.")
            st.exception(e)
