from google.adk.agents import Agent
from .tools import (
    get_game_info,
)
from . import prompt

game_search_agent = Agent(
    model="gemini-3-flash-preview",
    name="game_search_agent",
    description="Searches for the list of similar games based on user input.",
    instruction=prompt.GAME_SEARCH_PROMPT,
    tools=[get_game_info],
    output_key="game_data",
)
