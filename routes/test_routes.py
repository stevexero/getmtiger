from flask import Blueprint, jsonify
import bcrypt
import base64
from browser_automation import test_browser_automation

test_bp = Blueprint('test_bp', __name__)


@test_bp.route('/hello')
def hello_world():
    return jsonify({"message": 'Hello World!'})


@test_bp.route('/test-browser')
def test_browser():
    try:
        page_title = test_browser_automation()
        return jsonify({"message": "Browser automation successful", "pageTitle": page_title})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@test_bp.route('/test_hash')
def test_hash():
    password = "12345678"
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode(), salt)
    encoded_hash = base64.b64encode(hashed).decode('utf-8')
    decoded_hash = base64.b64decode(encoded_hash.encode('utf-8'))

    assert hashed == decoded_hash, "Mismatch in hash before and after encoding/decoding!"

    return f"Hashing test passed! Original: {hashed}, Encoded: {encoded_hash}, Decoded: {decoded_hash}"