import os
import jwt
from datetime import datetime, timedelta
import requests
from jwt import decode, exceptions
from jwt.jwks_client import PyJWKClient


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
    try:
        payload = jwt.decode(token, os.environ.get('TEMP_SECRET_KEY'), algorithms=['HS256'])
        return payload['user_id'], None
    except jwt.ExpiredSignatureError:
        return None, "Signature has expired."
    except jwt.InvalidTokenError:
        return None, "Invalid token."


openid_config_url = 'https://uncommon-mako-31.clerk.accounts.dev/.well-known/openid-configuration'


def get_jwks_uri():
    """ Fetch the JWKS URI from Clerk's OpenID configuration """
    response = requests.get(openid_config_url)
    return response.json()['jwks_uri']


def decode_clerk_token(token):
    """
    Decode a JWT token using the public key obtained from Clerk's JWKS URI.
    """
    print("from decode_clerk_token")
    print(token)

    jwks_url = "https://uncommon-mako-31.clerk.accounts.dev/.well-known/jwks.json"
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
            audience="http://localhost:3000",  # TODO: update to reflect production audience
            issuer="https://uncommon-mako-31.clerk.accounts.dev"
        )

        print('from decode_clerk_token')
        print("Decoded JWT payload:", decoded_token)

        return decoded_token['sub'], None
    except exceptions.PyJWTError as error:
        print("Error decoding JWT:", str(error))
        return None, str(error)
