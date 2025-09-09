#!/usr/bin/env python3
import os
import requests
from mcp.server.fastmcp import FastMCP
from dotenv import load_dotenv
import logging

load_dotenv()
# Create MCP server
mcp = FastMCP("Weather MCP Server")


# Tool: get_weather
@mcp.tool()
def get_weather(location: str) -> dict:
    """Get current weather for a given city using OpenWeatherMap."""
    api_key = os.getenv("OPENWEATHER_API_KEY")
    if not api_key:
        return {"error": "Missing OPENWEATHER_API_KEY environment variable"}
    # logging.info("Preparing URL")
    # logging.info(f"API KEY : {api_key}")
    url = "https://api.openweathermap.org/data/2.5/weather"
    params = {"q": location, "appid": api_key}
    resp = requests.get(url, params=params)

    if resp.status_code != 200:
        return {"error": f"API error: {resp.text}"}

    data = resp.json()
    return {
        "location": data["name"],
        "temperature": data["main"]["temp"],
        "condition": data["weather"][0]["description"],
        "humidity": data["main"]["humidity"],
    }


if __name__ == "__main__":
    mcp.run()
