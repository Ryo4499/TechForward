from traceback import format_exception_only
from flask.wrappers import Response
from sqlalchemy.sql.functions import func
from helper.response import ResponseHandler
from helper.error import ErrorHandler
from models.user import User
from schemas.article import ArticleSchema, TagSchema
from jwt_token import auth_required, get_jwt
from flask_restful import Resource
from sqlalchemy import desc
from apis.pagination import Pagination
from models.setting import Session
from models.article import Article
from models.tag import Tag
from helper.message import ARTICLE_NOT_FOUND, PAGE_VALUE_ERROR


class ArticlesAPI(Resource):
    @auth_required
    def get(self):
        # ページネーションのバリデーション
        try:
            pagination = Pagination()
            pagination.check_pagination()
        except ValueError as e:
            return ErrorHandler.error400(PAGE_VALUE_ERROR)
        except Exception as e:
            return ErrorHandler.error400(format_exception_only(type(e), e))

        with Session() as session:
            articles = (
                session.query(Article)
                .filter(Article.isActivate == True, Article.draft == False)
                .order_by(desc(Article.updatedAt), desc(Article.createdAt))
                .offset(pagination.getPage())
                .limit(pagination.perpage)
                .all()
            )
            count = (
                session.query(Article.articleId)
                .filter(Article.isActivate == True, Article.draft == False)
                .count()
            )
            session.commit()

            # 記事一覧が空リストなら
            if articles == [] or count == 0:
                return ResponseHandler.res204(ARTICLE_NOT_FOUND)

            return ResponseHandler.res200(
                ArticleSchema(
                    many=True,
                    only=[
                        "articleId",
                        "content",
                        "comments",
                        "createdAt",
                        "draft",
                        "isActivate",
                        "tags",
                        "title",
                        "updatedAt",
                        "user",
                    ],
                ).dump(articles),
                count,
            )


class ArticlesByUserAPI(Resource):
    @auth_required
    def get(self, userName):
        # ページネーションのバリデーション
        try:
            pagination = Pagination()
            pagination.check_pagination()
        except ValueError as e:
            return ErrorHandler.error400(PAGE_VALUE_ERROR)
        except Exception as e:
            return ErrorHandler.error400(format_exception_only(type(e), e))

        with Session() as session:
            articles = (
                session.query(Article)
                .join(User)
                .filter(
                    User.userName == userName,
                    Article.isActivate == True,
                    Article.draft == False,
                )
                .order_by(desc(Article.updatedAt), desc(Article.createdAt))
                .offset(pagination.getPage())
                .limit(pagination.perpage)
                .all()
            )
            count = (
                session.query(Article)
                .join(User)
                .filter(
                    User.userName == userName,
                    Article.isActivate == True,
                    Article.draft == False,
                )
                .count()
            )
            session.commit()

            # 記事一覧が空リストなら
            if articles == [] or count == 0:
                return ResponseHandler.res204(ARTICLE_NOT_FOUND)

            return ResponseHandler.res200(
                ArticleSchema(
                    many=True,
                    only=[
                        "articleId",
                        "content",
                        "comments",
                        "createdAt",
                        "draft",
                        "isActivate",
                        "tags",
                        "title",
                        "updatedAt",
                        "user",
                    ],
                ).dump(articles),
                count,
            )


class ArticlesTagAPI(Resource):
    @auth_required
    def get(self, tagName):
        # ページネーションのバリデーション
        try:
            pagination = Pagination()
            pagination.check_pagination()
        except ValueError as e:
            return ErrorHandler.error400(PAGE_VALUE_ERROR)
        except Exception as e:
            return ErrorHandler.error400(format_exception_only(type(e), e))

        with Session() as session:
            tag = session.query(Tag).filter(Tag.tagName == tagName).first()
            session.commit()

            # タグがない場合
            if tag is None:
                return ErrorHandler.error404(ARTICLE_NOT_FOUND)

            # タグにバインドされている記事を格納
            articles = []
            for article in tag.articles:
                if article.isActivate == True and article.draft == False:
                    articles.append(article)

            # 記事一覧が空リストなら
            if articles == []:
                return ResponseHandler.res204(ARTICLE_NOT_FOUND)

            articles = sorted(
                articles, key=lambda x: (x.updatedAt, x.createdAt), reverse=True
            )
            count = len(articles)
            articles = pagination.sliceList(articles)

            return ResponseHandler.res200(
                ArticleSchema(
                    many=True,
                    only=[
                        "articleId",
                        "content",
                        "comments",
                        "createdAt",
                        "draft",
                        "isActivate",
                        "tags",
                        "title",
                        "updatedAt",
                        "user",
                    ],
                ).dump(articles),
                count,
            )


class MyArticlesAPI(Resource):
    @auth_required
    def get(self):
        # ページネーションのバリデーション
        try:
            pagination = Pagination()
            pagination.check_pagination()
        except ValueError as e:
            return ErrorHandler.error400(PAGE_VALUE_ERROR)
        except Exception as e:
            return ErrorHandler.error400(format_exception_only(type(e), e))

        claims = get_jwt()

        with Session() as session:
            articles = (
                session.query(Article)
                .filter(Article.userId == claims["userId"], Article.isActivate == True)
                .order_by(desc(Article.updatedAt), desc(Article.createdAt))
                .offset(pagination.getPage())
                .limit(pagination.perpage)
                .all()
            )
            count = (
                session.query(Article)
                .filter(Article.userId == claims["userId"], Article.isActivate == True)
                .count()
            )
            session.commit()

            # 記事一覧が空リストなら
            if articles == [] or count == 0:
                return ResponseHandler.res204(ARTICLE_NOT_FOUND)

            return ResponseHandler.res200(
                ArticleSchema(
                    many=True,
                    only=[
                        "articleId",
                        "content",
                        "comments",
                        "createdAt",
                        "draft",
                        "isActivate",
                        "tags",
                        "title",
                        "updatedAt",
                        "user",
                    ],
                ).dump(articles),
                count,
            )


class SearchByTitleArticleAPI(Resource):
    @auth_required
    def get(self, title):
        # ページネーションのバリデーション
        try:
            pagination = Pagination()
            pagination.check_pagination()
        except ValueError as e:
            return ErrorHandler.error400(PAGE_VALUE_ERROR)
        except Exception as e:
            return ErrorHandler.error400(format_exception_only(type(e), e))

        with Session() as session:
            articles = (
                session.query(Article)
                .filter(
                    func.lower(Article.title).contains(title.lower(), autoescape=True),
                    Article.isActivate == True,
                    Article.draft == False,
                )
                .order_by(desc(Article.updatedAt), desc(Article.createdAt))
                .offset(pagination.getPage())
                .limit(pagination.perpage)
                .all()
            )
            count = (
                session.query(Article)
                .filter(
                    func.lower(Article.title).contains(title.lower(), autoescape=True),
                    Article.isActivate == True,
                    Article.draft == False,
                )
                .count()
            )
            session.commit()

            # 記事が存在しない場合
            if articles == [] or count == 0:
                return ResponseHandler.res204(ARTICLE_NOT_FOUND)

            return ResponseHandler.res200(
                ArticleSchema(
                    many=True,
                    only=[
                        "articleId",
                        "content",
                        "comments",
                        "createdAt",
                        "draft",
                        "isActivate",
                        "tags",
                        "title",
                        "updatedAt",
                        "user",
                    ],
                ).dump(articles),
                count,
            )
