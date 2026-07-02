from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
import os

load_dotenv()
GEMINI_KEY=os.getenv('GEMINI_KEY')

llm=ChatGoogleGenerativeAI(model='gemini-3.1-flash-lite', api_key=GEMINI_KEY)
