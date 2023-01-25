import os
import datetime

# 開発環境のconfig
class Development(object):
    SECRET_KEY = os.urandom(24)
    PORT = 5000
    HOST = "127.0.0.1"
    DEBUG = True
    TESTING = False
    JSON_AS_ASCII = False
    JSON_SORT_KEYS = False
    JWT_TOKEN_LOCATION = ["headers"]
    JWT_ACCESS_TOKEN_EXPIRES = datetime.timedelta(days=1)
    JWT_ACCESS_CSRF_HEADER_NAME = "X-CSRF-TOKEN-ACCESS"


# テスト環境のconfig
class Testing(object):
    SECRET_KEY = os.urandom(24)
    PORT = 5000
    HOST = "127.0.0.1"
    DEBUG = True
    TESTING = True
    JSON_AS_ASCII = False
    JSON_SORT_KEYS = False
    JWT_TOKEN_LOCATION = ["headers"]
    JWT_ACCESS_TOKEN_EXPIRES = datetime.timedelta(days=1)
    JWT_ACCESS_CSRF_HEADER_NAME = "X-CSRF-TOKEN-ACCESS"


# 本番環境のconfig
class Production(object):
    SECRET_KEY = os.urandom(24)
    PORT = 5000
    HOST = "127.0.0.1"
    DEBUG = False
    TESTING = False
    JSON_AS_ASCII = False
    JSON_SORT_KEYS = False
    JWT_TOKEN_LOCATION = ["headers"]
    JWT_ACCESS_TOKEN_EXPIRES = datetime.timedelta(days=1)
    JWT_ACCESS_CSRF_HEADER_NAME = "X-CSRF-TOKEN-ACCESS"
