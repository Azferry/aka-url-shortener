from flask import abort, Blueprint, jsonify, request
from app.common.UrlOperations import UrlOperations
from app.common.metrics import mmap, short_url_cr_measure,vanity_url_cr_measure, tmap
import logging
log = logging.getLogger('app')
app_name = __name__.split(".")[-1]
app = Blueprint(app_name, app_name)

@app.route('/heartbeat', methods=['GET'])
def heart_beat():
    return 'Hello World, Heart Beat - Root App'

@app.route('/robots933456.txt', methods=['GET'])
def appsrv_catch():
    """appsrv_catch is a dummy URL path that App Service uses to check if the container is serving requests.
    Catches the response to stop exceptions in application insights
    https://github.com/MicrosoftDocs/azure-docs/blob/main/includes/app-service-web-configure-robots933456.md
    Returns:
        str: robots933456.txt
    """
    return 'robots933456.txt'

@app.route('/', methods=['GET'])
def root():
    return "RootApp"