from langchain_ollama import ChatOllama
from langchain_openai import ChatOpenAI
import requests
import json
import os

# 华为内部会默认走代理，导致报错
os.environ["NO_PROXY"] = "localhost,127.0.0.1"

# 初始化模型（确保 Ollama 已启动且模型已安装）
model = ChatOllama(
    # model="deepseek-r1:8b",      # 替换为你本地已安装的模型名
    model="deepseek-r1:1.5b",  # 替换为你本地已安装的模型名
)

# 构造对话消息
messages = [
    ("human", '解释1+1=3')
]

# 调用模型
response = model.invoke(messages)

# 输出结果
print(response)

chat_model = ChatOpenAI(
    model="deepseek-r1:1.5b",
    temperature=1.0,
    api_key='',
    base_url=''
)
