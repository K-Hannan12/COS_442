from flask import Flask
import random

app = Flask(__name__)

@app.route('/')
def wind():
    num = random.randint(5, 120)
    return f'wind = {num}'


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5005)