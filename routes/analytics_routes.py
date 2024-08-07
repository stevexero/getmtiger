from datetime import datetime
from flask import Blueprint, jsonify, request
import requests
from flask_cors import cross_origin

analytics_bp = Blueprint('session', __name__)


#
# Get Website Stats
#
@analytics_bp.route('/api/getstats', methods=['GET'])
@cross_origin(supports_credentials=True)
def get_stats():
    print('getstats fired')
    try:
        current_time = int(datetime.utcnow().timestamp() * 1000)

        time_24_hours_ago = current_time - 24 * 3600 * 1000
        # time_7_days_ago = current_time - 7 * 24 * 3600 * 1000
        # time_30_days_ago = current_time - 30 * 24 * 3600 * 1000
        # time_90_days_ago = current_time - 90 * 24 * 3600 * 1000
        # time_6_months_ago = current_time - 6 * 30 * 24 * 3600 * 1000
        # time_12_months_ago = current_time - 12 * 30 * 24 * 3600 * 1000
        # time_all_time = 0

        website_id = request.args.get('website_id')
        api_key = request.args.get('api_key')

        if not website_id or not api_key:
            return jsonify({'error': 'Missing required parameters'}), 400

        api_url = f"https://api.umami.is/v1/websites/{website_id}/stats?startAt={time_24_hours_ago}&endAt={current_time}"
        headers = {
            'Accept': 'application/json',
            'x-umami-api-key': api_key
        }
        response = requests.get(api_url, headers=headers)
        response.raise_for_status()
        stats = response.json()

        return jsonify(stats)
    except requests.RequestException as e:
        return jsonify({'error': str(e)}), 500
