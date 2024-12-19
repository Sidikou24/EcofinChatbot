import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.getenv('FLASK_SECRET_KEY')
    FLASK_ENV = os.getenv('FLASK_ENV', 'development')
    GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
    USER_AGENT = os.getenv('USER_AGENT')
