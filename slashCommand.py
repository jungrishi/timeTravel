import time

from slack.errors import SlackApiError, SlackClientError, SlackRequestError
from slack import WebClient

from config import Config
from templates.message_templates import MessageTemplate

class SlackClient():
    def __init__(self, token, timeout=None, bot_icon=None, bot_emoji=None, connect=True):
        self.token = token
        self.bot_icon=bot_icon
        self.bot_emoji = bot_emoji
        self.username=None
        self.domain=None
        self.users = {}
        self.channels = {}

        self.time_travel_slack_client = WebClient(self.token) #Implement TimeOut v2.0
        
    def get_user(self, user_id):
        return self.users.get(user_id)
    
    def get_channel(self, channel_id):
        return #Channel(self, self.channels[channel_id])
    
    def schedule_message(self, channel, message, timestamp, as_user=True):
        try:
            scheduled_message = self.time_travel_slack_client.chat_scheduleMessage(
                channel=channel,
                text=message,
                post_at=timestamp,
                as_user=as_user
            )
            if scheduled_message['ok'] is True:
                return True
            else:
                raise SlackApiError("Message Not Send")
        except SlackApiError as err:
            raise SlackApiError('', MessageTemplate(
                "Error Sending Scheduled Message",
                time=time.time()
            ).get_template())