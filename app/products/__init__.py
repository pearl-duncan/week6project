from flask import Blueprint

product_blueprint = Blueprint('product', __name__, url_prefix="/product")

from . import routes
