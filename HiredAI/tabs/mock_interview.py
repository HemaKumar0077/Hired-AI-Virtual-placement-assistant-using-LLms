# tabs/mock_interview.py
import streamlit as st
from ai_logic import get_ollama_response, speech_to_text, text_to_speech

def render_mock_interview(inputs):
    st.subheader("🤖 Mock Interview")

    job_role = inputs["job_role"]
    conversation_history = []

    if st.button("Start Interview"):
        if job_role:
            ai_question = get_ollama_response(job_role, "", "Act as interviewer, ask interview questions.")
            st.write("🗣 Interviewer:", ai_question)
            text_to_speech(ai_question)

            user_response = speech_to_text()
            st.write("🎙 You said:", user_response)

            if user_response.lower() not in ["exit", "quit", "stop"]:
                ai_feedback = get_ollama_response(job_role, user_response, "Evaluate response and provide feedback.")
                st.write("💡 Feedback:", ai_feedback)
                text_to_speech(ai_feedback)
        else:
            st.warning("⚠ Please enter the Job Role.")