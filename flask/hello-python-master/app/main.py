#from flask import Flask
#app = Flask(__name__)

#@app.route("/")
#def hello():
#   return "Hello from Python!"

#if __name__ == "__main__":
#    app.run(host='0.0.0.0')

#!/usr/bin/python3

from flask import Flask, jsonify, request, abort
from flask_restful import Api, Resource
import jsonpickle

app = Flask(__name__)
api = Api(app)

# Creating an empty dictionary and initializing user id to 0.. will increment every time a person makes a POST request.
# This is bad practice but only using it for the example. Most likely you will be pulling this information from a
# database.
user_dict = {}
user_id = 0


# Define a class and pass it a Resource. These methods require an ID
class User(Resource):
    @staticmethod
    def get(path_user_id):
        if path_user_id not in user_dict:
            abort(400)

        return jsonify(jsonpickle.encode(user_dict.get(path_user_id, "This user does not exist")))

    @staticmethod
    def put(path_user_id):
        update_and_add_user_helper(path_user_id, request.get_json())

    @staticmethod
    def delete(path_user_id):
        user_dict.pop(path_user_id, None)


# Get all users and add new users
class UserList(Resource):
    @staticmethod
    def get():
        return jsonify(jsonpickle.encode(user_dict))

    @staticmethod
    def post():
        global user_id
        user_id = user_id + 1
        update_and_add_user_helper(user_id, request.get_json())


# Since post and put are doing pretty much the same thing, I extracted the logic from both and put it in a separate
# method to follow DRY principles.
def update_and_add_user_helper(u_id, request_payload):
    name = request_payload["name"]
    age = request_payload["age"]
    address = request_payload["address"]
    city = request_payload["city"]
    state = request_payload["state"]
    zip_code = request_payload["zip"]
    user_dict[u_id] = Person(name, age, address, city, state, zip_code)


# Represents a user's information
class Person:
    def __init__(self, name, age, address, city, state, zip_code):
        self.name = name
        self.age = age
        self.address = address
        self.city = city
        self.state = state
        self.zip_code = zip_code


# Add a resource to the api. You need to give the class name and the URI.
api.add_resource(User, "/users/<int:path_user_id>")
api.add_resource(UserList, "/users")

if __name__ == "__main__":
    app.run(host='0.0.0.0')
