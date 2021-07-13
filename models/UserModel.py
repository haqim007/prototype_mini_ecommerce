import datetime
import jwt
from flask import current_app as app
from alembic import op

# local
from app import db, bcrypt
from models.BlacklistTokenModel import BlacklistToken


class User(db.Model):
    """ User Model for storing user credential """

    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    created_datetime = db.Column(db.DateTime, nullable=False)
    is_admin = db.Column(db.Boolean, nullable=False, default=False)

    def __init__(self, email, password, is_admin=False):
        self.email = email
        self.password = bcrypt.generate_password_hash(
            password, app.config.get('BCRYPT_LOG_ROUNDS')
        ).decode()
        self.created_datetime = datetime.datetime.now()
        self.is_admin = is_admin

    def save(self):
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def get_all():
        return User.query.all()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def __repr__(self):
        return "<User: {}>".format(self.email)

    def encode_auth_token(self, user_id, timedelta=datetime.timedelta(days=0, seconds=60)):
        """
        Generate auth token
        \n
        :return: string
        """
        try:
            payload = {
                "exp": datetime.datetime.utcnow() + timedelta,
                "iat": datetime.datetime.utcnow(),
                "sub": user_id
            }

            return jwt.encode(
                payload,
                app.config.get("SECRET_KEY"),
                algorithm='HS256'
            )
        except Exception as Ex:
            print('Caught this error: ' + repr(Ex))
            return Ex

    @staticmethod
    def decode_auth_token(auth_token):
        """
        Decode the token \n
        :param str auth_token: JWT Token
        :return: integer|string
        """
        try:
            payload = jwt.decode(auth_token, app.config.get(
                'SECRET_KEY'), algorithms='HS256')
            is_token_blacklisted = BlacklistToken.check_blacklist(auth_token)
            if is_token_blacklisted:
                return 'Token blacklisted. Please log in again.'
            else:
                return int(payload['sub'])
        except jwt.ExpiredSignatureError:
            return "Signature expired. Please login"
        except jwt.InvalidTokenError:
            return "Invalid token. Please login"
        except Exception as Ex:
            return Ex
