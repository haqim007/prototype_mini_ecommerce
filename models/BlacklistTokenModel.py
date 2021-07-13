import datetime

# local
from app import db, bcrypt

class BlacklistToken(db.Model):
    """
    Token Model for storing JWT tokens
    """
    __tablename__ = 'blacklist_tokens'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    token = db.Column(db.String(500), unique=True, nullable=False)
    blacklisted_on = db.Column(db.DateTime, nullable=False)

    def __init__(self, token):
        self.token = token
        self.blacklisted_on = datetime.datetime.now()

    def __repr__(self):
        return '<id: token: {}'.format(self.token)

    def save(self):
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def check_blacklist(token):
        """
        Check whether the token is blacklisted or not
        """
        check = BlacklistToken.query.filter_by(token=str(token)).first()

        return check
