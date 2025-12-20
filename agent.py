from google.adk.agents.llm_agent import Agent
import requests
import json

store_data = {
    "1": "Steam",
    "2": "GamersGate",
    "3": "GreenManGaming",
    "4": "Amazon",
    "5": "GameStop",
    "6": "Direct2Drive",
    "7": "GOG",
    "8": "Origin",
    "9": "Get Games",
    "10": "Shiny Loot",
    "11": "Humble Store",
    "12": "Desura",
    "13": "Uplay",
    "14": "IndieGameStand",
    "15": "Fanatical",
    "16": "Gamesrocket",
    "17": "Games Republic",
    "18": "SilaGames",
    "19": "Playfield",
    "20": "ImperialGames",
    "21": "WinGameStore",
    "22": "FunStockDigital",
    "23": "GameBillet",
    "24": "Voidu",
    "25": "Epic Games Store",
    "26": "Razer Game Store",
    "27": "Gamesplanet",
    "28": "Gamesload",
    "29": "2Game",
    "30": "IndieGala",
    "31": "Blizzard Shop",
    "32": "AllYouPlay",
    "33": "DLGamer",
    "34": "Noctre",
    "35": "DreamGame",
}


# Mock tool implementation
def get_game_deals() -> dict:
    """Returns a list of games that are currently on sale"""

    url = "https://www.cheapshark.com/api/1.0/deals?storeID=1&upperPrice=15"
    results = requests.get(url)

    try:

        data = results.json()
        deal_data = []
        for games in data:
            deal_data.append(
                {
                    "game_name": games["title"],
                    "game_sale_price": games["salePrice"],
                    "game_normal_price": games["normalPrice"],
                    "gameSavings": games["savings"],
                }
            )

    except Exception:
        print("Broken")

    return {
        "status": "success",
        "deal_data": deal_data,
    }


def get_deals_on_game(gameID: str) -> dict:
    """Returns a list of deals for each store along with the price

    Args:
        gameID (str): The id of the game
    """
    url = f"https://www.cheapshark.com/api/1.0/games?id={gameID}"
    result = requests.get(url)

    try:
        data = result.json()
        game_data = data["deals"]

        game_deal_detail = []
        for detail in game_data:
            game_deal_detail.append(
                {
                    "store": store_data[detail["storeID"]],
                    "discounted_price": detail["price"],
                    "original_price": detail["retailPrice"],
                    "savings": detail["savings"],
                    "store_link": f"https://www.cheapshark.com/redirect?dealID={detail["dealID"]}",
                }
            )

    except Exception:
        print("broken")

    return {"status": "success", "game_deals_data": game_deal_detail}


def get_game_info(game: str) -> dict:
    """Returns information about a game"""

    url = f"https://www.cheapshark.com/api/1.0/games?title={game}&limit=5&exact=0"
    result = requests.get(url)

    try:
        data = result.json()
        game_data = []

        for game in data:
            game_data.append(
                {
                    "game_id": game["gameID"],
                    "game_name": game["external"],
                    "game_thumbnail": game["thumb"],
                    "game_steam_id": (
                        f"https://store.steampowered.com/app/{game["steamAppID"]}"
                        if game["steamAppID"]
                        else None
                    ),
                }
            )

    except Exception:
        print("broken")

    return {"status": "success", "game_info_data": game_data}


root_agent = Agent(
    model="gemini-3-flash-preview",
    name="root_agent",
    description="Gets the list of games the user wants and the discounts available in the game stores",
    instruction=""" You are a helpful assistant that tells the list of games the user wants. 
    Once you show the list, let the user pick the game he wants. 
    If he picks one game, output the id, name of the game, thumbnail and link to the game on Steam, if available.
    Then, take the id and use it to return a list of discounts for that game.
    Use the 'get_game_info' to return a list of games. Use the 'get_deals_on_game' to return a list of discounts with more than 0 percent savings for that game, with the given game id, along with the link to the store using the store_link """,
    tools=[get_game_info, get_deals_on_game],
)
