from flask import make_response
from flask.json import jsonify
import traceback


class ErrorHandler:
    @classmethod
    def error400(cls, description):
        return make_response(
            jsonify({"error": "400 Bad Request", "description": description}), 400
        )

    @classmethod
    def error401(cls, description):
        return make_response(
            jsonify({"error": "401 Unauthorized", "description": description}), 401
        )

    @classmethod
    def error403(cls, description="許可されていません｡"):
        return make_response(
            jsonify({"error": "403 Forbidden", "description": description}), 403
        )

    @classmethod
    def error404(cls, description):
        return make_response(
            jsonify({"error": "404 Not Found", "description": description}), 404
        )

    @classmethod
    def error421(cls, description):
        return make_response(
            jsonify({"error": "421 Misdirected Request", "description": description}),
            421,
        )

    @classmethod
    def error422(cls, description):
        return make_response(
            jsonify({"error": "422 Unprocessable Entity", "description": description}),
            422,
        )
