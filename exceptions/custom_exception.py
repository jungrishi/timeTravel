from http import HTTPStatus
import time

from exceptions.generic_exception import GenericException
from slack.errors import SlackClientError, SlackRequestError
from templates.message_templates import MessageTemplate

class BaseException(Exception):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    
    @classmethod
    def get_error_message(cls, message, response):
        return MessageTemplate(message, response).get_template()

class AuthException(GenericException):
    status = HTTPStatus.UNAUTHORIZED

class ClientException(BaseException):
    response=HTTPStatus.BAD_REQUEST

class RequestException(SlackRequestError):
    pass
    
class RequestTimeOutException(RequestException):
    message="Request TimeOut"
    response = HTTPStatus.REQUEST_TIMEOUT    
    
class InvalidSignature(AuthException):
    message = "Signature Mismatch"
    
class CommandParserException(ClientException):
    message="Message Wrong"
    
class UserMentionException(ClientException):
    message="Mention User To Send"  
    
    def get_message(self):
        return super.get_error_message()
     