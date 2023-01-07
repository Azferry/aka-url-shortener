from flask import abort, Blueprint, jsonify, request
from app.common.UrlOperations import UrlOperations
from app.common.metrics import mmap, short_url_cr_measure,vanity_url_cr_measure, tmap
import logging
log = logging.getLogger('app')
app_name = __name__.split(".")[-1]
app = Blueprint(app_name, app_name)


@app.route('/v1/shorten/<string:shortcode>', methods=['GET'])
def shortenurl(shortcode):
    urlOps = UrlOperations()
    ul = urlOps.getLongUrl(shortcode)
    if ul == None:
        return jsonify({'Return': "URL Not Found"})
    return jsonify({'longUrl': ul, 'shortUrl': shortcode})

@app.route('/v1/shorten', methods=['POST'])
def create():
    """create _summary_
    Args:
        longurl(str): 
        vaniety(str, optional): 
    Methods: POST
    Returns:
        201: If the short url was created 
        200: The vanity url already exists 
    """
    longurl = request.args.get('longurl')
    vaniety = request.args.get('vaniety')
    urlOps = UrlOperations()
    if vaniety:
        ch = urlOps.checkIfShortUrlExists(str(vaniety))
        if ch == False:
            shorturl = urlOps.createShortUrl(longUrl=str(longurl), vaniety=str(vaniety))
            mmap.measure_int_put(vanity_url_cr_measure, 1)
            mmap.record(tmap)
        else:
            return jsonify({'Return': "Vaniety URL Name not aviable."})
    else:
        shorturl = urlOps.createShortUrl(longUrl=str(longurl))
        mmap.measure_int_put(short_url_cr_measure, 1)
        mmap.record(tmap)
    response = jsonify(shorturl)
    response.status_code = 201
    return response

@app.route('/v1/shorten/<string:shortcode>', methods=['DELETE'])
def delete(shortcode):

    return NotImplemented
