from traceback import format_exception_only
from api.helper.response import ResponseHandler
from api.helper.error import ErrorHandler
from api.schemas.user import UserSchema
from flask import request
from marshmallow.exceptions import ValidationError
from flask_restful import Resource
from api.models.setting import Session
from api.models.token_blocklist import TokenBlocklist
from api.models.user import User
from api.token import create_access_token, get_jwt, auth_required
from api.helper.message import UNAUTHORIZED, USER_IS_DELETED, INPUT_VALUE_DO_NOT_MATCH


class LoginAPI(Resource):
    def post(self):
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
    def post(self):
        jti = get_jwt()["jti"]

        if jti is None:
            return ErrorHandler.error401(UNAUTHORIZED)

        with Session() as session:
            session.add(TokenBlocklist(jti=jti))
            session.commit()
            return ResponseHandler.res200({"message": "ログアウトしました｡"})
