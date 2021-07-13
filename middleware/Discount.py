from flask_api import FlaskAPI
from flask import current_app as app, request, Blueprint, make_response, jsonify
from flask.views import MethodView
from app import bcrypt
import os
import datetime

# local
from models.UserModel import User
from models.DiscountModel import Discount

discounts_blueprint = Blueprint('discounts', __name__)


class DiscountsAPI(MethodView):
    """"
    discounts CRUD Resources
    """

    @staticmethod
    def get_header_auth(header_auth):
        # get the post data
        auth_header = header_auth
        if auth_header:
            auth_token = auth_header.split(" ")[1]
        else:
            auth_token = ''

        return auth_token

    def post(self):
        """
        Endpoint to create/add new discount
        """
        # get token
        token = self.get_header_auth(request.headers.get("Authorization"))

        if token:
            # will return message if token is invalid
            user_id = User.decode_auth_token(token)
            if not isinstance(user_id, str):
                user = User.query.filter_by(id=user_id).first()
                try:
                    if not user.is_admin:
                        resObj = {
                            "status": "fail",
                            "message": "Only admin can add discount.",
                            "discount": None
                        }

                        return make_response(jsonify(resObj)), 401
                    else:
                        # get the post data
                        post = request.get_json()
                        discount = Discount(
                            name=post.get("name"),
                            start_campaign_datetime=post.get("start_campaign_datetime"),
                            end_campaign_datetime=post.get("end_campaign_datetime"),
                            product_id=post.get("product_id"),
                            rate=post.get("rate"))
                        discount.save()
                        resObj = {
                            "status": "success",
                            "message": "Successfully added the discount.",
                            "discount": {"id": discount.id, "name": discount.name, "rate": discount.rate,
                                         "start_campaign_datetime": discount.start_campaign_datetime,
                                         "end_campaign_datetime": discount.end_campaign_datetime}
                        }

                        return make_response(jsonify(resObj)), 201
                except Exception as Ex:
                    resObj = {
                        "status": "fail",
                        "message": "Some error eccured. Please try again later",
                        "discount": None,
                        "log": str(Ex)
                    }

                    return make_response(jsonify(resObj)), 500
            else:
                responseObject = {
                    'status': 'fail',
                    'message': user_id,
                    'discount': None
                }
                return make_response(jsonify(responseObject)), 401
        else:
            responseObject = {
                'status': 'fail',
                'message': 'Provide a valid auth token.',
                'discount': None
            }
            return make_response(jsonify(responseObject)), 403

    def get(self):
        # get token
        token = self.get_header_auth(request.headers.get("Authorization"))

        if token:
            # will return message if token is invalid
            user_id = User.decode_auth_token(token)
            if not isinstance(user_id, str):
                try:
                    # will return message if token is invalid
                    user_id = User.decode_auth_token(token)
                    discounts = Discount.get_all()
                    results = []

                    for prod in discounts:
                        obj = {
                            'id': prod.id,
                            'group_code': prod.group_code,
                            'name': prod.name,
                            'price': prod.price,
                            'is_active': prod.is_active,
                            'stocks': prod.stocks,
                            'created_datetime': prod.created_datetime,
                            'updated_datetime': prod.updated_datetime
                        }
                        results.append(obj)

                    responseObject = {
                        'status': 'success',
                        'message': 'Successfully retrieved discounts.',
                        'discounts': results
                    }
                    return make_response(jsonify(responseObject)), 200
                except Exception as e:
                    responseObject = {
                        'status': 'fail',
                        'message': str(e),
                        'discounts': []
                    }
                    return make_response(jsonify(responseObject)), 500
            else:
                responseObject = {
                    'status': 'fail',
                    'message': user_id,
                    'discounts': []
                }
                return make_response(jsonify(responseObject)), 401

        else:
            responseObject = {
                'status': 'fail',
                'message': 'Provide a valid auth token.',
                'discounts': []
            }
            return make_response(jsonify(responseObject)), 403


discounts_view = DiscountsAPI.as_view('discounts_api')

discounts_blueprint.add_url_rule(
    '',
    view_func=discounts_view,
    methods=['POST']
)

discounts_blueprint.add_url_rule(
    '',
    view_func=discounts_view,
    methods=['GET']
)
