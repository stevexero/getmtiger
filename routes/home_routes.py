from flask import Blueprint, request, make_response

home_bp = Blueprint('home', __name__)


@home_bp.route('/')
def home():
    return 'Welcome to the Home Page!'


@home_bp.route('/make-cookie')
def make_cookie():
    response = make_response("Hello cookies")
    response.set_cookie('mycookie', 'ChocolateChip')
    return response


@home_bp.route('/show-cookie')
def show_cookie():
    cookie_value = request.cookies.get('mycookie')
    return cookie_value
