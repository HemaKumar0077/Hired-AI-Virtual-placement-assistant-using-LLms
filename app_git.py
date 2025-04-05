import streamlit as st
import requests
from bs4 import BeautifulSoup
import os
from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from typing import Optional, List

# Importing your custom modules
from github_parser.validation import get_user_repositories
from langchain_community.document_loaders import PyPDFLoader
from llm.llm_project import llm_project_details, extract_project_names, validate_projects, project_scorer, final_scorer
from llm.llm import load_llm, load_llm_think
from parser_scorer.parser import read_pdf
from github_parser.project_details import scrape_readme

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

def main():
    st.title("LLM Project Analyzer")
    st.write("Upload your resume (PDF) and enter your GitHub username to start the analysis.")

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

            with st.expander("Show Project Details"):
                st.write(project_details)

            with st.expander("Show Valid Projects"):
                st.write(valid_projects)

            st.write("Processing valid projects:")

            for prj in valid_projects.valid_projects:
                if prj != 'N/A':
                    st.write("**Current project:**", prj)
                    branch, readme_content = scrape_readme(github_name, prj)
                    deep_results = project_scorer(prj, readme_content, project_details, llm_think)

                    with st.expander(f"Deep/detailed Details for {prj}"):
                        st.write(deep_results)

                    result_projects = final_scorer(deep_results, llm)
                    st.write("**Result:**", result_projects)
                    st.markdown("---")

                    # Generate and display questions & answers
                    qa_pairs = generate_questions_and_answers(prj, readme_content, llm)

                    with st.expander(f"Interview Questions for {prj}"):
                        for q, a in qa_pairs:
                            st.write(f"**Q:** {q}")
                            st.write(f"**A:** {a}")
                            st.markdown("---")

if __name__ == '__main__':
    main()
