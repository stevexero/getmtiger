import os
import jwt
from datetime import datetime, timedelta
import requests
from jwt import decode, exceptions
from jwt.jwks_client import PyJWKClient
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.serialization import load_pem_public_key, load_pem_private_key
import uuid


def load_test_private_key(path):
    try:
        with open(path, 'rb') as key_file:
            return load_pem_private_key(key_file.read(), password=None, backend=default_backend())
    except Exception as e:
        print(f"Failed to load private key from {path}: {str(e)}")
        raise SystemExit("Critical error: Private key could not be loaded.")


private_key_path = os.path.expanduser(os.environ.get('BOXVALET_TEST_PRIVATE_KEY_PATH'))

if not private_key_path:
    print("Private key path not set.")
    raise SystemExit("Configuration error: Private key path is missing.")

private_key = load_test_private_key(private_key_path)


def load_test_public_key(path):
    try:
        with open(path, 'rb') as key_file:
            return load_pem_public_key(key_file.read(), backend=default_backend())
    except Exception as e:
        print(f"Failed to load public key from {path}: {str(e)}")
        raise SystemExit("Critical error: Public key could not be loaded.")


public_key_path = os.path.expanduser(os.environ.get('BOXVALET_TEST_PUBLIC_KEY_PATH'))

if not public_key_path:
    print("Public key path not set.")
    raise SystemExit("Configuration error: Public key path is missing.")

public_key = load_test_public_key(public_key_path)


key_id = os.getenv('BOXVALET_TEST_KEY_ID')
if not key_id:
    raise ValueError("Configuration error: BOXVALET_TEST_KEY_ID is not set.")

audience = os.getenv('BOX_VALET_JWT_AUDIENCE')
if not audience:
    raise ValueError("Configuration error: BOX_VALET_JWT_AUDIENCE is not set.")

test_issuer = os.getenv('BOX_VALET_JWT_TEST_ISSUER')
if not test_issuer:
    raise ValueError("Configuration error: BOX_VALET_JWT_TEST_ISSUER is not set.")

prod_issuer = os.getenv('BOX_VALET_JWT_PROD_ISSUER')
if not prod_issuer:
    raise ValueError("Configuration error: BOX_VALET_JWT_PROD_ISSUER is not set.")


def generate_temp_token(user_id):
    """
    Generate a temporary JWT token for a given user ID.
    """
    jwt_id = str(uuid.uuid4())

    header = {
        "alg": "RS256",
        "typ": "JWT",
        "kid": key_id
    }

    payload = {
        "user_id": user_id,
        "exp": datetime.utcnow() + timedelta(days=1),
        "iat": datetime.utcnow(),
        "nbf": datetime.utcnow(),
        "sub": user_id,
        "aud": audience,
        "iss": test_issuer,
        "jti": jwt_id
    }

    return jwt.encode(payload, private_key, algorithm="RS256", headers=header)


def decode_temp_token(token):
    try:
        payload = jwt.decode(token, public_key, algorithms=["RS256"])
        return payload['user_id'], None
    except jwt.ExpiredSignatureError:
        return None, "Signature has expired."
    except jwt.DecodeError:
        return None, "Error decoding token."
    except jwt.InvalidTokenError:
        return None, "Invalid token."


openid_config_url = os.environ.get('OPENID_CONFIG_URL')


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

    jwks_url = os.environ.get('JWKS_URL')
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
