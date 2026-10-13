import requests
from langchain.agents import create_agent
from langchain.tools import tool
from langchain_google_genai import ChatGoogleGenerativeAI


@tool
def get_weather(city: str) -> str:
    """Get current weather for a city."""
    url = "https://wttr.in/" + city + "?format=3"
    response = requests.get(url, timeout=10)
    return response.text


llm = ChatGoogleGenerativeAI(
    model="gemini-3.5-flash",
    google_api_key="AQ.Ab8RN6Kfum6U3OLXiKouSjdIgtFwY6C4CYQKcb6ZIVD9FRaYCQ"
)

agent = create_agent(
    model=llm,
    tools=[get_weather],
    system_prompt="You are a weather assistant. Use the tool to check weather."
)

result = agent.invoke({
    "messages": [
        {"role": "user", "content": "What is the weather in Hyderabad?"}
    ]
})

print(result["messages"][-1].content[0]["text"])
