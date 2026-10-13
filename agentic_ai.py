import requests

from langchain.agents import create_agent
from langchain.tools import tool
from langchain_google_genai import ChatGoogleGenerativeAI


# STEP 1: Live weather tool
@tool
def get_weather(city: str) -> str:
    """Get real-time weather for a city."""

    print(f"\n[TOOL] Fetching live weather for {city}...")

    url = f"https://wttr.in/{city}?format=j1"
    response = requests.get(url, timeout=15)
    response.raise_for_status()

    data = response.json()["current_condition"][0]

    temperature = int(data["temp_C"])
    condition = data["weatherDesc"][0]["value"]

    result = (
        f"City: {city}, "
        f"Temperature: {temperature} C, "
        f"Condition: {condition}"
    )

    print("[TOOL RESULT]", result)
    return result


# STEP 2: Evaluate weather for outdoor activities
@tool
def evaluate_weather(
    city: str, temperature: int, condition: str
) -> str:
    """Evaluate weather and recommend suitable activities."""

    print(f"\n[TOOL] Evaluating outdoor activities in {city}...")

    condition = condition.lower()

    if "rain" in condition or "thunder" in condition:
        score = 1
        activity = "Indoor activities"
    elif temperature >= 35:
        score = 2
        activity = "Outdoor activities during cooler hours"
    else:
        score = 3
        activity = "Outdoor sightseeing"

    result = (
        f"{city}: {activity}. "
        f"Suitability score: {score}/3"
    )

    print("[TOOL RESULT]", result)
    return result


# STEP 3: Initialize Gemini
llm = ChatGoogleGenerativeAI(
    model="gemini-3.5-flash",
    google_api_key="AQ.Ab8RN6Kfum6U3OLXiKouSjdIgtFwY6C4CYQKcb6ZIVD9FRaYCQ",
    temperature=0
)


# STEP 4: Create the agent
agent = create_agent(
    model=llm,
    tools=[get_weather, evaluate_weather],
    system_prompt="""
    You are an agentic travel assistant.

    GOAL:
    Recommend the better city for outdoor activities today.

    Follow these steps:
    1. Call get_weather for Hyderabad.
    2. Call get_weather for Bengaluru.
    3. Extract the actual temperature and condition for each.
    4. Call evaluate_weather for each city using those results.
    5. Compare both evaluation results.
    6. Recommend the better city and explain why.

    Use actual tool results only.
    Do not invent weather data or claim a tool ran if it did not.
    """
)


# STEP 5: Give the agent a goal
print("=== AGENTIC AI STARTED ===")

result = agent.invoke({
    "messages": [{
        "role": "user",
        "content": (
            "Compare Hyderabad and Bengaluru using current weather. "
            "Evaluate outdoor activities in both cities and "
            "recommend the better option."
        )
    }]
})


# STEP 6: Print the final answer
print("\n=== FINAL RECOMMENDATION ===")

message = result["messages"][-1]
content = message.content

if isinstance(content, str):
    print(content)
else:
    for item in content:
        if item.get("type") == "text":
            print(item["text"])
