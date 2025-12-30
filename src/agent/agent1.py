from langchain.agents import create_agent
from agent.llm import llm_ollama
from agent.tools.weather import send_mail, get_weather, web_search

tools = [send_mail, get_weather, web_search]

agent = create_agent(
    model=llm_ollama,
    tools=tools,
    system_prompt='you are a agent, use send_email tools always',
)

