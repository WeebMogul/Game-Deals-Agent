from google.adk.agents.llm_agent import Agent
from google.adk.agents import SequentialAgent
from .sub_agents.general_game_deals.agent import general_deals_agent
from .sub_agents.specific_game_deal.agent import specific_game_agent
from .sub_agents.game_search.agent import game_search_agent
from google.adk.sessions import InMemorySessionService
from google.adk.runners import Runner


spes_agent = SequentialAgent(
    name="spes_agent",
    description="Gets the list of games the user wants and the discounts available in the game stores",
    sub_agents=[
        game_search_agent,
        specific_game_agent,
    ],
)


root_agent = Agent(
    model="gemini-3-flash-preview",
    name="root_agent",
    description="Gets the list of games the user wants and the discounts available in the game stores",
    instruction=""" You are a helpful assistant that tells the list of games the user wants, along with their discounts.
    If the user asks about a list of games that are currently on sale, transfer to the 'general_deals_agent' and generate a list of games, their deals and savings, once the deal_data is available.
    If the user asks about a specific game, transfer to the 'spes_agent'
     """,
    sub_agents=[general_deals_agent, spes_agent],
)
