import os
from dotenv import load_dotenv

load_dotenv(override=True)

DEEPSEEK_BASE_URL = os.getenv('DEEPSEEK_BASE_URL')
DEEPSEEK_API_KEY = os.getenv('DEEPSEEK_API_KEY')

OPENAI_BASE_URL = os.getenv('OPENAI_BASE_URL')
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

ZHIPU_API_KEY =  os.getenv('ZHIPU_API_KEY')


if __name__ == "__main__":
    print("OPENAI_API_KEY from env:", os.getenv('OPENAI_API_KEY'))
