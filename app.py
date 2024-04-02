from flask import Flask
from browser_automation import download_spreadsheet

app = Flask(__name__)


@app.route('/success')
def success():
    return "app is live"


@app.route('/download_spreadsheet')
def download_spreadsheet_action():
    try:
        download_spreadsheet()
        return "Spreadsheet download initiated!"
    except Exception as e:
        return f"An error occurred: {str(e)}"


if __name__ == '__main__':
    app.run(debug=True)
