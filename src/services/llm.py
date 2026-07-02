from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
import os

load_dotenv()
GEMINI_KEY=os.getenv('GEMINI_KEY')

llm=ChatGoogleGenerativeAI(model='gemini-2.5-flash', api_key=GEMINI_KEY)
