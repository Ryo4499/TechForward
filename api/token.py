from flask import jsonify, make_response
from flask_jwt_extended import (
    JWTManager,
    create_access_token,
    get_jwt_identity,
    get_jwt,
    verify_jwt_in_request,
)
from api.models.setting import Session
from api.models.token_blocklist import TokenBlocklist
from api.models.user import User
from functools import wraps

# JWTのデフォルトの挙動を変更しているため､他の場所で使うものに関してもimportで定義

# JWTインスタンスを作成
jwt = JWTManager()

# トークンにroleの情報を追加
@jwt.additional_claims_loader
def add_claims_to_access_token(identity):
    with Session() as session:
        user = session.query(User).filter_by(userId=identity).first()
        session.commit()
        return {"userId": identity, "role": user.role, "isActivate": user.isActivate}


def auth_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        verify_jwt_in_request()
        claims = get_jwt()
        with Session() as session:
            user = session.query(User).filter_by(userId=claims["userId"]).first()
            session.commit()
            if claims["isActivate"] == False:
                return make_response(jsonify({"message": "許可されていません｡"}), 403)
            elif user.isActivate != claims["isActivate"] or user.role != claims["role"]:
                return make_response(
                    jsonify({"message": "エラーが発生しました｡ログアウトして下さい｡"}), 409
                )
            else:
                return fn(*args, **kwargs)

    return wrapper


# 管理者のみの許可
def admin_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        verify_jwt_in_request()
        claims = get_jwt()
        with Session() as session:
            user = session.query(User).filter_by(userId=claims["userId"]).first()
            session.commit()
            if claims["role"] != "admin" or claims["isActivate"] == False:
                return make_response(jsonify({"message": "許可されていません｡"}), 403)
            elif user.isActivate != claims["isActivate"] or user.role != claims["role"]:
                return make_response(
                    jsonify({"message": "エラーが発生しました｡ログアウトして下さい｡"}), 409
                )
            else:
                return fn(*args, **kwargs)

    return wrapper


# 管理者と自分のみ許可
def self_or_admin_required_user(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        # kwargs: 修飾する関数の引数（対象のユーザID）が入る
        verify_jwt_in_request()
        claims = get_jwt()
        with Session() as session:
            user = session.query(User).filter_by(userId=claims["userId"]).first()
            session.commit()
            if (
                claims["userId"] != kwargs["userId"] or claims["role"] != "admin"
            ) and claims["isActivate"] != True:
                return make_response(jsonify({"message": "許可されていません｡"}), 403)
            elif user.isActivate != claims["isActivate"] or user.role != claims["role"]:
                return make_response(
                    jsonify({"message": "エラーが発生しました｡ログアウトして下さい｡"}), 409
                )
            else:
                return fn(*args, **kwargs)

    return wrapper


# トークンの有効期限切れ時の挙動
@jwt.expired_token_loader
def my_expired_token_callback(expired_token):
    token_type = expired_token["type"]

    if token_type == "access":
        return make_response(jsonify({"message": "アクセストークンが有効期限切れです｡"}), 401)


# 無効な形式のトークン時の挙動
@jwt.invalid_token_loader
def my_invalid_token_callback(error_string):
    return make_response(jsonify({"message": "トークンが無効です｡", "error": error_string}), 401)


# 認証エラー時の挙動
@jwt.unauthorized_loader
def my_unauthorized_callback(error_string):
    return make_response(
        jsonify({"message": "認証時にエラーが発生しました｡", "error": error_string}), 401
    )


# ログアウト処理
@jwt.token_in_blocklist_loader
def check_if_token_revoked(jwt_header, jwt_payload):
    jti = jwt_payload["jti"]
    token = Session.query(TokenBlocklist.id).filter_by(jti=jti).scalar()
    return token is not None


# ログアウト後に以前のトークンが使用された場合
@jwt.revoked_token_loader
def revoked_token_response(jwt_header, jwt_payload):
    return make_response(jsonify({"message": "既にログアウトしています｡"}), 401)


def init_jwt(app):
    jwt.init_app(app)
