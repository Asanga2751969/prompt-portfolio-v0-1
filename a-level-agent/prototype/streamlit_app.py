import streamlit as st
import re
from openai import OpenAI

# --- OpenAI Client ---
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# --- Page Configuration ---
st.set_page_config(page_title="A-Level Study Assistant", layout="wide")
st.title("📘 A-Level Study Assistant")
st.info("Ask any A-Level or AS-Level study question. Use the sidebar to choose a mode.")

# --- Sidebar ---
st.sidebar.markdown("### 🛠️ Settings")
level = st.sidebar.selectbox("Exam Level", ["A-Level", "AS-Level"])
study_mode = st.sidebar.radio("Study Mode", ["Explain Mode", "Quiz Mode", "Past Paper Style"])

if st.sidebar.button("🔄 Reset Chat"):
    st.session_state["history"] = []
    st.session_state["current_quiz"] = []
    st.session_state["quiz_index"] = 0
    st.session_state["quiz_answers"] = []
    st.session_state["awaiting_quiz_answer"] = False

# --- Prompt Components ---
def get_base_prompt(level: str) -> str:
    return (
        f"You are an expert tutor helping a student prepare for their {level} exam. "
        "Answer clearly, using A-Level depth and terminology. "
        "Use LaTeX for any mathematical expressions (e.g., $F = ma$)."
    )

MODE_PROMPTS = {
    "Explain Mode": (
        "You are in Explain Mode. Break down topics simply and clearly, using examples and analogies. "
        "Emphasize understanding and key ideas."
    ),
    "Quiz Mode": (
        "You are in Quiz Mode. Ask short, focused questions to test the student's understanding. "
        "If the student requests a quiz, generate 3–5 questions on the topic."
    ),
    "Past Paper Style": (
        "You are in Past Paper Style Mode. Respond in the tone and format of a model A-Level exam answer. "
        "Be formal, concise, and subject-specific where relevant."
    )
}

def build_system_prompt(level: str, mode: str) -> str:
    return f"{get_base_prompt(level)} {MODE_PROMPTS[mode]}"

def is_quiz_request(user_input: str) -> bool:
    quiz_keywords = ["quiz me", "test me", "give me a quiz", "mini quiz", "quick quiz"]
    return any(keyword in user_input.lower() for keyword in quiz_keywords)

def extract_questions_from_response(response_text: str) -> list:
    pattern = r"\d+\.\s+(.*?)\n"
    questions = re.findall(pattern, response_text + "\n")  # ensure final newline
    return questions

# --- Initialize Session State ---
if "history" not in st.session_state:
    st.session_state["history"] = []

if "current_quiz" not in st.session_state:
    st.session_state["current_quiz"] = []
if "quiz_index" not in st.session_state:
    st.session_state["quiz_index"] = 0
if "quiz_answers" not in st.session_state:
    st.session_state["quiz_answers"] = []
if "awaiting_quiz_answer" not in st.session_state:
    st.session_state["awaiting_quiz_answer"] = False

# --- Question Form ---
with st.form("question_form"):
    st.markdown("### ❓ Ask a Study Question")
    user_input = st.text_area(
        "Enter your question or quiz answer below:",
        height=180,
        placeholder="E.g. Explain the difference between mitosis and meiosis."
    )
    submitted = st.form_submit_button("Submit")

# --- Handle Submission ---
if submitted and user_input:
    # --- If student is answering a quiz question ---
    if st.session_state.awaiting_quiz_answer:
        user_answer = user_input.strip()
        st.session_state.quiz_answers.append(user_answer)

        current_index = st.session_state.quiz_index
        total_questions = len(st.session_state.current_quiz)

        feedback = f"✅ Received your answer: **{user_answer}**\n\n"

        st.session_state.quiz_index += 1

        if st.session_state.quiz_index < total_questions:
            next_q = st.session_state.current_quiz[st.session_state.quiz_index]
            feedback += f"**Question {st.session_state.quiz_index + 1}:** {next_q}"
        else:
            st.session_state.awaiting_quiz_answer = False
            feedback += "\n🎉 **Quiz complete!**\n\nHere’s a summary:"
            for i, (q, a) in enumerate(zip(st.session_state.current_quiz, st.session_state.quiz_answers)):
                feedback += f"\n{i+1}. {q}\n**Your answer:** {a}\n"

        st.session_state["history"].append({"role": "user", "content": user_answer})
        st.session_state["history"].append({"role": "assistant", "content": feedback})

    # --- If user requests a quiz ---
    elif study_mode == "Quiz Mode" and is_quiz_request(user_input):
        quiz_prompt = (
            f"Create a short quiz of 3 to 5 questions for an A-Level student based on this request: '{user_input}'. "
            "Only include the questions, clearly numbered. Do not include answers unless asked."
        )
        messages = [
            {"role": "system", "content": build_system_prompt(level, study_mode)},
            {"role": "user", "content": quiz_prompt}
        ]

        try:
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=messages
            )
            quiz_text = response.choices[0].message.content.strip()
            quiz_questions = extract_questions_from_response(quiz_text)

            if quiz_questions:
                st.session_state["current_quiz"] = quiz_questions
                st.session_state["quiz_index"] = 0
                st.session_state["quiz_answers"] = []
                st.session_state["awaiting_quiz_answer"] = True

                first_q = quiz_questions[0]
                quiz_intro = f"🧪 Here's your quiz:\n\n**Question 1:** {first_q}"

                st.session_state["history"].append({"role": "user", "content": user_input})
                st.session_state["history"].append({"role": "assistant", "content": quiz_intro})
            else:
                st.session_state["history"].append({"role": "user", "content": user_input})
                st.session_state["history"].append({"role": "assistant", "content": "Sorry, I couldn't extract any questions."})

        except Exception as e:
            st.error(f"❌ API Error: {e}")

    # --- Regular Question (not quiz-related) ---
    else:
        messages = [
            {"role": "system", "content": build_system_prompt(level, study_mode)},
            {"role": "user", "content": user_input}
        ]

        try:
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=messages
            )
            reply = response.choices[0].message.content.strip()
            st.session_state["history"].append({"role": "user", "content": user_input})
            st.session_state["history"].append({"role": "assistant", "content": reply})
        except Exception as e:
            st.error(f"❌ API Error: {e}")

# --- Display Chat History ---
if st.session_state["history"]:
    st.markdown("### 🧠 Chat History")
    for msg in st.session_state["history"]:
        if msg["role"] in ["user", "assistant"]:
            with st.chat_message(msg["role"]):
                for line in msg["content"].split("\n"):
                    line = line.strip()
                    if re.match(r"^\$\$(.*?)\$\$", line):
                        expr = re.findall(r"\$\$(.*?)\$\$", line)[0]
                        st.latex(expr)
                    else:
                        st.markdown(line)

st.write("\n" * 2)




















