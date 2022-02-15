from crypt import methods
from email.policy import default
from flask import Flask
from flask import render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from datetime import datetime
import pytz

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///memo.db'
db = SQLAlchemy(app)
bootstrap = Bootstrap(app)

class Post(db.Model): #データベース定義
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), nullable=False)
    url = db.Column(db.String(100), nullable=True)
    body = db.Column(db.String(500), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now(pytz.timezone('Asia/Tokyo')))

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "GET":
        posts = Post.query.all() #Post内の全てのデータをリスト形式で取得
        return render_template("index.html", posts=posts)

@app.route("/create", methods=["GET", "POST"])
def create():
    if request.method == "GET":
        return render_template("create.html")
    else:
        title = request.form.get("title") #formでPOSTされたデータを取得
        url = request.form.get("url")
        body = request.form.get("body")

        post = Post(title=title, url=url, body=body) #フォームで取ってきたものをデータベースの値に代入

        db.session.add(post) #データベースに追加
        db.session.commit() #コミットしないと追加、保存されない
        return redirect("/") #初期画面へリダイレクト

@app.route("/<int:id>/update", methods=["GET", "POST"])
def update(id): #post.idがidに入る
    post = Post.query.get(id) #Post内の特定のデータをリスト形式で取得
    if request.method == "GET":
        return render_template("update.html", post=post)
    else:
        post.title = request.form.get("title") #formでPOSTされたデータを取得
        post.url = request.form.get("url")
        post.body = request.form.get("body")

        db.session.commit() #更新するときはコミットのみでOK
        return redirect("/") #初期画面へリダイレクト

@app.route("/<int:id>/delete", methods=["GET"])
def delete(id): #post.idがidに入る
    post = Post.query.get(id) #Post内の特定のデータをリスト形式で取得
    
    db.session.delete(post) #データベースのデータを削除
    db.session.commit()
    return redirect("/") #初期画面へリダイレクト