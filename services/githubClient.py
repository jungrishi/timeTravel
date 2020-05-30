from decorators.logging import with_logging
from bot import Bot

@with_logging
def send_message(payload):
    print(payload)
    parse_github_request(payload)
    bot = Bot(payload)
    
def parse_github_request(payload):
    message_template = "message" 