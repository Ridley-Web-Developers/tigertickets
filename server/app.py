import os
from datetime import datetime

from flask import Flask
from flask_bcrypt import Bcrypt
from flask_cors import CORS
from flask_mail import Mail
from flask_pymongo import PyMongo
from flask_qrcode import QRcode

from server.config import *
from server.models.events import *

mode = os.environ.get('FLASK_ENV') or 'default'

app = Flask(__name__)
app.config.from_object(config[mode])

CORS(app, resources={r'/*': {'origins': '*'}})

bcrypt = Bcrypt(app)
mail = Mail(app)
mongo = PyMongo(app)
qrcode = QRcode(app)


@app.route('/', methods=['GET'])
def hello_world():
    print(qrcode("hello"))
    return 'Hello World'


@app.route('/users/register', methods=['POST'])
def register():
    users = mongo.db.users
    first_name = request.get_json()['first_name']
    last_name = request.get_json()['last_name']
    username = request.get_json()['username']
    email = request.get_json()['email']
    password = bcrypt.generate_password_hash(request.get_json()['password']).decode('utf-8')
    created = datetime.utcnow()

    # TODO: Check for created accounts
    user_id = users.insert({
        'username': username,
        'first_name': first_name,
        'last_name': last_name,
        'email': email,
        'password': password,
        'created': created
    })

    new_user = users.find_one({'_id': user_id})
    result = {'email': new_user['email'] + ' registered'}

    return jsonify({'result': result})


@app.route('/users/login', methods=['POST'])
def login():
    users = mongo.db.users
    email = request.get_json()['email']
    password = request.get_json()['password']

    response = users.find_one({'email': email})

    if response:
        if bcrypt.check_password_hash(response['password'], password):
            access_token = create_access_token(identity={
                'first_name': response['first_name'],
                'last_name': response['last_name'],
                'email': response['email']
            })
            result = jsonify({"token": access_token})
        else:
            result = jsonify({"error": "Invalid username and password"})
    else:
        result = jsonify({"result": "No results found"})
    return result


if __name__ == '__main__':
    app.run(port='5001')
