# AI PM Copilot

AI PM Copilot is a web-based dashboard designed to automate core product management workflows. It combines Python logic for mathematical scoring with Gemini AI for document drafting and feedback analysis.

## Features

### 1. PRD Generator Studio
- Instant Documentation: Converts feature briefs into structured Product Requirements Documents.
- Preset Templates: Quick-launch options for common patterns such as Google SSO or Dark Mode.
- Structured Output: Generates sections covering Overview, Problem Statement, Goals, User Stories, and Technical Requirements.

### 2. RICE Prioritization Engine
- Math Core: Calculates RICE priority scores directly in Python using the formula (Reach x Impact x Confidence) / Effort.
- Priority Matrix: Categorizes features into P0, P1, or P2 priority levels.
- Strategic Analysis: Uses Gemini AI to explain risk versus value trade-offs and suggest execution improvements.

### 3. Customer Feedback Hub
- Sentiment Analysis: Categorizes customer reviews into Positive, Neutral, or Negative sentiment.
- Theme Extraction: Summarizes review trends into key feature requests and actionable PM guidance.

## Tech Stack
- Frontend: Streamlit with custom CSS styling
- Backend: Python (ai_engine.py)
- AI Model: Gemini 3.5 Flash Lite API
- Libraries: google-genai, python-dotenv, streamlit

## Directory Structure

ai-pm-copilot/
├── .streamlit/
├── .gitignore
├── ai_engine.py
├── app.py
├── requirements.txt
└── README.md


## Team Members
- Backend Engineering: Ritvik Naik, Adithya MK
- Frontend Development: Vaibhav, Pramath
- Project Overview and Presentation: Rehan, Sumanth

---

## 🏗️ Folder Structure
