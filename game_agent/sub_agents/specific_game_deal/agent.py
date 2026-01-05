from google.adk.agents import Agent
from .tools import (
    get_deals_on_game,
)
from . import prompt

specific_game_agent = Agent(
    model="gemini-3-flash-preview",
    name="specific_game_agent",
    description="Displays the list of games and the discounts available in the game stores using {game_data}",
    instruction=prompt.SPECIFIC_AGENT_PROMPT,
    tools=[get_deals_on_game],
)
