from dotenv import load_dotenv
import os

class BaseConfig():
    load_dotenv(verbose=True)
    SLACK_BOT_TOKEN = os.getenv("SLACK_BOT_TOKEN")
    LOG_LEVEL = os.getenv("LOG_LEVEL", "DEBUG")
    LOG_PATH = os.getenv("LOG_PATH", "logs/timeTravel.log")
    PORT = os.getenv("PORT", 33507)
    SLACK_SIGNING_SECRET = os.environ("SLACK_SIGNING_SECRET", "")
    
Config = BaseConfig()    