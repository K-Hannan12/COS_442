from flask import Flask
import random

app = Flask(__name__)

@app.route('/')
def humidity():
    num = random.randint(0, 98)
    return f'’humidity = {num}'


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5005)