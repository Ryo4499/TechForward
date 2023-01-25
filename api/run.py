import os
import ipaddress
import logging
import models
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from datetime import datetime
from flask import Flask
from flask.globals import request
from flask.helpers import make_response
from flask.json import jsonify
from flask_restful import Api
from models.setting import ENGINE, Session, CONNECTION
from jwt_token import init_jwt
from apis.auth import LoginAPI, LogoutAPI
from apis.user import UserAPI, UserPostAPI, UserSelfAPI
from apis.tag import (
    TagAPI,
    TagPostAPI,
    TagsAPI,
    TagsArticleAPI,
    TagsPopularAPI,
)
from apis.tag_admin import (
    TagAdminAPI,
)
from apis.user_modify import (
    UserModifyEmailAPI,
    UserModifyPasswordAPI,
    UserModifyUserNameAPI,
)
from apis.article import ArticleAPI, ArticlePostAPI
from apis.articles import (
    ArticlesAPI,
    ArticlesByUserAPI,
    ArticlesTagAPI,
    MyArticlesAPI,
    SearchByTitleArticleAPI,
)
from apis.articles_admin import (
    ArticlesAdminAPI,
    ArticlesByUserAdminAPI,
    ArticlesTagAdminAPI,
    SearchByTitleArticleAdminAPI,
)
from apis.comment import (
    CommentAPI,
    CommentPostAPI,
    MyCommentsAPI,
    CommentsByArticleAPI,
)
from apis.user_admin import UsersAdminAPI
from apis.comment_admin import (
    CommentsAdminAPI,
    CommentsByArticleAdminAPI,
    CommentsByUserAdminAPI,
    SearchCommentContentAdminAPI,
)


def create_app(test_config=None) -> Flask:
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object("config.Production")
    app.url_map.strict_slashes = False

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # ロギング
    os.makedirs("./log/", exist_ok=True)
    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)s %(name)-12s %(levelname)-8s %(message)s",
        datefmt="%m-%d %H:%M",
        handlers=[
            logging.FileHandler("./log/{:%Y-%m-%d}.log".format(datetime.now())),
            logging.StreamHandler(),
        ],
    )

    # dbの初期化
    models.init_db()
    # テストデータの挿入
    models.test_data()

    init_jwt(app)

    CORS(app, resources={r"/*": {"origins": "*"}})

    limiter = Limiter(
        get_remote_address,
        app=app,
        storage_uri="memcached://memcached:11211",
        default_limits=[
            "1080000 per day",
            "18000 per hour",
            "300 per minute",
            "5 per second",
        ],
    )

    api = Api(app, prefix="/api")

    api.add_resource(LoginAPI, "/login")
    api.add_resource(LogoutAPI, "/logout")

    api.add_resource(UserPostAPI, "/user")
    api.add_resource(UserSelfAPI, "/user/me")
    api.add_resource(UserAPI, "/user/<string:userId>")
    api.add_resource(UserModifyEmailAPI, "/user/<string:userId>/email")
    api.add_resource(UserModifyPasswordAPI, "/user/<string:userId>/password")
    api.add_resource(UserModifyUserNameAPI, "/user/<string:userId>/username")

    api.add_resource(TagPostAPI, "/tag")
    api.add_resource(TagAPI, "/tag/<string:tagId>")
    api.add_resource(TagsAPI, "/tags")
    api.add_resource(TagsPopularAPI, "/tags/popular")
    api.add_resource(TagsArticleAPI, "/tags/article/<string:articleId>")

    api.add_resource(ArticlesAPI, "/articles")
    api.add_resource(MyArticlesAPI, "/articles/me")
    api.add_resource(SearchByTitleArticleAPI, "/articles/title/<string:title>")
    api.add_resource(ArticlesByUserAPI, "/articles/user/<string:userName>")
    api.add_resource(ArticlesTagAPI, "/articles/tag/<string:tagName>")
    api.add_resource(ArticlePostAPI, "/article")
    api.add_resource(ArticleAPI, "/article/<string:articleId>")

    api.add_resource(CommentPostAPI, "/article/<string:articleId>/comment")
    api.add_resource(CommentAPI, "/comment/<string:commentId>")
    api.add_resource(MyCommentsAPI, "/comments/me")
    api.add_resource(CommentsByArticleAPI, "/comments/article/<string:articleId>")

    api.add_resource(UsersAdminAPI, "/admin/users")
    api.add_resource(TagAdminAPI, "/admin/tag/<string:tagId>")
    api.add_resource(ArticlesAdminAPI, "/admin/articles")
    api.add_resource(
        SearchByTitleArticleAdminAPI, "/admin/articles/title/<string:title>"
    )
    api.add_resource(ArticlesByUserAdminAPI, "/admin/articles/user/<string:userName>")
    api.add_resource(ArticlesTagAdminAPI, "/admin/articles/tag/<string:tagName>")
    api.add_resource(CommentsAdminAPI, "/admin/comments")
    api.add_resource(CommentsByUserAdminAPI, "/admin/comments/user/<string:userName>")
    api.add_resource(
        CommentsByArticleAdminAPI, "/admin/comments/article/<string:articleId>"
    )
    api.add_resource(
        SearchCommentContentAdminAPI, "/admin/comments/content/<string:content>"
    )

    # IPアドレスによるアクセス制限
    ALLOW_NETWORKS = ["172.16.0.0/12", "192.168.0.0/16", "127.0.0.1"]

    @app.before_request
    def before_request():
        req_address = ipaddress.ip_address(request.remote_addr)
        app.logger.info(req_address)

        for allow_network in ALLOW_NETWORKS:
            ip_network = ipaddress.ip_network(allow_network)
            if req_address in ip_network:
                app.logger.info(ip_network)
                return
        return make_response(
            jsonify({"error": "access denied from your IP address"}), 403
        )

    @app.after_request
    def after_request(response):
        response.headers.add(
            "Access-Control-Allow-Methods", "GET,PUT,POST,DELETE,OPTIONS"
        )
        response.headers.add("Content-Security-Policy", "self")

        return response

    @app.teardown_request
    def teardown_request(x):
        Session.remove()
        CONNECTION.close()
        ENGINE.dispose()

    return app


app = create_app()
if __name__ == "__main__":
    app.run()
