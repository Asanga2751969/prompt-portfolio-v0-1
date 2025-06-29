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

# --- Mini Quiz Detection ---
def is_quiz_request(user_input: str) -> bool:
    quiz_keywords = ["quiz me", "test me", "give me a quiz", "mini quiz", "quick quiz"]
    return any(keyword in user_input.lower() for keyword in quiz_keywords)

# --- Initialize Chat History ---
if "history" not in st.session_state:
    st.session_state["history"] = []

# --- Question Form ---
with st.form("question_form"):
    st.markdown("### ❓ Ask a Study Question")
    user_input = st.text_area(
        "Enter your question below:",
        height=180,
        placeholder="E.g. Explain the difference between mitosis and meiosis."
    )
    submitted = st.form_submit_button("Submit")

# --- Handle Submission ---
if submitted and user_input:
    # Build prompt based on mode and request type
    if study_mode == "Quiz Mode" and is_quiz_request(user_input):
        quiz_topic = user_input
        quiz_prompt = (
            f"Create a short quiz of 3 to 5 questions for an A-Level student based on this request: '{quiz_topic}'. "
            "Include a mix of formats if appropriate (e.g., multiple choice, definition, short answer). "
            "Clearly number each question. Do not include answers unless explicitly asked."
        )
        messages = [
            {"role": "system", "content": build_system_prompt(level, study_mode)},
            {"role": "user", "content": quiz_prompt}
        ]
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


















