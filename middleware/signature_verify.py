from functools import wraps
import hashlib
import hmac
from urllib.parse import quote_plus
from flask import request, Response, abort 
import requests
import time
from werkzeug.datastructures import ImmutableMultiDict, MultiDict
from http import HTTPStatus

from slack.errors import SlackRequestError, SlackClientError, SlackApiError
from exceptions.custom_exception import AuthException, RequestTimeOutException, InvalidSignature
from config import Config
from utils.util_functions import quote_payload, pluck_payloads

def get_request_body(req):
    payload = {}
    payload['token'] = req.get('token')
    payload['team_id'] = req.get('team_id')
    payload['team_domain'] = req.get('team_domain')
    payload['channel_id'] = req.get('channel_id')
    payload['channel_name'] = req.get('channel_name')
    payload['user_id'] = req.get('user_id')
    payload['user_name'] = req.get('user_name')
    payload['command'] = req.get('command')
    payload['text'] = req.get('text')
    payload['response_url'] = req.get('response_url')
    payload['trigger_id'] = req.get('trigger_id')
    
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
        timestamp = request.headers['X-Slack-Request-Timestamp']
        signature = request.headers['X-Slack-Signature']
        if abs(time.time() - float(timestamp)) > 60 * 3:
            raise SlackApiError("cannnnno", response=HTTPStatus.REQUEST_TIMEOUT)
        get_form_body = MultiDict(request.form)
        hashed_signature = generate_signature(get_form_body, timestamp)
        if compare_signature(hashed_signature, signature):
            return func(*args, **kwargs)
        else:
            raise SlackApiError("Cannnot verify signature", response=HTTPStatus.FORBIDDEN)
    return decorated_function
