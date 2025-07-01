from flask import Blueprint, render_template


bookmark = Blueprint('bookmark', __name__)

@bookmark.route('/')
def hello_world():
    return "hello world"

@bookmark.route("/home" )
def login():
    return "kjbkjfsjk"
@bookmark.route("/notes")
def login_get():
    return 'login'

