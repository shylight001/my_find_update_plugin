import json

#载入json
def load_json(path):
    data = {}
    with open(path, "r", encoding="utf-8") as file:
        data = json.load(file)
    return data

#json储存
def save_json(path, data):
    with open(path, "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=4)
