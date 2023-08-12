from os import path, getenv

class Config:
    API_ID = int(getenv("API_ID", "21590558"))
    API_HASH = getenv("API_HASH", "9767814b790f12ad9a333a20bcaf1200")
    BOT_TOKEN = getenv("BOT_TOKEN", "6466372597:AAGTPhW8XVaW64O_BDeY7k7Tq6yZXuacYZg ")

config = Config()
