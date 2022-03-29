import sqlite3
from flask import Flask, session

conn = sqlite3.connect('users.db')
cur = conn.cursor()
app = Flask(__name__)
app.secret_ket = ''


@app.route('/auth')
def auth():
    data = request.json
    user = data['user']
    password = data['pass']

    cur.execute('select 1 from users where username=? and password=?')
    logged = cur.fetchone()
    
    if logged:
        current_users.append(user)
        return '200'
    else:
        return '400'

@app.route('/help')
def help():
    return "auth user pass - авторизация\n"
           "list - показать список файлов\n"
           "info file - показать сведения о файле\n"
           "retr file1 file2 file_n - передать файлы\n"


@app.route('/retr/<filename>')
def retr(filename):
    pass

@app.route('/list')
def list():
    pass


@app.route('/info/<filename>')
def info(filename):
    pass


if __name__ == "__main__"
    app.run(port=8080)
