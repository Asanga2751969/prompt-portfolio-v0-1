#  📚 Prompt Portfolio v0.1

A curated collection of high-quality prompts designed for AI tools such as ChatGPT and Claude, focused on regulatory, technical, and business applications.

---

## 📁 Category: Technical / Regulatory Writing

### ✈️ Prompt 1 — FAA Memo Generation

> Generate a realistic FAA compliance memo related to the inspection and 400-hour replacement of a rotor blade retention bolt on a light utility helicopter.

### 🔍 Prompt 2 — NDT Inspection Elaboration

> Please elaborate on how a magnetic particle inspection would be performed for a rotor blade retention bolt under FAA maintenance guidelines. Include steps, tools, and what constitutes a pass or fail.

### 📊 Prompt 3 — Estimate Engineering Workload

> Estimate the number of stress analysis hours required for re-certification if a new material is used for the rotor blade retention bolt. Include a breakdown of tasks.

### ⚠️ Prompt 4 — Certification Risk Analysis

> What are the likely FAA certification risks if a bolt with higher tensile strength but reduced fatigue resistance is introduced in place of the current one?

### 🛠 Prompt 5 — Memo Rewrite with Urgency

> Rewrite the FAA memo using a more urgent tone and highlight the consequences of delayed bolt replacement, using plain language suitable for maintenance teams.

---

## 📁 Category: Business / Marketing / AI Use

### 🚁 Prompt 6 — AI Feature List for Startup

> Brainstorm a feature list for a hypothetical startup called BoltAI that helps helicopter maintenance teams track FAA compliance using GPT agents.

### 📈 Prompt 7 — AI-Powered Marketing Automation

> Please elaborate on the idea of automated marketing tools. How could it work for a time-strapped small business owner to automate campaigns across email, SMS, or social?

### ✍️ Prompt 8 — Prompt Enhancement

> Revise this prompt to be more specific and suited to Claude or ChatGPT: "Help me create a weekly rotor bolt inspection checklist that integrates FAA guidelines and field-level usability."

---

> 🗂️ Last updated: Day 4 of the 30-Day GPT Sprint
>
> Author: \[Asanga Costa]
# 🎓 A-Level Study Assistant

An AI-powered assistant to help Edexcel A-Level students learn faster and more effectively — with clear explanations, step-by-step solutions, visual aids, and smart quizzes.

---

## 💡 What It Does

This agent is designed to:

- Explain difficult subject concepts (Physics, Chemistry, etc.)
- Provide visuals like diagrams or simplified formulas
- Generate mini quizzes or revision questions
- Offer breakdowns of past paper questions
- Guide students using the Edexcel syllabus

---

## 🔧 Planned Features

- Interactive Q&A (powered by GPT)
- Support for visual explanations
- Study planner integration
- Trend analysis of past papers
- Custom mock paper generator

---

## 🚀 Current Status

- ✅ Idea finalized
- ✅ Agent spec completed
- ✅ GitHub repo set up
- ⏳ First prototype to be built in Day 10

---

## 🛠️ Tools (Exploration Phase)

- Python + OpenAI API  
- Gradio or Streamlit (for UI)  
- PDF parser (for past paper ingestion)  
- Basic data analysis (mock paper logic)

---

## 📂 Files

- `agent-spec.md`: Full description of agent goals, features, and system prompt  
- `README.md`: This file — overview of the project

---

## 👨‍🎓 Who It’s For

Students, tutors, and parents preparing for the Edexcel A-Level or IGCSE curriculum — with a focus on creating a smoother, smarter study experience using AI.

---
### 🧠 A-Level Study Assistant – Agent Workflow (Markdown Flowchart)

```markdown
User Input
   ↓
[Topic or Question (e.g., "Explain Kirchhoff's Laws")]
   ↓
[System Prompt Guides AI Tone + Depth]
   ↓
[LLM Processes Request]
   ↓
┌───────────────────────────────────────────────├───────────────────────────────────────────────┐
│ Optional Tools:            │                            │
│ • Curriculum Filter        │                            │
│ • Past Paper Analyzer      │  (used later in roadmap)   │
└───────────────────────────────────────────────┘
   ↓
[Structured Explanation Returned]
   ↓
┌───────────────────────────────────────────────────────┐
│ Optional Add-ons (future):                            │
│ • Visual aids (diagrams, graphs)                      │
│ • Quiz or MCQ follow-up                               │
│ • Memory Tracker for weak topics                      │
└───────────────────────────────────────────────┘
   ↓
Final Output to Student


