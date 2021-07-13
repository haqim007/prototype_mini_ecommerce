from flask_api import FlaskAPI
from flask import current_app as app, request, Blueprint, make_response, jsonify
from flask.views import MethodView
from app import bcrypt
import os
import datetime

# local
from models.UserModel import User
from models.BlacklistTokenModel import BlacklistToken
auth_blueprint = Blueprint('auth', __name__)

class RegistrationAPI(MethodView):
    """
    User registration resource
    """
    def post(self):
        # get post data
        post = request.get_json()
        # check if user already exists
        user = User.query.filter_by(email=post.get("email")).first()
        if not user:
            try:
                user = User(
                    email=post.get("email"),
                    password=post.get("password"),
                    is_admin=post.get("is_admin")
                )

                # insert user
                user.save()
                # generate token
                auth_token = user.encode_auth_token(user.id)
                resObj = {
                    "status": "success",
                    "message": "Successfully registered.",
                    "auth_token": auth_token
                }

                return make_response(jsonify(resObj)), 201
            except Exception as Ex:
                resObj = {
                    "status": "fail",
                    "message": "Some error eccured. Please try again later",
                    # "error": str(Ex)
                }
                return make_response(jsonify(resObj)), 401
        else:
            resObj = {
                "status": "fail",
                "message": "User already exists. Please Login.",
                # "error": str(user)
            }
            return make_response(jsonify(resObj)), 202


class LoginAPI(MethodView):
    """
    User Login Resource
    """

    def post(self):
        # get the post data
        post = request.get_json()

        try:
            # fetch the user data
            user = User.query.filter_by(
                email=post.get('email')
            ).first()
            if user and bcrypt.check_password_hash(
                user.password, post.get('password')
            ):
                session_live = datetime.timedelta(days=0, seconds=5) if app.config["TESTING"] else \
                    datetime.timedelta(days=0, seconds=60)
                auth_token = user.encode_auth_token(user.id, session_live)
                if auth_token:
                    responseObject = {
                        'status': 'success',
                        'message': 'Successfully logged in.',
                        'auth_token': auth_token
                    }
                    return make_response(jsonify(responseObject)), 200
            else:
                responseObject = {
                    'status': 'fail',
                    'message': 'User does not exist.'
                }
                return make_response(jsonify(responseObject)), 404
        except Exception as e:
            print(e)
            responseObject = {
                'status': 'fail',
                'message': 'Try again'
            }
            return make_response(jsonify(responseObject)), 500

class LogoutAPI(MethodView):
    """
    User logout resource
    """

    def post(self):
        # get the post data
        auth_header = request.headers.get("Authorization")
        if auth_header:
            auth_token = auth_header.split(" ")[1]
        else:
            auth_token = ''

        if auth_token:
            token = User.decode_auth_token(auth_token)
            if not isinstance(token, str):
                try:
                    blacklist_token = BlacklistToken(token=auth_token)
                    # insert the token
                    blacklist_token.save()
                    responseObject = {
                        'status': 'success',
                        'message': 'Successfully logged out.'
                    }
                    return make_response(jsonify(responseObject)), 200
                except Exception as e:
                    responseObject = {
                        'status': 'fail',
                        'message': str(e)
                    }
                    return make_response(jsonify(responseObject)), 401
            else:
                responseObject = {
                    'status': 'fail',
                    'message': token
                }
                return make_response(jsonify(responseObject)), 401
        else:
            responseObject = {
                'status': 'fail',
                'message': 'Provide a valid auth token.'
            }
            return make_response(jsonify(responseObject)), 403


register_view = RegistrationAPI.as_view("registration_api")
login_view = LoginAPI.as_view('login_api')
logout_view = LogoutAPI.as_view('logout_api')

auth_blueprint.add_url_rule(
    '/register',
    view_func=register_view,
    methods=['POST']
)

auth_blueprint.add_url_rule(
    '/login',
    view_func=login_view,
    methods=['POST']
)

auth_blueprint.add_url_rule(
    '/logout',
    view_func=logout_view,
    methods=['POST']
)
