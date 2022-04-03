from sqlite3 import Cursor, connect
from flask import Flask, request, make_response

app = Flask(__name__)
authed_users = set()
users_coefficients = {}


def get_cursor(database: str) -> Cursor:
    if database in authed_users:
        connect_name = f'messages/{database}.db'
    else:
        connect_name = f'{database}.db'

    conn = connect(connect_name)
    return conn.cursor()


@app.route('/login', methods=['POST'])
def auth():
    data = request.json
    user = data['user']
    password = data['pass']

    cur = get_cursor('users')
    cur.execute('select 1 from users where username=? and password=?', (user, password))
    exists = cur.fetchone()

    if exists:
        authed_users.add(user)
        users_coefficients[user] = []
        return make_response('', 200)
    else:
        return make_response('', 404)


@app.route('/exit', methods=['POST'])
def shutdown():
    authed_users.remove(request.json['user'])
    users_coefficients.pop(request.json['user'])
    return make_response('', 200)


@app.route('/store', methods=['PUT'])
def get_list():
    user = request.json['user']
    coefficients = request.json['coefficients']
    if user not in authed_users:
        return make_response('', 401)

    if len(coefficients) == 3:
        users_coefficients[user] = coefficients
        return make_response('', 204)
    else:
        return make_response({'error': 'incorrect_coeff'}, 400)


@app.route('/solve')
def solve():
    user = request.json['user']
    coefficients = request.json['coefficients']

    if len(coefficients) != 3 and len(users_coefficients[user]) != 3:
        return make_response({'error': 'incorrect_coeff'}, 400)
    else:
        solve_coefficients = coefficients if len(coefficients) == 3 else users_coefficients[user]

    if user not in authed_users:
        return make_response('', 401)

    d = solve_coefficients[1] ** 2 - 4 * solve_coefficients[0] * solve_coefficients[2]

    if d > 0:
        x1 = (-solve_coefficients[1] + d)/(2 * solve_coefficients[0])
        x2 = (-solve_coefficients[1] - d)/(2 * solve_coefficients[0])
        result = f"x1 = {x1}; x2 = {x2}"
    elif d == 0:
        x12 = (-solve_coefficients[1] + d) / (2 * solve_coefficients[0])
        result = f"x12 = {x12}"
    else:
        result = "Нет действительных корней"

    return make_response({'result': result}, 200)


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
