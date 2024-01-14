from flask import Flask, jsonify, request
from flask_restful import Resource, Api, reqparse
from flask_cors import CORS
from add_tasks import add_task, check_login, new_user

app = Flask("ToDoList")
api = Api(app)

parser = reqparse.RequestParser()
CORS(app, support_credentials=True)
app.config['CORS_HEADERS'] = 'Content-Type'

@app.route('/add-task/', methods=['POST'])
@cross_origin()
def add_task():
        json_response = request.get_json()
        add_task(json_response["user_id"], json_response["task_content"])
        return json_response, 201


@app.route('/register/', methods=['POST'])
@cross_origin()
def register():
        json_response = request.get_json()
        print(json_response)
        is_valid = new_user(json_response["username"], json_response["user_email"], json_response["password"])
        if is_valid:
                return json_response, 201
        else:
                return json_response, 401


@app.route('/login/', methods=['POST'])
@cross_origin()
def login():
        json_response = request.get_json()
        is_correct = check_login(json_response["username"], json_response["password"])
        if is_correct:
                return json_response, 201
        else:
                return json_response, 401

if __name__ == "__main__":
  app.run(debug=True)