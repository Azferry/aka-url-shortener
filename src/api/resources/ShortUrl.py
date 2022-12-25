from flask import Flask, jsonify, request,redirect
from flask_restful import Resource, Api, reqparse
from common.UrlOperations import UrlOperations

parser = reqparse.RequestParser()
parser.add_argument('url', location='args')

class ShortUrl(Resource):
    def __init__(self) -> None:
        self.urlOps = UrlOperations()
        pass

    def get(self, shortcode):
        ul = self.urlOps.getLongUrl(shortcode)
        if ul == None:
            return
        return redirect(ul) #, code=302)

    def delete(self, shortcode):
        return

    # def post(self):
    #     args = parser.parse_args()
    #     arg1 = str(args['url'])
    #     shorturl = self.urlOps.createShortUrl(longUrl=arg1)
    #     response = jsonify(shorturl)
    #     response.status_code = 201
    #     return response
