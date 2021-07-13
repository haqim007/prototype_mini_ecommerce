from flask_api import FlaskAPI
from flask import current_app as app, request, Blueprint, make_response, jsonify
from flask.views import MethodView
from app import bcrypt
import os
from datetime import datetime

# local
from models.UserModel import User
from models.ProductModel import Product
from models.DiscountModel import Discount

products_blueprint = Blueprint('products', __name__)

class ProductsAPI(MethodView):
    """"
    Products CRUD Resources
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
        Endpoint to create/add new product
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
                            "message": "Only admin can add product.",
                            "product": None
                        }

                        return make_response(jsonify(resObj)), 401
                    else:
                        # get the post data
                        post = request.get_json()
                        product = Product(
                            group_code=post.get("group_code"),
                            name=post.get("name"),
                            price=post.get("price"),
                            stocks=post.get("stocks"),
                            is_active=post.get("is_active"))
                        product.save()
                        resObj = {
                            "status": "success",
                            "message": "Successfully added the product.",
                            "product": {
                                "id": product.id, "name": product.name,
                                "stocks": product.stocks, "price": product.price}
                        }

                        return make_response(jsonify(resObj)), 201
                except Exception as Ex:
                    resObj = {
                        "status": "fail",
                        "message": "Some error eccured. Please try again later",
                        "product": None,
                        "log": str(Ex)
                    }

                    return make_response(jsonify(resObj)), 500
            else:
                responseObject = {
                    'status': 'fail',
                    'message': user_id,
                    'product': None
                }
                return make_response(jsonify(responseObject)), 401
        else:
            responseObject = {
                'status': 'fail',
                'message': 'Provide a valid auth token.',
                'product': None
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
                    user = User.query.filter_by(id=user_id).first()
                    # will return message if token is invalid
                    user_id = User.decode_auth_token(token)

                    if user.is_admin:
                        products = Product.get_all()
                        from flask_sqlalchemy import get_debug_queries
                    else:
                        products = Product.query.filter_by(is_active=True).all()

                    results = []
                    for prod in products:
                        obj = {
                            'id': prod.id,
                            'group_code': prod.group_code,
                            'name': prod.name,
                            'price': prod.price,
                            'is_active': prod.is_active,
                            'stocks': prod.stocks,
                            'created_datetime': prod.created_datetime,
                            'updated_datetime': prod.updated_datetime,
                            'discount': prod.discount[0].rate if len(prod.discount) > 0 else None
                        }
                        results.append(obj)

                    responseObject = {
                        'status': 'success',
                        'message': 'Successfully retrieved products.',
                        'products': results
                    }
                    return make_response(jsonify(responseObject)), 200
                except Exception as e:
                    responseObject = {
                        'status': 'fail',
                        'message': str(e),
                        'products': []
                    }
                    return make_response(jsonify(responseObject)), 500
            else:
                responseObject = {
                    'status': 'fail',
                    'message': user_id,
                    'products': []
                }
                return make_response(jsonify(responseObject)), 401

        else:
            responseObject = {
                'status': 'fail',
                'message': 'Provide a valid auth token.',
                'products': []
            }
            return make_response(jsonify(responseObject)), 403


products_view = ProductsAPI.as_view('products_api')

products_blueprint.add_url_rule(
    '',
    view_func=products_view,
    methods=['POST']
)

products_blueprint.add_url_rule(
    '',
    view_func=products_view,
    methods=['GET']
)
