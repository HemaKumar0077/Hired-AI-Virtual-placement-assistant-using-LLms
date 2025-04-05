import ollama
import fitz  # PyMuPDF for PDF text extraction
from groq import Groq
from gtts import gTTS
import speech_recognition as sr
from pydub import AudioSegment
from playsound import playsound
import re

# Initialize Groq client (Replace with your API Key)
client = Groq(api_key="")

def get_ollama_response(input_text, resume_text, prompt):
    model = "llama2"  # Change to "mistral" if needed
    full_prompt = f"{prompt}\n\nJob Description:\n{input_text}\n\nResume Content:\n{resume_text}"
    response = ollama.chat(model=model, messages=[{"role": "user", "content": full_prompt}])
    return response['message']['content'] if 'message' in response else "Error: Unexpected response format."

def extract_text_from_pdf(uploaded_file):
    """Extract text from a PDF file."""
    if uploaded_file is not None:
        pdf_document = fitz.open(stream=uploaded_file.read(), filetype="pdf")
        text = "\n".join([page.get_text("text") for page in pdf_document])
        return text if text.strip() else "Error: No readable text found in PDF."
    else:
        raise FileNotFoundError("No file uploaded")

def interview_chatbot(job_type, conversation_history, prompt_type="next_question"):
    """Generate questions and feedback for mock interviews."""
    prompts = {
        "start": f"""
        Act as an interviewer for a {job_type} interview. Start by introducing yourself and asking the first question.
        Format your response with a brief introduction followed by "Question 1:" and then your first question.
        Ask only one question at a time and wait for the response.
        """,
        "feedback": f"""
        Act as an interviewer for a {job_type} interview. You've just received an answer to your question.
        Provide feedback on the answer, including strengths, areas for improvement, and a score out of 10.
        """,
        "next_question": f"""
        Act as an interviewer for a {job_type} interview. You've already asked previous questions and provided feedback.
        Now ask the next logical question in the interview sequence.
        """
    }
    
    messages = [{"role": "system", "content": prompts[prompt_type]}] + conversation_history

    response = client.chat.completions.create(
        model="llama3-70b-8192",
        messages=messages,
        temperature=1,
        max_tokens=1024,
        top_p=1,
    )
    
    return response.choices[0].message.content.strip()

def extract_next_question(response_text):
    """Extract the next question from a response that might contain feedback."""
    match = re.search(r"(?:Question \d+:|Next question:)(.*?)(?=$)", response_text, re.DOTALL)
    return match.group(1).strip() if match else response_text

def text_to_speech(text, speed=200):
    """Convert text to speech and play it with increased speed."""
    tts = gTTS(text=text, lang='en', slow=False)
    tts.save("response.mp3")
    
    audio = AudioSegment.from_file("response.mp3")
    faster_audio = audio.speedup(playback_speed=1.5)  # Adjust speed
    faster_audio.export("faster_response.mp3", format="mp3")
    playsound("faster_response.mp3")

def speech_to_text():
    """Convert speech input to text."""
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source, duration=1)
        recognizer.energy_threshold = 400
        recognizer.pause_threshold = 10
        audio = recognizer.listen(source, timeout=None, phrase_time_limit=90)
    
    try:
        return recognizer.recognize_google(audio)
    except sr.UnknownValueError:
        return "Could not understand audio. Please try again."
    except sr.RequestError:
        return "Speech recognition service unavailable."