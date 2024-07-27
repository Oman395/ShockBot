import json

def getJson(filePath: str):
    with open(filePath) as f:
        data = json.load(f)
    return data

def setJson(filePath: str, jsonData):
    with open(filePath, 'w') as f:
        f.seek(0)
        json.dump(jsonData, f, indent=2)

def loadConfig():
    return getJson("./config.json")