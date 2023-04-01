from traceback import format_exception_only
from flask import request, Response
from flask_restful import Resource
from marshmallow.exceptions import ValidationError
from jwt_token import create_access_token, get_jwt, auth_required
from schemas.user import UserSchema
from entities import Session
from entities.token_blocklist import TokenBlocklist
from entities.user import User
from helper.message import UNAUTHORIZED, USER_IS_DELETED, INPUT_VALUE_DO_NOT_MATCH
from helper.response import ResponseHandler
from helper.error import ErrorHandler


class LoginAPI(Resource):
    def post(self) -> Response:
        """ログイン処理

        Returns:
            Response: 正常系または異常系のレスポンス
        """
        with Session() as session:
            try:
                data = UserSchema(
                    only=(
                        "userName",
                        "password",
                    ),
                    partial=(
                        "email",
                        "role",
                        "isActivate",
                    ),
                ).load(
                    request.get_json(),
                    session=session,
                )
            except ValidationError as e:
                return ErrorHandler.error422(e.messages)
            except Exception as e:
                return ErrorHandler.error400(format_exception_only(type(e), e))

            user = session.query(User).filter(User.userName == data.userName).first()

            if user is None:
                session.rollback()
                return ErrorHandler.error422(INPUT_VALUE_DO_NOT_MATCH)

            if user.isActivate == False:
                session.rollback()
                return ErrorHandler.error403(USER_IS_DELETED)
            elif not user.check_password(data.password):
                session.rollback()
                return ErrorHandler.error422(INPUT_VALUE_DO_NOT_MATCH)

            access_token = create_access_token(identity=user.userId)

            return ResponseHandler.res200(
                {
                    "message": "ログインしました｡",
                    "access_token": access_token,
                }
            )


class LogoutAPI(Resource):
    @auth_required
    def post(self) -> Response:
        """ログアウト処理

        Returns:
            Response: 正常系または異常系のレスポンス
        """
        jti = get_jwt()["jti"]

        if jti is None:
            return ErrorHandler.error401(UNAUTHORIZED)

        with Session() as session:
            session.add(TokenBlocklist(jti=jti))
            session.commit()
            return ResponseHandler.res200({"message": "ログアウトしました｡"})
