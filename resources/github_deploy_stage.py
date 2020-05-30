from flask_restplus import Resource, abort

from slack.errors import SlackApiError
from http import HTTPStatus
from resources.api import api as github_api

@github_api.route("/slack/deploy-state")
class GIthubWebhook(Resource):
    def get(self):
        return "Hello! POST for any meaningful resource"
    def post(self):
        return "Hello"