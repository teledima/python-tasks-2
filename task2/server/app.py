from sqlite3 import Cursor, connect
from flask import Flask, request, make_response

app = Flask(__name__)
authed_users = set()


def get_cursor(database: str) -> Cursor:
    if database in authed_users:
        connect_name = f'messages/{database}.db'
    else:
        connect_name = f'{database}.db'

    conn = connect(connect_name)
    return conn.cursor()


@app.route('/auth', methods=['POST'])
def auth():
    data = request.json
    user = data['user']
    password = data['pass']

    cur = get_cursor('users')
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
           "read msg - вывести сообщение под номером msg\n" \
           "send user - ввод сообщения \n"


@app.route('/exit', methods=['POST'])
def shutdown():
    authed_users.remove(request.json['user'])
    return make_response('', 200)


@app.route('/list')
def get_list():
    user = request.json['user']
    if user not in authed_users:
        return make_response('', 401)

    cur = get_cursor(database=user)
    cur.execute('select id, message from messages order by id')
    messages = cur.fetchall()

    return '\n'.join([f'{message[0]}: {message[1]}' for message in messages])


@app.route('/read/<int:msg>')
def read_msg(msg: int):
    user = request.json['user']
    if user not in authed_users:
        return make_response('', 401)

    cur = get_cursor(database=user)
    cur.execute('select id, message from messages where id = ?', (msg, ))
    result = cur.fetchone()
    return f'{result[0]}: {result[1]}'


@app.route('/send')
def send():
    user = request.json['user']
    message = request.json['message']
    if user not in authed_users:
        return make_response('', 401)

    cur = get_cursor(user)
    cur.execute('insert into messages(message) values (?)', (message, ))
    cur.connection.commit()
    return make_response('', 200)


if __name__ == "__main__":
    app.run(port=8080)
