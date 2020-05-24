from http import HTTPStatus
from typing import Union
import logging
from flask import jsonify, Response

class GenericException(Exception):
    def __init__(self, message=None, status=None):
        super(GenericException, self).__init__(self)
        if message:
            self.message = message
        if status:
            self.status = status
        self.detail = self.status.phrase
        if not self.message:
            self.message = self.status.description

        def get_response(self):
            map_dict = self.__dict__()
            response = jsonify(map_dict)
            response.status_code = self.status.value
            logging.debug("Exception")
            logging.debug(response)
            logging.debug(map_dict)
            logging.debug("******************")
            return map_dict

        def __dict__(self):
            data = {
                    "blocks": [
                        {
                            "type": "section",
                            "text": {
                                "type": "mrkdwn",
                                "text":f"{self.message}"
                            }
                        },
                        {
                            "type": "actions",
                            "elements": [
                                {
                                    "type": "button",
                                    "text": {
                                        "type": "plain_text",
                                        "text": "Examples",
                                        "emoji": True
                                    },
                                    "value": "click_me_123"
                            }
                        ]
                    },
                        {
        			"type": "section",
        			"fields": [
        				{
        					"type": "plain_text",
        					"text": "*this is plain_text text*",
        					"emoji": True
        				},
        				{
        					"type": "plain_text",
        					"text": "*this is plain_text text*",
        					"emoji": True
        				},
        				{
        					"type": "plain_text",
        					"text": "*this is plain_text text*",
        					"emoji": True
        				},
        				{
        					"type": "plain_text",
        					"text": "*this is plain_text text*",
        					"emoji": True
        				},
        				{
        					"type": "plain_text",
        					"text": "*this is plain_text text*",
        					"emoji": True
        				}
			]
		}
                ]
            }