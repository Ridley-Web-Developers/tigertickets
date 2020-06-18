import os

from flask import Flask, request, jsonify, session, render_template, render_template_string
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


#
# @app.route('/login', methods=['POST'])
# def login():
#     users = mongo.db.users
#     login_user = users.find_one({'name': request.form['username']})
#     if login_user:
#         if bcrypt.hashpw(request.form['password'].encode('utf-8'), login_user['password'].encode('utf-8')) == login_user[
#             'password'].encode('utf-8'):
#             session['username'] = request.form['username']
#             return redirect(url_for('index'))
#
#     return 'Invalid username/password combination'
#
#
# @app.route('/register', methods=['POST', 'GET'])
# def register():
#     if request.method == 'POST':
#         users = mongo.db.users
#         existing_user = users.find_one({'name': request.form['username']})
#
#         if existing_user is None:
#             hashpass = bcrypt.hashpw(request.form['pass'].encode('utf-8'), bcrypt.gensalt())
#             users.insert({'name': request.form['username'], 'password': hashpass})
#             session['username'] = request.form['username']
#             return redirect(url_for('index'))
#
#         return 'That username already exists!'
#
#     return render_template('register.html')
#
# @app.route('/users/register', methods=['POST'])
# def register():
#     users = mongo.db.users
#     first_name = request.get_json()['first_name']
#     last_name = request.get_json()['last_name']
#     username = request.get_json()['username']
#     email = request.get_json()['email']
#     password = bcrypt.generate_password_hash(request.get_json()['password']).decode('utf-8')
#     created = datetime.utcnow()
#
#     user_id = users.insert({
#         'username': username,
#         'first_name': first_name,
#         'last_name': last_name,
#         'email': email,
#         'password': password,
#         'created': created
#     })
#
#     new_user = users.find_one({'_id': user_id})
#     result = {'email': new_user['email'] + ' registered'}
#
#     return jsonify({'result': result})
#
#
# @app.route('/users/login', methods=['POST'])
# def login():
#     users = mongo.db.users
#     email = request.get_json()['email']
#     password = request.get_json()['password']
#
#     response = users.find_one({'email': email})
#
#     if response:
#         if bcrypt.check_password_hash(response['password'], password):
#             access_token = create_access_token(identity={
#                 'first_name': response['first_name'],
#                 'last_name': response['last_name'],
#                 'email': response['email']
#             })
#             result = jsonify({"token": access_token})
#         else:
#             result = jsonify({"error": "Invalid username and password"})
#     else:
#         result = jsonify({"result": "No results found"})
#     return result


if __name__ == '__main__':
    app.run(port='5001')
