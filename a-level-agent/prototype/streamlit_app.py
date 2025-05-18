import streamlit as st
import openai

# Set your OpenAI API key
openai.api_key = "sk-proj-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"  # Replace safely when testing

# System prompt (you can also load from file if needed)
system_prompt = """
You are an A-Level Exam Study Assistant specialized in helping students prepare for Edexcel A-Level exams in subjects like Physics, Biology, Chemistry, and Mathematics...

When a student asks a question:
- Give a clear, concise explanation of the concept  
- Use analogies, step-by-step logic, or visual metaphors (in text)  
- Include 1–2 past-paper-style example questions with answers  
- Suggest study tips if relevant  

Use a friendly and focused tone. Assume the student’s goal is exam success. Avoid overly technical jargon unless necessary. If the topic is too broad, ask clarifying questions before answering.
"""

# Streamlit UI layout
st.title("🎓 A-Level Study Assistant")
st.subheader("Powered by GPT-3.5 — Ask anything from your Edexcel syllabus!")

# User input
user_question = st.text_input("Enter your question:")

# On submit
if user_question:
    with st.spinner("Thinking..."):
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_question}
            ]
        )
        st.markdown("**Assistant:**")
        st.write(response.choices[0].message.content)
