import base64
import os
import bcrypt
import datetime
import jwt
from supabase import create_client, Client
import resend

SB_URL = os.environ.get('SUPABASE_URL')
if not SB_URL:
    raise ValueError("Configuration error: SUPABASE_URL is not set.")

# SB_KEY = os.getenv('SUPABASE_KEY')  # TODO: Set up for production w/ permissions

SB_KEY = os.environ.get('SUPABASE_SERVICE_ROLE_KEY')
if not SB_KEY:
    raise ValueError("Configuration error: SUPABASE_SERVICE_ROLE_KEY is not set.")

RESEND_API_KEY = os.environ.get("RESEND_API_KEY")
if not RESEND_API_KEY:
    raise ValueError("Configuration error: RESEND_API_KEY is not set")

supabase: Client = create_client(SB_URL, SB_KEY)
resend.api_key = RESEND_API_KEY


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
    try:
        response = supabase.table('users').select('*').eq('email', email).execute()

        if response.data:
            return response.data[0], None, 200
        else:
            return None, "User not found", 404

    except Exception as e:
        print("Error fetching user:", str(e))
        return None, str(e), 500


def send_code_to_user_email(data):
    email = data['email']
    code = data['temp_code']
    try:
        params: resend.Emails.SendParams = {
            "from": "BoxValet <onboarding@box-valet.com>",
            "to": [email],
            "subject": "BoxValet Verification Code",
            "html": f"<div>"
                    f"<h1>Thank you for choosing BoxValet!</h1>"
                    f"<h2>You're verification code is:</h2>"
                    f"<br />"
                    f"<h3>{code}</h3>"
                    f"<br />"
                    f"<p>Use this code in the input field on your BoxValet dashboard</p>"
                    f"<br />"
                    f"<p>This code will expire in 15 minutes if not used, at which point you'll need to request another.</p>"
                    f"<br />"
                    f"<p>Sincerely,</p>"
                    f"<p>The BoxValet Team</p>"
                    f"</div>",
        }

        email_response = resend.Emails.send(params)

        return email_response
    except Exception as e:
        print("Error sending email:", str(e))
        return None, str(e), 500


def send_code_to_database(email, code):
    try:
        response = supabase.from_('users').update({"temp_code": code}).eq('email', email).execute()

        response_id = send_code_to_user_email(response.data[0])

        if response_id:
            return response_id
        else:
            return None, "User not found", 404
    except Exception as e:
        print("Error setting code to user:", str(e))
        return None, str(e), 500


def compare_code_to_database(email, code):
    try:
        response = supabase.from_('users').select('*').eq('email', email).single().execute()

        if not response.data:
            return None, "User not found", 404

        db_code = response.data['temp_code']

        if db_code != code:
            return None, "Code didn't match", 401

        update_response = supabase.from_('users').update({"email_verified": True, "temp_code": None}).eq('email',
                                                                                                         email).execute()

        if update_response.data is None:
            return None, "Failed to update email_verified field", 500

        return True, None, 200
    except Exception as e:
        print("Error comparing code:", str(e))
        return None, str(e), 500


def update_user_email_in_database(email, new_email):
    try:
        response = supabase.from_('users').select('*').eq('email', email).single().execute()

        if response.data is None:
            return None, "User not found", 404

        update_response = supabase.from_('users').update({"email": new_email}).eq('email',
                                                                                  email).execute()

        if update_response.data is None:
            return None, "Failed to update email", 500

        return True, None, 200
    except Exception as e:
        print("Error updating email:", str(e))
        return None, str(e), 500
