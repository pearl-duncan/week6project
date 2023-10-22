from . import product_blueprint as product
from flask import request
from flask_jwt_extended import jwt_required, current_user
from ..models import Product
from ..utils import bad_request_if_none

@product.post("/new")
@jwt_required()
def handle_create_product():
    body = request.json

    if body is None:
        response = {
            "message": "invalid request"
        }
        return response, 400
    
    img_url = body.get("img_url")
    if img_url is None or img_url == "":
        response = {
            "message": "invalid request"
        }
        return response, 400

    name= body.get("name")
    if name is None or img_url == "":
        response = {
            "message": "invalid request"
        }
        return response, 400


    description = body.get("description")
    if description is None or description == "":
        response = {
            "message": "invalid request"
        }
        return response, 400
    
    price = body.get("price")
    if price is None or img_url == "":
        response = {
            "message": "invalid request"
        }
        return response, 400

    product= Product(img_url=img_url, name=name, description=description, price=price, created_by=current_user.id)
    product.create()

    response = {
        "message": "successfully created product",
        "product": product.to_response()
    }
    return response, 201

@product.delete("/product/<produt_id>")
@jwt_required()
def handle_delete_product(product_id):
    product = Product.query.filter_by(id=product_id).one_or_none()
    if product is None:
        response = {
            "message": "product does not exist"
        }
        return response, 404

    if product.created_by != current_user.id:
        response = {
            "message":"you cant delete products"
        }
        return response, 401
    
    product.delete()

    response = {
        "message": f"product {product.id} deleted"
    }
    return response, 200
