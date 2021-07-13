import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


from app import create_app, db
from models.UserModel import User
from models.BlacklistTokenModel import BlacklistToken

config_name = os.environ.get("FLASK_ENV")
app = create_app(config_name)

# migration
Migrate(app, db)
# end of migration

@app.cli.command("seed-users")
def seed():
    """Seed the user table."""
    user1 = User(
        email="admin@mail.com",
        password="password123",
        is_admin=True
    ).save()
    user2 = User(
        email="user@mail.com",
        password="password123",
        is_admin=False
    ).save()

if __name__ == "__main__":
    app.run()
