from flask import Flask, jsonify, request,redirect
from flask_restful import Resource, Api, reqparse
from common.UrlOperations import UrlOperations

parser = reqparse.RequestParser()
parser.add_argument('url', location='args')

class Shorten(Resource):
    def __init__(self) -> None:
        # super().__init__()
        self.urlOps = UrlOperations()
        pass

    def get(Resource):
        return jsonify({'message': 'hello world'})

    def post(self):
        args = parser.parse_args()
        arg1 = str(args['url'])
        shorturl = self.urlOps.createShortUrl(longUrl=arg1)
        response = jsonify(shorturl)
        response.status_code = 201
        return response

