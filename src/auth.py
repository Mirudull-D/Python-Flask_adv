from flask import Blueprint,request,jsonify,redirect
from werkzeug.security import generate_password_hash, check_password_hash
import validators
from src.database import User,db,Bookmark
from flask_jwt_extended import create_access_token,create_refresh_token,jwt_required,get_jwt_identity,get_jwt
from src.constants.http_status_code import HTTP_409_CONFLICT, HTTP_406_NOT_ACCEPTABLE, HTTP_201_CREATED, HTTP_200_OK, HTTP_401_UNAUTHORIZED
from src.blacklist import BLACKLIST

auth = Blueprint('auth', __name__)

@auth.route('/register', methods=['POST', 'GET'])
def register():
    
    username=request.json['username']
    email=request.json['email']
    password=request.json['password']

    if len(username) < 3:
        return jsonify({'error': 'Username must be at least 3 characters long.'}),HTTP_406_NOT_ACCEPTABLE
    if len(password) < 6:
        return jsonify({'error': 'Password must be at least 6 characters long.'}),HTTP_406_NOT_ACCEPTABLE
    if not validators.email(email):
        return jsonify({'error': 'Invalid email address.'}),HTTP_406_NOT_ACCEPTABLE
    if User.query.filter_by(username=username).first():
        return jsonify({'error': 'Username already exists.'}),HTTP_409_CONFLICT
    if User.query.filter_by(email=email).first():
        return jsonify({'error': 'Email already exists.'}),HTTP_409_CONFLICT
    

    hpass= generate_password_hash(password, method='pbkdf2:sha256')
    user = User(username=username, email=email, password=hpass)
    db.session.add(user)
    db.session.commit()
    
    

    return jsonify({'message': 'User registered successfully.',
                    "user":{"username":username,"email":email}}), HTTP_201_CREATED

@auth.post('/login')
def login():
    email = request.json.get('email')
    password = request.json.get('password')
    user = User.query.filter_by(email=email).first()

    if user:
        passcheck = check_password_hash(user.password, password)
        if passcheck:
            refresh= create_refresh_token(identity=str(user.id))
            access = create_access_token(identity=str(user.id))
            resp={
                'user':{
                    'username': user.username,
                    'email': user.email,
                    'access_token': access,
                    'refresh_token': refresh
                }
            }



            return jsonify(resp),HTTP_200_OK
    return jsonify({'error': 'Wrong Credentials'}), HTTP_401_UNAUTHORIZED
@auth.get('/me')
@jwt_required()
def me():
    user_id = get_jwt_identity()
    user = User.query.filter_by(id=user_id).first()

    return jsonify({
        'username': user.username,
        'email': user.email
    }),HTTP_200_OK

@auth.post('/refresh')
@jwt_required(refresh=True)
def refresh():
    user= get_jwt_identity()
    access_token = create_access_token(identity=str(user))
    resp={
        'access_token': access_token
    }
    return jsonify(resp),HTTP_200_OK

@auth.get('/<short_url>')
def redirect_to_url(short_url):
    bookmark=Bookmark.query.filter_by(short_url=short_url).first_or_404()
    if bookmark:
        bookmark.visits = bookmark.visits+1
        db.session.commit()
        return redirect(bookmark.url)

@auth.route("/logout", methods=["POST"])
@jwt_required()
def logout():
    jti = get_jwt()["jti"]
    BLACKLIST.add(jti)
    return jsonify(msg="Logged out successfully"), 200

    
