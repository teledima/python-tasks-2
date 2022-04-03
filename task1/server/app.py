from sqlite3 import Cursor, connect
from flask import Flask, request, make_response, send_file
from datetime import datetime

import os
import mimetypes

app = Flask(__name__)
authed_users = set()


def get_cursor() -> Cursor:
    conn = connect('users.db')
    return conn.cursor()


@app.route('/auth', methods=['POST'])
def auth():
    data = request.json
    user = data['user']
    password = data['pass']

    cur = get_cursor()
    cur.execute('select 1 from users where username=? and password=?', (user, password))
    exists = cur.fetchone()

    if exists:
        authed_users.add(user)
        return make_response('', 200)
    else:
        return make_response('', 404)


@app.route('/help')
def get_help():
    return "auth user pass - авторизация\n" \
           "list - показать список файлов\n" \
           "info file - показать сведения о файле\n" \
           "retr file1 file2 file_n - передать файлы\n"


@app.route('/exit', methods=['POST'])
def shutdown():
    authed_users.remove(request.json['user'])
    return make_response('', 200)


@app.route('/list')
def get_list():
    user = request.json['user']
    if user not in authed_users:
        return make_response('', 401)

    return ','.join([file for file in os.listdir('.') if os.path.isfile(os.path.join('.', file)) and file not in ('app.py', 'users.db')])


@app.route('/info/<filename>')
def info(filename):
    user = request.json['user']
    if user not in authed_users:
        return make_response('', 401)

    if not os.path.exists(filename):
        return make_response('', 404)

    mimetype = mimetypes.guess_type(filename)[0]
    size = os.stat(filename).st_size
    time = datetime.fromtimestamp(os.path.getctime(filename)).strftime('%Y-%m-%d %H:%M:%S')
    return f'mime тип: {mimetype}\n'\
           f'Размер (в байтах): {size}\n'\
           f'Дата создания: {time}'


@app.route('/retr/<filename>')
def retr(filename):
    user = request.json['user']
    if user not in authed_users:
        return make_response('', 401)

    if not os.path.exists(filename):
        return make_response('', 404)

    if filename not in ('app.py', 'users.db'):
        return send_file(filename)


if __name__ == "__main__":
    app.run(port=8080)
