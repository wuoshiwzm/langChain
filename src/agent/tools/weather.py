from langchain_core.tools import tool


# 3. 定义工具
@tool("Send an email to the specified recipient")
def send_mail(to: str, subject: str, body: str):
    """
    Send an email to the specified recipient.

    Args:
        to (str): The recipient's email address
        subject (str): The email subject
        body (str): The email body content
    """
    # 模拟发送邮件
    print(f"📧 Sending email to: {to}")
    print(f"📧 Subject: {subject}")
    print(f"📧 Body: {body}")
    return f"✅ Email sent successfully to {to}"


@tool("Get current weather for a city")
def get_weather(city: str):
    """
    Get current weather for the specified city.

    Args:
        city (str): The city name
    """
    # 模拟获取天气
    import random
    temperatures = [20, 22, 25, 28, 30, 18, 15, 32, 27, 23]
    conditions = ["Sunny", "Cloudy", "Rainy", "Partly Cloudy", "Windy", "Snowy"]

    temp = random.choice(temperatures)
    condition = random.choice(conditions)

    return f"🌤️ Weather in {city}: {condition}, {temp}°C"


@tool("Search the web for information")
def web_search(query: str):
    """
    Search the web for the specified query.

    Args:
        query (str): The search query
    """
    # 模拟网络搜索
    return f"🔍 Search results for '{query}': This is simulated search result. In a real implementation, this would connect to a search API."

@tool("sending email")
def send_mail(to:str, subject:str, body:str):
    """发送邮件"""
    email={
        'to':to,
        'subject':subject,
        'body':body
    }
    # todo send email ...
    return f'email sent to {to}'