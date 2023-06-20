import re

from exts import db
from models import User
from flask import Blueprint, render_template, request, redirect, url_for, session

bp = Blueprint("public", __name__, url_prefix="/")


@bp.route("/")
def index():
    return render_template("index.html")

@bp.route("/login", methods=['GET', 'POST'])
def login(sesson=None):
    if request.method == 'GET':
        return render_template("login.html")
    else:
        email1 = request.form.get('email')
        password1 = request.form.get('password')
        user = User.query.filter_by(email=email1).first()
        if not user:
            return render_template("login.html",data=1)
        else:
            if user.password == password1:
                # print(user.username)
                session['user_id'] = user.id
                return redirect(url_for('user.user_index'))
            else:
                return render_template("login.html", data=0)


@bp.route("/register")
def register():
    return render_template("register.html")

# @bp.route("/eidt_user/<id>")
# def edit_user(id):
