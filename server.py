from flask import Flask, request, Response
from werkzeug.middleware.proxy_fix import ProxyFix
import json
from slack import WebClient

from  config import Config
from resources.api import api
from slashCommand import *
from logger import init_logging

def simple_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    return app

def create_app():
    app = simple_app()
    app.wsgi_app = ProxyFix(app.wsgi_app)
    
    api.init_app(app)
    
    init_logging(app)
    return app

if __name__ == '__main__':
    application = create_app()
    application.run(host='0.0.0.0', port=Config.PORT, debug=True)
