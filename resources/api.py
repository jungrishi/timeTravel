from http import HTTPStatus
from flask_restplus import Api

authorizations = {
    "slackKey": {
        "type": "slackKey",
        "in": "header",
        "name": "Authorization",
        "template": "Bearer {slackKey}"
    }
}

api = Api(
    version="1",
    title="API-v1",
    description="TimeTravel API v1",
    prefix="/api/v1",
    authorizations=authorizations
)

@api.errorhandler(BaseException)
def not_found_error(error):
    return error