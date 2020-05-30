import logging

from slashCommand import SlackClient
from slack.errors import SlackApiError
from config import Config
from templates.message_templates import MessageTemplate

logger = logging.getLogger(__name__)

class Bot(object):
    def __init__(self, client_data):
        logger.info('Bot Connecting to SlackClient')
        self.client_api = SlackClient(
            Config.SLACK_BOT_TOKEN,
            bot_icon=Config.BOT_ICON if hasattr(Config, 'BOT_ICON') else None,
            bot_emoji=Config.BOT_EMOJI  if hasattr(Config, 'BOT_EMOJI') else None
        )
        logger.info('Bot Connection Complete')
        self.client_data = client_data
        
    def default_reply(self):
        return MessageTemplate(
            message=self.client_data['message'],
            time=self.client_data['timestamp']
        ).get_template()
        
    def send_status_message(self):
        channel_id = Config.CLIENT_ID
        post_message = self.client_api.post_message(channel_id, self.client_data)
        if post_message:
            return True
        else:
            raise Exception()
    
    def send_message(self):
        scheduled_message = self.client_api.schedule_message(
            channel=self.client_data['channel_id'], 
            message=self.client_data['message'], 
            timestamp=self.client_data['timestamp']
            )
        if scheduled_message:
            return True
        else:
            raise Exception()