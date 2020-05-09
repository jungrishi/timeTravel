from http import HTTPStatus
from flask_restplus import Api

from logger import logger

authorizations = {
    "slackKey": {
        "type": "slackKey",
        "in": "header",
        "name": "Authorization",
        "template": "{slackKey}"
    }
}

api = Api(
    version="1",
    title="API-v1",
    description="TimeTravel API v1",
    prefix="/api/v1",
    authorizations=authorizations
)

@api.errorhandler(GenericException)
def generic_exception(error: GenericException):
    logger(error)
    return error.get_response()
