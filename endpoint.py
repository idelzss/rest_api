from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_restful import Api, Resource
from flask_swagger_ui import get_swaggerui_blueprint
from sqlalchemy.sql.functions import user
from .models import User, session
from . import app
import json

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
CORS(app,resources={r'/*': {'origins': 'http://127.0.0.1:5000'}})

api = Api(app)

class HelloWorld(Resource):
    def get(self):
        dict_return = {
            'message': 'Hello World!'
        }
        return jsonify(dict_return)


class UserGetAll(Resource):
    def get(self):
        users = User.query.all()
        users_list = [{"user_id": user.id, "name": user.name, "email": user.email} for user in users]
        return jsonify(users_list)

    def post(self):
        data = request.get_json()
        name = data.get("name")
        email = data.get("email")

        if not name or not email:
            return jsonify({"message": "Name and email are required."}), 400

        if User.query.filter_by(name=name).first():
            return jsonify({"message": "User with this email already exists."}), 400


        new_user = User(
            name=name,
            email=email
        )

        session.add(new_user)
        session.commit()

        message = {
            "message": "User created .",
            "user": {
                "id": new_user.id,
                "name": new_user.name,
                "email": new_user.email
            }
        }
        return jsonify(message)


api.add_resource(HelloWorld, '/')
api.add_resource(UserGetAll, '/users')


SWAGGER_URL = '/swagger'
API_URL = 'http://127.0.0.1:5000/swagger.json'
swagger_blueprint = get_swaggerui_blueprint(

    SWAGGER_URL,
    API_URL,
    config={
        "app_name": "SAMPLE API",
    }

)
app.register_blueprint(swagger_blueprint, url_prefix=SWAGGER_URL)

@app.route("/swagger.json")
def swagger():
    with open("swagger.json", "r") as file:
        return jsonify(json.load(file))
