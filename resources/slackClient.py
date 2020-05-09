import functools
import os
import time
from logger import logger
from datetime import timedelta, datetime
from slack import WebClient
from flask_restplus import abort

from config import Config

time_travel_slack_client = WebClient(Config.SLACK_BOT_TOKEN)

def with_logging(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        logger.debug("Running function '%s'", func.__name__)
        result = func(*args, **kwargs)
        logger.debug("Completed function '%s'", func.__name__)
        return result
    return wrapper

@with_logging
def send_message(msg, future_time):
    # is_ok = time_travel_slack_client.api_call("users.list").get('ok')
    try:
        updateMsg = time_travel_slack_client.chat_scheduleMessage(
            channel="#welcome",
            text=msg,
            post_at=future_time,
            as_user=True
        )
        logger.debug('print slack-api',updateMsg)
    except:
        abort(500, "Server Error")

