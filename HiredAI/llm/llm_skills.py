import os
from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from pydantic import BaseModel, Field
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from typing import Optional,List
import time
# GROQ_API_KEY = "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"
load_dotenv()
groq_api_key = os.getenv("GROQ_API_KEY")

llm = init_chat_model("llama3-8b-8192", model_provider="groq")

resume_details = '''
Document(metadata={'producer': 'pdfTeX-1.40.25', 'creator': 'LaTeX with hyperref', 'creationdate': '2024-10-03T15:39:50+00:00', 'author': '', 'keywords': '', 'moddate': '2024-10-03T15:39:50+00:00', 'ptex.fullbanner': 'This is pdfTeX, Version 3.141592653-2.6-1.40.25 (TeX Live 2023) kpathsea version 6.3.5', 'subject': '', 'title': 'Aditeya Baral Resume', 'trapped': '/False', 'source': 'KS_Abhiram_CSE.pdf', 'total_pages': 2, 'page': 0, 'page_label': '1'}, page_content='K S Abhiram\n+91-8660946912 | abhiramkaranth700@gmail.com | GitHub |\nEducation\nPES University Bangalore, India\nB.Tech in Computer Science CGPA - 8.12 Dec 2021 – 2025\n• 1x Professor MRD Scholarship Awardee for being in the top 20% of the batch\n• 3x DAC Scholarship Awardee for maintaining cgpa over 7.75\nKarkala Jnanasudha PU College Ganit Nagar Udupi, India\nState Board (PCMS) - 100% June 2019 – October 2021\n• KCET Rank 969\n• JEE Main 96.66 percentile\nJagadheeshwara English Medium High School Kalasa Chikkamagalur, India\nState Board - 99.36% June 2017 – May 2019\nProjects\nInstaEngage: Instagram Engagement Analysis Platform\n• InstaEngage is an advanced analytics platform designed to evaluate and optimize social media engagement for\nmajor Instagram accounts\n• Leveraged Apache Spark for distributed data processing and analytics to handle large-scale engagement data.\n• Employed Apache Kafka for real-time data streaming, ensuring timely insights and updates.\n• Utilized SQLite for storing and managing processed engagement data efficiently.\n• Developed an interactive dashboard using Streamlit to visualize and explore social media engagement metrics\ndynamically.\nDiscoverForge :Forge Ahead, Discover More\n• Automated B2B software product listings on G2 using web scraping, real-time data streaming, and workflows to\nenhance visibility in low-penetration regions.\n• Utilized BeautifulSoup and Selenium for web scraping data from primary sources like software directories, official\npages, tech news sites (ProductHunt, Slashdot, Betalist), and social media (Twitter, LinkedIn), including\nTechAfrica for low-visibility regions.\n• Implemented web scraping, real-time data streaming with Apache Kafka, and managed data with MongoDB,\nDocker, and Kubernetes.\n• Leveraged G2 API and Large Language Models (LLMs) for advanced data processing and API integration.\nEnhanced RAG using KG and Collapsed Tree Approach\n• Built a comprehensive RAG , enhancing the textual output to an user’s queries\n• Implemented a Collapsed Tree Approach to improve understanding and connections between disjoint but related\nPDFs uploaded by users.\n• Utilized Neo4j as a secondary storage system to track and manage all crucial semantics\n• Created more detailed and precise responses to user queries by leveraging both databases for optimal results.\nDrug Bio-activity Prediction - Alzheimer\n• Pioneering drug bioactivity prediction project targeting Alzheimer’s disease, employing a range of machine learning\nmodels including Random Forest Regressor, Support Vector Machines, and Gradient Boosting\n• strong showcase of data preprocessing, feature selection, and model optimization to predict drug effectiveness\n• Successfully trained and compared multiple machine learning models to identify the most accurate and\ninterpretable model for bioactivity prediction\n• This project contributed valuable insights into potential drug candidates, showcasing proficiency in computational\nbiology, machine learning, and the ability to address critical healthcare challenges\nTechnical Skills\nLanguages and skills: Python, SQL, Neo4j, Apache Spark, Apache Kafka, MongoDB , Kubernetes , Docker\nFamiliar Libraries: Scikit-learn, LangChain, Keras, Pandas, NumPy, Seaborn, OpenCV, Mediapipe and few others'), Document(metadata={'producer': 'pdfTeX-1.40.25', 'creator': 'LaTeX with hyperref', 'creationdate': '2024-10-03T15:39:50+00:00', 'author': '', 'keywords': '', 'moddate': '2024-10-03T15:39:50+00:00', 'ptex.fullbanner': 'This is pdfTeX, Version 3.141592653-2.6-1.40.25 (TeX Live 2023) kpathsea version 6.3.5', 'subject': '', 'title': 'Aditeya Baral Resume', 'trapped': '/False', 'source': 'KS_Abhiram_CSE.pdf', 'total_pages': 2, 'page': 1, 'page_label': '2'}, page_content='Extra Curricular\nNexus mentor and member of EVM\n• Mentored the Nexgen Hackathon, guiding teams in the AI/ML domain, which resulted in a highly successful event.\nProvided expert support and insights, significantly enhancing participants’ experience and project outcomes.\n• Successfully orchestrated an engaging full day AI-ML hackathon that attracted the participation of over 150\nindividuals. The event was hosted exclusively to give AI-ML students a great insight on kaggle and problem solving\nin AI-ML domain .\nHackathons\n• Participated and got in top 10 of HashCode hackathon for a project on AI-based nutrition recommender\n• Participated and got in top 10 of G2 hackathon for the above mentioned project DiscoverForge\nMentored at RAPID lab\n• Mentored a team to develop a real-time golf swing analyzer using OpenCV and Mediapipe, providing instant\nfeedback on player posture and swing mechanics.\n• Integrated an SVC model within the system to predict and correct movements, enhancing player performance\nthrough continuous real-time analysis.')]

'''

def llm_skills_details(llm,resume_details):
    prompt_template = '''
        Consider this resume , go over the skills of the candidate and return all the skills 
        
        expected return format :
        <skill list>:

        this is the resume
        {resume}

    '''
    prompt = ChatPromptTemplate.from_template(prompt_template)
    output_parser = StrOutputParser()

        
    chain = prompt | llm | output_parser

    return chain.invoke({"resume": resume_details})

print(llm_skills_details(llm,resume_details))