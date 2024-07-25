from flask import Blueprint, jsonify
import requests
from services.session_service import save_ip_address

session_bp = Blueprint('session', __name__)


#
# Get Session IP Address
#
@session_bp.route('/api/getsessionip', methods=['GET'])
def get_session_ip():
    try:
        ip_uri = 'https://api.ipify.org?format=json'
        response = requests.get(ip_uri)
        response.raise_for_status()
        ip_data = response.json()

        ip_address = ip_data.get('ip')

        result = save_ip_address(ip_address)

        return jsonify({"ip": ip_address, "result": result})
    except requests.RequestException as e:
        return jsonify({'error': str(e)}), 500
