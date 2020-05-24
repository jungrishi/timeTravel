from dotenv import load_dotenv
import os

class BaseConfig():
    load_dotenv(verbose=True)
    SLACK_BOT_TOKEN = os.getenv("SLACK_BOT_TOKEN")
    LOG_LEVEL = os.getenv("LOG_LEVEL", "DEBUG")
    LOG_PATH = os.getenv("LOG_PATH", "logs/timeTravel.log")
    PORT = os.getenv("PORT", 33507)
    SLACK_SIGNING_SECRET = os.getenv("SLACK_SIGNING_SECRET", "")
    COMMAND = os.getenv("SLACK_COMMAND", "/test-travel")
    BOT_ICON = os.getenv("BOT_ICON", ':godmode:')

Config = BaseConfig()    