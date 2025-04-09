from flask import Flask

app = Flask(__name__)

@app.route('/')
def temp():
    return "Temp"


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5021)
