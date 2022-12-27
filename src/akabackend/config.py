import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    SECRET_KEY = '57e19ea558d4967a552d0d3deece34a70'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class ProductionConfig(Config):
    DEBUG = False
    # SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')

class DevelopmentConfig(Config):
    ENV="development"
    DEVELOPMENT=True
    DEBUG=True


# class Config(object):
#     # SECRET_KEY = os.environ.get('SECRET_KEY')
#     SECRET_KEY = '57e19ea558d4967a552d03deece34a70'
#     # SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URI')\
#         # or 'sqlite:///' + os.path.join(basedir, 'app.db')
#     # SQLALCHEMY_TRACK_MODIFICATIONS = False
#     # DEBUG = False

# # class Config(object):
# #     DEBUG = False
# #     TESTING = False
# #     CSRF_ENABLED = True
# #     SECRET_KEY = '57e19ea558d4967a552d03deece34a70'
# #     SQLALCHEMY_TRACK_MODIFICATIONS = False

# class ProductionConfig(Config):
#     DEBUG = False
#     DEVELOPMENT=False
#     # SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')

# class DevelopmentConfig(Config):
#     ENV="development"
#     DEVELOPMENT=True
#     DEBUG=True
# # SQLALCHEMY_DATABASE_URI="sqlite:///development_database.db"
