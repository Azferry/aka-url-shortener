import uuid
# import jsonpatch
from flask import abort, Blueprint, jsonify, request, redirect
from common.UrlOperations import UrlOperations
app_name = __name__.split(".")[-1]
app = Blueprint(app_name, app_name)


@app.route('/v1/shorten/<string:shortcode>')
def shortenurl(shortcode):
    urlOps = UrlOperations()
    ul = urlOps.getLongUrl(shortcode)
    if ul == None:
        return jsonify({'Return': "URL Not Found"})
    return jsonify({'longUrl': ul, 'shortUrl': shortcode})

@app.route('/v1/shorten/<string:longurl>', methods=['POST'])
def create(longurl):
    urlOps = UrlOperations()
    arg1 = str(longurl)
    shorturl = urlOps.createShortUrl(longUrl=arg1)
    response = jsonify(shorturl)
    response.status_code = 201
    return response

@app.route('/v1/shorten', methods=['POST'])
def createvanity():
    longurl = request.args.get('longurl')
    vaniety = request.args.get('vaniety')
    urlOps = UrlOperations()
    shorturl = urlOps.createShortUrl(longUrl=str(longurl), vaniety=str(vaniety))
    response = jsonify(shorturl)
    response.status_code = 201
    return response

@app.route('/v1/shorten/<string:shortcode>', methods=['DELETE'])
def delete(shortcode):

    return NotImplemented
