import asyncio
from intent import extract_intent_and_city
from weather_client import get_weather_from_mcp


async def handle_message(message: str):
    parsed = extract_intent_and_city(message)

    if parsed["intent"] != "weather request":
        return "Agent: No weather tool call needed."

    city = parsed["city"] or "Delhi"  # Default fallback city
    result = await get_weather_from_mcp(city)
    return f"Agent: Weather in {city} → {result}"


async def main():
    print("Agent is running. Type your message (type 'exit' to quit).")
    while True:
        user_msg = input("\nYou: ")
        if user_msg.lower() in ["exit", "quit"]:
            break
        response = await handle_message(user_msg)
        print(response)


if __name__ == "__main__":
    asyncio.run(main())
