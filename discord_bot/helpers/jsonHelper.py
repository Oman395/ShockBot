import json
import pathlib
path = pathlib.Path(__file__).parent.parent.resolve()

def getJson(filePath: str):
    with open(filePath) as f:
        data = json.load(f)
    return data

def setJson(filePath: str, jsonData):
    with open(filePath, 'w') as f:
        f.seek(0)
        json.dump(jsonData, f, indent=2)

def loadConfig():
    return getJson(path / "config.json")