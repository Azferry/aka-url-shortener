


# from app import create_app


# __version__ = "3.2"

# if __name__ == '__main__':
#     app = create_app()
#     # app.run(host='0.0.0.0', port=8000)
#     app.run()

import logging
from flask import Flask
from config import Config, __version__
from logging import DEBUG
from app.common.sqldb import init_db #sqldb_create
from opencensus.ext.azure.trace_exporter import AzureExporter
from opencensus.ext.flask.flask_middleware import FlaskMiddleware
from opencensus.trace.samplers import ProbabilitySampler
from opencensus.ext.azure.log_exporter import AzureLogHandler
from opencensus.ext.azure import metrics_exporter
import sys
import os
# sys.path.insert(0, os.getcwd())

def configure_logging(app):
    # Deactivate the default flask logger so that log messages don't get duplicated 
    # from flask.logging import default_handler
    # app.logger.removeHandler(default_handler)

    logger = logging.getLogger(__name__)
    az_appinsights_handler  = AzureLogHandler(connection_string=Config.APPINSIGHTS_CONNSTR)
    
    log_formatter = logging.Formatter('%(asctime)s %(levelname)s: %(message)s [in %(filename)s: %(lineno)d]')

    # Apply the file formatter object to the file handler object
    az_appinsights_handler.setFormatter(log_formatter)
    logger.addHandler(az_appinsights_handler)
    app.logger.setLevel(DEBUG)
    return

def create_app(config_class=Config):
    app = Flask(__name__)

    configure_logging(app)
    
    # app.config.from_object(config_class)
    
    app.logger.info("Initializing Application")
    init_db()

    middleware = FlaskMiddleware(
        app,
        exporter=AzureExporter(connection_string=Config.APPINSIGHTS_CONNSTR),
        sampler=ProbabilitySampler(rate=1.0),
    )

    exporter = metrics_exporter.new_metrics_exporter(
        enable_standard_metrics=False,
        connection_string=Config.APPINSIGHTS_CONNSTR)

    def callback_function(envelope):
        envelope.tags['ai.cloud.role'] = Config.ROLE
        return True

    middleware.exporter.add_telemetry_processor(callback_function)

    @app.route('/')
    def heart_beat():
        return 'Hello World, Heart Beat - Root App'

    import app.api as api
    app.logger.info("Initializing API Blueprints")
    api.init_app(app, version=__version__, title=Config.APP_TITLE)
    

    return app

# if __name__ == '__main__':
#     app = create_app()
#     app.run()
    # app = create_app()
    # app.run()
    # if app.config["HOST_TYPE"].lower() == "azwebapp":
    #     app.run(host='0.0.0.0',port=5000)
    # else:
    #     PORT = int(os.getenv('PORT', 5000))
    #     app.run(port=PORT, threaded=True)


# To run Flask under uWSGI in a Docker environment, you must first add lazy-apps = true to the uWSGI configuration file 
# (uwsgi.ini). For more information, see the issue description.
