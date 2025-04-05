# tabs/resume_analysis.py
import streamlit as st
from ai_logic import get_ollama_response, extract_text_from_pdf

def render_resume_analysis(inputs):
    st.subheader("📄 Resume Analysis")

    uploaded_resume = inputs["uploaded_resume"]
    job_description = inputs["job_description"]

    analyze_resume = st.button("Tell Me About the Resume")
    check_match = st.button("Percentage Match")

    prompts = {
        "evaluation": "You are an experienced HR Manager. Evaluate the resume based on the job description, highlighting strengths and weaknesses.",
        "percentage_match": "You are an ATS scanner. Evaluate the resume vs. the job description and provide percentage match, missing keywords, and final thoughts."
    }

    if uploaded_resume:
        if analyze_resume:
            resume_text = extract_text_from_pdf(uploaded_resume)
            response = get_ollama_response(job_description, resume_text, prompts["evaluation"])
            st.subheader("📌 Response:")
            st.write(response)

        if check_match:
            resume_text = extract_text_from_pdf(uploaded_resume)
            response = get_ollama_response(job_description, resume_text, prompts["percentage_match"])
            st.subheader("📌 ATS Percentage Match:")
            st.write(response)
    else:
        if analyze_resume or check_match:
            st.warning("⚠ Please upload your resume.")