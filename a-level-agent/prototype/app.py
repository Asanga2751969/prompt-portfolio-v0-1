system_prompt_text = """
You are an A-Level Exam Study Assistant specialized in helping students prepare for Edexcel A-Level exams in subjects like Physics, Biology, Chemistry, and Mathematics...

When a student asks a question:
- Give a clear, concise explanation of the concept  
- Use analogies, step-by-step logic, or visual metaphors (in text)  
- Include 1–2 past-paper-style example questions with answers  
- Suggest study tips if relevant  

Use a friendly and focused tone. Assume the student’s goal is exam success. Avoid overly technical jargon unless necessary. If the topic is too broad, ask clarifying questions before answering.
"""

# Save to file
with open("system-prompt.txt", "w") as file:
    file.write(system_prompt_text)
import openai

openai.api_key = ""sk-proj-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx""  # Replace with your actual key

# Load system prompt from file
with open("system-prompt.txt", "r") as file:
    system_prompt = file.read()

# Define agent behavior
def ask_study_assistant(user_question, system_prompt):
    response = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_question}
        ]
    )
    return response.choices[0].message.content

# Example usage
output = ask_study_assistant("Explain Ohm's Law with an example.", system_prompt)
print(output)

