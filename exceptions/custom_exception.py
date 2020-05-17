from http import HTTPStatus

from exceptions.generic_exception import GenericException
from slack.errors import SlackClientError, SlackRequestError

class AuthException(GenericException):
    status = HTTPStatus.UNAUTHORIZED

class ClientException(SlackClientError):
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