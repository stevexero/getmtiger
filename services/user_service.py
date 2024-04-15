import os
from supabase import create_client, Client

SB_URL = os.getenv('SUPABASE_URL')
# SB_KEY = os.getenv('SUPABASE_KEY')  # TODO: Set up for production w/ permissions
SB_KEY = os.getenv('SUPABASE_SERVICE_ROLE_KEY')
supabase: Client = create_client(SB_URL, SB_KEY)


def check_user_exists(user_id, email):
    try:
        query = supabase.table('users').select("user_id, email").or_(f"user_id.eq.{user_id},email.eq.{email}").execute()
        if query.data:
            return True  # User exists
        return False  # User does not exist
    except Exception as e:
        print(f"Error checking user exists: {str(e)}")
        return False


def add_user_to_database(data):
    if check_user_exists(data['user_id'], data['email']):
        return None, 'User with this ID or Email already exists'

    try:
        response = supabase.table('users').insert(data).execute()
        if hasattr(response, 'error') and response.error:
            return None, response.error
        return response.data[0], None
    except Exception as e:
        return None, str(e)
