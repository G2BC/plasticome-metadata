from flask_jwt_extended import create_access_token
from plasticome_metadata.models.user_model import PlasticomeUsers
import bcrypt
from datetime import timedelta
from peewee import IntegrityError


def hash_secret(secret: str):
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(secret.encode('utf-8'), salt)
    return hashed.decode('utf-8')


def create_user(username: str, secret: str):
    try:
        hashed_secret = hash_secret(secret)

        PlasticomeUsers.create(username=username, secret=hashed_secret)
        return True, 'User created successfully'
    except IntegrityError:
        return False, 'This username already exists'
    except Exception as error:
        return None, error


def verify_secret(plain_secret: str, hashed_secret: str):
    return bcrypt.checkpw(
        plain_secret.encode('utf-8'), hashed_secret.encode('utf-8')
    )


def verify_credentials(username: str, secret: str):
    try:
        user = PlasticomeUsers.get(PlasticomeUsers.username == username)
        if verify_secret(secret, user.secret):
            access_token = create_access_token(
                identity=username, expires_delta=timedelta(hours=1)
            )
            return access_token, None
        else:
            return False, 'Invalid crendentials'
    except Exception as error:
        return None, error
