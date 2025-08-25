import json

with open("output.json", "r", encoding="utf-8") as fobj:
    data = json.load(fobj)
    for key, value in data.items():
        print(f"{key} : {value}")