from functools import wraps
import re
import time
from logger import logger
from datetime import timedelta, datetime
from slack import WebClient
from flask_restplus import abort
import inflect

from slack.errors import SlackApiError, SlackClientError, SlackRequestError
from slackeventsapi import SlackEventAdapter
import random
import hashlib
import hmac
from http import HTTPStatus
from utils.util_functions import pluck_payloads
from utils.command_parser import command_parser
from config import Config
from templates.message_templates import MessageTemplate

time_travel_slack_client = WebClient(Config.SLACK_BOT_TOKEN)

def with_logging(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        logger.debug("Running function '%s'", func.__name__)
        result = func(*args, **kwargs)
        logger.debug("Completed function '%s'", func.__name__)
        return result
    return wrapper

def schedule_message(result):
        try:
            updateMsg = time_travel_slack_client.chat_scheduleMessage(
                channel=result['channel_id'],
                text=result['text'],
                post_at=result['timestamp'],
                as_user=True
            )
            local_time=time.strftime("%a, %d %b %Y %H:%M:%S", time.localtime(result['timestamp']))
            return_data = MessageTemplate(result['text'], local_time)
            return return_data.get_template(), 200
        except SlackApiError as err:
            raise err

@with_logging
def send_message(payload):
    result = command_parser(payload)
    return schedule_message(result)
