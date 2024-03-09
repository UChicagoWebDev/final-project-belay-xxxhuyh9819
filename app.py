from flask import Flask
import string
import sqlite3
import random
from datetime import datetime
from flask import *
from flask_cors import CORS, cross_origin

from functools import wraps
import os


os.chdir(os.getcwd())
app = Flask(__name__, template_folder="./template", static_folder="./static/static")


@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    if path != "" and os.path.exists(os.path.join(app.static_folder, path)):
        print("path exists")
        return send_from_directory(app.static_folder, path)
    else:
        print("index.html")
        return send_from_directory(app.static_folder, 'index.html')

def get_db():
    db = getattr(g, '_database', None)

    if db is None:
        db = g._database = sqlite3.connect('db/Belay.sqlite3')
        db.row_factory = sqlite3.Row
        setattr(g, '_database', db)
    return db


@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


def query_db(query, args=(), one=False):
    db = get_db()
    cursor = db.execute(query, args)
    rows = cursor.fetchall()
    db.commit()
    cursor.close()
    if rows:
        if one:
            return rows[0]
        return rows
    return None


def new_user(username, password):
    api_key = ''.join(random.choices(string.ascii_lowercase + string.digits, k=40))

    u = query_db('insert into user (name, password, api_key) ' +
                 'values (?, ?, ?) returning id, name, password, api_key',
                 (username, password, api_key),
                 one=True)
    return u


# if there is a user with the name already, return None directly
def is_user_already_there(username):
    user_already_there = query_db('select * from user where name = ?', [username], one=True)
    return user_already_there if user_already_there is not None else None


@app.route('/')
@app.route('/login')
@app.route('/signup')
@app.route('/home')
@app.route('/profile')
@app.route('/createChannel')
@app.route('/channels/<channel_id>')
@app.route('/channels/<chat_id>/message/<message_id>')
def index(chat_id=None, message_id=None):
    return app.send_static_file('index.html')


@app.route('/')
def hello_world():  # put application's code here
    return {'Hello World!'}


@app.route('/api/login', methods=['POST'])
@cross_origin()
def login():
    username = request.json.get('username')
    password = request.json.get('password')

    query = "select * from user where name = ? and password = ?"
    try:
        user = query_db(query, [username, password], one=True)

        if not user:
            print("user not found")
            return jsonify({"code": 403, "msg": "User not found!"})

        print("user found")
        return jsonify({"code": 200,
                        "user":
                            {'user_id': user['id'],
                             'user_name': user['name'],
                             'api_key': user['api_key']}
                        })
    except Exception as e:
        return jsonify({"code": 500, "msg": e})


@app.route('/api/signup', methods=['POST'])
# src: https://flask-cors.readthedocs.io/en/3.0.7/
@cross_origin()
def signup():
    username = request.json.get('username')
    password = request.json.get('password')

    '''
    deal with duplicate name and creation failure???
    '''
    try:
        if is_user_already_there(username):
            return jsonify({"code": 403, "msg": "This username has already been occupied!"})
        user = new_user(username, password)
        return jsonify({"code": 200,
                        "user":
                            {'user_id': user['id'],
                             'user_name': user['name'],
                             'api_key': user['api_key']}
                        })
    except Exception as e:
        return jsonify({"code": 500, "msg": e})


@app.route('/api/update_username', methods=['POST'])
@cross_origin()
def update_username():
    api_key = request.json.get('api_key')
    new_name = request.json.get('new_name')

    if not api_key:
        return jsonify({"code": 403, "msg": "API key is required."})

    query = "select * from user where api_key = ?"

    # Find the user by API key
    user = query_db(query, (api_key,), one=True)
    if not user:
        return jsonify({"code": 404, "msg": "Invalid API key."})
    else:
        # check if the name has been occupied by another user
        old_user = query_db("select * from user where name = ?", (new_name,), one=True)
        if old_user:
            return jsonify({"code": 403, "msg": "This name has been occupied!"})
        try:
            query_db('update user set name = ? where api_key = ?',
                     (new_name, api_key))
            return jsonify({"code": 200, "msg": "Username updated successfully."})
        except Exception as e:
            return jsonify({"code": 500, "msg": e})


@app.route('/api/update_password', methods=['POST'])
@cross_origin()
def update_password():
    api_key = request.json.get('api_key')
    new_password = request.json.get('new_password')

    if not api_key:
        return jsonify({"code": 403, "msg": "API key is required."})

    query = "select * from user where api_key = ?"

    # Find the user by API key
    user = query_db(query, (api_key,), one=True)
    if not user:
        return jsonify({"code": 404, "msg": "Invalid API key."})
    else:
        try:
            query_db('update user set password = ? where api_key = ?',
                     (new_password, api_key))
            return jsonify({"code": 200, "msg": "Password updated successfully."})
        except Exception as e:
            return jsonify({"code": 500, "msg": e})


@app.route('/api/channels', methods=['GET'])
@cross_origin()
def get_channels():
    try:
        channel = query_db('select * from channel')
        if channel:
            return jsonify([dict(i) for i in channel]), 200
        else:
            jsonify([]), 200
    except Exception as e:
        return jsonify({"msg": e}), 500

@app.route('/api/channels/<int:channel_id>/messages', methods=['GET'])
def get_messages_by_channel_id(channel_id):
    try:
        # rid = request.args.get('room_id')
        messages = query_db('select * from message where channel_id = ?', (channel_id,), one=False)
        if messages:
            return jsonify([dict(msg) for msg in messages]), 200
        else:
            return jsonify([]), 200
    except Exception as e:
        return jsonify([]), 500

if __name__ == '__main__':
    app.run()
