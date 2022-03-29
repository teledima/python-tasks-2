from datetime import datetime
from genericpath import isfile
import mimetypes
from flask import Flask, request, send_file
import json
import os

app = Flask(__name__)

users = dict(json.load(open('pass.json')))

current_users = []

@app.route("/auth")
def auth():
    rq_json = request.json
    user = rq_json['user']
    password = rq_json['pass']


    if user in users and users[user] == password:
        current_users.append(user)
        return '200'
    else:
        return '400'

@app.route("/list/<user>")
def get_list(user):
    if not (user in current_users):
        return "unauthorized"
    answer = ""
    listOfFiles = os.listdir('.') 
    for file in listOfFiles:  
        isFile = os.path.isfile(os.path.join('.', file))
        if isFile and file != "pass.json" and file != "app.py":
            answer += file + '\n'
    return answer

@app.route("/info/<user>")
def info(user):
    if not (user in current_users):
        return "unauthorized"
    answer = ""
    filename = request.json['filename']

    if filename == "pass.json" or filename == "app.py":
        return "Access denied"

    mimetype = mimetypes.MimeTypes().guess_type(filename)[0]
    size = os.stat(filename).st_size
    time = datetime.fromtimestamp(os.path.getctime(filename)).strftime('%d-%m-%Y_%H:%M')

    answer += "mime тип: " + mimetype + '\n'
    answer += "размер файла в байтах: " + str(size) + '\n'
    answer += "дата создания: " + time + '\n'

    return answer

@app.route("/retr/<filename>/<user>")
def retr(filename, user):
    if not (user in current_users):
        return "unauthorized"
    if filename == "pass.json" or filename == "app.py":
        return "Access denied"
    return send_file(filename)

@app.route("/help")
def help():
    answer = "auth user pass — авторизация" + '\n'
    answer += "list — показать список файлов" + '\n'
    answer += "info file — напечатать сведения о файле" + '\n'
    answer += "retr file1 file2 file_n — передать файлы" + '\n'
    return answer

@app.route("/exit")
def exit():
    user = request.json['user']
    current_users.remove(user)