import os
from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from pydantic import BaseModel, Field
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from typing import Optional,List
import time
from github_parser.validation import get_user_repositories


load_dotenv()
groq_api_key = os.getenv("GROQ_API_KEY")

llm = init_chat_model("llama3-70b-8192", model_provider="groq")


resume_details = '''
Document(metadata={'producer': 'pdfTeX-1.40.25', 'creator': 'LaTeX with hyperref', 'creationdate': '2024-10-03T15:39:50+00:00', 'author': '', 'keywords': '', 'moddate': '2024-10-03T15:39:50+00:00', 'ptex.fullbanner': 'This is pdfTeX, Version 3.141592653-2.6-1.40.25 (TeX Live 2023) kpathsea version 6.3.5', 'subject': '', 'title': 'Aditeya Baral Resume', 'trapped': '/False', 'source': 'KS_Abhiram_CSE.pdf', 'total_pages': 2, 'page': 0, 'page_label': '1'}, page_content='K S Abhiram\n+91-8660946912 | abhiramkaranth700@gmail.com | GitHub |\nEducation\nPES University Bangalore, India\nB.Tech in Computer Science CGPA - 8.12 Dec 2021 – 2025\n• 1x Professor MRD Scholarship Awardee for being in the top 20% of the batch\n• 3x DAC Scholarship Awardee for maintaining cgpa over 7.75\nKarkala Jnanasudha PU College Ganit Nagar Udupi, India\nState Board (PCMS) - 100% June 2019 – October 2021\n• KCET Rank 969\n• JEE Main 96.66 percentile\nJagadheeshwara English Medium High School Kalasa Chikkamagalur, India\nState Board - 99.36% June 2017 – May 2019\nProjects\nInstaEngage: Instagram Engagement Analysis Platform\n• InstaEngage is an advanced analytics platform designed to evaluate and optimize social media engagement for\nmajor Instagram accounts\n• Leveraged Apache Spark for distributed data processing and analytics to handle large-scale engagement data.\n• Employed Apache Kafka for real-time data streaming, ensuring timely insights and updates.\n• Utilized SQLite for storing and managing processed engagement data efficiently.\n• Developed an interactive dashboard using Streamlit to visualize and explore social media engagement metrics\ndynamically.\nDiscoverForge :Forge Ahead, Discover More\n• Automated B2B software product listings on G2 using web scraping, real-time data streaming, and workflows to\nenhance visibility in low-penetration regions.\n• Utilized BeautifulSoup and Selenium for web scraping data from primary sources like software directories, official\npages, tech news sites (ProductHunt, Slashdot, Betalist), and social media (Twitter, LinkedIn), including\nTechAfrica for low-visibility regions.\n• Implemented web scraping, real-time data streaming with Apache Kafka, and managed data with MongoDB,\nDocker, and Kubernetes.\n• Leveraged G2 API and Large Language Models (LLMs) for advanced data processing and API integration.\nEnhanced RAG using KG and Collapsed Tree Approach\n• Built a comprehensive RAG , enhancing the textual output to an user’s queries\n• Implemented a Collapsed Tree Approach to improve understanding and connections between disjoint but related\nPDFs uploaded by users.\n• Utilized Neo4j as a secondary storage system to track and manage all crucial semantics\n• Created more detailed and precise responses to user queries by leveraging both databases for optimal results.\nDrug Bio-activity Prediction - Alzheimer\n• Pioneering drug bioactivity prediction project targeting Alzheimer’s disease, employing a range of machine learning\nmodels including Random Forest Regressor, Support Vector Machines, and Gradient Boosting\n• strong showcase of data preprocessing, feature selection, and model optimization to predict drug effectiveness\n• Successfully trained and compared multiple machine learning models to identify the most accurate and\ninterpretable model for bioactivity prediction\n• This project contributed valuable insights into potential drug candidates, showcasing proficiency in computational\nbiology, machine learning, and the ability to address critical healthcare challenges\nTechnical Skills\nLanguages and skills: Python, SQL, Neo4j, Apache Spark, Apache Kafka, MongoDB , Kubernetes , Docker\nFamiliar Libraries: Scikit-learn, LangChain, Keras, Pandas, NumPy, Seaborn, OpenCV, Mediapipe and few others'), Document(metadata={'producer': 'pdfTeX-1.40.25', 'creator': 'LaTeX with hyperref', 'creationdate': '2024-10-03T15:39:50+00:00', 'author': '', 'keywords': '', 'moddate': '2024-10-03T15:39:50+00:00', 'ptex.fullbanner': 'This is pdfTeX, Version 3.141592653-2.6-1.40.25 (TeX Live 2023) kpathsea version 6.3.5', 'subject': '', 'title': 'Aditeya Baral Resume', 'trapped': '/False', 'source': 'KS_Abhiram_CSE.pdf', 'total_pages': 2, 'page': 1, 'page_label': '2'}, page_content='Extra Curricular\nNexus mentor and member of EVM\n• Mentored the Nexgen Hackathon, guiding teams in the AI/ML domain, which resulted in a highly successful event.\nProvided expert support and insights, significantly enhancing participants’ experience and project outcomes.\n• Successfully orchestrated an engaging full day AI-ML hackathon that attracted the participation of over 150\nindividuals. The event was hosted exclusively to give AI-ML students a great insight on kaggle and problem solving\nin AI-ML domain .\nHackathons\n• Participated and got in top 10 of HashCode hackathon for a project on AI-based nutrition recommender\n• Participated and got in top 10 of G2 hackathon for the above mentioned project DiscoverForge\nMentored at RAPID lab\n• Mentored a team to develop a real-time golf swing analyzer using OpenCV and Mediapipe, providing instant\nfeedback on player posture and swing mechanics.\n• Integrated an SVC model within the system to predict and correct movements, enhancing player performance\nthrough continuous real-time analysis.')]

'''


