import streamlit as st
from github_parser.validation import get_user_repositories
from github_parser.project_details import scrape_readme
from parser_scorer.parser import read_pdf
from llm.llm_project import (
    llm_project_details,
    extract_project_names,
    validate_projects,
    project_scorer,
    final_scorer
)
from llm.llm import load_llm, load_llm_think

def generate_questions_and_answers(prj, readme_content, llm):
    """
    Generate interview-style questions and answers for a given project.
    """
    prompt = f"""
    Generate 5 interview-style questions about the project '{prj}' based on the following README content:
    {readme_content}
    """
    questions_response = llm.invoke(prompt)
    questions_text = questions_response.content.strip()
    
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

def render_llm_project_analyzer(inputs):
    st.subheader("📝 LLM Project Analyzer")

    uploaded_resume = inputs["uploaded_resume"]
    github_name = inputs["github_username"]

    if st.button("🚀 Run Analysis"):
        if not uploaded_resume or not github_name:
            st.error("⚠️ Please upload your resume and provide your GitHub username.")
            return

        with st.spinner("🔄 Analyzing your resume and GitHub projects..."):
            temp_file_path = "other/temp_resume.pdf"
            with open(temp_file_path, "wb") as f:
                f.write(uploaded_resume.read())

            documents = read_pdf(temp_file_path)
            llm = load_llm()
            llm_think = load_llm_think()

            project_details = llm_project_details(llm, documents)
            structured_projects = extract_project_names(project_details, llm)
            repository_list = get_user_repositories(github_name)
            valid_projects = validate_projects(structured_projects, repository_list, llm)

            st.subheader("📚 Project Details")
            st.write(project_details)

            st.subheader("✅ Valid Projects Found")
            st.write(valid_projects)

            for prj in valid_projects.valid_projects:
                if prj != 'N/A':
                    st.write(f"### 🔹 Analyzing Project: {prj}")

                    branch, readme_content = scrape_readme(github_name, prj)

                    if not readme_content:
                        st.warning(f"No README found for '{prj}'. Skipping...")
                        continue

                    deep_results = project_scorer(prj, readme_content, project_details, llm_think)

                    with st.expander(f"🔍 Deep Analysis for {prj}"):
                        st.write(deep_results)

                    result_projects = final_scorer(deep_results, llm)
                    st.write("📊 **Final Score:**", result_projects)

                    qa_pairs = generate_questions_and_answers(prj, readme_content, llm)

                    with st.expander(f"🎤 Interview Questions & Answers for {prj}"):
                        for q, a in qa_pairs:
                            st.markdown(f"**Q:** {q}")
                            st.markdown(f"**A:** {a}")
                            st.markdown("---")