from datetime import datetime
from traceback import format_exception_only
from jwt_token import (
    auth_required,
    self_or_admin_required_user,
    get_jwt,
)
from helper.error import ErrorHandler
from helper.response import ResponseHandler
from sqlalchemy import desc
from flask_restful import Resource, request
from marshmallow.exceptions import ValidationError
from models.setting import Session
from models.user import User
from models.token_blocklist import TokenBlocklist
from schemas.user import UserSchema
from helper.message import (
    USER_ALREADY_REGISTED,
    USER_IS_DELETED,
    USER_NOT_FOUND,
    ADMIN_REQUIRED,
)


class UserAPI(Resource):
    # ユーザの更新
    @self_or_admin_required_user
    def put(self, userId):
        claims = get_jwt()
        isAdmin = claims["role"] == "admin"
        json = request.get_json()
        with Session() as session:
            try:
                if (
                    isAdmin
                    and "role" in json
                    and "isActivate" in json
                    and "password" in json
                ):
                    jsonData = UserSchema(
                        only=(
                            "userName",
                            "email",
                            "password",
                            "role",
                            "isActivate",
                        ),
                    ).load(
                        json,
                        session=session,
                    )
                elif isAdmin and "role" in json and "isActivate" in json:
                    jsonData = UserSchema(
                        only=(
                            "userName",
                            "email",
                            "role",
                            "isActivate",
                        ),
                        partial=("password"),
                    ).load(
                        json,
                        session=session,
                    )
                elif isAdmin and "role" in json:
                    jsonData = UserSchema(
                        only=(
                            "userName",
                            "email",
                            "password",
                            "role",
                        ),
                        partial=("isActivate"),
                    ).load(
                        json,
                        session=session,
                    )
                elif isAdmin and "isActivate" in json:
                    jsonData = UserSchema(
                        only=(
                            "userName",
                            "email",
                            "password",
                            "isActivate",
                        ),
                        partial=("role"),
                    ).load(
                        json,
                        session=session,
                    )
                else:
                    jsonData = UserSchema(
                        only=(
                            "userName",
                            "email",
                            "password",
                        ),
                        partial=("role", "isActivate"),
                    ).load(
                        json,
                        session=session,
                    )
            except ValidationError as e:
                return ErrorHandler.error422(e.messages)
            except Exception as e:
                return ErrorHandler.error400(format_exception_only(type(e), e))

            user = session.query(User).filter_by(userId=userId).first()

            # ユーザが存在しない場合
            if user is None:
                session.rollback()
                return ErrorHandler.error404(USER_NOT_FOUND)

            if user.isActivate == False and not isAdmin:
                session.rollback()
                return ErrorHandler.error404(USER_IS_DELETED)

            # 同じ名前で既に登録されているユーザが存在しないなら
            already = (
                session.query(User)
                .filter(
                    User.userName == jsonData.userName,
                    User.userId != user.userId,
                )
                .first()
            )

            if already is None:
                try:
                    user.userName = jsonData.userName
                    user.email = jsonData.email
                    if "password" in json:
                        user.set_password(jsonData.password)
                    user.updatedAt = datetime.now()
                    if claims["role"] == "admin":
                        admins = (
                            session.query(User)
                            .filter(User.role == "admin", User.isActivate == True)
                            .all()
                        )
                        if "role" in json:
                            if (
                                claims["userId"] == user.userId
                                and jsonData.role == "user"
                                and user.role != "user"
                            ):
                                if len(admins) <= 2:
                                    session.rollback()
                                    return ErrorHandler.error422(ADMIN_REQUIRED)
                                else:
                                    user.role = jsonData.role
                            else:
                                user.role = jsonData.role
                        if "isActivate" in json:
                            if (
                                claims["userId"] == user.userId
                                and jsonData.isActivate == False
                                and user.role != "user"
                            ):
                                if len(admins) <= 2:
                                    session.rollback()
                                    return ErrorHandler.error422(ADMIN_REQUIRED)
                                else:
                                    user.isActivate = bool(jsonData.isActivate)
                            else:
                                user.isActivate = bool(jsonData.isActivate)
                    session.commit()
                    if isAdmin:
                        return ResponseHandler.res200(
                            UserSchema(
                                only=(
                                    "userId",
                                    "userName",
                                    "email",
                                    "isActivate",
                                    "role",
                                )
                            ).dump(user)
                        )
                    else:
                        return ResponseHandler.res200(
                            UserSchema(
                                only=(
                                    "userId",
                                    "userName",
                                    "email",
                                )
                            ).dump(user)
                        )
                except Exception as e:
                    return ErrorHandler.error400(format_exception_only(type(e), e))

            session.rollback()
            return ErrorHandler.error421(USER_ALREADY_REGISTED)

    @self_or_admin_required_user
    def delete(self, userId):
        with Session() as session:
            user = session.query(User).filter_by(userId=userId).first()

            # ユーザが存在しない場合
            if user is None:
                session.rollback()
                return ErrorHandler.error404(USER_NOT_FOUND)
            if user.isActivate == False:
                session.rollback()
                return ErrorHandler.error400(USER_IS_DELETED)

            claims = get_jwt()

            if user.role == "admin":
                admins = (
                    session.query(User)
                    .filter(User.role == "admin", User.isActivate == True)
                    .all()
                )
                if len(admins) <= 2:
                    session.rollback()
                    return ErrorHandler.error422(ADMIN_REQUIRED)
                else:
                    user.isActivate = False
                    if claims["userId"] == user.userId:
                        jti = claims["jti"]
                        Session.add(TokenBlocklist(jti=jti))
                        session.commit()
                    return ResponseHandler.res200({"message": "削除されました｡"})
            else:
                user.isActivate = False
                session.commit()
                jti = claims["jti"]
                Session.add(TokenBlocklist(jti=jti))
                session.commit()
                return ResponseHandler.res200({"message": "削除されました｡"})


# ユーザの作成
class UserPostAPI(Resource):
    def post(self):
        try:
            with Session() as session:
                jsonData = UserSchema(only=("userName", "email", "password",),).load(
                    request.get_json(), session=session, partial=("role", "isActivate")
                )

                already = (
                    session.query(User)
                    .filter(User.userName == jsonData.userName)
                    .first()
                )

                # 同じ名前で既に登録されているユーザが存在しないなら
                if already is None:
                    jsonData.set_password(jsonData.password)
                    session.add(jsonData)
                    session.commit()

                    return ResponseHandler.res201(UserSchema().dump(jsonData))

                session.rollback()
                return ErrorHandler.error421(USER_ALREADY_REGISTED)
        except ValidationError as e:
            return ErrorHandler.error400(e.messages)
        except Exception as e:
            return ErrorHandler.error400(format_exception_only(type(e), e))


# 自分自身の情報を取得
class UserSelfAPI(Resource):
    @auth_required
    def get(self):
        claims = get_jwt()
        with Session() as session:
            user = session.query(User).filter_by(userId=claims["userId"]).first()
            session.commit()
            # ユーザが存在しない場合
            if user is None:
                return ErrorHandler.error404(USER_NOT_FOUND)

            return ResponseHandler.res200(UserSchema().dump(user))