def llm_project_details(llm,resume_details):
    prompt_template = '''
        Consider this resume , go over the projects of the candidate and return all the project names , followed by the corresponding description of the project , make sure to miss no important detail
        And keep the description as detailed as possible 
        expected return format :
        <project_name>:
        <description>:

        this is the resume
        {resume}

    '''
    prompt = ChatPromptTemplate.from_template(prompt_template)
    output_parser = StrOutputParser()

        
    chain = prompt | llm | output_parser

    return chain.invoke({"resume": resume_details})

#project_details = llm_project_details(llm,resume_details)

def extract_project_names(project_details,llm):

    max_retries = 10  # Set to None to retry indefinitely, or use an integer for a limit
    attempt = 0

    class ProjectNameOut(BaseModel):
        projects: List[str] = Field(..., description="List of all project names")

    # Wrap your LLM with structured output using the updated schema
    project_names_llm = llm.with_structured_output(ProjectNameOut)

    # Define a prompt that instructs the LLM to extract only the project names.
    query = f'''
    Extract all the project names from the given project details. 
    Be strict with the format
    Return the output as a JSON object with the following format:
    {{
        "projects": ["project1", "project2", ...]
    }}
    Do not include any additional text not even newline or anything .
    {project_details}
    '''

    while True:
        try:
            result = project_names_llm.invoke(query)
            return result
        except Exception as e:
            attempt += 1
            print(f"Attempt {attempt}: Error encountered: {e}")
            print("Retrying...")
            # Optionally wait a little before retrying
            time.sleep(2)
            if max_retries is not None and attempt >= max_retries:
                raise Exception("Maximum retry attempts reached") from e
        

#structured_names = extract_project_names(project_details,llm)

# extras , clean up later 
'''print(structured_names)
print(type(structured_names))
for idx, prj in enumerate(structured_names.projects):
    if isinstance(prj, str):
        # If it's a string, compare directly and update the list element.
        if prj == 'DiscoverForge':
            structured_names.projects[idx] = 'hi'
print(structured_names)

print(get_user_repositories('AbhiramKaranth'))'
'''
'''repository_list = get_user_repositories('AbhiramKaranth')'''

