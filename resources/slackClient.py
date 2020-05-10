import functools
import os
import time
from logger import logger
from datetime import timedelta, datetime
from slack import WebClient
from flask_restplus import abort
from slackeventsapi import SlackEventAdapter
import random
import hashlib
from http import HTTPStatus
from operator import itemgetter

from config import Config

time_travel_slack_client = WebClient(Config.SLACK_BOT_TOKEN)

pluck_payloads = lambda dict, *args: (dict[arg] for arg in args) #destructing the payloads to get required values from dict

def is_private(event):
    return event.get("channel").startswith('D')

def get_mention():
    return '@here'

def send_response(user_mention):
    response_template = random.choice(['Sup, {mention}...',
                                       'Yo!',
                                       'Hola {mention}',
                                       'Bonjour!'])
    
    return response_template.format(mention=user_mention)

def generate_signature(request_body, timestamp):
    str_basestring = 'v0:' + timestamp + ':' + request_body
    my_signature = 'v0=' + hashlib.sha256(Config.SLACK_SIGNING_SECRET, str_basestring).hexdigest()
    return my_signature

def compare_signature(hashed_signature, request_signature):
    signature, salt = hashed_signature.split(':')
    return signature == hashlib.sha256(salt.encode() + request_signature.encode()).hexdigest()

def with_logging(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        logger.debug("Running function '%s'", func.__name__)
        result = func(*args, **kwargs)
        logger.debug("Completed function '%s'", func.__name__)
        return result
    return wrapper

def sender_decorator(func):
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        print(result)
        # updateMsg = time_travel_slack_client.chat_scheduleMessage(
        #     channel=result['channel_id'],
        #     text=result['text'],
        #     post_at=result['time_stamp'],
        #     as_user=True
        # )
        return result
    return wrapper

@with_logging
@sender_decorator
def send_message(payload, timestamp, signature):
    print(payload)
    hashed_signature = generate_signature(payload, timestamp)
    if not compare_signature(hashed_signature,signature):
        abort(HTTPStatus.METHOD_NOT_ALLOWED, HTTPStatus.METHOD_NOT_ALLOWED.phrase)
        
    command, text, channel_id = pluck_payloads(payload, 'command', 'text', 'channel_id') 
    print(command)

