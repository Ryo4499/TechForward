import os
import re
from datetime import datetime
from traceback import format_exception_only
from jsonschema import validate
from jsonschema.exceptions import ValidationError
from jwt_token import auth_required, get_jwt
from flask import request, Response
from flask_restful import Resource
from entities import Session, REGEX_PATTERN
from entities.article import Article
from entities.user import User
from entities.tag import Tag
from helper.message import (
    ARTICLE_NOT_FOUND,
    TITLE_VALIDATION_ERROR,
    TAG_VALIDATION_ERROR,
    ARTICLE_IS_DELETED,
)
from helper.error import ErrorHandler
from helper.response import ResponseHandler
from schemas.article import ArticleSchema, adminReqSchema, userReqSchema


TAG_RESTRICTION = f"タグは{os.getenv('MAX_TAG',5)}つまでしか登録できません"


def regex_pattern(target: str) -> bool:
    """対象のパターンがREGEX_PATTERNと一致しているかを検証

    Args:
        target (str): 対象のパターン

    Returns:
        bool: 一致したかのフラグ(Trueなら一致、Falseなら不一致)
    """
    p = re.compile(REGEX_PATTERN)
    return p.fullmatch(target)


class ArticleAPI(Resource):
    @auth_required
    def get(self, articleId: str) -> Response:
        """記事取得処理

        Args:
            articleId (str): 記事ID

        Returns:
            Response: 正常系または、異常系のレスポンス
        """
        with Session() as session:
            article = (
                session.query(Article)
                .filter(
                    Article.articleId == articleId,
                )
                .first()
            )
            session.commit()
            # 記事が存在しない場合
            if article is None:
                return ErrorHandler.error404(ARTICLE_NOT_FOUND)

            if get_jwt()["role"] == "admin":
                return ResponseHandler.res200(ArticleSchema().dump(article))

            if article.isActivate == False:
                return ErrorHandler.error404(ARTICLE_NOT_FOUND)
            else:
                if article.draft == False:
                    return ResponseHandler.res200(ArticleSchema().dump(article))

                elif (
                    article.user.userId == get_jwt()["userId"] and article.draft == True
                ):
                    return ResponseHandler.res200(ArticleSchema().dump(article))

                else:
                    return ErrorHandler.error403()

    @auth_required
    def put(self, articleId: str) -> Response:
        """記事更新処理

        Args:
            articleId (str): 記事ID

        Returns:
            Response: 正常系または、異常系のレスポンス
        """
        claims = get_jwt()
        isAdmin = claims["role"] == "admin"
        json = request.get_json()

        if isAdmin and "isActivate" in json:
            try:
                validate(
                    instance=json,
                    schema=adminReqSchema,
                )
                if not regex_pattern(json["title"]):
                    raise ValidationError(TITLE_VALIDATION_ERROR)
                if "tags" in json:
                    for tag in json["tags"]:
                        if not regex_pattern(tag):
                            raise ValidationError(TAG_VALIDATION_ERROR)
            except ValidationError as e:
                return ErrorHandler.error400(e.message)
            except Exception as e:
                return ErrorHandler.error400(format_exception_only(type(e), e))
        else:
            try:
                validate(
                    instance=json,
                    schema=userReqSchema,
                )
                if not regex_pattern(json["title"]):
                    raise ValidationError(TITLE_VALIDATION_ERROR)
                if "tags" in json:
                    for tag in json["tags"]:
                        if not regex_pattern(tag):
                            raise ValidationError(TAG_VALIDATION_ERROR)
            except ValidationError as e:
                return ErrorHandler.error400(e.message)
            except Exception as e:
                return ErrorHandler.error400(format_exception_only(type(e), e))

        with Session() as session:
            article = session.query(Article).filter_by(articleId=articleId).first()

            # 記事が存在しない場合
            if article is None:
                session.rollback()
                return ErrorHandler.error404(ARTICLE_NOT_FOUND)

            # 記事が削除されている場合
            if article.isActivate == False and not isAdmin:
                session.rollback()
                return ErrorHandler.error404(ARTICLE_IS_DELETED)

            if article.user.userId == claims["userId"] or isAdmin:
                try:
                    article.title = json["title"]
                    article.content = json["content"]
                    article.draft = bool(json["draft"])
                    article.updatedAt = datetime.now()
                    article.tags = []
                    if "tags" in json:
                        # 入力されたタグを抽出してあればそのまま追加し､なければ新しく作って追加
                        for newTag in json["tags"]:
                            tag = session.query(Tag).filter_by(tagName=newTag).first()
                            if tag is None:
                                tag = Tag(newTag)
                                session.add(tag)
                            article.tags.append(tag)
                    if claims["userId"] == article.userId:
                        userQuery = (
                            session.query(User)
                            .filter_by(userId=claims["userId"])
                            .first()
                        )
                        article.user = userQuery
                    article.isActivate = json["isActivate"]

                    session.add(article)
                    session.commit()
                except Exception as e:
                    session.rollback()
                    return ErrorHandler.error400(format_exception_only(type(e), e))
                if isAdmin:
                    return ResponseHandler.res200(
                        ArticleSchema(
                            only=(
                                "title",
                                "content",
                                "draft",
                                "tags",
                                "isActivate",
                            )
                        ).dump(article)
                    )
                else:
                    return ResponseHandler.res200(
                        ArticleSchema(
                            only=(
                                "title",
                                "content",
                                "draft",
                                "tags",
                            )
                        ).dump(article)
                    )
            else:
                session.rollback()
                return ErrorHandler.error403()

    @auth_required
    def delete(self, articleId: str) -> Response:
        """記事削除処理

        Args:
            articleId (str): 記事ID

        Returns:
            Response: 正常系または、異常系のレスポンス
        """
        with Session() as session:
            article = session.query(Article).filter_by(articleId=articleId).first()

            # 記事が存在しない場合
            if article is None:
                session.rollback()
                return ErrorHandler.error404(ARTICLE_NOT_FOUND)

            if article.isActivate == False:
                session.rollback()
                return ErrorHandler.error404(ARTICLE_IS_DELETED)
            if (
                article.user.userId == get_jwt()["userId"]
                or get_jwt()["role"] == "admin"
            ):
                article.isActivate = False
                session.commit()
                return ResponseHandler.res200({"message": "削除されました｡"})
            else:
                session.rollback()
                return ErrorHandler.error403()


