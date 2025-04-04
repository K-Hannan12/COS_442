import socket

import redis
from flask import Flask, jsonify

app = Flask(__name__)
cache = redis.Redis(host='redis', port=6379)

def get_hit_count():
    return cache.incr('hits')
def get_hit_squared():
	count = cache.incr('hits')
	countSquared = count * count
	return countSquared

@app.route('/')
def hello():
    count = get_hit_count()
    return f'I love all the attention: Viewed {count} times\n'
@app.route('/squared')
def squared():
	count = get_hit_squared()
	return f'Hits Squared: {count}\n'


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5021)
