import json

with open("store_data.json", "r") as file:
    store_data = json.load(file)

store_list = {}
for data in store_data:
    store_list[data["storeID"]] = data["storeName"]

print(store_list)
