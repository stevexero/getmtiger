import os
from supabase import create_client, Client

SB_URL = os.getenv('SUPABASE_URL')
# SB_KEY = os.getenv('SUPABASE_KEY')  # TODO: Set up for production w/ permissions
SB_KEY = os.getenv('SUPABASE_SERVICE_ROLE_KEY')
supabase: Client = create_client(SB_URL, SB_KEY)


def check_user_exists(user_id, email):
    print("from check_user_exists")
    print(user_id, email)

    try:
        query = supabase.table('users').select("user_id, email").or_(f"user_id.eq.{user_id},email.eq.{email}").execute()
        print("from check_user_exists")
        print(query)

        if query.data:
            print("from check_user_exists")
            print(query.data)
            print("User exists")
            return True  # User exists
        print("from check_user_exists")
        print("User does not exists")
        return False  # User does not exist
    except Exception as e:
        print(f"Error checking user exists: {str(e)}")
        return False


def add_user_to_database(data):
    print("from add_user_to_database")
    print(data)

    if check_user_exists(data['user_id'], data['email']):
        return None, 'User with this ID or Email already exists', 409

    print("from add_user_to_database")
    print(data['user_id'], data['email'])

    try:
        response = supabase.table('users').insert(data).execute()
        print("from add_user_to_database")
        print(response)
        if hasattr(response, 'error') and response.error:
            return None, response.error, 500
        print("from add_user_to_database")
        print(response.data[0])
        return response.data[0], None, 201
    except Exception as e:
        return None, str(e), 500


def get_user_from_database(user_id):
    print("from get_user_from_database")
    print(user_id)

    try:
        response = supabase.table('users').select('*').eq('user_id', user_id).execute()
        print("from get_user_from_database")
        print(response)

        print("from get_user_from_database")
        data = response.data
        print(data)
        if data:
            print("User fetched successfully:", data)
            return data[0] if data else None, None, 200
        else:
            return None, "User not found", 404

    except Exception as e:
        return None, str(e), 500
