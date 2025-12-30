from langchain.agents import create_agent
from langchain_openai import ChatOpenAI
import dotenv
import os

# 华为内部会默认走代理，导致报错
os.environ["NO_PROXY"] = "localhost,127.0.0.1"
dotenv_path = '.env'

llm = ChatOpenAI(
    model='qwen3-max',
    temperature=0.6,
    base_url="https://api.closeai-proxy.xyz/v1",
    api_key="sk-FL6sYxBsHe12p0xBMyxPjU1NDR5Pp8kThnS7zD8W9RGfTezg"
)


# DEEPSEEK_BASE_URL='https://api.closeai-proxy.xyz/v1'
# DEEPSEEK_API_KEY='sk-FL6sYxBsHe12p0xBMyxPjU1NDR5Pp8kThnS7zD8W9RGfTezg'