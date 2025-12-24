from google.adk.agents.llm_agent import Agent
from . import prompt
from .tools import get_game_deals

general_deals_agent = Agent(
    name="general_deals_agent",
    description="Provides a list of games that are currently on sale",
    instruction=prompt.DEAL_PROMPT,
    tools=[get_game_deals],
)
