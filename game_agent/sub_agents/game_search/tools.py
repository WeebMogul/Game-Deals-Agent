import requests


def get_game_info(game: str) -> dict:
    """Returns information about a game"""

    url = f"https://www.cheapshark.com/api/1.0/games?title={game}&limit=2&exact=0"
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
