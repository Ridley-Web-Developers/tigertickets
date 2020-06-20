import os
import sys

from flask import Flask, request, jsonify, session, render_template, render_template_string
from flask_bcrypt import Bcrypt
from flask_cors import CORS
from flask_mail import Mail
from flask_pymongo import PyMongo
from flask_qrcode import QRcode
from flask_jwt_extended import JWTManager, create_access_token

# sys.path.append(os.path.abspath('../'))
from server.config import *
from server.models.events import *

mode = os.environ.get('FLASK_ENV') or 'default'

app = Flask(__name__)
app.config.from_object(config[mode])

CORS(app, resources={r'/*': {'origins': '*'}})

bcrypt = Bcrypt(app)
jwt = JWTManager(app)
mail = Mail(app)
mongo = PyMongo(app)
qrcode = QRcode(app)


@app.route('/qrcode', methods=['GET'])
def qr_code():
    qr_string = qrcode('Hello', error_correction='H')
    rendered = render_template('email.html', qr_string=qr_string)
    return rendered


@app.route('/')
def index():
    if 'username' in session:
        return 'You are logged in as ' + session['username']
    return 'Hello World'


@app.route('/users/register', methods=['POST'])
def register():
    users = mongo.db.users
    first_name = request.get_json()['first_name']
    last_name = request.get_json()['last_name']
    email = request.get_json()['email']
    password = bcrypt.generate_password_hash(request.get_json()['password']).decode('utf-8')
    created = datetime.utcnow()

    user_id = users.insert({
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
