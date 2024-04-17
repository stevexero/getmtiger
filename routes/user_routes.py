from flask import Blueprint, jsonify, request
from services.temp_service import generate_temp_token, decode_temp_token, decode_clerk_token
from models.user_models import User
from services.user_service import add_user_to_database
from pydantic import ValidationError

user_bp = Blueprint('user', __name__)


@user_bp.route('/temp-login', methods=['POST'])
def temp_login():
    user_id = request.json.get('user_id')
    if user_id:
        token = generate_temp_token(user_id)
        return jsonify({'token': token}), 200
    else:
        return jsonify({'error': 'Invalid credentials'}), 401


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
