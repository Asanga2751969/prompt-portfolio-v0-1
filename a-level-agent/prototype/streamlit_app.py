import streamlit as st
import openai
import re

# --- Page Configuration ---
st.set_page_config(page_title="A-Level Study Assistant", layout="wide")

# --- Title and Info Banner ---
st.title("📘 A-Level Study Assistant")
st.info("☝️ Use the sidebar to choose subject, level, and study mode. Tap 'Reset Chat' to start over.")

# --- Sidebar ---
st.sidebar.markdown("### 🛠️ Settings")
subject = st.sidebar.selectbox("Subject", ["Physics", "Biology", "Mathematics", "Economics"])
level = st.sidebar.selectbox("Exam Level", ["AS Level", "A Level"])

study_mode = st.sidebar.selectbox("Study Mode", ["Explain Mode", "Quiz Mode", "Past Paper Style"])

st.sidebar.markdown("---")
if st.sidebar.button("🔄 Reset Chat"):
    st.session_state["history"] = []

# --- System Prompt Setup ---
base_prompt = (
    f"You are an expert A-Level tutor helping a student prepare for the {level} exam in {subject}. "
    "Only answer questions relevant to this subject. If the question seems unrelated, suggest switching subjects."
)

mode_prompts = {
    "Explain Mode": "Explain the topic clearly using simple language and examples.",
    "Quiz Mode": "Ask a follow-up question to test understanding. Keep it short and focused.",
    "Past Paper Style": "Respond in the format of a model exam answer using formal, subject-specific language."
}

subject_tone = {
    "Physics": "Use real-world analogies and explain formulas clearly with units.",
    "Biology": "Provide concise definitions and labeled biological processes.",
    "Mathematics": "Use step-by-step structure and clear examples.",
    "Economics": "Clarify terms with relatable examples like a coffee shop scenario."
}

system_prompt = (
    f"{base_prompt} {mode_prompts[study_mode]} {subject_tone.get(subject, '')} "
    "Use labels like 'Definition:', 'Example:', or 'Exam Tip:'. "
    "Always format mathematical content using LaTeX. Wrap full equations with double dollar signs (e.g., $$E = mc^2$$)."
)

# --- Session State Initialization ---
if "history" not in st.session_state:
    st.session_state["history"] = [{"role": "system", "content": system_prompt}]

# --- Question Form ---
with st.form("question_form"):
    st.markdown("### ❓ Ask a Study Question")
    prompt = st.text_area("Enter your question here:", height=150)
    submitted = st.form_submit_button("Submit")

# --- Handle Submission ---
if submitted and prompt:
    st.session_state["history"].append({
        "role": "system",
        "content": f"Reminder: Stick to {subject}. Suggest switching if question is unrelated."
    })

    enhanced_prompt = prompt.strip()
    if subject in ["Mathematics", "Physics"]:
        enhanced_prompt += " Please format any math using LaTeX and wrap full equations in $$...$$."

    st.session_state["history"].append({"role": "user", "content": enhanced_prompt})

    try:
        client = openai.OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=st.session_state["history"]
        )
        reply = response.choices[0].message.content
        st.session_state["history"].append({"role": "assistant", "content": reply})
    
    except Exception as e:
        st.error(f"❌ API Error: {e}")

# --- Display Assistant Response ---
if st.session_state["history"]:
    st.markdown("### 🧠 Chat History")
    for msg in st.session_state["history"]:
        if msg["role"] == "user":
            st.markdown(f"**👤 You:** {msg['content']}")
        elif msg["role"] == "assistant":
            st.markdown("**🤖 Tutor:**")
            for line in msg["content"].split("\n"):
                line = line.strip()
                if re.match(r"^\$\$(.*?)\$\$", line):
                    expr = re.findall(r"\$\$(.*?)\$\$", line)[0]
                    st.latex(expr)
                else:
                    st.markdown(line)

# --- Footer Padding ---
st.write("\n" * 2)













