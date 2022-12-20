
from flask import Flask, jsonify, request
from flask_restful import Resource, Api
import os
from os.path import join, dirname
from dotenv import load_dotenv

## Restful Resources Imports
from resources.ShortUrl import ShortUrl
from resources.Shorten import Shorten




dotenv_path = join(dirname(__file__), '.env')
load_dotenv()

# creating the flask app
app = Flask(__name__)
api = Api(app)

"""
V1 Default
"""
api.add_resource(ShortUrl, '/v1/<string:urlkey>')

"""
V1 Data
"""
# api.add_resource(Shorten, '/shorten')
api.add_resource(Shorten, '/v1/data/shorten')



if __name__ == '__main__':
    app.run(debug = False)
