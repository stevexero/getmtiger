import os
import traceback
from flask import Blueprint, jsonify, request, make_response
from datetime import timedelta, datetime
from flask_cors import cross_origin
from pydantic import ValidationError
from models.user_models import User
from services.auth_service import add_user_to_database, hash_password, generate_token, check_password_hash, \
    get_user_from_database_by_email

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/api/register', methods=['POST'])
@cross_origin(supports_credentials=True)
def register():
    try:
        user = User.parse_obj(request.get_json())
    except ValidationError as ve:
        return jsonify({'error': ve.messages}), 400

    hashed_password = hash_password(user.password)
    print(hashed_password)
    user_dict = user.dict()
    print(user_dict)
    user_dict['password'] = hashed_password
    print(user_dict)

    user_data, error, status_code = add_user_to_database(user_dict)

    if error:
        return jsonify({'error': str(error)}), status_code

    user_data.pop('password', None)

    token = generate_token(user_data['user_id'])

    response = make_response(jsonify(user_data), status_code)
    expires = datetime.utcnow() + timedelta(days=14)
    response.set_cookie('boxvalettoken', value=token, expires=expires, httponly=True, path='/',
                        secure=os.environ.get('ENVIRONMENT') == 'production', samesite=os.environ.get('SAMESITE'))

    return response


@auth_bp.route('/api/login', methods=['POST'])
@cross_origin(supports_credentials=True)
def login():
    try:
        input_data = request.get_json()
        user_email = input_data['email']
        user_password = input_data['password']

        user, error, status_code = get_user_from_database_by_email(user_email)

        if error:
            print("Error fetching user:", error)
            return jsonify({'error': error}), status_code

        if not user:
            return jsonify({'error': 'User not found'}), 404

        try:
            if not check_password_hash(user_password, user['password']):
                return jsonify({'error': 'Invalid username or password'}), 401
        except ValueError as e:
            print("Error checking password:", str(e))
            return jsonify({'error': 'Internal server error'}), 500

        # if not user or not check_password_hash(user_password, user['password']):
        #     return jsonify({'error': 'Invalid username or password'}), 401

        token = generate_token(user['user_id'])
        # response = make_response(jsonify({'message': 'Login successful', 'user_id': user['user_id']}), 200)
        response = make_response(jsonify(user), status_code)
        expires = datetime.utcnow() + timedelta(days=14)
        response.set_cookie('boxvalettoken', value=token, expires=expires, httponly=True,
                            path='/', secure=os.environ.get('ENVIRONMENT') == 'production',
                            samesite=os.environ.get('SAMESITE'))

        return response
    except Exception as e:
        print("An error occurred:", traceback.format_exc())
        return jsonify({'error': str(e)}), 500


@auth_bp.route('/api/logout', methods=['POST'])
@cross_origin(supports_credentials=True)
def logout():
    response = make_response(jsonify({"message": "Logged out successfully"}))
    response.delete_cookie('boxvalettoken')
    return response
