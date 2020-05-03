from flask import Flask, g, Response, request
import logging
from config import Config
from logzero import logfile, logger, loglevel
import time
from uuid import uuid4

FORMAT = '%(asctime)-15s || %(message)s'

def init_logging(app:Flask):
    # logging.basicConfig(format=FORMAT)
    logger = logging.getLogger("timeTravel")
    logger.setLevel(Config.LOG_LEVEL)
        
    if Config.LOG_PATH:
        logfile(
            Config.LOG_PATH,
            maxBytes=1000000,
            backupCount=3,
            loglevel=Config.LOG_LEVEL,
        )
    _register_before_request(app)
    _register_after_request(app)
        

def _register_before_request(app: Flask):
    def before_request():
        """
            A function to run before each request.
        """
        g.start_time = time.time()
        g.request_id = uuid4().hex

    app.before_request(before_request)
    

def _register_after_request(app: Flask):
    encoder = app.json_encoder()

    def after_request(response: Response):
        """
            A function to run after each request.
        """
        execution_time = time.time() - g.start_time

        try:
            logger.debug({
                "url_rule": request.url_rule,
                "execution_time": execution_time,
                "request_id": g.request_id,
                "request": {
                    "method": request.method,
                    "url": request.url,
                    "payload": encoder.encode(request.json) if request.is_json and request.json and len(
                        request.data) > 0 else ""
                },
                "response": {
                    "status": response.status,
                    "payload": encoder.encode(response.json) if response.is_json and response.json and len(
                        response.data) > 0 else ""
                }
            })
        except Exception as e:
            # Log Exception but otherwise don't do anything since we don't want to fail a customer request b/c our
            # logging is broken
            logger.error(e)

        return response

    app.after_request(after_request)
    