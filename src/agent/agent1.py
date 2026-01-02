from langchain.agents import create_agent

from agent.llm import llm_openai
from agent.tools.tool_demo1 import MyWebSearchTool
from agent.tools.weather import send_mail, get_weather, web_search

# 创建一个自定义的工具
mywebsearch = MyWebSearchTool()

agent1 = create_agent(
    model=llm_openai,
    tools=[mywebsearch],
    system_prompt='you are a agent, use websearch tools always',
)

