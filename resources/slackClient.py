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
import hmac
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

def get_request_body(payload):
    token, team_id, team_domain, channel_id, channel_name, user_id, user_name, command, text, response_url, trigger_id = pluck_payloads(payload,
                                                                                                                        'token',
                                                                                                                        'team_id',
                                                                                                                        'team_domain',
                                                                                                                        'channel_id',
                                                                                                                        'channel_name',
                                                                                                                        'user_id',
                                                                                                                        'user_name',
                                                                                                                        'command',
                                                                                                                        'text',
                                                                                                                        'response_url',
                                                                                                                        'trigger_id')
    return f'''token={token}
                team_id={team_id}&
                team_domain={team_domain}&
                channel_id={channel_id}&
                channel_name={channel_name}&
                user_id={user_id}&
                user_name={user_name}&
                command={command}&
                text={text}&
                response_url={response_url}&
                trigger_id={trigger_id}'''

def generate_signature(request_body, timestamp):
    str_basestring = str.encode('v0:' + timestamp + ':' + get_request_body(request_body))
    sign_hash = 'v0=' + hmac.new(str.encode(Config.SLACK_SIGNING_SECRET), str_basestring, hashlib.sha256).hexdigest()
    return sign_hash

def compare_signature(hashed_signature, request_signature):
    aa = hmac.compare_digest(hashed_signature, request_signature)
    print(aa)
    print("************")
    return aa

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
    hashed_signature = generate_signature(payload, timestamp)
    if not compare_signature(hashed_signature,signature):
        abort(HTTPStatus.METHOD_NOT_ALLOWED, message="Cannot Verify The App")
        
    command, text, channel_id = pluck_payloads(payload, 'command', 'text', 'channel_id') 
    print(command)

