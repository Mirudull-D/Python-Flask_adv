from flask import Blueprint, render_template


bookmark = Blueprint('bookmark', __name__)

@bookmark.route("/login" )
def login():
    return "kjbkjfsjk"
@bookmark.route("/signin")
def login_get():
    return 'login'

