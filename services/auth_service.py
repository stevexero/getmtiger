import base64
import os
import bcrypt
import datetime
import jwt
from supabase import create_client, Client

SB_URL = os.environ.get('SUPABASE_URL')
if not SB_URL:
    raise ValueError("Configuration error: SUPABASE_URL is not set.")

# SB_KEY = os.getenv('SUPABASE_KEY')  # TODO: Set up for production w/ permissions

SB_KEY = os.environ.get('SUPABASE_SERVICE_ROLE_KEY')
if not SB_KEY:
    raise ValueError("Configuration error: SUPABASE_SERVICE_ROLE_KEY is not set.")

supabase: Client = create_client(SB_URL, SB_KEY)


def generate_token(user_id):
    expiration_time = datetime.datetime.utcnow() + datetime.timedelta(days=14)
    token = jwt.encode({
        'user_id': user_id,
        'exp': expiration_time
    }, os.environ.get('SECRET_KEY'), algorithm='HS256')

    return token


def hash_password(password):
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode(), salt)
    result = base64.b64encode(hashed_password).decode('utf-8')
    return result


def check_password_hash(password, hashed):
    try:
        hashed_bytes = base64.b64decode(hashed.encode('utf-8'))

        if not hashed_bytes.startswith(b'$2b$'):
            raise ValueError("Decoded hash does not start with bcrypt format")

        result = bcrypt.checkpw(password.encode(), hashed_bytes)
        return result
    except Exception as e:
        print("Failed to verify hash:", str(e))
        raise


def check_user_exists(email):
    try:
        query = supabase.table('users').select("email").or_(f"email.eq.{email}").execute()

        if query.data:
            return True  # User exists
        return False  # User does not exist
    except Exception as e:
        print(f"Error checking user exists: {str(e)}")
        return False


def add_user_to_database(data):

    if check_user_exists(data['email']):
        return None, 'User with this Email already exists', 409

    try:
        response = supabase.table('users').insert(data).execute()
        if hasattr(response, 'error') and response.error:
            return None, response.error, 500
        return response.data[0], None, 201
    except Exception as e:
        return None, str(e), 500


def get_user_from_database_by_email(email):
    print("Fetching user from database by email")
    try:
        response = supabase.table('users').select('*').eq('email', email).execute()

        if response.data:
            return response.data[0], None, 200
        else:
            return None, "User not found", 404

    except Exception as e:
        print("Error fetching user:", str(e))
        return None, str(e), 500
