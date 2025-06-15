import json
import os

CONFIG_FILE = "config.json"

def load_secret_code():
    if not os.path.exists(CONFIG_FILE):
        return "9999"
    with open(CONFIG_FILE, "r") as f:
        data = json.load(f)
        return data.get("secret_code", "9999")

def save_secret_code(new_code):
    with open(CONFIG_FILE, "w") as f:
        json.dump({"secret_code": new_code}, f)
