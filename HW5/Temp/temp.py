from flask import Flask
import random

app = Flask(__name__)

@app.route('/')
def temp():
    num = random.randint(-10, 110)
    return f'temp = {num}'


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5005)
