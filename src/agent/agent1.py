from langchain.agents import create_agent

from llm import llm

def send_mail(to:str, subject:str, body:str):
    email={
        'to':to,
        'subject':subject,
        'body':body
    }
    # todo send email ...
    return f'email sent to {to}'


create_agent(
    model=llm,
    tools=[send_mail],
    system_prompt='you are a agent, use send_email tools always'
)

