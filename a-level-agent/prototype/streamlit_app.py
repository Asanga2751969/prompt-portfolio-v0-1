import streamlit as st
from openai import OpenAI

# Title of the app
st.title("🎓 A-Level Study Assistant")

# Load the system prompt from file
with open("a-level-agent/prototype/system-prompt.txt", "r") as file:
    system_prompt = file.read()

# Create OpenAI client using API key stored in Streamlit secrets
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# Input box for user question
user_input = st.text_input("Ask a question about your A-Level subject:")

# If there's user input, call the assistant
if user_input:
    with st.spinner("Thinking..."):
        try:
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_input}
                ]
            )
            st.success(response.choices[0].message.content)
        except Exception as e:
            st.error(f"An error occurred: {e}")

