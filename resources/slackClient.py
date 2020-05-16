import functools
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
from urllib.parse import quote_plus

from config import Config

inflect_engine = inflect.engine()

VERBS = {
    Config.COMMAND: ["send", "after", "in"]    
}

global_mentions = ['@channel', '@here']

time_period ={
    "second": {
        "mul_factor": 1
    }, 
    "minute": {
        "mul_factor": 60
    },
    "hour": {
        "mul_factor": 60*60
    }
}

time_travel_slack_client = WebClient(Config.SLACK_BOT_TOKEN)

pluck_payloads = lambda dict, *args: (dict[arg] for arg in args) #destructing the payloads to get required values from dict
quote_payload = lambda dict: { k : quote_plus(str(v)) for k,v in dict.items()}

def get_users():
    try:
        request = time_travel_slack_client.channels_info(token=Config.SLACK_BOT_TOKEN, channel='#ideas')
        if request['ok']:
            for item in request['members']:
                print(item['real_name'])
                print(item['deleted'])

    except SlackApiError as err:
        raise Exception(err)

def command_parser(payload):
    try:
        parts = payload["text"].split(" ")
        verb = VERBS[payload['command']]
        whom = parts[1]
        message = parts[2:]
            
        if whom in global_mentions and whom[0] == '@':
            whom = '@' + payload['channel_id'] 

        else:
            raise Exception("Mention Properly")
            
        find_index = 0
        count = 1
        for i in range(len(message)-1, 0, -1):
            if message[i] in verb:
                find_index = i
                count = 0
                break
        if count == 1:
            raise Exception("Error")

        text_message = message[:find_index]
        time_ = message[find_index+1:]
        message_to_send = f'<{whom}>' + " " + " ".join(i for i in text_message)
        timestamp = -1
        error = 0
        for k, v in time_period.items():
            if time_[1] in k or time_[1] in inflect_engine.plural(k):
                time_in_second = int(time_[0]) * int(v['mul_factor'])
                timestamp = time.time() + int(time_in_second)
                break
        if timestamp < 0 :
            raise Exception("error")

        payload['timestamp'] = timestamp
        payload['text'] = message_to_send
        return payload
    except Exception as err:
        raise err.with_traceback() #command Parser Error

def get_request_body(payload):
    quoted_payload = quote_payload(payload)
    token, team_id, team_domain, channel_id, channel_name, user_id, user_name, command, text, response_url, trigger_id = pluck_payloads(quoted_payload,
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
    return f'''token={token}&team_id={team_id}&team_domain={team_domain}&channel_id={channel_id}&channel_name={channel_name}&user_id={user_id}&user_name={user_name}&command={command}&text={text}&response_url={response_url}&trigger_id={trigger_id}'''

def generate_signature(request_body, timestamp):
    str_basestring = str.encode('v0:' + timestamp + ':' + get_request_body(request_body))
    sign_hash = 'v0=' + hmac.new(str.encode(Config.SLACK_SIGNING_SECRET), str_basestring, hashlib.sha256).hexdigest()
    return sign_hash

def compare_signature(hashed_signature, request_signature):
    return hmac.compare_digest(hashed_signature, request_signature)

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
        try:
            updateMsg = time_travel_slack_client.chat_scheduleMessage(
                channel=result['channel_id'],
                text=result['text'],
                post_at=result['timestamp'],
                as_user=True
            )
            assert updateMsg["message"]["text"] == result['text']
        except SlackApiError as err:
            raise err
    
        return result
    return wrapper

@with_logging
@sender_decorator
def send_message(payload, timestamp, signature):
    hashed_signature = generate_signature(payload, timestamp)
    if not compare_signature(hashed_signature,signature):
        abort(HTTPStatus.UNAUTHORIZED, message="Not A VAlid User")
    result = command_parser(payload)
    command, text, channel_id,timestamp = pluck_payloads(result, 'command', 'text', 'channel_id', 'timestamp') 

    return {"channel_id":channel_id, "timestamp":timestamp, "text":text }

