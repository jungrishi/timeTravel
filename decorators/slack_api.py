from config import Config

def verify_slack():
    def deco(token):
        if Config.SLACK_BOT_TOKEN == token:
            pass
        else:
            pass
    pass
    