from flask import Blueprint, jsonify, request
from services.user_service import decode_clerk_token
from models.user_models import User
from services.user_service import add_user_to_database, get_user_from_database
from pydantic import ValidationError

user_bp = Blueprint('user', __name__)


# Add User
@user_bp.route('/api/add-user', methods=['POST'])
def add_user():
    token = request.headers.get('Authorization', '').split(' ')[1] if 'Authorization' in request.headers else None
    if not token:
        return jsonify({'error': 'Authorization token is missing or invalid'}), 401
    print('from add user')
    print(token)

    user_id, error = decode_clerk_token(token)
    if error:
        return jsonify({'error': error}), 403
    print('from add user')
    print(user_id)

    print('from add user')
    print("Raw JSON received:", request.json)
    try:
        user = User.parse_obj(request.get_json())
        print('from add user')
        print(user)
    except ValidationError as ve:
        return jsonify({'error': str(ve)}), 400

    user_data, error, status_code = add_user_to_database(user.dict())
    print('from add user')
    print(user_data)

    if error:
        return jsonify({'error': str(error)}), status_code

    return jsonify(user_data), status_code


# Get Current User
@user_bp.route('/api/get-current-user', methods=['GET'])
def get_current_user():
    token = request.headers.get('Authorization', '').split(' ')[1] if 'Authorization' in request.headers else None
    if not token:
        return jsonify({'error': 'Authorization token is missing or invalid'}), 401
    print('from get_current_user')
    print(token)

    user_id, error = decode_clerk_token(token)
    if error:
        return jsonify({'error': error}), 403

    print('from get_current_user')
    print("User ID retrieved:", user_id)

    user_data, error, status_code = get_user_from_database(user_id)
    print('from get_current_user')
    print(user_data)

    if error:
        return jsonify({'error': str(error)}), status_code

    return jsonify(user_data), status_code


@user_bp.route('/api/add-user-manually', methods=['POST'])
def add_user_manually():
    token = request.headers.get('Authorization', '').split(' ')[1] if 'Authorization' in request.headers else None
    if not token:
        return jsonify({'error': 'Authorization token is missing or invalid'}), 401
    print('from get_current_user')
    print(token)

    user_id, error = decode_clerk_token(token)
    if error:
        return jsonify({'error': error}), 403

    print('from get_current_user')
    print("User ID retrieved:", user_id)

    user_data, error, status_code = get_user_from_database(user_id)
    print('from get_current_user')
    print(user_data)

#     if user role is, read from body the user inputs