class ArticlePostAPI(Resource):
    @auth_required
    def post(self) -> Response:
        """記事登録処理

        Raises:
            ValidationError: タイトルまたはタグがパターンに一致しない場合

        Returns:
            Response: 正常系または、異常系のレスポンス
        """
        json = request.get_json()
        try:
            validate(
                instance=json,
                schema=userReqSchema,
            )
            if not regex_pattern(json["title"]):
                raise ValidationError(TITLE_VALIDATION_ERROR)
            if "tags" in json:
                for tag in json["tags"]:
                    if not regex_pattern(tag):
                        raise ValidationError(TAG_VALIDATION_ERROR)
        except ValidationError as e:
            return ErrorHandler.error400(e.message)
        except Exception as e:
            return ErrorHandler.error400(format_exception_only(type(e), e))

        # DB登録処理
        userId = get_jwt()["userId"]
        with Session() as session:
            try:
                article = Article(
                    title=json["title"],
                    content=json["content"],
                    draft=bool(json["draft"]),
                )
                if "tags" in json:
                    # 入力されたタグを抽出してあればそのまま追加し､なければ新しく作って追加
                    for newTag in json["tags"]:
                        tag = session.query(Tag).filter_by(tagName=newTag).first()
                        if tag is None:
                            tag = Tag(newTag)
                            session.add(tag)
                        article.tags.append(tag)

                # 投稿したユーザを取得して
                user = session.query(User).filter_by(userId=userId).first()
                article.user = user

                session.add(article)
                session.commit()
            except Exception as e:
                session.rollback()
                return ErrorHandler.error400(format_exception_only(type(e), e))

            return ResponseHandler.res201(ArticleSchema().dump(article))
