import functools
import os
import time
from logger import logger
from datetime import timedelta, datetime
from slack import WebClient
from config import Config

slack_client = WebClient(Config.SLACK_BOT_TOKEN)

def with_logging(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        logger.debug("Running function '%s'", func.__name__)
        result = func(*args, **kwargs)
        logger.debug("Completed function '%s'", func.__name__)
        return result
    return wrapper

@with_logging
def send_message(slack_client, msg, future_time):
    updateMsg = slack_client.chat_scheduleMessage(
        channel="#welcome",
        text=msg,
        post_at=future_time,
        as_user=True
    )
    

