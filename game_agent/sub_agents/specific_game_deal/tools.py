import requests

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
        print(game_deal_detail)

    except Exception:
        print("broken")

    return {"status": "success", "game_deals_data": game_deal_detail}
