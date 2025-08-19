import streamlit as st
import re
from difflib import SequenceMatcher
from openai import OpenAI
# === Pro Access Helpers ===

def user_is_pro():
    """Returns True if the user has Pro access (dev or real in future)."""
    return st.session_state.get("is_pro", False)

def pro_lock(message: str = "This feature is available in the Pro version."):
    """Standard locked message shown to free users."""
    st.warning(f"🔒 {message}")

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
    st.session_state["quiz_score"] = 0
    st.session_state["awaiting_quiz_answer"] = False
# --- Upgrade to Pro button placeholder ---
st.sidebar.markdown("---")
st.sidebar.markdown("### 🚀 Unlock More Features")

# Dev-only toggle to simulate Pro access
st.sidebar.checkbox("✅ I’m Pro (dev toggle)", key="is_pro")

# Upgrade button with placeholder info
if st.sidebar.button("🔓 Upgrade to Pro (Coming Soon)"):
    st.sidebar.info("Pro features like **Quiz History**, **Detailed Feedback**, and **Past Papers** coming soon!")


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
        "If the student requests a quiz, generate 3–5 questions on the topic, each with the correct answer."
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

def extract_questions_and_answers(response_text: str) -> list:
    pattern = r"(\d+)\.\s+(.*?)\nAnswer:\s+(.*?)(?=\n\d+\.|\Z)"
    matches = re.findall(pattern, response_text.strip(), re.DOTALL)
    return [{"question": q.strip(), "answer": a.strip()} for _, q, a in matches]

def is_answer_correct(user_answer: str, correct_answer: str, threshold=0.6) -> bool:
    user = user_answer.strip().lower()
    correct = correct_answer.strip().lower()

    # Block known "non-answers"
    if user in ["", "idk", "i don't know", "dont know"]:
        return False

    # Check if numbers match
    user_numbers = re.findall(r"[-+]?\d*\.?\d+", user)
    correct_numbers = re.findall(r"[-+]?\d*\.?\d+", correct)

    if user_numbers and correct_numbers:
        try:
            if float(user_numbers[0]) == float(correct_numbers[0]):
                return True
        except:
            pass  # Fallback to fuzzy match

    # Fallback: fuzzy token comparison
    similarity = SequenceMatcher(None, user, correct).ratio()
    return similarity >= threshold

# --- Session State Initialization ---
if "history" not in st.session_state:
    st.session_state["history"] = []

if "current_quiz" not in st.session_state:
    st.session_state["current_quiz"] = []
if "quiz_index" not in st.session_state:
    st.session_state["quiz_index"] = 0
if "quiz_answers" not in st.session_state:
    st.session_state["quiz_answers"] = []
if "quiz_score" not in st.session_state:
    st.session_state["quiz_score"] = 0
if "awaiting_quiz_answer" not in st.session_state:
    st.session_state["awaiting_quiz_answer"] = False

# --- Question Form ---
with st.form("question_form"):
    st.markdown("### ❓ Ask a Study Question or Answer a Quiz")
    user_input = st.text_area(
        "Enter your question or quiz answer below:",
        height=180,
        placeholder="E.g. Explain the difference between mitosis and meiosis."
    )
    submitted = st.form_submit_button("Submit")

# --- Handle Submission ---
if submitted and user_input:
    if st.session_state.awaiting_quiz_answer:
        # Quiz answer flow
        user_answer = user_input.strip()
        quiz_item = st.session_state.current_quiz[st.session_state.quiz_index]
        correct_answer = quiz_item["answer"]

        st.session_state.quiz_answers.append(user_answer)

        if is_answer_correct(user_answer, correct_answer):
            feedback = f"✅ Correct!\n**Model answer:** {correct_answer}\n\n"
            st.session_state.quiz_score += 1
        else:
            feedback = f"❌ Not quite.\n**Model answer:** {correct_answer}\n\n"

        st.session_state.quiz_index += 1

        if st.session_state.quiz_index < len(st.session_state.current_quiz):
            next_q = st.session_state.current_quiz[st.session_state.quiz_index]["question"]
            feedback += f"**Question {st.session_state.quiz_index + 1}:** {next_q}"
        else:
            total = len(st.session_state.current_quiz)
            score = st.session_state.quiz_score
            st.session_state.awaiting_quiz_answer = False

            feedback += f"\n🎉 **Quiz complete!**\n\n**Score: {score}/{total}**\n\nSummary:"
            for i, qa in enumerate(st.session_state.current_quiz):
                q = qa["question"]
                a = st.session_state.quiz_answers[i]
                correct = qa['answer']
                is_correct = is_answer_correct(a, correct)
                icon = "✅" if is_correct else "❌"
                feedback += f"\n{icon} **Q{i+1}.** {q}\nYour answer: {a}\nCorrect answer: {correct}\n"

        st.session_state["history"].append({"role": "user", "content": user_answer})
        st.session_state["history"].append({"role": "assistant", "content": feedback})

    elif study_mode == "Quiz Mode" and is_quiz_request(user_input):
        # New quiz requested
        quiz_prompt = (
            f"Create a quiz with exactly 3 questions for an A-Level student based on this request: '{user_input}'. "
            "For each question, include the correct answer using this format:\n\n"
            "1. Question text\nAnswer: correct answer\n\n2. ..."
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
            quiz_items = extract_questions_and_answers(quiz_text)

            if quiz_items:
                st.session_state["current_quiz"] = quiz_items
                st.session_state["quiz_index"] = 0
                st.session_state["quiz_answers"] = []
                st.session_state["quiz_score"] = 0
                st.session_state["awaiting_quiz_answer"] = True

                first_q = quiz_items[0]["question"]
                quiz_intro = f"🧪 Here's your quiz:\n\n**Question 1:** {first_q}"

                st.session_state["history"].append({"role": "user", "content": user_input})
                st.session_state["history"].append({"role": "assistant", "content": quiz_intro})
            else:
                st.session_state["history"].append({"role": "user", "content": user_input})
                st.session_state["history"].append({"role": "assistant", "content": "⚠️ Couldn't extract quiz questions."})

        except Exception as e:
            st.error(f"❌ API Error: {e}")

    else:
        # General study question
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























