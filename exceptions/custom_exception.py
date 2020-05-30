from http import HTTPStatus
import time

from exceptions.generic_exception import GenericException
from slack.errors import SlackClientError, SlackRequestError
from templates.message_templates import MessageTemplate

class AuthException(GenericException):
    def __init__(self, status,message=None):
        self.status = HTTPStatus.UNAUTHORIZED
        self.message = message

class ClientException(GenericException):
    def __init__(self, status=None, message = None, **kwargs):
        self.status = HTTPStatus.BAD_REQUEST
        self.message = message
        super().__init__(self.status, self.message)

class RequestException(SlackRequestError):
    pass
    
class RequestTimeOutException(GenericException):
    def __init__(self, status, message = None):
        self.status = HTTPStatus.REQUEST_TIMEOUT
        self.message = message
    
class InvalidSignature(AuthException):
    message = "Signature Mismatch"
    
class CommandParserException(ClientException):
    message="Message Wrong"
    
class UserMentionException(ClientException):
    def __init__(self, status=None, message=None):
        self.message = "Mention User Properly"
        super().__init__(self.message)
