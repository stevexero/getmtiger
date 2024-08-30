import os
from supabase import create_client, Client
from jwt import decode, exceptions
from jwt.jwks_client import PyJWKClient

SB_URL = os.environ.get('SUPABASE_URL')
if not SB_URL:
    raise ValueError("Configuration error: SUPABASE_URL is not set.")

# SB_KEY = os.getenv('SUPABASE_KEY')  # TODO: Set up for production w/ permissions

SB_KEY = os.environ.get('SUPABASE_SERVICE_ROLE_KEY')
if not SB_KEY:
    raise ValueError("Configuration error: SUPABASE_SERVICE_ROLE_KEY is not set.")

audience = os.environ.get('BOX_VALET_JWT_AUDIENCE')
if not audience:
    raise ValueError("Configuration error: BOX_VALET_JWT_AUDIENCE is not set.")

prod_issuer = os.environ.get('BOX_VALET_JWT_PROD_ISSUER')
if not prod_issuer:
    raise ValueError("Configuration error: BOX_VALET_JWT_PROD_ISSUER is not set.")

jwks_url = os.environ.get('JWKS_URL')
if not jwks_url:
    raise ValueError("Configuration error: JWKS_URL is not set.")

supabase: Client = create_client(SB_URL, SB_KEY)


def decode_clerk_token(token):
    """
    Decode a JWT token using the public key obtained from Clerk's JWKS URI.
    """
    print("from decode_clerk_token")
    print(token)

    jwk_client = PyJWKClient(jwks_url)
    print('from decode_clerk_token')
    print(jwk_client)

    # Decode the token using the public key
    try:
        signing_key = jwk_client.get_signing_key_from_jwt(token)
        print('from decode_clerk_token')
        print("Using signing key with KID:", signing_key.key_id)

        decoded_token = decode(
            token,
            signing_key.key,
            algorithms=["RS256"],
            audience=audience,
            issuer=prod_issuer
        )

        print('from decode_clerk_token')
        print("Decoded JWT payload:", decoded_token)

        return decoded_token['sub'], None
    except exceptions.PyJWTError as error:
        print("Error decoding JWT:", str(error))
        return None, str(error)


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


#
# Get All Customers From Database
#
def get_all_customers_from_database():
    try:
        response = supabase.table('users').select('*').eq('user_role', 'customer_active').execute()

        filtered_response = [
            {k: v for k, v in user.items() if k != 'password'}
            for user in response.data
        ]

        data = filtered_response

        if data:
            return data, None, 200
        else:
            return None, "Customers not found", 404

    except Exception as e:
        return None, str(e), 500


def get_all_bim_users_from_database():
    try:
        response = supabase.table('user_profiles').select('*').execute()

        if response and response.data:
            return response.data, None, 200
        else:
            return None, "Bim Users not found", 404

    except Exception as e:
        return None, str(e), 500


def add_bim_user_to_database(user_data):
    print('add_bim_user_to_database')
    email = user_data.get('email')
    password = user_data.get('password')
    bim_number = user_data.get('bim_number')

    try:
        # Create user in Supabase Auth
        auth_response = supabase.auth.admin.create_user({
            'email': email,
            'password': password,
            'email_confirm': True,
            # 'user_metadata': {
            #     'bim_number': bim_number
            # }
        })

        print(auth_response)

        if hasattr(auth_response, 'error') and auth_response.error:
            print(f"Auth error: {auth_response.error['message']}")
            return None, auth_response.error['message'], 400

        supabase_user_id = auth_response.user.id

        # Add user profile to the database
        profile_response = supabase.table('user_profiles').insert({
            'user_id': supabase_user_id,
            'username': bim_number,
            'first_login': True
        }).execute()

        print(profile_response)

        if not profile_response.data:
            print(f"Profile creation error: {profile_response}")
            return None, 'Failed to create user profile', 500

        return {
            'user_id': supabase_user_id,
            'email': email,
            'bim_number': bim_number,
            'message': 'User created successfully'
        }, None, 201

    except Exception as e:
        print(f"Exception: {e}")
        return None, str(e), 500

