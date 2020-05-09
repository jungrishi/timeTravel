import functools
import os
import time
from logger import logger
from datetime import timedelta, datetime
from slack import WebClient
from config import Config

time_travel_slack_client = WebClient(Config.SLACK_BOT_TOKEN)

# is_ok = time_travel_slack_client.api_call("users.list").get('ok')

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
    is_ok = time_travel_slack_client.api_call("users.list").get('ok')
    logger.debug("IS_OK",is_ok)
    
    updateMsg = time_travel_slack_client.chat_scheduleMessage(
        channel="#welcome",
        text=msg,
        post_at=future_time,
        as_user=True
    )
    

