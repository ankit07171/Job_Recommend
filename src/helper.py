import fitz
import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate

load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

def extract_text_from_pdf(uploaded_pdf):
    if not os.path.isfile(uploaded_pdf):
        raise FileNotFoundError(f"The file {uploaded_pdf} does not exist.")
    document = fitz.open(uploaded_pdf)
    text = ""
    for page_num in range(len(document)):
        text += document.load_page(page_num).get_text()
    return text

def ask_gemini(user_prompt):
    chat_model = ChatGoogleGenerativeAI(
        model="gemini-1.5-flash",
        google_api_key=GEMINI_API_KEY
    )
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a career assistant."),
        ("human", "{input}"),
    ])
    chain = prompt | chat_model
    return chain.invoke({"input": user_prompt}).content
