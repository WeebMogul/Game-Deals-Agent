from google.adk.agents import Agent
from .tools import (
    get_deals_on_game,
    get_game_info,
)
from . import prompt

specific_game_agent = Agent(
    model="gemini-3-flash-preview",
    name="specific_game_agent",
    description="Gets the list of games the user wants and the discounts available in the game stores.",
    instruction=prompt.SPECIFIC_AGENT_PROMPT,
    tools=[get_game_info, get_deals_on_game],
)
