import requests


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
