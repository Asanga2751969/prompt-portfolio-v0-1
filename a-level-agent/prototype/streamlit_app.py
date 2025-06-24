import streamlit as st
import openai
import os

# Page config
st.set_page_config(page_title="A-Level Study Assistant", layout="centered")

st.info("☝️ Tap the menu icon on the top left to select subject, exam level, or to start a new chat.")
st.title("📘 A-Level Study Assistant")

# Sidebar settings
st.sidebar.markdown("### 🛠️ Settings Panel")
subject = st.sidebar.selectbox("Select subject", ["Physics", "Biology", "Mathematics", "Economics"])
level = st.sidebar.selectbox("Study level", ["AS Level", "A Level"])
# 🧭 Mobile user tip


# Reset chat button
if st.sidebar.button("🔄 Reset Chat"):
    st.session_state["history"] = []


# --- Study Mode Selection ---
study_mode = st.sidebar.selectbox("Study Mode", ["Explain Mode", "Quiz Mode", "Past Paper Style"])

# --- Base prompt ---
base_prompt = (
    f"You are an expert A-Level tutor helping a student prepare for the {level} exam in {subject}. "
    "Only answer questions relevant to this subject. "
    "If the question seems unrelated to the selected subject, politely ask the student to switch to the correct subject in the settings panel. "
)

# --- Study mode behavior ---
mode_prompts = {
    "Explain Mode": "Explain the topic clearly and concisely using simple language and examples. Emphasize exam-relevant concepts and make it beginner-friendly.",
    "Quiz Mode": "Ask the student a follow-up question to test their understanding. Keep it short and focused on one concept at a time.",
    "Past Paper Style": "Answer in the format of a model exam response. Be concise, formal, and use subject-specific terminology."
}

# --- Subject-specific tone ---
subject_tone = {
    "Physics": "Use real-world analogies, explain formulas clearly, and mention units of measurement.",
    "Biology": "Focus on concise definitions, labeled processes, and visual analogies (e.g., 'cell = factory').",
    "Mathematics": "Structure explanations step-by-step, with examples. Avoid overly technical language.",
    "Economics": "Clarify key terms, use relatable scenarios (e.g., coffee shop for supply/demand), and highlight exam-style phrasing."
}

# --- Final system prompt ---
system_prompt = (
    f"{base_prompt} "
    f"{mode_prompts[study_mode]} "
    f"{subject_tone.get(subject, '')} "
    "When helpful, organize your response using labels like 'Definition:', 'Example:', 'Exam Tip:', 'Note:', or 'Key Point:'."
)




# Initialize memory
if "history" not in st.session_state:
    st.session_state["history"] = [{"role": "system", "content": system_prompt}]


# --- User Input via Form ---
with st.form("question_form"):
    prompt = st.text_input("Ask a study question:")
    submitted = st.form_submit_button("Submit")

# --- Handle the prompt submission ---
if submitted and prompt:
    # ⏪ Reminder to keep assistant focused on selected subject
    subject_reminder = {
        "role": "system",
        "content": f"Reminder: The selected subject is {subject}. Only answer questions relevant to {subject}. "
                   f"If the question seems unrelated, inform the user politely and suggest switching subjects."
    }
    st.session_state["history"].append(subject_reminder)

    # Add the user's actual question
    st.session_state["history"].append({"role": "user", "content": prompt})

    try:
        client = openai.OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=st.session_state["history"]
        )
        assistant_reply = response.choices[0].message.content

        # Store assistant reply
        st.session_state["history"].append({"role": "assistant", "content": assistant_reply})

        # ✅ Display the assistant's response
        if assistant_reply:
            
            st.markdown("### 📘 AI Tutor Response")
            # Escape risky characters that may confuse JS regex engine
            safe_reply = assistant_reply.replace("\\", "").replace("{", "").replace("}", "").replace("**", "").replace("$", "")
            # Basic structure fallback – no emojis or markdown
            for line in safe_reply.split("\n"):
            st.write(line.strip())
           

    except Exception as e:
        st.error(f"❌ API Error: {e}")









# --- Display chat history ---
if st.session_state["history"]:
    st.markdown("### 🧠 Chat History")
    for msg in st.session_state["history"]:
        if msg["role"] == "user":
            st.markdown(f"**👤 You:** {msg['content']}")
        elif msg["role"] == "assistant":
            st.markdown(f"**🤖 Tutor:** {msg['content']}")
