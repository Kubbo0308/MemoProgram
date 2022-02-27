from crypt import methods
from email.policy import default
from enum import unique
from flask import Flask
from flask import render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, LoginManager, login_user, login_required, logout_user
from flask_bootstrap import Bootstrap

from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import os
import re
import pytz

app = Flask(__name__)
db_uri = os.environ.get('DATABASE_URL') or "postgresql://localhost/flaskmemo"
if db_uri and db_uri.startswith("postgres://"):
    db_uri = db_uri.replace("postgres://", "postgresql://", 1)
app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
#app.config['SECRET_KEY'] = os.urandom(24)
db = SQLAlchemy(app)
bootstrap = Bootstrap(app)

#login_manager = LoginManager()
#login_manager.init_app(app)

class Post(db.Model): #データベース定義
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), nullable=False)
    url = db.Column(db.String(100), nullable=True)
    body = db.Column(db.String(500), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now(pytz.timezone('Asia/Tokyo')))
'''
class User(UserMixin, db.Model): #データベース定義
    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(20), nullable=False, unique=True)
    password = db.Column(db.String(30), nullable=False)

@login_manager.user_loader
def load_user(user_id): #セッション情報取得
    return User.query.get(int(user_id))
'''

@app.route("/", methods=["GET", "POST"])
#@login_required #デコレータ追加
def index():
    if request.method == "GET":
        posts = Post.query.all() #Post内の全てのデータをリスト形式で取得
    return render_template("index.html", posts=posts)

'''
@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "GET":
        return render_template("signup.html")
    else:
        user_name = request.form.get("user_name") #formでPOSTされたデータを取得
        password = request.form.get("password")

        user = User(user_name=user_name, password=generate_password_hash(password, method='sha256')) #パスワードをハッシュ化

        db.session.add(user) #データベースに追加
        db.session.commit() #コミットしないと追加、保存されない
        return redirect("/login") #ログイン画面へリダイレクト

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    else:
        user_name = request.form.get("user_name") #formでPOSTされたデータを取得
        password = request.form.get("password")

        if (user_name == None) or (password == None):
            return redirect('/login')
        else:
            user = User.query.filter_by(user_name=user_name).first() #ユーザ名を取ってくる
            if check_password_hash(user.password, password): #パスワードハッシュがあっている場合
                login_user(user) #userにログイン
                return redirect("/") #初期画面へリダイレクト

@app.route("/logout")
@login_required #デコレータ追加
def logout():
    logout_user()
    return redirect("/login")
'''

@app.route("/create", methods=["GET", "POST"])
#@login_required #デコレータ追加
def create():
    if request.method == "GET":
        return render_template("create.html")
    else:
        title = request.form.get("title") #formでPOSTされたデータを取得
        url = request.form.get("url")
        body = request.form.get("body")

        post = Post(title=title, url=url, body=body)

        db.session.add(post) #データベースに追加
        db.session.commit() #コミットしないと追加、保存されない
        return redirect("/") #初期画面へリダイレクト

@app.route("/<int:id>/update", methods=["GET", "POST"])
#@login_required #デコレータ追加
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
#@login_required #デコレータ追加
def delete(id): #post.idがidに入る
    post = Post.query.get(id) #Post内の特定のデータをリスト形式で取得
    
    db.session.delete(post) #データベースのデータを削除
    db.session.commit()
    return redirect("/") #初期画面へリダイレクト

