from flask import Blueprint, jsonify
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
