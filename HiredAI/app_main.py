import streamlit as st
import requests
from bs4 import BeautifulSoup
import os
from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from typing import Optional, List

# Importing custom modules
from github_parser.validation import get_user_repositories
from langchain_community.document_loaders import PyPDFLoader
from llm.llm_project import llm_project_details, extract_project_names, validate_projects, project_scorer, final_scorer
from llm.llm import load_llm, load_llm_think
from parser_scorer.parser import read_pdf
from github_parser.project_details import scrape_readme

from learn import get_company_description, generate_interview_questions, generate_solutions
from ai_logic import get_ollama_response, extract_text_from_pdf, interview_chatbot, speech_to_text, text_to_speech

# Streamlit App Configuration
st.set_page_config(page_title="AI Interview & Project Suite", layout="wide")
st.title("🚀 AI-Powered Interview & Project Analysis Suite")
def generate_questions_and_answers(prj, readme_content, llm):
    """
    Generate interview-style questions and answers for a given project.
    """
    prompt = f"""
    Generate 5 interview-style questions about the project '{prj}' based on the following README content:
    {readme_content}
    """
    
    questions_response = llm.invoke(prompt)  # Get AIMessage
    questions_text = questions_response.content.strip()  # Extract text content
    
    qa_pairs = []
    for question in questions_text.split("\n"):
        if question.strip():
            answer_prompt = f"""
            Provide a concise answer for the following question about the project '{prj}':
            {question}
            """
            answer_response = llm.invoke(answer_prompt)
            answer_text = answer_response.content.strip()
            qa_pairs.append((question, answer_text))

    return qa_pairs

# Tabs for different functionalities
tab1, tab2, tab3, tab4 = st.tabs([
    "📄 Resume Analysis", 
    "🤖 Mock Interview", 
    "📌 Question Generator", 
    "📝 LLM Project Analyzer"
])

# ==============================
# 📄 Resume Analysis Tab
# ==============================
with tab1:
    st.subheader("📄 Resume Analysis")
    input_text = st.text_area("Job Description:")
    uploaded_file = st.file_uploader("Upload your resume (PDF)...", type=["pdf"])

    if uploaded_file:
        st.write("✅ PDF Uploaded Successfully")
    
    analyze_resume = st.button("Tell Me About the Resume")
    check_match = st.button("Percentage Match")

    prompts = {
        "evaluation": """
        You are an experienced HR Manager. Evaluate the resume based on the job description, highlighting strengths and weaknesses.
        """,
        "percentage_match": """
        You are an ATS scanner. Evaluate the resume vs. the job description and provide:
        1️⃣ Percentage match
        2️⃣ Missing keywords
        3️⃣ Final thoughts
        """
    }
    
    if analyze_resume and uploaded_file:
        resume_text = extract_text_from_pdf(uploaded_file)
        response = get_ollama_response(input_text, resume_text, prompts["evaluation"])
        st.subheader("📌 Response:")
        st.write(response)
    elif check_match and uploaded_file:
        resume_text = extract_text_from_pdf(uploaded_file)
        response = get_ollama_response(input_text, resume_text, prompts["percentage_match"])
        st.subheader("📌 ATS Percentage Match:")
        st.write(response)
    elif analyze_resume or check_match:
        st.warning("⚠ Please upload a resume.")

# ==============================
# 🤖 Mock Interview Tab
# ==============================
with tab2:
    st.subheader("🤖 Mock Interview")
    job_type = st.text_input("Enter Job Role for the Interview:")
    conversation_history = []

    if st.button("Start Interview"):
        if job_type:
            while True:
                ai_question = get_ollama_response(job_type, "", "Act as an interviewer. Ask questions one by one and provide feedback.")
                st.write("🗣️ Interviewer:", ai_question)
                text_to_speech(ai_question)

                user_response = speech_to_text()
                st.write("🎙️ You said:", user_response)

                if user_response.lower() in ["exit", "quit", "stop"]:
                    st.write("🛑 Interview Ended.")
                    break

                conversation_history.append({"role": "user", "content": user_response})

                ai_feedback = get_ollama_response(job_type, user_response, "Evaluate response, provide feedback and a score.")  
                st.write("💡 Feedback:", ai_feedback)
                text_to_speech(ai_feedback)

                conversation_history.append({"role": "system", "content": ai_feedback})


# ==============================
# 📌 Question Generator Tab
# ==============================
with tab3:
    st.subheader("📌 Interview Question Generator")
    
    company = st.text_input("Enter Company Name", placeholder="e.g., Google")
    role = st.text_input("Enter Job Role", placeholder="e.g., Software Engineer")
    category = st.selectbox("Select Category", ["DSA", "SQL", "System Design", "Behavioral", "AI/ML", "Other"])

    if company:
        with st.spinner(f"Fetching description for {company}..."):
            company_description = get_company_description(company)
        
        st.subheader(f"About {company}")
        st.write(company_description)

    if st.button("Generate Questions"):
        if company and role and category:
            with st.spinner("Generating interview questions..."):
                questions = generate_interview_questions(company, role, category)
            
            if questions:
                st.success(f"Successfully generated {len(questions)} {category} questions!")

                # Generate solutions
                with st.spinner("Generating solutions..."):
                    solutions = generate_solutions(category, questions)

                # Display results
                st.subheader(f"{category} Interview Questions & Answers")
                for solution in solutions:
                    st.markdown(solution)
            else:
                st.error("No questions generated. Try different inputs!")
        else:
            st.warning("Please enter a company, role, and category!")

# ==============================
# 📝 LLM Project Analyzer Tab
# ==============================
with tab4:
    st.subheader("📝 LLM Project Analyzer")
    uploaded_resume = st.file_uploader("Upload your resume (PDF)", type=["pdf"])
    github_name_input = st.text_input("Enter your GitHub username:")

    if st.button("Run Analysis"):
        if not uploaded_resume or not github_name_input:
            st.error("Please upload a resume and enter a valid GitHub username.")
        else:
            temp_file_path = "other/temp_resume.pdf"
            with open(temp_file_path, "wb") as f:
                f.write(uploaded_resume.read())

            file_path = temp_file_path
            github_name = github_name_input

            st.write("Extracting PDF, loading LLM, and processing project details...")

            documents = read_pdf(file_path)
            llm = load_llm()
            llm_think = load_llm_think()

            project_details = llm_project_details(llm, documents)
            structured_projects = extract_project_names(project_details, llm)
            repository_list = get_user_repositories(github_name)
            valid_projects = validate_projects(structured_projects, repository_list, llm)

            st.subheader("Project Details")
            st.write(project_details)

            st.subheader("Valid Projects")
            st.write(valid_projects)

            for prj in valid_projects.valid_projects:
                if prj != 'N/A':
                    st.write(f"### 🔹 Analyzing Project: {prj}")
                    
                    # Scrape README content
                    branch, readme_content = scrape_readme(github_name, prj)
                    
                    # Perform deep analysis
                    deep_results = project_scorer(prj, readme_content, project_details, llm_think)

                    with st.expander(f"🔍 Deep Analysis for {prj}"):
                        st.write(deep_results)

                    result_projects = final_scorer(deep_results, llm)
                    st.write("✅ **Final Score:**", result_projects)
                    st.markdown("---")

                    # Generate and display interview questions & answers
                    qa_pairs = generate_questions_and_answers(prj, readme_content, llm)

                    with st.expander(f"🎤 Interview Questions for {prj}"):
                        for q, a in qa_pairs:
                            st.write(f"**Q:** {q}")
                            st.write(f"**A:** {a}")
                            st.markdown("---")