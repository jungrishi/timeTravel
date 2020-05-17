from http import HTTPStatus
from typing import Union

from flask import jsonify, Response

class GenericException(Exception):
    def __init__(self, message=None, detail=None,status=None):
        super(GenericException, self).__init__(self)
        if message:
            self.message = message
        if detail:
            self.detail = detail
        if status:
            self.status = status
        if not self.detail:
            self.detail = self.status.phrase
        if not self.message:
            self.message = self.status.description
        self.type = 'mrkdwn'
            
        def get_response(self):
            map_dict = self.__dict__()
            response = jsonify(map_dict)
            response.status_code = self.status.value
            return response

        def __dict__(self):
            data = {
            'status': self.status.value,
            'detail': self.detail,
            'message': self.message,
            'type':self.type,
            "response_type": "ephemeral"
        }
            return data

        def __str__(self):
            return str({
            'error': self.detail,
            'status': self.status
        })