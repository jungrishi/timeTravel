from flask_restplus import Resource, abort
from flask import request
from datetime import datetime, timedelta
from slack.errors import SlackApiError
from http import HTTPStatus

from resources.slackClient import send_message
from resources.api import api as slack_api

@slack_api.route("/slack/test")
class SlackTest(Resource):
    def get(self):
        return "Hello"
    
    def post(self):
        print("Api***********8")
        print(request.get_json())
        print(request.form)
        # info = request.form
        current_time = datetime.now()
        future_time = (current_time + timedelta(minutes=1)).timestamp()
        msg = 'Welcome Scheduled Message In python'
        try:
            send_message(msg, future_time)
        except SlackApiError as error:
            abort(HTTPStatus.BAD_REQUEST, "Please tRY")