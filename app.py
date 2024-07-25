from flask import Flask
from dotenv import load_dotenv
from flask_cors import CORS
from routes.home_routes import home_bp
from routes.test_routes import test_bp
from routes.auth_routes import auth_bp
from routes.user_routes import user_bp
from routes.session_routes import session_bp

load_dotenv()


def create_app():
    app = Flask(__name__)
    CORS(app, resources={r"/*": {"origins": ["https://www.box-valet.com", "http://localhost:3000"]}}, supports_credentials=True)

    app.register_blueprint(home_bp)
    app.register_blueprint(test_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(user_bp)
    app.register_blueprint(session_bp)

    return app


app = create_app()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)