# function to get valid names only from the list containing all names 
def validate_projects(structured_output,repositories_list,llm):
    max_retries = 10  
    attempt = 0

    class ProjectNameValidation(BaseModel):
        valid_projects: List[str] = Field(..., description="List of all project names")
    
    valid_projects_llm = llm.with_structured_output(ProjectNameValidation)
    query = f'''
    You are given two lists:
    Actual repository projects (correct names): {repositories_list}
    Currently known projects (which may be misspelled or non-existent): {structured_output}

    For each project in the Currently known projects list:
    - If it is a misspelling or abbreviation of a project in the Actual repository projects list, replace it with the exact correct project name. This step is crucial.
    - The abbreviations will be very similar to the actual names, possibly missing only a few characters if it is completely different with no matching words , it is different.
    - If a project does not correspond to any project in the Actual repository projects list, replace it with "N/A".


    Return the output as a JSON object in this exact format:
    {{
        "valid_projects": ["project1", "project2", ...]
    }}

        
    Ensure that the number of items in "valid_projects" exactly matches the number of items in the Currently known projects list, with no extra items. Do not include any additional text, whitespace, or newlines.

    Example: Replace "InstaEngage" with "Instagram_engagement_analysis_kafka", and do the same for the rest.

    '''
    while True:
        try:    
            result = valid_projects_llm.invoke(query)
            return result
        except Exception as e:
            attempt += 1
            print(f"Attempt {attempt}: Error encountered: {e}")
            print("Retrying...")
            # Optionally wait a little before retrying
            time.sleep(2)
            if max_retries is not None and attempt >= max_retries:
                raise Exception("Maximum retry attempts reached") from e

'''print(repository_list)
print(structured_names)
print(validate_projects(structured_names,repository_list,llm))'''


def project_scorer(project_name,extracted_project_details,resume_project_details,llm):
    query = f"""
    Project Analysis and Description Evaluation

    Project Name:
    ---------------
    {project_name}

    Resume Project Details:
    -----------------------
    {resume_project_details}

    Actual Project Details:
    -----------------------
    {extracted_project_details}

    Instructions:
    --------------
    1. Compare the resume project details with the actual project details.
    2. Evaluate how well the actual project description aligns with the resume details.
    3. Identify any discrepancies or mismatches. If the actual description does not match or appears completely invalid relative to the resume details, provide a very low score.
    4. Provide detailed insights on the following criteria:
    - Accuracy: How accurately does the actual description represent the project as outlined in the resume?
    - Completeness: How comprehensive is the actual project description compared to the resume details?
    - Validity: Does the actual description seem credible and consistent with the resume information? (Rate low if it appears mismatched or invalid.)
    - Overall Quality: How useful is the actual project description in conveying the project details?
    5. For each criterion, assign a numerical score (e.g., on a scale of 1 to 10) and include your reasoning.
    6. Structure your response with clear sections or bullet points so that an interviewer can easily understand the evaluation.

    Please provide specific insights, recommendations for improvement, and a final summary of the overall quality of the actual project description.
"""

    result = llm.invoke(query)
    return result

def final_scorer(think_results,llm):

    query = """
        Please analyze the following project evaluation text and produce a concise, structured  summary.
        The summary should have the following keys:
        Give output just as text not JSON
        - project_name: string
        - accuracy: "score" and "explanation"
        - completeness: "score" and "explanation"
        - validity:  "score" and "explanation"
        - overall_quality:  "score" and "explanation"
        - insights: string
        - recommendations: string
        If any detail is missing in the evaluation text, set its value to not much available.
        
        Only return the output without additional commentary.
        It's better if actual description has more info 
        
        Evaluation text:
        {thinkresults}
    """
    prompt = ChatPromptTemplate.from_template(query)
    output_parser = StrOutputParser()

        
    chain = prompt | llm | output_parser

    return chain.invoke({"thinkresults": think_results})




