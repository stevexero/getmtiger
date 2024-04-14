from flask import Flask
from flask import jsonify
# from flask import request
from dotenv import load_dotenv
import os
# import pandas as pd
# from browser_automation import download_spreadsheet, add_user_to_spreadsheet, test_browser_automation
from browser_automation import test_browser_automation

load_dotenv()


def create_app():
    app = Flask(__name__)

    # download_dir = os.path.expanduser(os.environ.get('ASSET_TIGER_FILEPATH'))

    @app.route('/')
    def home():
        return 'Welcome to the Home Page!'

    @app.route('/hello')
    def hello_world():
        return jsonify({"message": 'Hello World!'})

    @app.route('/test-browser')
    def test_browser():
        try:
            page_title = test_browser_automation()
            return jsonify({"message": "Browser automation successful", "pageTitle": page_title})
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=5000, debug=True)

# @app.route('/api/items/get-all', methods=['GET'])
# def read_spreadsheet():
#     user_id = request.args.get('userId')
#     if not user_id:
#         return jsonify({"error": "User ID is required"}), 400
#
#     try:
#         print("Reading spreadsheet")
#         filename = os.environ.get('ASSET_TIGER_FILENAME')
#         print(filename)
#         # Assuming download_spreadsheet() returns the path of the downloaded spreadsheet
#         print("reading download directory")
#         print(download_dir)
#         file_path = os.path.join(download_dir, filename)
#         print(file_path)
#
#         # # Read the spreadsheet into a DataFrame
#         print("reading excel")
#         df = pd.read_excel(file_path, engine='openpyxl')
#         df = df.fillna(value="")
#         print(df)
#
#         if user_id:
#             df = df[df['Customer ID'] == user_id]
#
#         if df.empty or 'Customer ID' not in df:
#             return jsonify({"error": "No data found for the given user ID"}), 404
#
#         print("to dictionary")
#         data = df.to_dict(orient='records')
#         print("Data read")
#         print(data)
#
#         print("returning")
#         print(jsonify(data))
#         return jsonify(data)
#     except Exception as e:
#         return jsonify({"error": str(e)}), 500
#
#
# # ADD USER TO SPREADSHEET
# @app.route('/api/add-user', methods=['POST'])
# def add_user_to_sheet():
#     print("Adding user to sheet")
#     data = request.get_json()  # Get the JSON data sent in the request
#     print("data", end="")
#     print(data)
#
#     user_id = data.get('userId')
#     print("user id: ", end="")
#     print(user_id)
#
#     user_email = data.get('userEmail')
#     print("user email: ", end="")
#     print(user_email)
#
#     if user_id is None:
#         return jsonify({'error': 'userId is required'}), 400
#
#     # return jsonify({'message': f'User {user_id} added to spreadsheet'})
#
#     try:
#         print("starting standard_file_path")
#         standard_file_path = os.path.join(download_dir, os.environ.get('ASSET_TIGER_FILENAME'))
#         print("standard_file_path", end="")
#         print(standard_file_path)
#
#         # Download the latest spreadsheet from Asset Tiger
#         # download_spreadsheet()
#
#         # Add the user ID to the downloaded spreadsheet
#         print("adding user to spreadsheet")
#         add_user_to_spreadsheet(user_id, user_email, standard_file_path)
#         print("add_user_to_spreadsheet DONE", end="")
#
#         # TODO: Delete the following two lines, as this function is called in add_user_to_spreadsheet()
#         # Upload the updated spreadsheet back to Asset Tiger
#         # upload_spreadsheet_to_asset_tiger(standard_file_path)
#
#         # return jsonify({'message': f'User {user_id} added to spreadsheet and spreadsheet uploaded successfully'})
#         return jsonify({'message': f'User {user_id} added to spreadsheet and spreadsheet uploaded successfully'})
#
#     except Exception as e:
#         return jsonify({'error': str(e)}), 500
#
#
# @app.route('/download_spreadsheet')
# def download_spreadsheet_action():
#     try:
#         download_spreadsheet()
#         return "Spreadsheet download initiated!"
#     except Exception as e:
#         return f"An error occurred: {str(e)}"
