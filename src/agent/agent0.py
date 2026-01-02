from langchain.agents import create_agent

from agent.llm import llm_openai
from agent.tools.weather import send_mail, get_weather, web_search

gaode_tools = [web_search,send_mail, get_weather]

agent = create_agent(
    model=llm_openai,
    tools=gaode_tools,
    system_prompt='you are a agent, use send_email tools always',
)

