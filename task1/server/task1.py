from flask import Flask

app = Flask(__name__)


@app.route('/auth')
def home():
    pass

@app.route('/help')
def help():
    pass


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
