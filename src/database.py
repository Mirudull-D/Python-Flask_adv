from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import random
import string
from sqlalchemy.orm import backref
from . import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now())
    updated_at = db.Column(db.DateTime, default=datetime.now(), onupdate=datetime.now())
    bookmarks = db.relationship('Bookmark', backref='user')

    def __repr__(self):
        return f'User>>> {self.username}>'
    
class Bookmark(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.Text(200), nullable=False)
    url = db.Column(db.Text(), nullable=False)
    user_id =db.Column(db.Integer,db.ForeignKey('user.id'), nullable=False)
    short_url = db.Column(db.String(100), unique=True, nullable=False)
    visits = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.now())
    updated_at = db.Column(db.DateTime, default=datetime.now(), onupdate=datetime.now())

    def generate_short_Characters(self):
        char=string.ascii_letters + string.digits
        picked_characters = "".join(random.choices(char, k=6)) 
        link=self.query.filter_by(short_url=picked_characters).first()
        if link:
            self.generate_short_Characters() 
        else:
            return picked_characters


    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        self.short_url = self.generate_short_Characters()

    def __repr__(self):
        return f'Bookmark>>> {self.url}>'