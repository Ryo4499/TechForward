from traceback import format_exception_only
from schemas.user import UserSchema
from helper.error import ErrorHandler
from helper.response import ResponseHandler
from jwt_token import self_or_admin_required_user
from flask import request
from helper.message import (
    USER_ALREADY_REGISTED,
    USER_IS_DELETED,
    USER_NOT_FOUND,
)
from flask_restful import Resource
from marshmallow.exceptions import ValidationError
from models.setting import Session
from models.user import User


class UserModifyEmailAPI(Resource):
    @self_or_admin_required_user
    def put(self, userId):
        with Session() as session:
            try:
                jsonData = UserSchema(only=("email",)).load(
                    request.get_json(),
                    partial=("userName", "password", "role", "isActivate"),
                    session=session,
                )

                user = session.query(User).filter_by(userId=userId).first()

                # ユーザが存在しない場合
                if user is None:
                    session.rollback()

                    return ErrorHandler.error404(USER_NOT_FOUND)

                if user.isActivate == False:
                    session.rollback()
                    return ErrorHandler.error404(USER_IS_DELETED)
                user.email = jsonData.email
                session.commit()
                return ResponseHandler.res200(
                    UserSchema(only=("userId", "email")).dump(user)
                )

            except ValidationError as e:
                session.rollback()
                return ErrorHandler.error422(e.messages)
            except Exception as e:
                session.rollback()
                return ErrorHandler.error400(format_exception_only(type(e), e))


class UserModifyPasswordAPI(Resource):
    @self_or_admin_required_user
    def put(self, userId):
        with Session() as session:
            try:
                jsonData = UserSchema(only=("password",),).load(
                    request.get_json(),
                    session=session,
                    partial=("userName", "email", "role", "isActivate"),
                )
                user = session.query(User).filter_by(userId=userId).first()
            except ValidationError as e:
                session.rollback()
                return ErrorHandler.error422(e.messages)
            except Exception as e:
                session.rollback()
                return ErrorHandler.error400(format_exception_only(type(e), e))

            # ユーザが存在しない場合
            if user is None:
                session.rollback()
                return ErrorHandler.error404(USER_NOT_FOUND)

            if user.isActivate is False:
                session.rollback()
                return ErrorHandler.error404(USER_IS_DELETED)
            try:
                user.set_password(jsonData.password)
            except Exception as e:
                session.rollback()
                return ErrorHandler.error400(format_exception_only(type(e), e))

            session.commit()
            return ResponseHandler.res200({"message": "パスワードの変更が完了しました｡"})


class UserModifyUserNameAPI(Resource):
    @self_or_admin_required_user
    def put(self, userId):
        with Session() as session:
            try:
                jsonData = UserSchema(only=("userName",),).load(
                    request.get_json(),
                    session=session,
                    partial=("email", "password", "role", "isActivate"),
                )
                user = session.query(User).filter_by(userId=userId).first()
            except ValidationError as e:
                session.rollback()
                return ErrorHandler.error422(e.messages)
            except Exception as e:
                session.rollback()
                return ErrorHandler.error400(format_exception_only(type(e), e))

            # ユーザが存在しない場合
            if user is None:
                session.rollback()
                return ErrorHandler.error404(USER_NOT_FOUND)

            if user.isActivate is False:
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
                user.userName = jsonData.userName
                session.commit()

                return ResponseHandler.res200(
                    UserSchema(only=("userId", "userName")).dump(user)
                )

            session.rollback()
            return ErrorHandler.error421(USER_ALREADY_REGISTED)
