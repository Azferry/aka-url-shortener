from flask import abort, Blueprint, jsonify, request, redirect
from common.UrlOperations import UrlOperations
from common.metrics import mmap, short_url_cr_measure,vanity_url_cr_measure, tmap
app_name = __name__.split(".")[-1]
app = Blueprint(app_name, app_name)


@app.route('/v1/shorten/<string:shortcode>', methods=['GET'])
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
    mmap.measure_int_put(short_url_cr_measure, 1)
    mmap.record(tmap)
    response = jsonify(shorturl)
    response.status_code = 201
    return response

@app.route('/v1/shorten', methods=['POST'])
def createvanity():
    longurl = request.args.get('longurl')
    vaniety = request.args.get('vaniety')
    urlOps = UrlOperations()
    shorturl = urlOps.createShortUrl(longUrl=longurl, vaniety=str(vaniety))
    mmap.measure_int_put(vanity_url_cr_measure, 1)
    mmap.record(tmap)
    response = jsonify(shorturl)
    response.status_code = 201
    return response

@app.route('/v1/shorten/<string:shortcode>', methods=['DELETE'])
def delete(shortcode):

    return NotImplemented
