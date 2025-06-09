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

# Dynamic system prompt
system_prompt = (
    f"You are an expert A-Level tutor helping a student prepare for the {level} exam in {subject}. "
    "Give concise explanations with examples where appropriate. Prioritize what is needed to score high marks in exams. "
    "Make concepts beginner-friendly but academically accurate."
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
    # Add user message
    st.session_state["history"].append({"role": "user", "content": prompt})

    try:
        client = openai.OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=st.session_state["history"]
        )
        assistant_reply = response.choices[0].message.content

        # Add assistant message
        st.session_state["history"].append({"role": "assistant", "content": assistant_reply})

        # ✅ Display the assistant's response (LaTeX-friendly)
        if assistant_reply:
            st.markdown("### 📘 AI Tutor Response")

            import re
            for line in assistant_reply.split("\n"):
                line = line.strip()
                if not line:
                    continue

                # Detect block-level LaTeX and render it
                if line.startswith("[") and line.endswith("]"):
                    try:
                        st.latex(line[1:-1].replace("**", "^").replace("sqrt", "\\sqrt"))
                        continue
                    except:
                        pass

                # Detect inline LaTeX patterns and wrap in $...$
                inline_math = re.findall(r"\\frac\{.*?\}|\\sqrt\{.*?\}|[a-zA-Z0-9\^\*/=\+\-]+", line)
                if any("\\frac" in part or "\\sqrt" in part or "^" in part for part in inline_math):
                    # Wrap entire line if it seems mostly math
                    if all(" ".join(inline_math).strip() in line for part in inline_math):
                        try:
                            st.latex(line.replace("**", "^").replace("sqrt", "\\sqrt"))
                            continue
                        except:
                            pass

                # Else fallback to markdown
                st.markdown(line)

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
