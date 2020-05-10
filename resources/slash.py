from flask_restplus import Resource, abort, reqparse
from flask import request
from datetime import datetime, timedelta
from slack.errors import SlackApiError
from http import HTTPStatus
from werkzeug.datastructures import ImmutableMultiDict, MultiDict
import time

from resources.slackClient import send_message
from resources.api import api as slack_api


parser = reqparse.RequestParser()
parser =slack_api.parser()

parser.add_argument('token', required = True, type=str, location = 'form')
parser.add_argument('team_id', required = True, type=str, location = 'form')
parser.add_argument('team_domain', required = True, type=str, location = 'form')
parser.add_argument('channel_id', required = True, type=str, location = 'form')
parser.add_argument('channel_name', required = True, type=str, location = 'form')
parser.add_argument('user_id', required = True, type=str, location = 'form')
parser.add_argument('user_name', required = True, type=str, location = 'form')
parser.add_argument('command', required = True, type=str, location = 'form')
parser.add_argument('text', required = True, type=str, location = 'form')
parser.add_argument('response_url', required = True, type=str, location = 'form')
parser.add_argument('trigger_id', required = True, type=str, location = 'form')

@slack_api.route("/slack/test")
class SlackTest(Resource):
    def get(self):
        return "Hello"
    
    @slack_api.doc(parser=parser)
    def post(self):
        payload = parser.parse_args()
        timestamp = request.headers['X-Slack-Request-Timestamp']
        signature = request.headers['X-Slack-Signature']
        if abs(time.time() - float(timestamp)) > 60 * 30:
            abort(HTTPStatus.NOT_ACCEPTABLE, HTTPStatus.NOT_ACCEPTABLE.phrase)
        try:
            send_message(payload,timestamp, signature)
            return payload
        except SlackApiError as error:
            abort(HTTPStatus.BAD_REQUEST, error)