import os
import traceback
import random
from flask import Blueprint, jsonify, request, make_response
from datetime import timedelta, datetime
from flask_cors import cross_origin
from pydantic import ValidationError
from models.user_models import User
from services.auth_service import add_user_to_database, hash_password, generate_token, check_password_hash, \
    get_user_from_database_by_email, send_code_to_database, compare_code_to_database, update_user_email_in_database

auth_bp = Blueprint('auth', __name__)


#
# Register User
#
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


#
# Login User
#
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


#
# Logout User
#
@auth_bp.route('/api/logout', methods=['POST'])
@cross_origin(supports_credentials=True)
def logout():
    response = make_response(jsonify({"message": "Logged out successfully"}))
    response.delete_cookie('boxvalettoken')
    return response


#
# Send Verification Code
#
@auth_bp.route('/api/sendverificationcode', methods=['POST'])
@cross_origin(supports_credentials=True)
def send_verification_code():
    try:
        data = request.get_json()
        email = data['email']

        code = random.randint(100000, 999999)

        res = send_code_to_database(email, code)

        return jsonify(res)
    except Exception as e:
        print("An error occurred:", traceback.format_exc())
        return jsonify({'error': str(e)}), 500


#
# Submit Verification Code
#
@auth_bp.route('/api/submitverificationcode', methods=['POST'])
@cross_origin(supports_credentials=True)
def submit_verification_code():
    try:
        data = request.get_json()
        email = data['email']
        verification_code = data['verification_code']

        res, error, status_code = compare_code_to_database(email, verification_code)

        if error:
            print("Error comparing code:", error)
            return jsonify({'error': error}), status_code

        user, error, status_code = get_user_from_database_by_email(email)

        if not user:
            return jsonify({'error': 'User not found'}), 404

        if res:
            return jsonify(user), 200
        else:
            return jsonify({'message': 'Invalid code'}), 401
    except Exception as e:
        print("An error occurred:", traceback.format_exc())
        return jsonify({'error': str(e)}), 500


#
# Update User Email
#
@auth_bp.route('/api/updateuseremail', methods=['POST'])
@cross_origin(supports_credentials=True)
def update_user_email():
    try:
        data = request.get_json()
        old_email = data['oldEmail']
        new_email = data['newEmail']

        res, error, status_code = update_user_email_in_database(old_email, new_email)

        if error:
            print("Error updating email:", error)
            return jsonify({'error': error}), status_code

        user, error, status_code = get_user_from_database_by_email(new_email)

        if not user:
            return jsonify({'error': 'User not found'}), 404

        if res:
            return jsonify(user), 200
        else:
            return jsonify({'message': 'Invalid email'}), 401

    except Exception as e:
        print("An error occurred:", traceback.format_exc())
        return jsonify({'error': str(e)}), 500
