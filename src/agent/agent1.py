from langchain.agents import create_agent

from llm import zhipuai_llm
from agent.tools.tool_demo0 import web_search

agent = create_agent(
    zhipuai_llm,
    tools=[web_search],
    system_prompt="you are agent, do something..."
)


