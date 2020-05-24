import time
from datetime import timedelta, datetime
from slack import WebClient
from flask_restplus import abort
import inflect

from decorators.logging import with_logging
from utils.command_parser import command_parser
from bot import Bot

@with_logging
def send_message(payload):
    result = command_parser(payload)
    bot = Bot(result)
    is_send = bot.send_message()
    if is_send:
        return bot.default_reply()
