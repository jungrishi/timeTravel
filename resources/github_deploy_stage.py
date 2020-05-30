from flask_restplus import Resource, abort
from json import dumps
from flask import request
from slack.errors import SlackApiError
from http import HTTPStatus
from resources.api import api as github_api
from services.githubClient import send_message

@github_api.route("/slack/deploy-state")
class GIthubWebhook(Resource):
    def get(self):
        return "Hello! POST for any meaningful resource"
    def post(self):
        payload = request.get_json()
        try:
            send_message(payload)
            return dumps({'msg': 'success'})
        except Exception as err:
            return dumps({'err': err})