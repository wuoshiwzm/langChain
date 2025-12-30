import dotenv
from langchain_ollama import ChatOllama
from langchain_openai import ChatOpenAI
import os
from dotenv import load_dotenv

load_dotenv()

# 华为内部会默认走代理，导致报错
os.environ["NO_PROXY"] = "localhost,127.0.0.1"

# ? 1. ollama 模型
llm_ollama = ChatOllama(
    model="deepseek-r1:1.5b",  # 替换为你本地已安装的模型名
)
# messages = [
#     ("human", '解释1+1=3')
# ]
# response = llm_ollama.invoke(messages)
# print(response)

# ? 2. openai 模型
llm_openai = ChatOpenAI(
    model='qwen3-max',
    temperature=0.6,
    base_url="https://api.closeai-proxy.xyz/v1",
    api_key='sk-FL6sYxBsHe12p0xBMyxPjU1NDR5Pp8kThnS7zD8W9RGfTezg'
)
# messages = [
#     ("human", '解释1+1=3')
# ]
# response = llm_openai.invoke(messages)
# print(response)
