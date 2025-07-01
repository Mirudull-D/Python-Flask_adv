from flask import Blueprint, render_template,jsonify
from flask import request
import validators
from src.constants.http_status_code import HTTP_400_BAD_REQUEST,HTTP_409_CONFLICT,HTTP_200_OK,HTTP_201_CREATED
from src.database import Bookmark,db
from flask_jwt_extended import get_jwt_identity,jwt_required

bookmark = Blueprint('bookmark', __name__)

@bookmark.route('/home',methods=['GET','POST'])
@jwt_required()
def hello_world():
    current_user=get_jwt_identity()
    if request.method=="POST":
        body=request.json.get('body')
        url=request.json.get('url')
        if not validators.url(url):
            return {
                "message": "Enter a valid url"
            },HTTP_400_BAD_REQUEST
        if Bookmark.query.filter_by(url=url).first():
            return {
                "message":"URL already exist"
            },HTTP_409_CONFLICT
        
        bookmark=Bookmark(body=body,url=url,user_id=current_user)
        db.session.add(bookmark)
        db.session.commit()
        return {
            "id":bookmark.id,
            "url":bookmark.url,
            "short_url":bookmark.short_url,
            "created_at":bookmark.created_at,
            "visits":bookmark.visits,
            "body":bookmark.body
        },HTTP_201_CREATED

    else:
        page=request.args.get('page',1,type=int)
        per_page=request.args.get('per_page',5,type=int)

        bookmarks=Bookmark.query.filter_by(user_id=current_user).paginate(page=page,per_page=per_page)
        
        data=[]

        for bookmark in bookmarks:
            data.append({
            "id":bookmark.id,
            "url":bookmark.url,
            "short_url":bookmark.short_url,
            "created_at":bookmark.created_at,
            "visits":bookmark.visits,
            "body":bookmark.body
        })
        meta = {
            "page": bookmarks.page,
            'pages': bookmarks.pages,
            'total_count': bookmarks.total,
            'prev_page': bookmarks.prev_num,
            'next_page': bookmarks.next_num,
            'has_next': bookmarks.has_next,
            'has_prev': bookmarks.has_prev,

        }

        return jsonify({"data":data,
                        "meta":meta}),HTTP_200_OK