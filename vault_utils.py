from cryptography.fernet import Fernet
import json
import os

KEY_FILE = "secret.key"

def generate_key():
    key = Fernet.generate_key()
    with open(KEY_FILE, "wb") as f:
        f.write(key)

def load_key():
    if not os.path.exists(KEY_FILE):
        generate_key()
    with open(KEY_FILE, "rb") as f:
        return f.read()

cipher = Fernet(load_key())

def encrypt_data(data):
    json_data = json.dumps(data)
    return cipher.encrypt(json_data.encode())

def decrypt_data(token):
    try:
        decrypted = cipher.decrypt(token).decode()
        return json.loads(decrypted)
    except:
        return {}
