# main.py
import streamlit as st
from utils.common_inputs import get_common_inputs

from tabs.resume_analysis import render_resume_analysis
from tabs.mock_interview import render_mock_interview
from tabs.question_generator import render_question_generator
from tabs.llm_project_analyzer import render_llm_project_analyzer

st.set_page_config(page_title="AI Interview & Project Suite", layout="wide")
st.title("🚀 AI-Powered Interview & Project Analysis Suite")

inputs = get_common_inputs()

tab1, tab2, tab3, tab4 = st.tabs([
    "📄 Resume Analysis", 
    "🤖 Mock Interview", 
    "📌 Question Generator", 
    "📝 LLM Project Analyzer"
])

with tab1:
    render_resume_analysis(inputs)

with tab2:
    render_mock_interview(inputs)

with tab3:
    render_question_generator(inputs)

with tab4:
    render_llm_project_analyzer(inputs)