from flask import Flask, jsonify, request,redirect
from flask_restful import Resource, Api



class ShortUrl(Resource):

    def get(self, urlkey):

        # If short url exists return site
        # else short does not exist in db return error page
        return redirect("http://www.google.com", code=301)
        # return jsonify({'long': urlkey})
