# utils/common_inputs.py
import streamlit as st

def get_common_inputs():
    st.sidebar.header("📥 Common Inputs")
    
    uploaded_resume = st.sidebar.file_uploader("📄 Upload your Resume (PDF)", type=["pdf"])
    job_description = st.sidebar.text_area("📃 Job Description")
    job_role = st.sidebar.text_input("💼 Job Role")
    company_name = st.sidebar.text_input("🏢 Company Name")
    github_username = st.sidebar.text_input("🐙 GitHub Username")

    return {
        "uploaded_resume": uploaded_resume,
        "job_description": job_description,
        "job_role": job_role,
        "company_name": company_name,
        "github_username": github_username
    }