from flask import Blueprint

main_controllers = Blueprint('main', __name__, url_prefix="/")

@main_controllers.route('/')
def index():
    return "Hello World!"