
import os
import logging
from flask import Flask
from config import Config, __version__
from logging import DEBUG
from common.sqldb import init_db #sqldb_create
from opencensus.ext.azure.trace_exporter import AzureExporter
from opencensus.ext.flask.flask_middleware import FlaskMiddleware
from opencensus.trace.samplers import ProbabilitySampler
from opencensus.ext.azure.log_exporter import AzureLogHandler
from opencensus.ext.azure import metrics_exporter


def create_app(config_class=Config):
    init_db()
    app = Flask(__name__)
    logger = logging.getLogger(__name__)
    logger.addHandler(AzureLogHandler(connection_string=Config.APPINSIGHTS_CONNSTR))
    
    app.config.from_object(config_class)
    app.logger.setLevel(DEBUG)

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

    import api
    api.init_app(app, version=__version__, title=Config.APP_TITLE)

    return app

if __name__ == '__main__':
    app = create_app()
    if app.config["HOST_TYPE"].lower() == "azwebapp":
        app.run()
    else:
        PORT = int(os.getenv('PORT', 5000))
        app.run(port=PORT, threaded=True)


# To run Flask under uWSGI in a Docker environment, you must first add lazy-apps = true to the uWSGI configuration file 
# (uwsgi.ini). For more information, see the issue description.