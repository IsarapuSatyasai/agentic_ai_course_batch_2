# config.py
import os
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Default Models
GENERATION_MODEL = "gpt-4o-mini"
JUDGE_MODEL = "gpt-4.1"

# Default Parameters
TEMPERATURE = 0.1
MAX_TOKENS = 300