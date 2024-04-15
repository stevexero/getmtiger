import os
import jwt
from datetime import datetime, timedelta


def generate_temp_token(user_id):
    """
    Generate a temporary JWT token for a given user ID.
    """
    payload = {
        'user_id': user_id,
        'exp': datetime.utcnow() + timedelta(days=1)  # Token expires in one day
    }
    return jwt.encode(payload, os.environ.get('TEMP_SECRET_KEY'), algorithm='HS256')


def decode_temp_token(token):
    """
    Decode a temporary JWT token to extract user details.
    """
    try:
        payload = jwt.decode(token, os.environ.get('TEMP_SECRET_KEY'), algorithms=['HS256'])
        return payload['user_id'], None
    except jwt.ExpiredSignatureError:
        return None, "Signature has expired."
    except jwt.InvalidTokenError:
        return None, "Invalid token."
