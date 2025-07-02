from flask import Flask,jsonify,render_template
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_jwt_extended import JWTManager
from datetime import timedelta
from src.constants.http_status_code import HTTP_404_NOT_FOUND,HTTP_500_INTERNAL_SERVER_ERROR
from flask_swagger_ui import get_swaggerui_blueprint 
from flask_cors import CORS




db = SQLAlchemy()
DB_NAME = 'database.db'

def create_app():
    
    app= Flask(__name__,instance_relative_config=True)
    app.config['SECRET_KEY'] = 'dev'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    app.config['JWT_SECRET_KEY']='kjsdbkjdb'
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(minutes=30)
    app.config["JWT_REFRESH_TOKEN_EXPIRES"] = timedelta(days=7)


    from flasgger import Swagger
    from flasgger.utils import swag_from

    swagger = Swagger( app, config={
        'headers': [],
        'specs': [
            {
                'endpoint': 'apispec_1',
                'route': '/apispec_1.json',
                'rule_filter': lambda rule: True, 
                'model_filter': lambda tag: True,  
            }
        ],
        'static_url_path': "/static_swagger",
        'swagger_ui': True,
        'specs_route': "/apidocs/"
    }, template_file='config/swagger.yaml')
        
    db.init_app(app)
    JWTManager(app)
    CORS(app)

    
    from .bookmark import bookmark
    from .auth import auth

    app.register_blueprint(auth,url_prefix='/')
    app.register_blueprint( bookmark,url_prefix='/')

    from .database import User, Bookmark
    create_database(app)


    @app.errorhandler(HTTP_404_NOT_FOUND)
    def handle_404(e):
        return jsonify({'error': 'Not found'}), HTTP_404_NOT_FOUND

    @app.errorhandler(HTTP_500_INTERNAL_SERVER_ERROR)
    def handle_500(e):
        return jsonify({'error': 'Something went wrong, we are working on it'}), HTTP_500_INTERNAL_SERVER_ERROR
    return app

def create_database(app):
    if not path.exists('src/'+DB_NAME):
        with app.app_context():
            db.create_all()
        print('Created Database')
