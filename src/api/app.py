
from flask import Flask
from flask_restful import Api
from os.path import join, dirname
from dotenv import load_dotenv

## Restful Resources Imports
from resources.ShortUrl import ShortUrl
from resources.siteroot import siteroot
from resources.CreateUrl import CreateUrl

dotenv_path = join(dirname(__file__), '.env')
load_dotenv()

# creating the flask app
app = Flask(__name__)
api = Api(app)

"""
Root Landing
"""
# api.add_resource(siteroot, '/')
api.add_resource(ShortUrl, '/<string:shortcode>')

"""
V1
"""
api.add_resource(CreateUrl, '/v1/CreateUrl')


if __name__ == '__main__':
    app.run(debug = False)
