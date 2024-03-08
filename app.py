import os
import sqlite3
import random
import string
from flask_cors import CORS, cross_origin

from flask import *

app = Flask(__name__)


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


@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    if path != "" and os.path.exists(os.path.join(app.static_folder, path)):
        print("path exists")
        return send_from_directory(app.static_folder, path)
    else:
        print("index.html")
        return send_from_directory(app.static_folder, 'index.html')


@app.route('/')
@app.route('/login')
@app.route('/signup')
@app.route('/home')
@app.route('/profile')
@app.route('/createChannel')
@app.route('/channel/<chat_id>')
@app.route('/channel/<chat_id>/message/<message_id>')
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
    user = query_db(query, [username, password], one=True)

    if not user:
        print("user not found")
        return {}, 403

    print("user found")
    return jsonify({'user_id': user['id'],
                    'user_name': user['name'],
                    'api_key': user['api_key']}), 200


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
            return {}, 403
        user = new_user(username, password)
        return jsonify({
            "api_key": user["api_key"],
            "user_name": user["name"],
            "user_id": user["id"]
        }), 200
    except:
        return {}, 500


if __name__ == '__main__':
    app.run()
