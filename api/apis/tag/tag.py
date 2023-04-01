from traceback import format_exception_only
from flask import request, Response
from flask_restful import Resource
from marshmallow.exceptions import ValidationError
from sqlalchemy.sql.expression import asc, desc
from sqlalchemy.sql.functions import func
from jwt_token import auth_required, get_jwt
from ..utils.pagination import Pagination
from entities.article import Article
from entities import Session
from entities.tag import Tag
from schemas.tag import TagSchema
from helper.message import PAGE_VALUE_ERROR, TAG_ALREADY_REGISTED, TAG_NOT_FOUND
from helper.error import ErrorHandler
from helper.response import ResponseHandler


class TagAPI(Resource):
    @auth_required
    def get(self, tagId: str) -> Response:
        """タグの単体取得

        Args:
            tagId (str): タグID

        Returns:
            Response: 正常系または異常系のレスポンス
        """
        with Session() as session:
            tag = session.query(Tag).filter_by(tagId=tagId).first()
            session.commit()

            # タグが存在しない場合
            if tag is None:
                return ErrorHandler.error404(TAG_NOT_FOUND)

            return ResponseHandler.res200(TagSchema().dump(tag))


class TagPostAPI(Resource):
    @auth_required
    def post(self) -> Response:
        """タグの登録処理

        Returns:
            Response: 正常系または異常系のレスポンス
        """
        with Session() as session:
            try:
                data = TagSchema().load(
                    request.get_json(),
                    session=session,
                )
            except ValidationError as e:
                session.rollback()

                return ErrorHandler.error400(e.messages)
            except Exception as e:
                session.rollback()
                return ErrorHandler.error400(format_exception_only(type(e), e))

            already = session.query(Tag).filter(Tag.tagName == data.tagName).first()

            # 同じ名前で既に登録されているタグが存在しないなら
            if already is None:
                session.add(data)
                session.commit()
                return ResponseHandler.res201(TagSchema().dump(data))

            session.rollback()
            return ErrorHandler.error400(TAG_ALREADY_REGISTED)


class TagsAPI(Resource):
    @auth_required
    def get(self) -> Response:
        """タグの全件取得 タグ名を50音順にソート

        Returns:
            Response: 正常系または異常系のレスポンス
        """
        try:
            pagination = Pagination()
            pagination.check_pagination()
        except ValueError as e:
            return ErrorHandler.error400(PAGE_VALUE_ERROR)
        except Exception as e:
            return ErrorHandler.error400(format_exception_only(type(e), e))
        with Session() as session:
            tags = (
                session.query(Tag)
                .select_from(Article)
                .join(Article.tags)
                .filter(Article.isActivate == True, Article.draft == False)
                .order_by(asc(Tag.tagName))
                .offset(pagination.getPage())
                .limit(pagination.perpage)
                .all()
            )
            count = (
                session.query(Tag)
                .select_from(Article)
                .join(Article.tags)
                .filter(Article.isActivate == True, Article.draft == False)
                .count()
            )
            session.commit()

            # タグ一覧が空リストなら
            if tags == [] or count == 0:
                return ResponseHandler.res204(TAG_NOT_FOUND)

            return ResponseHandler.res200(TagSchema(many=True).dump(tags), count)


class TagsPopularAPI(Resource):
    @auth_required
    def get(self) -> Response:
        """紐づいている記事が多い順にタグを取得

        Returns:
            Response: 正常系または異常系のレスポンス
        """
        try:
            pagination = Pagination()
            pagination.check_pagination()
        except ValueError as e:
            return ErrorHandler.error400(PAGE_VALUE_ERROR)
        except Exception as e:
            return ErrorHandler.error400(format_exception_only(type(e), e))
        with Session() as session:
            tags = (
                session.query(Tag)
                .select_from(Article)
                .join(Article.tags)
                .filter(Article.isActivate == True, Article.draft == False)
                .group_by(Tag)
                .order_by(desc(func.count(Article.articleId)), asc(Tag.tagName))
                .offset(pagination.getPage())
                .limit(pagination.perpage)
                .all()
            )
            count = (
                session.query(Tag)
                .select_from(Article)
                .join(Article.tags)
                .filter(Article.isActivate == True, Article.draft == False)
                .count()
            )
            session.commit()

            # タグ一覧が空リストなら
            if tags == [] or count == 0:
                return ResponseHandler.res204(TAG_NOT_FOUND)

            return ResponseHandler.res200(TagSchema(many=True).dump(tags), count)


class TagsArticleAPI(Resource):
    def get(self, articleId: str) -> Response:
        """単一記事の全タグを取得する

        Args:
            articleId (str): 記事ID

        Returns:
            Response: 正常系または異常系のレスポンス
        """
        with Session() as session:
            article = session.query(Article).filter_by(articleId=articleId).first()
            session.commit()

            if article.isActivate == False and get_jwt()["role"] != "admin":
                return ErrorHandler.error400(TAG_NOT_FOUND)

            tags = article.tags

            if article is None:
                return ErrorHandler.error400(TAG_NOT_FOUND)

            # タグ一覧が空リストなら
            if tags == []:
                return ResponseHandler.res204(TAG_NOT_FOUND)
            count = len(tags)
            tags = sorted(
                tags,
                key=lambda x: (x.tagName),
            )
            return ResponseHandler.res200(TagSchema(many=True).dump(tags), count)
