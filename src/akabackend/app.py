from dotenv import load_dotenv
load_dotenv() # before other imports so os.getenv will include .env values
import os
from flask import Flask
from config import Config
import traceback
from logging import DEBUG



def create_app(config_class=Config):
    app = Flask(__name__)
    # app.config.from_object(config_class)
    app.config.from_object('config.DevelopmentConfig')
    app.logger.setLevel(DEBUG)

    import api
    api.init_app(app, version='1.0.0', title='AKA URL Shortner API')

    @app.route('/test')
    def test_page():
        return 'Hello World'


    return app

if __name__ == '__main__':
    PORT = int(os.getenv('PORT', 5000))
    app = create_app()
    app.run(debug = False, port=PORT)
