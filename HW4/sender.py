from flask import Flask
import requests

app = Flask(__name__)

@app.route('/')
def getbase():
    response = requests.get("http://receiver:5001/")
    return f"received this from receiver: {response.text}"

@app.route('/buya')
def gethoppy():
    response = requests.get("http://receiver:5001/hoppy")
    return f"is hoppy happy today?: {response.text}"

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=5000)