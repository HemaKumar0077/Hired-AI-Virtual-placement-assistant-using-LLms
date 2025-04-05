import os
import requests
from groq import Groq
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Set up Groq API Key
groq_api_key = os.getenv("GROQ_API_KEY")
if not groq_api_key:
    raise ValueError("Groq API Key is missing! Set the GROQ_API_KEY environment variable.")

# Initialize Groq LLM
llm = Groq(api_key=groq_api_key)

def chat_with_llm(prompt):
    """Chat with LLM using the provided prompt."""
    try:
        response = llm.chat.completions.create(
            model="llama3-70b-8192",
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"LLM API Error: {e}"

def get_company_description(company_name):
    """Fetch a brief description of a company from Wikipedia API."""
    try:
        url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{company_name}"
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
        
        response = requests.get(url, headers=headers)
        data = response.json()
        
        if "extract" in data:
            return data["extract"][:500] + "..."  # Limit description length
        else:
            return "No description available."
    except Exception as e:
        return f"Error fetching description: {e}"

def generate_interview_questions(company, role, category):
    """Generate 10 unique interview questions based on the given company, role, and category."""
    prompt = f"Generate exactly 10 unique and challenging interview questions asked at {company} for the role of {role} under the category of {category}. Provide each question on a new line, without numbering."
    response = chat_with_llm(prompt)
    
    if not response:
        return []
    
    # Remove duplicates and filter empty lines
    questions = list(set([q.strip() for q in response.split("\n") if q.strip()]))
    
    return questions[:10]  # Ensure exactly 10 questions

def generate_solutions(category, questions):
    """Generate structured solutions for the given interview questions."""
    solutions = []
    
    for i, question in enumerate(questions, 1):
        solution_prompt = f"Provide a concise and structured answer for this {category} interview question: {question}"
        solution = chat_with_llm(solution_prompt) or "Solution not available."
        
        # Remove unwanted introductory text
        unwanted_phrases = [
            "Here is a concise and structured answer to the",
            "Problem Statement:",
            "Solution:"
        ]
        
        # Filter out unwanted phrases
        for phrase in unwanted_phrases:
            if phrase in solution:
                solution = solution.split(phrase, 1)[-1].strip()

        solutions.append(f"**Q{i}: {question}**\n\n**Answer:** {solution}\n\n---")
    
    return solutions