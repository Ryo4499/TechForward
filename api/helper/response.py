from flask import make_response, jsonify


class ResponseHandler:
    @classmethod
    def res200(cls, result, count=[]):
        if count == []:
            return make_response(jsonify(result), 200)
        else:
            return make_response(jsonify({"result": result, "count": count}), 200)

    @classmethod
    def res201(cls, result):
        return make_response(jsonify(result), 201)

    @classmethod
    def res204(cls, result):
        return make_response(jsonify(result), 204)
