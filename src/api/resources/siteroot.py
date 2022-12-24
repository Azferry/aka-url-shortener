from flask import Flask, jsonify, request,redirect
from flask_restful import Resource, Api, reqparse
from common.UrlOperations import UrlOperations


class siteroot(Resource):
    def __init__(self) -> None:
        pass

    def get(self):
        # If short url exists return site
        # else short does not exist in db return error page
        return

