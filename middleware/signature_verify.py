from functools import wraps
import random
import hashlib
import hmac
from urllib.parse import quote_plus
from flask import request, Response 
from werkzeug.datastructures import ImmutableMultiDict, MultiDict

from config import Config
from slack.errors import SlackApiError, SlackClientError, SlackRequestError

quote_payload = lambda dict: { k : quote_plus(str(v)) for k,v in dict.items()}

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

def signature_verification_middleware(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        payload = MultiDict(request.form)
        print(payload)
        print(payload.get('text'))
        hashed_sign = generate_signature()
        return func(*args, **kwargs)
    return decorated_function        