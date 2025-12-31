from langchain_ollama import ChatOllama
from langchain_openai import ChatOpenAI
import os
from zhipuai import ZhipuAI

from env_utils import ZHIPU_API_KEY, OPENAI_API_KEY, OPENAI_BASE_URL


# 华为内部会默认走代理，导致报错
os.environ["NO_PROXY"] = "localhost,127.0.0.1"

#? 1. ollama 模型
llm_ollama = ChatOllama(
    model="deepseek-r1:1.5b",  # 替换为你本地已安装的模型名
)
# messages = [
#     ("human", '解释1+1=3')
# ]
# response = llm_ollama.invoke(messages)
# print(response)

print(f"open ai api key:::::{OPENAI_API_KEY}")

#? 2. openai 模型
llm_openai = ChatOpenAI(
    model='qwen3-max',
    temperature=0.6,
    base_url=OPENAI_BASE_URL,
    api_key=OPENAI_API_KEY
)
# messages = [
#     ("human", '解释1+1=3')
# ]
# response = llm_openai.invoke(messages)
# print(response)



#? 3. 智谱
# 默认 base_url = "https://open.bigmodel.cn/api/paas/v4"
zhipuai_llm = ZhipuAI(api_key=ZHIPU_API_KEY)
