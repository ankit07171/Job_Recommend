import fitz
import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate

load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

def extract_text_from_pdf(uploaded_file):
    
    if isinstance(uploaded_file, str) and os.path.isfile(uploaded_file):
        document = fitz.open(uploaded_file)
    else:
        pdf_bytes = uploaded_file.read()
        document = fitz.open(stream=pdf_bytes, filetype="pdf")

    text = ""
    for page_num in range(len(document)):
        page = document.load_page(page_num)
        text += page.get_text()
    return text


def ask_gemini(user_prompt):    
    chat_model = ChatGoogleGenerativeAI(
        model="gemini-1.5-flash",
        google_api_key=GEMINI_API_KEY
    )
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a career assistant AI that helps analyze resumes and jobs."),
        ("human", "{input}"),
    ])
    chain = prompt | chat_model
    response = chain.invoke({"input": user_prompt})
    return response.content
