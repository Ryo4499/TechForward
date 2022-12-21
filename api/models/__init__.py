import sys
from models.user import User
from models.tag import Tag
from models.article import Article
from models.comment import Comment
from models.article_tag import ArticleTag
from models.setting import CONNECTION, Base, ENGINE, Session


def init_db():
    Base.metadata.drop_all(bind=ENGINE)
    Base.metadata.create_all(bind=ENGINE)


def test_data():
    with Session() as session:
        user = User(
            userName="太郎",
            email="taro@example.com",
        )
        user.set_password("aaaaaaaa")
        user1 = User(
            userName="次郎",
            email="jiro@example.com",
        )
        user1.set_password("aaaaaaaa")
        user2 = User(
            userName="三郎",
            email="saburo@example.com",
        )
        user2.set_password("aaaaaaaa")
        user3 = User(
            userName="四郎",
            email="shiro@example.com",
        )
        user3.set_password("aaaaaaaa")
        admin = User(
            userId="571679d664084614a4947e141fe59224",
            userName="新井",
            email="arai@example.com",
            role="admin",
        )
        admin.set_password("adminadmin")
        admin1 = User(
            userName="管理者",
            email="admin@example.com",
            role="admin",
        )
        admin1.set_password("adminadmin")
        admin1 = User(
            userName="admin",
            email="admin@example.com",
            role="admin",
        )
        admin1.set_password("adminadmin")
        session.add(user)
        session.add(user1)
        session.add(user2)
        session.add(user3)
        session.add(admin)
        session.add(admin1)
        jstag = Tag(
            tagName="JavaScript",
        )
        pythontag = Tag(tagName="Python")
        gittag = Tag(tagName="Git")
        htmltag = Tag(tagName="HTML")
        progtag = Tag(tagName="プログラミング")
        umltag = Tag(tagName="plantUml")
        katextag = Tag(tagName="Katex")
        javatag = Tag(tagName="Java")
        pipArticle = Article(
            title="PIPでPythonのパッケージをインストールする",
            content="# PIPでのパッケージのインストール方法\n\n```python\npip install <:package name>\n```\nとすることでパッケージをインストール出来ます｡\nその他の機能については公式ドキュメント[^1]を参照してください｡\n[^1]:https://pip.pypa.io/en/stable/\n",
            draft=False,
        )
        pipArticle.user = user
        pipArticle.tags.append(progtag)
        pipArticle.tags.append(pythontag)
        comment = Comment(content="good!")
        comment.user = user
        comment.article = pipArticle

        gitArticle = Article(
            title="GitでGithubにプッシュを行う",
            content='# GitHubへのプッシュ方法\n\n- [git add](#add)でインデックスを追加\n- [git commit](#commit)でコミットメッセージを記入\n- [git push](#push)でリモートにプッシュ\n\n## add\n\n```bash\ngit add .\n```\n\n## commit\n\n```bash\ngit commit -m "コミットメッセージ"\n```\n\n## push\n\n```bash\ngit push origin main\n```\n\n:::container\n![](https://japan.cnet.com/storage/2015/06/04/ff39fe41f77272507cd878abe8d6e05f/t/584/438/d/150604_g_eye.jpg)\n:::\n',
            draft=False,
        )
        gitArticle.user = user3
        gitArticle.tags.append(progtag)
        gitArticle.tags.append(gittag)
        comment1 = Comment(
            content="Gitは便利です:fireworks:",
        )
        comment1.user = admin
        comment1.article = gitArticle

        jsArticle = Article(
            title="JSで四則演算やってみた",
            content="# 四則演算\n\n[[toc]]\n\n## 足し算\n\n```js\nconsole.log(10+2)\n```\n\n## 引き算\n\n```js\nconsole.log(10-2)\n```\n\n## 掛け算\n\n```js\nconsole.log(10*2)\n```\n\n## 割り算\n\n```js\nconsole.log(10/2)\n```",
            draft=False,
        )
        jsArticle.user = user2
        jsArticle.tags.append(progtag)
        jsArticle.tags.append(jstag)

        comment2 = Comment(
            content="変数を使うことでいろいろな値に対応できます｡\n\n```js\nlet a = 10\nlet b = 2\nconsole.log(a+b)\n```"
        )
        comment2.user = user1
        comment2.article = jsArticle

        htmlArticle = Article(
            title="HTML 基本",
            content="<h1>HTML基本タグ</h1>\n\n&lt;h1&gt;\n: 見出しを表します｡ \n: h6まであります｡\n\n&lt;img&gt;\n: 画像を表示する時に使います｡\n\n&lt;p&gt;\n: 段落を表します｡:)\n",
            draft=False,
        )
        htmlArticle.user = user3
        htmlArticle.tags.append(progtag)
        htmlArticle.tags.append(htmltag)
        comment3 = Comment(
            content="変数を使うことでいろいろな値に対応できます｡\n\n```js\nlet a = 10\nlet b = 2\nconsole.log(a+b)\n```"
        )
        comment3.user = admin1
        comment3.article = htmlArticle

        musicArticle = Article(
            title="プログラミングにおすすめの音楽",
            content="# プログラミングにおすすめの音楽\n\n@[youtube](https://www.youtube.com/watch?v=H-ZdkAu9-Vk)\n\nEnjoy!:smile:",
            draft=False,
        )
        musicArticle.user = user
        musicArticle.tags.append(progtag)
        comment4 = Comment(content="good :)")
        comment4.user = user1
        comment4.article = musicArticle

        plantUmlArticle = Article(
            title="ER図",
            content='@startuml kenshu2021論理\n\n!define MAIN_ENTITY #E2EFDA-C6E0B4\n!define MAIN_ENTITY_2 #FCE4D6-F8CBAD\n\n!define METAL #F2F2F2-D9D9D9\n!define MASTER_MARK_COLOR AAFFAA\n!define TRANSACTION_MARK_COLOR FFAA00\n\nskinparam class{\n BackgroundColor METAL\n BorderColor Black\n ArrowColor Black\n}\n\npackage "技術共有システム" as target_system {\n entity "ユーザテーブル" as users <<E,TRANSACTION_MARK_COLOR>> MAIN_ENTITY_2{\n + ユーザID [PK]\n ---\n ユーザ名\n Eメール\n パスワード\n ロール\n 作成日\n 更新日\n }\n\n entity "記事テーブル" as articles <<E,TRANSACTION_MARK_COLOR>> MAIN_ENTITY{\n + 記事ID [PK]\n ---\n # ユーザID <<FK>>\n タイトル\n 内容\n 作成日\n 更新日\n 下書き\n }\n\n entity "コメントテーブル" as comments <<E,MASTER_MARK_COLOR>>{\n + コメントID [PK]\n ---\n # 記事ID <<FK>>\n # ユーザID <<FK>>\n 内容\n 作成日\n 更新日\n }\n\n entity "タグテーブル" as tags <<E,MASTER_MARK_COLOR>>{\n + タグID[PK]\n ---\n タグ名\n }\n\n entity "記事タグテーブル" as article_tags <<E,MASTER_MARK_COLOR>>{\n + 記事ID [PK]<<FK>>\n + タグID [PK]<<FK>>\n }\n\n users ||-ri-o{ articles\n articles |o-ri-o{ article_tags\n users |o-d-o{ comments\n articles |o-d-o{ comments\n article_tags }o-ri-o| tags\n}\n@enduml\n\n\n',
            draft=False,
        )
        plantUmlArticle.user = admin
        plantUmlArticle.tags.append(umltag)

        katexArticle = Article(
            title="Katexで解の公式書いてみた",
            content="## 解の公式\n\n$$\n\color{red}{x = \dfrac{-b \pm \sqrt{ b^{2} - 4ac } }{2a}}\n$$\n\n```\n$$\nx = \\dfrac{-b \\pm \\sqrt{ b^{2} - 4ac } }{2a}\n$$\n```\n\n",
            draft=False,
        )
        katexArticle.user = user3
        katexArticle.tags.append(katextag)

        javaArticle = Article(
            title="javaでオブジェクト作ってみた",
            content=':::container\n# Javaでクラスを作成する\n:::\n## クラスの定義\n\n:::container\n```java\nclass Person(){\n String name\n int age\n\n public void sayHello(){\n\tSystem.out.println("Hello")\n }\n}\n```\n:::\n\n## インスタンス作成\n\n:::container\n```java\nPerson person = new Person()\nperson.sayHello()\n```\n:::\n\n## 実行結果\n:::container\n```bash\nHello\n```\n:::\n\n\n',
            draft=False,
        )
        javaArticle.user = user2
        javaArticle.tags.append(javatag)
        comment5 = Comment(content="Javaは楽しい:smiley:")
        comment5.user = admin
        comment5.article = javaArticle

        todoArticle = Article(
            title="projectでのtodo",
            content="# プロジェクトでのTODO\n\n[ ] 設計書を作る\n[ ] 開発\n[ ] テスト\n[ ] デプロイ\n\n",
            draft=False,
        )
        todoArticle.user = user1

        dockerArticle = Article(
            title="docker-compose",
            content="# コンテナの立ち上げ\n\n:::container\n```\ndocker-compose up -d\n```\n:::\n\n",
            draft=False,
        )
        dockerArticle.user = user3

        session.add(comment)
        session.add(comment1)
        session.add(comment2)
        session.add(comment3)
        session.add(comment4)
        session.add(comment5)

        session.add(pipArticle)
        session.add(gitArticle)
        session.add(jsArticle)
        session.add(htmlArticle)
        session.add(musicArticle)
        session.add(plantUmlArticle)
        session.add(katexArticle)
        session.add(todoArticle)
        session.add(dockerArticle)
        session.commit()
        session.close()
        CONNECTION.close()
        ENGINE.dispose()


# このPythonスクリプトを実行したとき、テーブルを一旦削除して新規作成する
def main(args):
    Base.metadata.drop_all(bind=ENGINE)
    Base.metadata.create_all(bind=ENGINE)
    CONNECTION.close()


# このファイルを直接実行したとき、mainメソッドでテーブルを作成する
if __name__ == "__main__":
    main(sys.argv)
