from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_jwt_extended import JWTManager
from datetime import timedelta


db = SQLAlchemy()
DB_NAME = 'database.db'

def create_app():
    
    app= Flask(__name__,instance_relative_config=True)
    app.config['SECRET_KEY'] = 'dev'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    app.config['JWT_SECRET_KEY']='kjsdbkjdb'
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(minutes=30)
    app.config["JWT_REFRESH_TOKEN_EXPIRES"] = timedelta(days=7)


    
    
    db.init_app(app)
    JWTManager(app)
    
    
    from .bookmark import bookmark
    from .auth import auth

    app.register_blueprint(auth,url_prefix='/')
    app.register_blueprint( bookmark,url_prefix='/')

    from .database import User, Bookmark
    create_database(app)


    return app
def create_database(app):
    if not path.exists('src/'+DB_NAME):
        with app.app_context():
            db.create_all()
        print('Created Database')
