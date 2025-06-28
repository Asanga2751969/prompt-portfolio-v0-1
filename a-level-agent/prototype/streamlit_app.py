import streamlit as st
import openai
import re

# --- Page Configuration ---
st.set_page_config(page_title="A-Level Study Assistant", layout="wide")
st.title("📘 A-Level Study Assistant")
st.info("Ask any A-Level or AS-Level study question. Use the sidebar to choose mode.")

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
    system_prompt = build_system_prompt(level, study_mode)

    st.session_state["history"] = [  # Always reset system for consistent behavior
        {"role": "system", "content": system_prompt}
    ] + st.session_state["history"]

    st.session_state["history"].append({"role": "user", "content": user_input})

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=st.session_state["history"]
        )
        reply = response.choices[0].message.content.strip()
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
















